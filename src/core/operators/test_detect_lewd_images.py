import unittest
from unittest.case import skip

from src.core.operators import detect_lewd_images
from core.models.media_factory import ImageFactory


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
            "nude_study_url": r"https://upload.wikimedia.org/wikipedia/commons/1/16/Nude_study_%2836207592445%29.jpg",
            "mobile_phone_local": "core/operators/sample_data/mobile_phone.png",
        }

    def tearDown(self):
        # Clean up any temp files created during tests
        pass

    @skip
    def test_sample_video_from_disk(self):
        image = ImageFactory.make_from_file_on_disk_to_path(self.test_images["mobile_phone_local"])
        paths = [image["path"]]
        results = detect_lewd_images.run(paths)
        # Assert that the lewd content prediction is less than 20%
        self.assertLess(results[1], 20)

    @skip
    def test_sample_image_from_url(self):
        image = ImageFactory.make_from_url(self.test_images["nude_study_url"])

        paths = [image["path"]]
        results = detect_lewd_images.run(paths)
        # Assert that the lewd content prediction is greater than 40%
        self.assertGreater(results[0], 40)
