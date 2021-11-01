from .installer import install_packages

requirement_list = [
    "numpy==1.20.2",
    "nltk==3.6",
    "scikit-learn==0.24.1",
    "scipy==1.6.2",
    "sentence-transformers==1.0.4",
    "-f https://download.pytorch.org/whl/torch_stable.html torch==1.8.1+cpu",
    "tqdm==4.60.0",
    "transformers==4.5.0",
]


def initialize(param):
    install_packages(requirement_list)

    global SentenceTransformer, sent_model, np

    from sentence_transformers import SentenceTransformer
    import numpy as np

    sent_model = SentenceTransformer("paraphrase-xlm-r-multilingual-v1")


def run(text):
    text_vec = sent_model.encode(text)
    if text_vec is None:
        text_vec = np.zeros(768).tolist()
    return text_vec
