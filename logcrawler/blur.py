from vaapi.client import Vaapi
import requests
import cv2
import os


def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    logs = client.logs.list()

    first_log = logs[0].id
    # TODO build a filter that excludes images that have already a value
    # TODO do it for all logs
    images = client.image.list(log=162)

    # TODO use tqdm here to have a progressbar
    for img in images:
        url = "https://logs.berlin-united.com/" + img.image_url

        dwn = requests.get(url)

        # TODO figure out how to do it without saving to file here
        with open("temp.jpg","wb") as f:
            f.write(dwn.content)

        image = cv2.imread("temp.jpg")
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)

        #if fm < 100:
        #    print(f"the image {url} is blurry ({int(fm)})")

        client.image.update(id=img.id,blurredness_value=int(fm))