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

import cProfile
import pstats
import io

def profile(fnc):
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        
        # Get the current file's path
        current_file = os.path.abspath(__file__)
        
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        
        # Filter stats to only include functions from the current file
        ps.print_stats(lambda func: func[0] == current_file)
        
        print(s.getvalue())
        return retval
    return inner


logpath = "/mnt/smb_share/naoth/logs/2024-07-15_RC24/2024-07-20_11-15-00_BerlinUnited_vs_HTWK_Einlauftest/game_logs/1_23_Nao0010_240720-1102/combined.log"

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

        #print("\tsaving images from frame ", i, end="\r", flush=True)


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
    with CodeTimer("File I/O"):
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


def my_generator(images, batch_size: int = 50):
    batch = []
    for image in images:
        batch.append(image)
        if len(batch) == batch_size:
            yield batch
            batch = []
    # for the last items
    if batch:
        yield batch

@profile
def main():
    data_queue = queue.Queue()

    os.makedirs("testlog/top",exist_ok=True)
    os.makedirs("testlog/bottom",exist_ok=True)
    
    output_paths = {
        "top": Path("testlog/top"),
        "bottom": Path("testlog/bottom")
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
                with LogReader(logpath, my_parser) as reader:
                    images = map(get_images, reader.read())
                    for batch in my_generator(images, batch_size):
                        my_array = [None] * len(batch)
                        for idx, image in enumerate(batch):
                            my_array[idx] = (image, output_paths["top"], output_paths["bottom"])

                        data_queue.put(my_array)

            with CodeTimer("Writing images"):
                # Wait for all tasks to be completed
                data_queue.join()

            # Signal worker threads to exit
            for _ in range(num_threads):
                data_queue.put(None)

            # Wait for all threads to complete
            concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()