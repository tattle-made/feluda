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
            "local_path": "operators/detect_lewd_images/image2.png",
        }

    def tearDown(self):
        # Clean up any temp files created during tests
        pass

    @skip
    def test_sample_image_from_disk(self):
        """Test inference on a local image file."""
        image = ImageFactory.make_from_file_on_disk_to_path(
            self.test_images["local_path"]
        )
        result = detect_lewd_images.run(image)
        result = float(result)
        # Check if result is a valid probability (0-1)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
        
    @skip
    def test_sample_image_from_url(self):
        """Test inference on a downloaded image from URL."""
        image = ImageFactory.make_from_url_to_path(self.test_images["url"])
        result = detect_lewd_images.run(image) # Clean up temp file
        result = float(result)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)

    @skip
    def test_invalid_image_path(self):
        """Test handling of invalid/nonexistent image paths."""        
        result = detect_lewd_images.run({"path": "nonexistent_file.jpg"})
        self.assertIsNone(result)

    @skip("Optional: Test batch processing if implemented later")
    def test_batch_processing(self):
        """Placeholder for future batch processing tests."""
        pass

