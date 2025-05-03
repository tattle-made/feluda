import contextlib
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np
import yaml

from feluda import Feluda
from feluda.models.media_factory import VideoFactory


class TestFeludaVidVecAndDimRedIntegration(unittest.TestCase):
    """
    Integration tests for:
      - vid_vec_rep_clip → CLIP‐based video embeddings
      - dimension_reduction → TSNE / UMAP
    """

    @classmethod
    def setUpClass(cls):
        # TSNE Config
        cls.tsne_cfg = {
            "operators": {
                "label": "Vid+TSNE",
                "parameters": [
                    {"name": "vid", "type": "vid_vec_rep_clip", "parameters": {}},
                    {
                        "name": "tsne",
                        "type": "dimension_reduction",
                        "parameters": {
                            "model_type": "tsne",
                            "n_components": 2,
                            "perplexity": 1,
                            "learning_rate": 100,
                            "max_iter": 250,
                            "random_state": 123,
                        },
                    },
                ],
            }
        }
        fd, cls.cfg_path = tempfile.mkstemp(suffix=".yml", text=True)
        with os.fdopen(fd, "w") as f:
            yaml.dump(cls.tsne_cfg, f)

        # 2) Initialize Feluda and grab operators
        cls.feluda = Feluda(cls.cfg_path)
        cls.feluda.setup()
        ops = cls.feluda.operators.get()
        cls.vid = ops["vid_vec_rep_clip"]
        cls.dr = ops["dimension_reduction"]

        # 3) Download sample and extract 3 real embeddings (avg + 2 frames)
        cls.sample_url = (
            "https://github.com/tattle-made/"
            "feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"
        )
        video_obj = VideoFactory.make_from_url(cls.sample_url)
        vecs = list(cls.vid.run(video_obj))
        if len(vecs) < 3:
            raise RuntimeError(f"Need ≥3 embeddings but got {len(vecs)}")
        cls.avg_vec = vecs[0]["vid_vec"]
        cls.frame_vecs = [vecs[1]["vid_vec"], vecs[2]["vid_vec"]]
        cls.expected_dim = len(cls.avg_vec)

    @classmethod
    def tearDownClass(cls):
        Path(cls.cfg_path).unlink(missing_ok=True)

    @contextlib.contextmanager
    def assertNoException(self, msg=None):
        try:
            yield
        except Exception as e:
            self.fail(f"{msg or 'Unexpected exception'}: {e}")

    def test_smoke_video_and_tsne(self):
        """Smoke: two 512d → TSNE→ two 2d embeddings."""
        self.assertIsInstance(self.avg_vec, list)
        self.assertEqual(self.expected_dim, 512)

        data = [
            {"payload": "avg", "embedding": self.avg_vec},
            {"payload": "f1",  "embedding": self.frame_vecs[0]},
        ]
        out = self.dr.run(data)
        self.assertEqual(len(out), 2)
        for item in out:
            self.assertIn("reduced_embedding", item)
            self.assertEqual(len(item["reduced_embedding"]), 2)

    def test_tsne_seed_consistency(self):
        """Fixed‐seed TSNE on the same two vectors yields identical outputs."""
        data = [
            {"payload": "avg", "embedding": self.avg_vec},
            {"payload": "f1",  "embedding": self.frame_vecs[0]},
        ]
        a = self.dr.run(data)
        b = self.dr.run(data)
        for x, y in zip(a, b):
            np.testing.assert_allclose(x["reduced_embedding"], y["reduced_embedding"])

    def test_full_video_to_tsne_pipeline(self):
        """End‑to‑end video→TSNE preserves payloads and dims."""
        data = [
            {"payload": "avg", "embedding": self.avg_vec},
            {"payload": "f2",  "embedding": self.frame_vecs[1]},
        ]
        out = self.dr.run(data)
        got = [o["payload"] for o in out]
        self.assertCountEqual(got, ["avg", "f2"])
        for o in out:
            self.assertEqual(len(o["reduced_embedding"]), 2)

    def test_umap_integration(self):
        """UMAP: avg + 2 frames + extra frames → 3d embeddings."""
        # build UMAP config (n_components=3, n_neighbors=2)
        umap_cfg = {
            "operators": {
                "label": "Vid+UMAP",
                "parameters": [
                    {"name": "vid", "type": "vid_vec_rep_clip", "parameters": {}},
                    {
                        "name": "umap",
                        "type": "dimension_reduction",
                        "parameters": {
                            "model_type": "umap",
                            "n_components": 3,
                            "n_neighbors": 2,
                            "min_dist": 0.1,
                            "random_state": 0,
                        },
                    },
                ],
            }
        }
        fd2, cfg2 = tempfile.mkstemp(suffix=".yml", text=True)
        with os.fdopen(fd2, "w") as f2:
            yaml.dump(umap_cfg, f2)

        fel2 = Feluda(cfg2)
        fel2.setup()
        vid2, dr2 = fel2.operators.get().values()

        # UMAP spectral needs at least (n_components + 2) samples
        n_cmp = umap_cfg["operators"]["parameters"][1]["parameters"]["n_components"]
        needed = n_cmp + 2
        video_obj = VideoFactory.make_from_url(self.sample_url)
        extra = list(vid2.run(video_obj))
        if len(extra) < needed:
            raise RuntimeError(f"Need ≥{needed} embeddings but got {len(extra)}")
        data = [
            {"payload": f"p{i}", "embedding": extra[i]["vid_vec"]}
            for i in range(needed)
        ]
        out = dr2.run(data)
        self.assertEqual(len(out), needed)
        for item in out:
            self.assertEqual(len(item["reduced_embedding"]), n_cmp)
        Path(cfg2).unlink(missing_ok=True)
