def initialize(param):
    global config_psm
    global config_oem
    config_psm = 6
    config_oem = 1
    global Image
    global pytesseract
    global requests
    global BytesIO
    import pytesseract
    from PIL import Image
    from io import BytesIO
    import requests


def run(image_path):
    
    with Image.open(image_path) as load_image:
        data = pytesseract.image_to_string(
            load_image, lang="eng+hin+tam+tel", config="--psm 6 --oem 1"
        )
    return data


def cleanup(param):
    pass


def state():
    pass


# image_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
# response = requests.get(image_url)
# response.raise_for_status()
# text_data = run(BytesIO(response.content))
# print(text_data)
