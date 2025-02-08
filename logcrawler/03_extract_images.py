import queue
import threading
import os
from linetimer import CodeTimer
from naoth.log import Reader as LogReader
from naoth.log import Parser
from pathlib import Path
import concurrent.futures
import numpy as np
import io
from PIL import PngImagePlugin
from PIL import Image as PIL_Image
from vaapi.client import Vaapi

def is_done(log_id):
    # get the log status object for a given log_id
    response = client.log_status.list(log_id=log_id)

    if len(response) == 0:
        print("\tno log_status found")
        return False
    
    log_status = response[0]
    # if all numbers are zero or null we return false
    total_images = int(log_status.num_jpg_bottom or 0) + int(log_status.num_jpg_top or 0) + int(log_status.num_bottom or 0) + int(log_status.num_top or 0)
    print(log_status)
    if total_images == 0:
        return False
    else:
        return True

def export_images(logfile, img, output_folder_top, output_folder_bottom, out_top_jpg, out_bottom_jpg):
    """
    creates two folders:
        <logfile name>_top
        <logfile name>_bottom

    and saves the images inside those folders
    """

    for i, img_b, img_b_jpg, img_t, img_t_jpg, cm_b, cm_t in img:
        frame_number = format(
            i, "07d"
        )  # make frame number a fixed length string so that the images are in the correct order
        if img_b:
            img_b = img_b.convert("RGB")
            save_image_to_png(
                frame_number, img_b, cm_b, output_folder_bottom, cam_id=1, name=logfile
            )
        # TODO add meta data indicating this was a jpeg image
        if img_b_jpg:
            img_b_jpg = img_b_jpg.convert("RGB")
            save_image_to_png(
                frame_number, img_b_jpg, cm_b, out_bottom_jpg, cam_id=1, name=logfile
            )

        if img_t:
            img_t = img_t.convert("RGB")
            save_image_to_png(
                frame_number, img_t, cm_t, output_folder_top, cam_id=0, name=logfile
            )

        # TODO add meta data indicating this was a jpeg image
        if img_t_jpg:
            img_t_jpg = img_t_jpg.convert("RGB")
            save_image_to_png(
                frame_number, img_t_jpg, cm_t, out_top_jpg, cam_id=0, name=logfile
            )

        print("\tsaving images from frame ", i, end="\r", flush=True)


def get_images(frame):
    try:
        image_top = image_from_proto(frame["ImageTop"])
    except KeyError:
        image_top = None
    
    try:
        image_top_jpeg = image_from_proto_jpeg(frame["ImageJPEGTop"])
    except KeyError:
        image_top_jpeg = None

    try:
        cm_top = frame["CameraMatrixTop"]
    except KeyError:
        cm_top = None

    try:
        image_bottom = image_from_proto(frame["Image"])
    except KeyError:
        image_bottom = None

    try:
        image_bottom_jpeg = image_from_proto_jpeg(frame["ImageJPEG"])
    except KeyError:
        image_bottom_jpeg = None

    try:
        cm_bottom = frame["CameraMatrix"]
    except KeyError:
        cm_bottom = None

    return [frame.number, image_bottom, image_bottom_jpeg, image_top, image_top_jpeg, cm_bottom, cm_top]


def image_from_proto(message):
    # read each channel of yuv422 separately
    yuv422 = np.frombuffer(message.data, dtype=np.uint8)
    y = yuv422[0::2]
    u = yuv422[1::4]
    v = yuv422[3::4]

    # convert from yuv422 to yuv888
    yuv888 = np.zeros(message.height * message.width * 3, dtype=np.uint8)

    yuv888[0::3] = y
    yuv888[1::6] = u
    yuv888[2::6] = v
    yuv888[4::6] = u
    yuv888[5::6] = v

    yuv888 = yuv888.reshape((message.height, message.width, 3))

    # convert the image to rgb and save it
    img = PIL_Image.frombytes(
        "YCbCr", (message.width, message.height), yuv888.tobytes()
    )
    return img


def image_from_proto_jpeg(message):
    
    # hack: 
    if message.format == message.JPEG:
        # unpack JPG
        img = PIL_Image.open(io.BytesIO(message.data))
    
        # HACK: for some reason the decoded image is inverted ...
        yuv422 = 255 - np.array(img, dtype=np.uint8)
        
        # flatten the image to get the same data formal like a usual yuv422
        yuv422 = yuv422.reshape(message.height * message.width * 2)
    else:
        # read each channel of yuv422 separately
        yuv422 = np.frombuffer(message.data, dtype=np.uint8)
    
    y = yuv422[0::2]
    u = yuv422[1::4]
    v = yuv422[3::4]

    # convert from yuv422 to yuv888
    yuv888 = np.zeros(message.height * message.width * 3, dtype=np.uint8)

    yuv888[0::3] = y
    yuv888[1::6] = u
    yuv888[2::6] = v
    yuv888[4::6] = u
    yuv888[5::6] = v

    yuv888 = yuv888.reshape((message.height, message.width, 3))
    
    # convert the image to rgb
    img = PIL_Image.frombytes('YCbCr', (message.width, message.height), yuv888.tobytes())
    
    return img


def save_image_to_png(j, img, cm, target_dir, cam_id, name):
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Message", "rotation maxtrix is saved column wise")
    meta.add_text("logfile", str(name))
    meta.add_text("CameraID", str(cam_id))

    if cm:
        meta.add_text("t_x", str(cm.pose.translation.x))
        meta.add_text("t_y", str(cm.pose.translation.y))
        meta.add_text("t_z", str(cm.pose.translation.z))

        meta.add_text("r_11", str(cm.pose.rotation[0].x))
        meta.add_text("r_21", str(cm.pose.rotation[0].y))
        meta.add_text("r_31", str(cm.pose.rotation[0].z))

        meta.add_text("r_12", str(cm.pose.rotation[1].x))
        meta.add_text("r_22", str(cm.pose.rotation[1].y))
        meta.add_text("r_32", str(cm.pose.rotation[1].z))

        meta.add_text("r_13", str(cm.pose.rotation[2].x))
        meta.add_text("r_23", str(cm.pose.rotation[2].y))
        meta.add_text("r_33", str(cm.pose.rotation[2].z))
    filename = target_dir / (str(j) + ".png")
    img.save(filename, pnginfo=meta)



def worker(data_queue, output_paths):
    while True:
        try:
            batch = data_queue.get(block=False)
            if batch is None:  # Sentinel value to exit
                break
            for image_data in batch:
                image, top_path, bottom_path = image_data
                export_images("test", [image], top_path, bottom_path, top_path, bottom_path)
            data_queue.task_done()
        except queue.Empty:
            continue


def calculate_output_path(log_folder: str):
    # FIXME have a better detection if its experiment log or not
    """
    log_path_w_prefix = log_root_path / Path(log_folder)
    if Path(log_path_w_prefix).is_file():
        print("\tdetected experiment log")
        actual_log_folder = log_root_path / Path(log_folder).parent
        log = log_path_w_prefix

        extracted_folder = (
            Path(actual_log_folder) / Path("extracted") / Path(log_path_w_prefix).stem
        )
        output_folder_top = extracted_folder / Path("log_top")
        output_folder_bottom = extracted_folder / Path("log_bottom")
        output_folder_top_jpg = extracted_folder / Path("log_top_jpg")
        output_folder_bottom_jpg = extracted_folder / Path("log_bottom_jpg")

        print(f"\toutput folder will be {extracted_folder}")

    else:
    """
    print("\tdetected normal game log")
    actual_log_folder = log_root_path / Path(log_folder)
    combined_log = log_root_path / Path(actual_log_folder) / "combined.log"
    game_log = log_root_path / Path(actual_log_folder) / "game.log"
    if combined_log.is_file():
        log = combined_log
    elif game_log.is_file():
        log = game_log
    else:
        log = None

    extracted_folder = (
        Path(actual_log_folder).parent.parent
        / Path("extracted")
        / Path(actual_log_folder).name
    )

    output_folder_top = extracted_folder / Path("log_top")
    output_folder_bottom = extracted_folder / Path("log_bottom")
    output_folder_top_jpg = extracted_folder / Path("log_top_jpg")
    output_folder_bottom_jpg = extracted_folder / Path("log_bottom_jpg")

    return log, output_folder_top, output_folder_bottom, output_folder_top_jpg, output_folder_bottom_jpg


if __name__ == "__main__":
    # FIXME aborting this script can result in broken images being written
    log_root_path = os.environ.get("VAT_LOG_ROOT") 

    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    existing_data = client.logs.list()

    def sort_key_fn(data):
        return data.log_path
    
    for data in sorted(existing_data, key=sort_key_fn, reverse=True):
        log_folder_path = Path(log_root_path) / Path(data.log_path).parent
        print(log_folder_path)

        log_id = data.id

        if is_done(log_id):
           print("\twe already counted all the images and put them in the db we assume that all images have been extracted")
           continue
        
        data_queue = queue.Queue()
        
        log, out_top, out_bottom, out_top_jpg, out_bottom_jpg = calculate_output_path(log_folder_path)
        if log is None:
            print("\tcouldnt find a valid log file")
            continue

        out_top.mkdir(exist_ok=True, parents=True)
        out_bottom.mkdir(exist_ok=True, parents=True)
        out_top_jpg.mkdir(exist_ok=True, parents=True)
        out_bottom_jpg.mkdir(exist_ok=True, parents=True)

        output_paths = {
            "top": out_top_jpg,
            "bottom": out_bottom_jpg
        }
        num_threads = os.cpu_count() * 2
        batch_size = 50  # Adjust based on your specific use case

        with CodeTimer("Total"):
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                # Start worker threads
                futures = [executor.submit(worker, data_queue, output_paths) for _ in range(num_threads)]

                my_parser = Parser()
                my_parser.register("ImageJPEG"   , "Image")
                my_parser.register("ImageJPEGTop", "Image")

                with CodeTimer("Reading and processing logs"):
                    with LogReader(log, my_parser) as reader:
                        batch = []
                        for image in map(get_images, reader.read()):
                            batch.append((image, output_paths["top"], output_paths["bottom"]))
                            if len(batch) >= batch_size:
                                data_queue.put(batch)
                                batch = []
                        if batch:  # Put any remaining items
                            data_queue.put(batch)

                with CodeTimer("Writing images"):
                    # Wait for all tasks to be completed
                    data_queue.join()

                # Signal worker threads to exit
                for _ in range(num_threads):
                    data_queue.put(None)

                # Wait for all threads to complete
                concurrent.futures.wait(futures)

        # HACK delete image folders if they are empty - this is just so that looking at the distracted folder is not confusing for humans
        if not any(out_top_jpg.iterdir()):
            out_top_jpg.rmdir()
        if not any(out_bottom_jpg.iterdir()):
            out_bottom_jpg.rmdir()
        if not any(out_top.iterdir()):
            out_top.rmdir()
        if not any(out_bottom.iterdir()):
            out_bottom.rmdir()