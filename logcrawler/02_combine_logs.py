"""
    Combine Image and game logs the right way
    see: https://scm.cms.hu-berlin.de/berlinunited/naoth-2020/-/commit/0a79c8c2ae1143ab63f8ec907580de9eae5bc50

    # TODO: we have stuff like this: /vol/repl261-vol4/naoth/logs/2023-08-cccamp/2023-08-18-testgame_04/2_22_Nao0004_230818-1213
    were we only have an image log and no game.log
"""

from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.pb.Framework_Representations_pb2 import Image
from naoth.log import Parser
from os import environ, stat
import os
from vaapi.client import Vaapi


def create_image_log_dict(image_log, first_image_is_top):
    """
    Return a dictionary with frame numbers as key and (offset, size, is_camera_bottom) tuples of image data as values.
    """
    # parse image log
    width = 640
    height = 480
    bytes_per_pixel = 2
    image_data_size = width * height * bytes_per_pixel

    file_size = os.path.getsize(image_log)

    images_dict = dict()

    with open(image_log, "rb") as f:
        # assumes the first image is a bottom image
        # NOTE: this was changed in 2023, for older image logs this might need adjustment.
        is_camera_top = first_image_is_top
        while True:
            # read the frame number
            frame = f.read(4)
            if len(frame) != 4:
                break

            frame_number = int.from_bytes(frame, byteorder="little")

            # read the position of the image data block
            offset = f.tell()
            # skip the image data block
            f.seek(offset + image_data_size)

            # handle the case of incomplete image at the end of the logfile
            if f.tell() >= file_size:
                print(
                    "Info: frame {} in {} incomplete, missing {} bytes. Stop.".format(
                        frame_number, image_log, f.tell() + 1 - file_size
                    )
                )
                break

            if frame_number not in images_dict:
                images_dict[frame_number] = {}

            name = "ImageTop" if is_camera_top else "Image"
            images_dict[frame_number][name] = (offset, image_data_size)

            # next image is of the other cam
            is_camera_top = not is_camera_top

    return images_dict

def create_jpeg_image_log_dict(image_log):
    """
    Return a dictionary with frame numbers as key and image data as values.
    """
    images_by_frame = {}

    myParser = Parser()
    myParser.register("ImageJPEG"   , "Image")
    myParser.register("ImageJPEGTop", "Image")

    reader = LogReader(image_log, parser=myParser)

    for frame in reader.read():
        images = {}

        if "ImageJPEG" in frame.get_names():
            images["ImageJPEG"] = frame["ImageJPEG"]

        if "ImageJPEGTop" in frame.get_names():
            images["ImageJPEGTop"] = frame["ImageJPEGTop"]

        
        images_by_frame[frame.number] = images

    return images_by_frame

def write_combined_log(log, combined_log_path, img_log_path, gamelog_path, image_jpeg_log_path=None):
    is_first_image_top = calculate_first_image(log)
    image_log_index = create_image_log_dict(
                str(img_log_path), first_image_is_top=is_first_image_top
            )

    # if there are jpeg images, load them
    image_jpeg_log_index = create_jpeg_image_log_dict(str(image_jpeg_log_path)) if image_jpeg_log_path else {}


    try:
        with open(str(combined_log_path), "wb") as output, open(
            str(img_log_path), "rb"
        ) as image_log, LogReader(str(gamelog_path)) as reader:
            for frame in reader.read():
                # only write frames which have corresponding images
                if frame.number in image_log_index:

                    # may contain 'ImageTop' and 'Image'
                    for image_name, (offset, size) in image_log_index[
                        frame.number
                    ].items():
                        # load image data
                        image_log.seek(offset)
                        image_data = image_log.read(size)

                        # add image from image.log
                        msg = Image()
                        msg.height = 480
                        msg.width = 640
                        msg.format = Image.YUV422
                        msg.data = image_data

                        frame.add_field(image_name, msg)

                # if there are jpeg images for this frame, add them to the frame
                if frame.number in image_jpeg_log_index:
                    images = image_log_index[frame.number]
                    for image_repr_name, image_msg in images.items():
                        frame.add_field(image_repr_name, image_msg)

                # write the potentially modified frame to the new log
                output.write(bytes(frame))

                # HACK: Frames are indexed by the log reader. 
                # Remove the image of already processed frames to preserve memory.
                if frame.number in image_log_index:
                    for image_name in image_log_index[frame.number]:
                        frame.remove(image_name)
                if frame.number in image_jpeg_log_index:
                    for image_name in image_jpeg_log_index[frame.number]:
                        frame.remove(image_name)               

    except Exception as e:
        print(f"failed to combine file: {e}")
        # TODO set a status in the db so that no one tries to parse this again
        # check 2023-08-cccamp/2023-08-17_12-00-00_Berlin United_vs_TestOpponent_testgame-02/game_logs/1_21_Nao0041_230817-1136
        # Maybe we can handle weird broken files better than completely ignoring them??
        if combined_log_path.is_file():
            combined_log_path.unlink()

def write_combined_log_jpeg(combined_log_path, img_log_path, gamelog_path):
    image_log_index = create_jpeg_image_log_dict(str(img_log_path))

    try:
        with open(combined_log_path, 'wb') as output, LogReader(gamelog_path) as reader:
            for frame in reader.read():
                # only write frames which have corresponding images
                if frame.number not in image_log_index:
                    print('Frame {} has no corresponding image data.'.format(frame.number))
                    continue

                # contains 'ImageTop' and 'Image'
                images = image_log_index[frame.number]

                for image_repr_name, image_msg in images.items():
                    frame.add_field(image_repr_name, image_msg)

                # write the modified frame to the new log
                output.write(bytes(frame))

                # HACK: Frames are indexed by the log reader. Remove the image of already processed frames to preserve memory.
                for image_name in image_log_index[frame.number]:
                    frame.remove(image_name)
    except Exception as e:
        print(f"failed to combine file: {e}")
        # TODO set a status in the db so that no one tries to parse this again
        if combined_log_path.is_file():
            combined_log_path.unlink()


def calculate_first_image(logpath):
    """
    calculate the age of the log file. For everything prior 2023 the first image in the log is top after that its bottom
    """
    # TODO fix me, prefix is annoying here
    logpath = str(logpath)
    event = logpath.split("_")[0]
    year = int(event.split("-")[0])
    if year < 2023:
        return True
    else:
        return False


if __name__ == "__main__":
    # TODO make it possible to run it locally without having to use a database. Useful for seeing the images in the log to figure out a good name.
    log_root_path = os.environ.get("VAT_LOG_ROOT")

    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    existing_data = client.logs.list()

    def sort_key_fn(data):
        return data.log_path


    for data in sorted(existing_data, key=sort_key_fn, reverse=True):
        log_id = data.id
        log_folder_path = Path(data.log_path).parent # data.log_path is path to file
        log_path = Path(log_root_path) / log_folder_path
        print("log_path: ", log_path)

        if Path(log_path).is_file():
            print(
                "\tpath is a experiment log - no automatic combining here. If needed combine the log manually and add to the event list"
            )
            continue

        combined_log_path = log_path / "combined.log"
        gamelog_path = log_path / "game.log"
        img_log_path = log_path / "images.log"
        img_jpeg_log_path = log_path / "images_jpeg.log"

        has_game_log = Path(gamelog_path).is_file() and stat(str(gamelog_path)).st_size > 0
        has_image_log = Path(img_log_path).is_file() and stat(str(img_log_path)).st_size > 0
        has_image_jpeg_log = Path(img_jpeg_log_path).is_file() and stat(str(img_jpeg_log_path)).st_size > 0

        if not has_game_log and (has_image_log or has_image_jpeg_log):
            print("\tcan't combine anything here, missing game.log or image.log/image_jpeg.log")
            continue

        if not combined_log_path.is_file():
            if has_image_log and has_image_jpeg_log:
                write_combined_log(log_folder_path, combined_log_path, img_log_path, gamelog_path, img_jpeg_log_path)
            elif has_image_log and not has_image_jpeg_log:
                write_combined_log(log_folder_path, combined_log_path, img_log_path, gamelog_path)
            elif has_image_jpeg_log and not has_image_log:
                write_combined_log_jpeg(combined_log_path, img_jpeg_log_path, gamelog_path)
            else:
                # not an error: /vol/repl261-vol4/naoth/logs/2024-04-17_GO24/2024-04-19_21-00-00_Berlin United_vs_Nao Devils_half1-test/game_logs/7_16_Nao0017_240419-1937
                #raise ValueError("We shouldn't have gotten this far, either image.log or image_jpeg.log should exist")
                print("WARNING: nothing to combine found here")
