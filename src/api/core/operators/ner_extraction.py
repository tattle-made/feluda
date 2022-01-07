from .installer import install_packages

"""
This operator uses google cloud API to extract text from an image.
the credentials to use the cloud vision API should be present in a file titled credentials.json
in the root folder. if it isn't present, it can be optionally fetched from an aws s3 bucket.
The AWS credentials to do this need to be set in the environment variables : AWS_ACCESS_KEY_ID, 
AWS_SECRET_ACCESS_KEY_ID, AWS_BUCKET, S3_CREDENTIALS_PATH

pip install :
google-cloud==0.34.0
google-cloud-vision==0.34.0
boto3
"""
requirement_list = ["translate==3.6.1", "spacy==3.2.1", "en_core_web_sm"]


def initialize(param):
    install_packages(requirement_list)

    global Translator, spacy, NER

    from translate import Translator
    import spacy

    NER = spacy.load("en_core_web_sm")


def run(text):
    translator = Translator(to_lang="en", from_lang="autodetect")
    translation = translator.translate(text)
    entity_tuple = NER(translation)
    entities = []
    for word in entity_tuple.ents:
        entities.append(word.text)

    return entities


def cleanup(param):
    pass


def state():
    return {
        "label": "Named Entity Extraction from Text in non english language",
    }
