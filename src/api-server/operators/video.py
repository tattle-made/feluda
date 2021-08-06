import wget
import os
from VideoAnalyzer import VideoAnalyzer, compress_video


def get_vector_from_file(file):
    text_bytes = file.read()
    text_vec = transform_text(text_bytes, sent_model)
    if text_vec is None:
        text_vec = np.zeros(768).tolist()
    return text_vec


def get_vector_from_url(url):
    fname = "/tmp/vid.mp4"
    print("Downloading video from url")
    wget.download(file_url, out=fname)
    print("video downloaded")
    fsize = os.path.getsize(fname) / 1e6
    print("original size: ", fsize)
    if fsize > 10:
        print("compressing video")
        fname = compress_video(fname)
        fsize = os.path.getsize(fname) / 1e6
        print("compressed video size: ", fsize)
    if fsize > 10:
        raise Exception("Video too large")
    video = cv2.VideoCapture(fname)
    vid_analyzer = VideoAnalyzer(video)
    vid_analyzer.set_fsize(fsize)

    doable, error_msg = vid_analyzer.check_constraints()
    os.remove(fname)

    if not doable:
        print(jsonify({"failed": 1, "error": error_msg}))
        return jsonify({"failed": 1, "error": error_msg})
    else:
        return vid_analyzer
    pass


def get_vector(source, type="url"):
    if type == "url":
        return get_vector_from_url(source)
    elif type == "file":
        return get_vector_from_file(source)
    else:
        raise "Unexpected image source."


def get_doc(source, data, featureFlags, type):
    """
    source could be a url or a wertrezeug.File object containing the raw
    bytes of the file.
    """
    doc = {}

    return doc
