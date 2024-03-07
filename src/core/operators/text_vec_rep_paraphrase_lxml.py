def initialize(param):
    global SentenceTransformer, sent_model, np

    from sentence_transformers import SentenceTransformer
    import numpy as np

    sent_model = SentenceTransformer("paraphrase-xlm-r-multilingual-v1")


def run(text):
    text_vec = sent_model.encode(text)
    if text_vec is None:
        text_vec = np.zeros(768).tolist()
    return text_vec
