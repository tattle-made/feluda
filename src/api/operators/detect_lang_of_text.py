from .installer import install_packages

requirement_list = ["pytest", "nltk==3.6", "textblob==0.15.3"]


def initialize(param):
    print("Intalling packages for detect_lang_of_text")
    install_packages(requirement_list)

    global TextBlob

    from textblob import TextBlob


def run(text):
    if text == "" or text == " " or len(text) < 3:
        return None
    supported = ["en", "hi", "gu"]
    blob = TextBlob(text)
    lang = blob.detect_language()
    if lang not in supported:
        return None
    else:
        return lang


def state():
    pass
