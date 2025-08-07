import contextlib
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np
import yaml

from feluda import Feluda
from feluda.factory import VideoFactory


class TestFeludaVidTSNEReductionIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # TSNE pipeline: video → 2D TSNE (perplexity=1, fixed seed)
        cfg = {
            "operators": {
                "label": "Vid+TSNE",
                "parameters": [
                    {"name": "vid", "type": "vid_vec_rep_clip", "parameters": {}},
                    {
                        "name": "tsne",
                        "type": "dimension_reduction",
                        "parameters": {
                            "perplexity": 1,
                            "n_components": 2,
                        },
                    },
                ],
            }
        }
        fd, cls.config_path = tempfile.mkstemp(suffix=".yml", text=True)
        with os.fdopen(fd, "w") as fp:
            yaml.dump(cfg, fp)

        cls.feluda = Feluda(cls.config_path)
        cls.feluda.setup()
        ops = cls.feluda.operators.get()
        cls.vid = ops["vid_vec_rep_clip"]
        cls.dr = ops["dimension_reduction"]

        sample_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"
        vecs = list(cls.vid.run(VideoFactory.make_from_url(sample_url)))
        if len(vecs) < 3:
            raise RuntimeError(f"Need ≥3 embeddings but got {len(vecs)}")
        cls.avg_vec = vecs[0]["vid_vec"]
        cls.frame_vecs = [vecs[1]["vid_vec"], vecs[2]["vid_vec"]]
        cls.expected_dim = len(cls.avg_vec)

    @classmethod
    def tearDownClass(cls):
        Path(cls.config_path).unlink(missing_ok=True)

    @contextlib.contextmanager
    def assertNoException(self, msg=None):
        try:
            yield
        except Exception as e:
            self.fail(f"{msg or 'Unexpected exception'}: {e}")

    def test_smoke_video_and_tsne(self):
        """Smoke: two 512d → TSNE→ two 2d embeddings."""
        data = [
            {"payload": "avg", "embedding": self.avg_vec},
            {"payload": "f1", "embedding": self.frame_vecs[0]},
        ]
        out = self.dr.run(data)
        self.assertEqual(len(out), 2)
        for item in out:
            self.assertIn("reduced_embedding", item)
            self.assertEqual(len(item["reduced_embedding"]), 2)

    def test_tsne_seed_consistency(self):
        """Fixed-seed TSNE on the same two vectors yields identical outputs."""
        data = [
            {"payload": "avg", "embedding": self.avg_vec},
            {"payload": "f1", "embedding": self.frame_vecs[0]},
        ]
        a = self.dr.run(data)
        b = self.dr.run(data)
        for x, y in zip(a, b):
            np.testing.assert_allclose(x["reduced_embedding"], y["reduced_embedding"])

    def test_full_video_to_tsne_pipeline(self):
        """End-to-end video→TSNE preserves payloads and dims."""
        data = [
            {"payload": "avg", "embedding": self.avg_vec},
            {"payload": "f2", "embedding": self.frame_vecs[1]},
        ]
        out = self.dr.run(data)
        got = [o["payload"] for o in out]
        self.assertCountEqual(got, ["avg", "f2"])
        for o in out:
            self.assertEqual(len(o["reduced_embedding"]), 2)


class TestFeludaVidUMAPReductionIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # UMAP pipeline: video → 3D UMAP
        cfg = {
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
                        },
                    },
                ],
            }
        }
        fd, cls.config_path = tempfile.mkstemp(suffix=".yml", text=True)
        with os.fdopen(fd, "w") as fp:
            yaml.dump(cfg, fp)

        cls.feluda = Feluda(cls.config_path)
        cls.feluda.setup()
        ops = cls.feluda.operators.get()
        cls.vid = ops["vid_vec_rep_clip"]
        cls.dr = ops["dimension_reduction"]

        sample_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"
        vecs = list(cls.vid.run(VideoFactory.make_from_url(sample_url)))
        needed = 5
        if len(vecs) < needed:
            raise RuntimeError(f"Need ≥{needed} embeddings but got {len(vecs)}")
        cls.samples = [v["vid_vec"] for v in vecs[:needed]]

    @classmethod
    def tearDownClass(cls):
        Path(cls.config_path).unlink(missing_ok=True)

    @contextlib.contextmanager
    def assertNoException(self, msg=None):
        try:
            yield
        except Exception as e:
            self.fail(f"{msg or 'Unexpected exception'}: {e}")

    def test_umap_integration(self):
        """UMAP: avg + frames → 3d embeddings."""
        data = [
            {"payload": f"p{i}", "embedding": vec} for i, vec in enumerate(self.samples)
        ]
        out = self.dr.run(data)
        self.assertEqual(len(out), len(self.samples))
        for item in out:
            self.assertEqual(len(item["reduced_embedding"]), 3)
