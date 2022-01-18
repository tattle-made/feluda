from endpoint.index.handler import generateDocument, generateRepresentation
from endpoint.index.model import Post
from core.feluda import ComponentType, Feluda
from core.logger import Logger
import json
import requests
from os import environ

log = Logger(__name__)

secret = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgyOGY2NjEzLWE0ZjYtNDAxYi1iZDQ0LTBjNTI0YjljOWMwMSIsInVzZXJuYW1lIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE2NDIzNjEzNDl9.cAMEH2bawvneGmj5Pw9d1lZ6EZvMOeQPofAnJ40ZxAQ"
headersAuth = {
    "Authorization": "Basic " + str(secret),
}


def reporter(ch, method, properties, body):
    print("MESSAGE RECEIVED")
    # print(type(body))
    # print(type(json.loads(body)))
    report = json.loads(json.loads(body))
    # print(type(report))
    log.prettyprint(report)

    try:
        requests.post(
            environ.get("KOSH_API") + "/index/report", headers=headersAuth, json=report
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        log.exception("Error Reporting Index Status")


try:
    feluda = Feluda("config-indexer.yml")
    # log.prettyprint(vars(feluda))
    feluda.start_component(ComponentType.QUEUE)
    feluda.queue.listen("tattle-search-report-queue", reporter)
except Exception as e:
    log.exception("Error Initializing Indexer")
