def es_to_sanitized(resp):
    doc_ids, dists, source_ids, sources, texts, metadata = [], [], [], [], [], []

    for h in resp["hits"]["hits"]:
        doc_ids.append(h["_id"])
        dists.append(h["_score"])
        source_ids.append(h["_source"]["source_id"])
        sources.append(h["_source"]["source"])
        texts.append(h["_source"].get("text", None))
        metadata.append(h["_source"]["metadata"])

    result = [
        {
            "doc_id": doc_ids[i],
            "dist": dists[i],
            "source": sources[i],
            "source_id": source_ids[i],
            "text": texts[i],
            "metadata": metadata[i],
        }
        for i in range(len(doc_ids))
    ]
    return result
