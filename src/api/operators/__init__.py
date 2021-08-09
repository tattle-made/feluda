import text
import image
import video


def get_operator(media_type):
    if media_type == "text":
        return text
    elif media_type == "image":
        return image
    elif media_type == "video":
        return video
