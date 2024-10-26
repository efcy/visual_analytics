from vaapi.client import Vaapi
import requests
import cv2
import os
from tqdm import tqdm
import numpy as np
import argparse
from pathlib import Path
#from PIL import Image 


def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--local", action="store_true", default=False)
    args = parser.parse_args()

    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    
    data = client.logs.list()

    def sort_key_fn(data):
        return data.log_path

    for data in sorted(data, key=sort_key_fn, reverse=True):
        log_id = data.id
        print(data.log_path)
        images = client.image.list(log=log_id, blurredness_value=None)

        image_data = list()
        print(len(images))
        #print(images)
        #quit()
        for idx, img in enumerate(tqdm(images)):
            if args.local:
                image_path = Path(log_root_path) / img.image_url
                image_cv = cv2.imread(image_path, cv2.IMREAD_COLOR)
                #im = Image.open(str(image_path))
                #image_cv = np.asarray(im)
            else:
                # TODO try for timeout use the other one if one is not working
                url = "https://logs.berlin-united.com/" + img.image_url
                url = "https://logs.naoth.de/" + img.image_url
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad status codes

                image = np.asarray(bytearray(response.content), dtype="uint8")
                image_cv = cv2.imdecode(image, cv2.IMREAD_COLOR)

            try:
                gray = cv2.cvtColor(image_cv,cv2.COLOR_BGR2GRAY)
                brightness_value = np.average(gray)
                blurredness_value = variance_of_laplacian(gray)
                height,width,channels = image_cv.shape

                json_obj = {
                     "id": img.id,
                     "blurredness_value":blurredness_value,
                     "brightness_value": brightness_value,
                     "resolution": f"{width}x{height}x{channels}"
                }

                image_data.append(json_obj)

            except Exception as e:
                 print(e)
                 continue
            
            if idx % 1000 == 0 and idx != 0:
                try:
                    response = client.image.bulk_update(
                        data=image_data
                    )
                    image_data.clear()
                except Exception as e:
                    print(e)
                    print(f"error inputing the data")
                    quit()

        if len(image_data) > 0:
            print(len(image_data))
            try:
                response = client.image.bulk_update(
                    data=image_data
                )
            except Exception as e:
                print(e)
                print(f"error inputing the data")
                quit()

