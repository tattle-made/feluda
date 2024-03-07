# from endpoint.index.handler import generateDocument, generateRepresentation
# from endpoint.index.model import Post
from core.feluda import ComponentType, Feluda
from core.logger import Logger
import json
import requests
from os import environ

log = Logger(__name__)

secret = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjMwN2IzMTYwLTE3MjktNDI2MS04MjExLTU1YzFlOTc1ZWQ2NCIsInVzZXJuYW1lIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE2NDI2Nzc4MTh9.p9UZ1xt1kOSyBTBMr3IoeONroZZVJYfUHcM7d9CHdR0"
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
            environ.get("KOSH_API_URL") + "/index/report",
            headers=headersAuth,
            json=report,
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        log.exception("Error Reporting Index Status")


try:
    feluda = Feluda("config-indexer.yml")
    # log.prettyprint(vars(feluda))
    feluda.start_component(ComponentType.QUEUE)
    feluda.queue.listen("tattle-search-report-queue", reporter)
except Exception:
    log.exception("Error Initializing Indexer")
