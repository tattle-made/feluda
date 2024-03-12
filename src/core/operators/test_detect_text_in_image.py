import unittest
from . import detect_text_in_image


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        param = {}
        detect_text_in_image.initialize(param)

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_sample_image_from_disk(self):
        with open("sample_data/image-with-text.jpg", mode="rb") as file:
            bytes = file.read()
            image = {"bytes": bytes}
            detected_text = detect_text_in_image.run(image)
            self.assertEqual(detected_text["text"], "GRAZY\n")

    def test_sample_image_from_memory(self):
        """
        todo implement later
        primary aim for this function is to have a way to test the operator
        without relying on external files. in the event that s3 goes down or someone modifies the files
        stored in the sample_data folder
        """

        # from PIL import Image, ImageDraw
        # import sys

        # img = Image.new("RGB", (100, 30), color=(73, 109, 137))
        # d = ImageDraw.Draw(img)
        # d.text((10, 10), "Hello World", fill=(255, 255, 0))

        # bytes = img.tobytes()
        # img.save(sys.stdout, "PNG")

        # print(type(bytes)) # should be <class 'bytes'>
        # image = {"bytes": bytes}
        # detected_text = detect_text_in_image.run(image)
        # print("TEXT : ", detected_text)
        # self.assertEqual(detected_text["text"], "Hello World")

    def test_sample_image_from_url(self):
        # todo : put URL of s3 endpoint in an environment variable to avoid s3 abuse
        import requests
        from requests.exceptions import ConnectTimeout

        try:
            # https://tattle-media.s3.amazonaws.com/test-data/tattle-search/image_with_text_handwritten_hindi.jpeg
            resp = requests.get(
                "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png",
                timeout=(3.05, 5)
            )

            image = {"image_bytes": resp.content}
            detected_text = detect_text_in_image.run(image)
            print("----> 1", detected_text["text"])
            self.assertEqual(detected_text["text"], "ठंड बहुत हैं:\nअपना ख्याल रखना\nठंडी- ठंडी\n")
        except ConnectTimeout:
            print('Request has timed out')

