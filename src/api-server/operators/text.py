from textblob import TextBlob
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer

sent_model = SentenceTransformer("paraphrase-xlm-r-multilingual-v1")


def detect_lang(text):
    if text == "" or text == " " or len(text) < 3:
        return None
    supported = ["en", "hi", "gu"]
    blob = TextBlob(text)
    lang = blob.detect_language()
    if lang not in supported:
        return None
    else:
        return lang


def transform_text(text):
    """
    New, transformer model-based method for generating text document vectors.
    Returns a 768-dimensional vector representation of the input text in any language.
    """
    vec = sent_model.encode(text)
    return vec


def get_vector_from_file(file):
    text_bytes = file.read()
    text_vec = transform_text(text_bytes, sent_model)
    if text_vec is None:
        text_vec = np.zeros(768).tolist()
    return text_vec


def get_vector_from_url(url):
    pass


def get_vector(imageSource, type="url"):
    if type == "url":
        return get_vector_from_url(imageSource)
    elif type == "file":
        return get_vector_from_file(imageSource)
    else:
        raise "Unexpected image source."


def get_doc(source, data, featureFlags, type):
    """
    source could be a url or a wertrezeug.File object containing the raw
    bytes of the file.
    """
    doc = {}

    doc_id = str(data["source_id"])
    text = get_text(source, type)
    text_vec = get_vector(source, type)
    date = datetime.utcnow()

    lang = detect_lang(text)

    doc = {
        "source_id": doc_id,
        "source": data.get("source", "tattle-admin"),
        "metadata": data.get("metadata", {}),
        "text": text,
        "lang": lang,
        "text_vec": text_vec,
        "date_added": date,
    }

    return doc
