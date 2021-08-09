indexer_text = {"use_sentence_transformer": False}

indexer_image = {"include_text_vector": True, "include_composite_vector": False}

indexer_video = {}


def getIndexFeatures(mediaType):
    if mediaType == "text":
        return indexer_text
    elif mediaType == "image":
        return indexer_image
    elif mediaType == "video":
        return indexer_video
