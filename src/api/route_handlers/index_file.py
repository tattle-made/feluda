import operators
import features
from services.es import get_es_instance
import os
from indices import get_index_name

es = get_es_instance()


def handle_index_file(request):
    try:
        res = {}
        file = request.files["file"]
        data = request.form.to_dict(flat=True)

        mediaType = data["media_type"]
        operator = operators(mediaType)
        featureFlags = features(mediaType)
        index_name = get_index_name(mediaType)

        es_doc = operator.get_doc(file, data, featureFlags, type="file")

        res = es.index(index=index_name, body=es_doc)

        return res
    except:
        raise "Could not index file"


def handle_index_url(request):
    try:
        res = {}

        return res
    except:
        raise "Could not index file from url"
