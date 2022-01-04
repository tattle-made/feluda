from endpoint.index.handler import generateDocument, generateRepresentation
from endpoint.index.model import Post
from core.feluda import ComponentType, Feluda
from core.logger import Logger
import json
import os

log = Logger(__name__)


def indexer(feluda):
    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")
        # print(type(body))
        # print(type(json.loads(body)))
        data = json.loads(body)
        report = {}
        report["id"] = data["post"]["id"]
        report["datasource"] = data["post"]["datasource_id"]
        try:
            print(data)
            report = {}
            post = Post.fromRequestPayload(data)
            operators = feluda.operators.active_operators
            representation = generateRepresentation(post, operators)
            document = generateDocument(post, representation)
            save_result = feluda.store.store(post.type, document)
            print(save_result)
            # return save_result
            report["status"] = "indexed"
            # print(report)
            feluda.queue.message("tattle-search-report-queue", report)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            log.exception("Error indexing media")
            report["status"] = "failed"
            feluda.queue.message("tattle-search-report-queue", report)
            try:
                os.remove("/tmp/vid.mp4")
            except:
                log.exception("Error deleting video file")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    return worker


try:
    feluda = Feluda("config-indexer.yml")
    # log.prettyprint(vars(feluda))
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
    feluda.queue.listen("tattle-search-index-queue", indexer(feluda))
except Exception as e:
    log.exception("Error Initializing Indexer")
