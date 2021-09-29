from datetime import datetime


def text_rep_to_es_doc(rep, data):
    doc = {
        "source_id": str(data["source_id"]),
        "source": data.get("source", "tattle-admin"),
        "metadata": data.get("metadata", {}),
        "text": rep["text"],
        "lang": rep["lang"],
        "date_added": datetime.utcnow(),
    }
    return doc


def image_rep_to_es_doc(rep, data):
    doc = {
        "source_id": str(data["source_id"]),
        "source": data.get("source", "tattle-admin"),
        "metadata": data.get("metadata", {}),
        "has_text": rep["has_text"],
        "text": rep["detected_text"],
        "lang": rep["lang"],
        "image_vec": rep["vec"],
        "date_added": datetime.utcnow(),
    }
    return doc


def video_rep_to_es_doc(rep, data):
    """
    returns a tuple (avg_vec_doc, generator_of_docs)
    """
    doc = {
        "source_id": str(data["source_id"]),
        "source": data.get("source", "tattle-admin"),
        "metadata": data.get("metadata", {}),
        "vid_vec": rep["avg"]["vec"],
        "is_avg": True,
        "duration": rep["duration"],
        "n_keyframes": rep["n_keyframes"],
        "date_added": datetime.utcnow(),
    }
    # todo : fix hardcode of _index
    def gendata():
        for i in range(rep["n_keyframes"]):
            yield {
                "_index": "video",
                "source_id": str(data["source_id"]),
                "source": data.get("source", "tattle-admin"),
                "metadata": data.get("metadata", {}),
                "vid_vec": rep["gen"][i],
                "is_avg": False,
                "duration": rep["duration"],
                "n_keyframes": rep["n_keyframes"],
                "date_added": datetime.utcnow(),
            }

    return (doc, gendata)
