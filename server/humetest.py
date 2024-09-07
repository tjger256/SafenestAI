import base64

with open("tree.jpeg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    print('data:image/jpeg;base64,' + encoded_string.decode())