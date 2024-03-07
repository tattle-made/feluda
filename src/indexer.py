from endpoint.index.handler import generateDocument, generateRepresentation
from endpoint.index.model import Post
from core.feluda import ComponentType, Feluda
from core.logger import Logger
import json
# import os

log = Logger(__name__)


def make_report(data, status):
    report = {}
    report["indexer_id"] = 1
    report["post_id"] = data["post"]["id"]
    report["status"] = status
    report["status_code"] = 200
    return json.dumps(report)


def indexer(feluda):
    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")
        # print(type(body))
        # print(type(json.loads(body)))
        data = json.loads(body)

        try:
            # print("---> 1", data)
            post = Post.fromRequestPayload(data)
            operators = feluda.operators.active_operators
            representation = generateRepresentation(post, operators)
            document = generateDocument(post, representation)
            # print("-----> 2", document)
            feluda.store.store(post.type, document)
            # return save_result
            report = make_report(data, "indexed")

            # print(report)
            feluda.queue.message("tattle-search-report-queue", report)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            log.exception("Error indexing media")
            report = make_report(data, "failed")
            feluda.queue.message("tattle-search-report-queue", report)
            # try:
            #     os.remove("/tmp/vid.mp4")
            # except:
            #     log.exception("Error deleting video file")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    return worker


try:
    feluda = Feluda("config-indexer.yml")

    # log.prettyprint(vars(feluda))
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
    feluda.queue.listen("tattle-search-index-queue", indexer(feluda))
except Exception as e:
    log.exception("Error Initializing Indexer:", e)
