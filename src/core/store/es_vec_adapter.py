from datetime import datetime


def text_rep_to_es_doc(rep, data):
    doc = {
        "e_kosh_id": str(data["source_id"]),
        "source": data.get("source", "tattle-admin"),
        "metadata": data.get("metadata", {}),
        "text": rep["text"],
        "lang": rep["lang"],
        "date_added": datetime.utcnow(),
    }
    return doc


def image_rep_to_es_doc(rep, data):
    doc = {
        "e_kosh_id": str(data["source_id"]),
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
        "e_kosh_id": str(data["source_id"]),
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
                "e_kosh_id": str(data["source_id"]),
                "source": data.get("source", "tattle-admin"),
                "metadata": data.get("metadata", {}),
                "vid_vec": rep["gen"][i],
                "is_avg": False,
                "duration": rep["duration"],
                "n_keyframes": rep["n_keyframes"],
                "date_added": datetime.utcnow(),
            }

    return (doc, gendata)


def es_to_sanitized(resp):
    doc_ids, dists, source_ids, sources, texts, metadata = [], [], [], [], [], []

    for h in resp["hits"]["hits"]:
        doc_ids.append(h["_id"])
        dists.append(h["_score"])
        source_ids.append(h["_source"]["e_kosh_id"])
        sources.append(h["_source"]["dataset"])
        texts.append(h["_source"].get("text", None))
        metadata.append(h["_source"]["metadata"])

    result = [
        {
            "doc_id": doc_ids[i],
            "dist": dists[i],
            "dataset": sources[i],
            "e_kosh_id": source_ids[i],
            "text": texts[i],
            "metadata": metadata[i],
        }
        for i in range(len(doc_ids))
    ]
    return result
