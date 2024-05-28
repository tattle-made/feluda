import sys
import traceback


def initialize(param):
    print("Installing packages for vid_vec_rep_resnet")

    global os, np, cv2, qr, torch, data, models, transforms, Image  # , wget #, FFmpeg
    global imagenet_transform, ImageListDataset, VideoAnalyzer, gendata  # , compress_video
    global contextmanager

    import os
    import numpy as np
    import cv2
    from scipy.linalg import qr
    import torch
    from torch.utils import data
    import torchvision.models as models
    import torchvision.transforms as transforms
    from PIL import Image
    from contextlib import contextmanager
    # from ffmpy import FFmpeg
    # import wget

    imagenet_transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    """
    def compress_video(fname):
        newname = "/tmp/compressed.mp4"
        FNULL = open(os.devnull, "w")
        ff = FFmpeg(
            global_options="-y",
            inputs={fname: None},
            outputs={newname: "-vcodec libx265 -crf 28"},
        )
        print(ff.cmd)
        ff.run(stdout=FNULL, stderr=FNULL)
        # os.remove(fname)
        return newname
    """

    def gendata(vid_analyzer):
        # average vector
        yield {
            "vid_vec": vid_analyzer.get_mean_feature().tolist(),
            "is_avg": True,
            "duration": vid_analyzer.duration,
            "n_keyframes": vid_analyzer.n_keyframes,
        }
        # keframe vectors
        for i in range(vid_analyzer.n_keyframes):
            yield {
                "vid_vec": vid_analyzer.keyframe_features[:, i].tolist(),
                "is_avg": False,
                "duration": vid_analyzer.duration,
                "n_keyframes": vid_analyzer.n_keyframes,
            }

    class ImageListDataset(data.Dataset):
        def __init__(self, image_list, transform=imagenet_transform):
            super().__init__()
            self.image_list = image_list
            self.transform = transform

        def __len__(self):
            return len(self.image_list)

        def __getitem__(self, index):
            x = self.image_list[index]
            return self.transform(x)

    class VideoAnalyzer:
        def __init__(self, video, sampling_rate=10, n_keyframes=5):
            """
            video: cv2.VideoCapture object
            sampling_rate: ratio of total frames to samples
            n_keyframes: number of keyframes whose features
                        we want to keep for search
            """
            self.video = video
            self.duration = self.frames = self.width = self.height = None
            _ = self.get_video_attributes(video)
            # check_sanity
            self.sampling_rate = sampling_rate
            self.n_samples = self.n_frames / sampling_rate
            self.n_keyframes = n_keyframes
            # print("init model")
            self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
            # print(type(self.model))
            # list of individual PIL Images
            self.frame_images = []

            # np.array of indices where the key frames are
            self.keyframe_indices = []

            # np.array of features corresponding to those key frames
            # should be a 512 x n_keyframes array
            self.keyframe_features = []

            self.analyze(video)

        def set_fsize(self, fsize):
            self.fsize = fsize

        def check_constraints(self):
            """
            check if video is too big/unsupported.
            return fail=1, set appropriate error
            """
            if self.fsize > 10:
                return False, "file size larger than 10 MB not supported"
            # TODO : based on data statistics, how long it takes to process a video decide thresholds based on  w x h, frames
            return True, None

        def get_mean_feature(self):
            return self.keyframe_features.mean(axis=1)

        def analyze(self, video):
            # print("analyzing video")
            self.frame_images = self.extract_frames(video)
            feature_matrix = self.extract_features(self.frame_images)
            self.keyframe_indices = self.find_keyframes(feature_matrix)
            self.keyframe_features = feature_matrix[:, self.keyframe_indices]
            # print("analysed video")

        def get_video_attributes(self, v):
            # print("getting video attributes")
            if self.duration is not None:
                return {
                    "duration": self.duration,
                    "n_frames": self.n_frames,
                    "width": self.width,
                    "height": self.height,
                }
            width = v.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = v.get(cv2.CAP_PROP_FRAME_HEIGHT)
            # duration in seconds
            v.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
            fps = v.get(cv2.CAP_PROP_FPS)
            frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration = frame_count / fps
            self.n_frames = frame_count
            self.width = width
            self.height = height
            v.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
            # print("got video attributes")
            return {
                "duration": self.duration,
                "n_frames": self.n_frames,
                "width": self.width,
                "height": self.height,
            }

        def extract_frames(self, v):
            # print("extracting frames")
            # images = []
            for i in range(self.n_frames):
                success, image = v.read()
                if image is None:
                    continue
                else:
                    if i % self.sampling_rate == 0:
                        # images.append(Image.fromarray(image))
                        yield [Image.fromarray(image)]
            # print("extracted frames")
            # print("len(images):", len(images))
            # print("sys.getsizeof(images[0])", sys.getsizeof(images[0]))
            # print("sys.getsizeof(images)", sys.getsizeof(images))
            # return images

        def extract_features(self, images, batch_size=1):
            res = []
            image_count = 0
            for img in images:
                # print("image_count: ", image_count)
                image_count += 1
                try:
                    dset = ImageListDataset(img)
                    dloader = data.DataLoader(
                        dset, batch_size=batch_size, shuffle=False
                    )
                    feature_layer = self.model._modules.get("avgpool")

                    def hook(m, i, o):
                        feature_data = o.data.reshape((512, batch_size))
                        embedding.copy_(feature_data)

                    self.model.eval()
                    for i, image in enumerate(dloader):
                        embedding = torch.zeros(512, batch_size)
                        h = feature_layer.register_forward_hook(hook)
                        self.model(image)
                        h.remove()
                        res.append(embedding.numpy())
                    # print("len(res)", len(res))
                    # res = np.hstack(res)
                    # print("res.shape:", res.shape)
                    # print("sys.getsizeof(res)", sys.getsizeof(res))
                    # assert res.shape == (512, len(images))
                    # return res

                except Exception:
                    print(traceback.format_exc())

            print("len(res)", len(res))
            res = np.hstack(res)
            print("res.shape:", res.shape)
            print("sys.getsizeof(res)", sys.getsizeof(res))
            # assert res.shape == (512, image_count)
            return res

        def find_keyframes(self, feature_matrix):
            # print("finding keyframes")
            Q, R, P = qr(feature_matrix, pivoting=True, overwrite_a=False)
            # Q is the orthogonal matrix that is an approximation of the featue matrix
            # P is a pivot matrix containing indices of the original (feature matrix) image vectors that have the largest vector norms
            # We select the first n indices from P to get the n keyframes
            # print(P)
            idx = P[: self.n_keyframes]
            # print("found keyframes")
            return idx


def run(file):
    fname = file["path"]
    fsize = os.path.getsize(fname) / 1e6
    print("original size: ", fsize)
    # if fsize < 10:
    #     print("compressing video")
    #     fname = compress_video(fname)
    #     fsize = os.path.getsize(fname) / 1e6
    #     print("compressed video size: ", fsize)
    # if fsize > 10:
    #     raise Exception("Video too large")

    @contextmanager
    def video_capture(fname):
        video = cv2.VideoCapture(fname)
        try:
            yield video
        finally:
            video.release()
            os.remove(fname)

    with video_capture(fname) as video:
        vid_analyzer = VideoAnalyzer(video)
        vid_analyzer.set_fsize(fsize)

        # doable, error_msg = vid_analyzer.check_constraints()

        # if not doable:
        #     raise Exception("Unsupported Video. Cannot index video.")

        return gendata(vid_analyzer)


def cleanup(param):
    pass


def state():
    pass
