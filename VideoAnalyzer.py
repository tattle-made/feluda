import numpy as np
import cv2

class VideoAnalyzer:
    def __init__(self, video, sampling_rate=10, n_keyframes=5):
        """
        video: cv2.VideoCapture object
        sampling_rate: ratio of total frames to samples
        """
        self.video = video
        self.length, self.n_frames = self._length(self.video)
        self.sampling_rate = sampling_rate
        self.n_samples = self.n_frames/sampling_rate
        self.n_keyframes = n_keyframes
        self.images = self._extract_fames(video)

    def _length(self, v):
        v.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
        # duration in seconds
        duration = v.get(cv2.CAP_PROP_POS_MSEC)/1000.0
        frames = v.get(cv2.CAP_PROP_FRAME_COUNT)
        v.set(cv2.CAP_PROP_POS_AVI_RATIO,0)
        return duration, int(frames)

    def _extract_fames(self, v):
        for i in range(self.n_frames):
            success, image = v.read()
            if image is None:
                continue
            else:
                if i % self.sampling_rate == 0:
                    self.images.append(image)

   def extract_feature(self, v): 
       #TODO: call Resnet18 extracter on all the images
       # do pivoted QR on the matrix of features
       # return the average of first n_keyframes features
       pass
