import unittest

from feluda.models.media_factory import ImageFactory
from operators.detect_lewd_images import detect_lewd_images


class TestDetectLewdImages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        param = {}
        detect_lewd_images.initialize(param)

    @classmethod
    def tearDownClass(cls):
        # Clean up any resources
        pass

    def setUp(self):
        self.test_images = {
            "nude_study": r"https://upload.wikimedia.org/wikipedia/commons/1/16/Nude_study_%2836207592445%29.jpg",
            "mobile_phone": "https://upload.wikimedia.org/wikipedia/commons/b/b6/Image_created_with_a_mobile_phone.png",
        }

    def tearDown(self):
        # Clean up any temp files created during tests
        pass

    def test_sample_image_from_url(self):
        image1 = ImageFactory.make_from_url(self.test_videos["nude_study"])
        image2 = ImageFactory.make_from_url(self.test_videos["mobile_phone"])
        paths = [image1["path"], image2["path"]]
        results = detect_lewd_images.run(paths)
        # Assert that the lewd content prediction is greater than 40%
        self.assertGreater(results[0], 40)
        self.assertLess(results[1], 20)
