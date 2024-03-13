# from endpoint.index.handler import generateDocument, generateRepresentation
# from endpoint.index.model import Post
from core.feluda import ComponentType, Feluda
from core.logger import Logger
import json

log = Logger(__name__)


def reporter(ch, method, properties, body):
    print("MESSAGE RECEIVED")
    # print(type(body))
    # print(type(json.loads(body)))
    report = json.loads(json.loads(body))
    # print(type(report))
    log.prettyprint(report)

    try:
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
