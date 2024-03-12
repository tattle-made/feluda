def initialize(param):
    global TextBlob

    from textblob import TextBlob


def run(text):
    if text == "" or text == " " or len(text) < 3:
        return None
    supported = ["en", "hi", "gu"]
    blob = TextBlob(text)
    lang = blob.detect_language()
    if lang not in supported:
        return "und"
    else:
        return lang


def state():
    pass
