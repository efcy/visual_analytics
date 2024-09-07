from vaapi import client

baseurl = "http://127.0.0.1:8000/api/"
token = "5317f1918d4281f8a2705d47b689cf162bb69add"

myclient = client(baseurl,token)

params = {'log':8,'camera':'TOP','type':'JPEG'}
img_count = myclient.image_count(params).get('count')
imgs = myclient.list_images(params)


img_list = []
for x in imgs:
    img_list.append(x.get('frame_number'))

img_array = [None]*img_count

print(len(img_array))
print(len(img_list))



i = 0  # Initial index
prev_start_index = None  # To keep track of the previous start
prev_end_index = None
while True:
    # Calculate the start and end indices ensuring that they are within bounds
    start_index = max(0, i - 2)
    end_index = min(len(img_array), i + 3)

    
    if prev_start_index is not None and prev_end_index is not None:
        if start_index > prev_start_index:
            # Set the elements that have shifted out of the range on the left side to None
            img_array[prev_start_index:start_index] = [None] * (start_index - prev_start_index)
        if end_index < prev_end_index:
            # Set the elements that have shifted out of the range on the right side to None
            img_array[end_index:prev_end_index] = [None] * (prev_end_index - end_index)



    # Copy 51 elements from img_list to img_array
    img_array[start_index:end_index] = img_list[start_index:end_index]

    # Print the current 51 elements in img_array
    print(img_array[prev_start_index:prev_end_index])

    print(img_array[start_index:end_index])

    # Take user input to move left ('l') or right ('r')
    u = input('Enter "l" to move left or "r" to move right: ').strip()

    if u == 'l':
        # Move left if possible
        if i > 0:
            i -= 1
    elif u == 'r':
        # Move right if possible
        if i < len(img_list) - 1:
            i += 1
    else:
        print("Invalid input. Please enter 'l' or 'r'.")

    prev_start_index, prev_end_index = start_index, end_index