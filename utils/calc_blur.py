from vaapi.client import Vaapi
import requests,cv2







def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

if __name__ == "__main__":
    client = Vaapi(
        base_url="http://127.0.0.1:8000/",  
        api_key="7c137988bd5316d6d22ebcbd1048bb5e07b56040",
    )


    #event = client.events.list()

    logs = client.logs.list(event_id=1)

    first_log = logs[0].id

    images = client.image.list(event_id=1,log=first_log)


    for img in images:
        url = "https://logs.berlin-united.com/" +img.image_url


        #print(img.blurredness_value)

        dwn = requests.get(url)

        with open("temp.jpg","wb") as f:
            f.write(dwn.content)

        image = cv2.imread("temp.jpg")
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        if fm < 100:
            print(f"the image {url} is blurry ({int(fm)})")

        client.image.update(id=img.id,blurredness_value=int(fm))