import cv2
from tqdm import tqdm

vidcap = cv2.VideoCapture('test.mp4')
success,image = vidcap.read()
count = 0

def video_length(v):
    v.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
    # duration in seconds
    duration = v.get(cv2.CAP_PROP_POS_MSEC)/1000.0
    frames = v.get(cv2.CAP_PROP_FRAME_COUNT)
    v.set(cv2.CAP_PROP_POS_AVI_RATIO,0)
    return duration, int(frames)

duration, frames = video_length(vidcap)

# get duration/50 samples from total frames
n_samples = frames/50

for i in tqdm(range(frames)):
#while success:
  success,image = vidcap.read()
  #print('Read a new frame: ', success)
  if image is None:
      continue
  else:
      #cv2.imwrite("frames/frame%d.jpg" % i, image)
      if i % 50 == 0:
          cv2.imwrite("samples/frame%d.jpg" % i, image)
      #print(image.shape)
