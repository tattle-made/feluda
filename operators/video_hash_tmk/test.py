import os
import unittest

from feluda.factory import VideoFactory
from operators.video_hash_tmk import video_hash_tmk


class TestVideoHashing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        video_hash_tmk.initialise(param=None)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_video_hashing_from_url(self):
        video_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"
        video_obj = VideoFactory.make_from_url(video_url)
        video_path = video_obj["path"]

        # # Ensure the video file exists
        self.assertTrue(os.path.exists(video_path))

        # # Generate the hash
        video_hash = video_hash_tmk.run(video_path)
        print(video_hash)
        self.assertIsNotNone(video_hash)
        self.assertTrue(isinstance(video_hash, str))

        self.assertTrue(
            all(
                c
                in "AnMnw7sQqEOw7CxD+7J5wk1V/sKQy6NDTq2gwv4GBsMkrRxCOd78vpnrEELX8n3C+DmZwa5HtUE2lTtBa41VQaJfm8NU+vlBSeWdQhtjesG1LjLDUOjNQqaSKkI4DM3C4XUBQgxv5kEZsBpCnKSewvFSL8Fki0LB+zxvwFQLVkGgIQrCqUEkQwFF80KPJrLCGm7cwY/8u0GynXpCfEztwb9vfcFrYBtBlSC2QB7WJ0G+ginBusmEwQ5UV8F6oL/BKHk+Q4680ELo/j7DDlXwQg3gsEIS20TCsdIBwux0E0JhytLBsmRfwtNnnMHYcrK/04cmQuZEysHCNfbAvZyKQYQCs8Fa2eHCyPp5Qjeli0I2hQrD4d8KwtaWoECMQK3AIHCqQRs4VsJW6BpBk1GoQWD6AsFQuqdAyxRoQXE7AsLHPgDCEjYMQoUgeEI6FZLCHPUAwqRtUUEL5aM/l6A9QpQmskHdSqtB7u6IwR7C9T+axzC/ywKTwXwCkEC+6e7AbvwAQn3wSkKne5XAbAeNwW1vE0Kr8YNCTYgKwWchwr/c4/TBEsmvwf5RtcBQjwbBtKJoQZdI/cHWpmlBuXjzP3b2JMJs8gLCmh+7QbSn+cGGwce/+6NdQOcfNMLaVZvA78wFwnZOicENW5rAeo1jPzm3FEI5r91BvQE1wYOkacCTPYPCOPHpwV2kIUEEUuzBRwsbwqC5KEFNuKpBpaB0wVFhe8Hx+tlBeayoQZ5zmUCHbqPA8MxFwdSnNUECRgnBdGCPwoMNjUJiCKJBJlw5wt9PIkFHtHNBaCdVvwvxHUFtnAHBt5+fQH2ZnkG/90HAcCBawXbz0sGDigxAosZewZOXicJgYJPAjQnGQdQzp8Azq5VBD7ymwQX0KcH+x4K/cPfQQCmMM0FuABrBVYFvwWR23EAYyTfAys4SwbQDrEG68mHC7QUYwiAt+cFdpbg/dHnYQbEYsEEqpHDB9+EvwcWZyL61YmBB4V+lwArdrMCVbTxAsvFxPzDuhUC+PPxAqkMewfHAQMJ45dPAVM9+QSXqxUGFzFzBKkTCQJDF+kCZPnBAYiIkwTbumEFoN39BZUmGwVphFME4mwxAgmBkQMLPo8Cgsw7CUr5dQYhY9EGjWMFAwruiwbzZjsHRask+/yZ/QasWVEGvDUbAhJFrQBqbGcE2/j5A98vcQDYFU8ErA11A3/KpwSpoE0CVc9NBSvKdPzsE2sArIeI+GvSfwZRUY0E7ZTdBesM1QY6qSMHiyNTADVERQcrdOkEsxZnAhcOEwGRABML0yF++COXpQI14CEH9ktDA1sShQOA6H0Egy6/AlExnvw2NVUDVQzlBRcEewco7Ub8e4iJBic5UwA=="
                for c in video_hash
            )
        )
