import unittest
from unittest.case import skip

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
            "url": r"https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/text.png",
            "local_path": "core/operators/sample_data/mobile_phone.png",
        }

    def tearDown(self):
        # Clean up any temp files created during tests
        pass

    @skip
    def test_sample_video_from_disk(self):
        image = ImageFactory.make_from_file_on_disk_to_path(
            self.test_images["local_path"]
        )
        paths = [image["path"]]
        results = detect_lewd_images.run(paths)
        # Assert that the lewd content prediction is less than 20%
        self.assertLess(results[1], 20)

    def test_sample_image_from_url(self):
        image = ImageFactory.make_from_url_to_path(self.test_images["url"])
        result = detect_lewd_images.run(image)

        self.assertGreaterEqual(result, 0.10)
        self.assertLessEqual(result, 0.15)
