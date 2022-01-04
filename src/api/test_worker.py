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
        print(data)
        report = {}
        post = Post.fromRequestPayload(data)
        operators = feluda.operators.active_operators
        representation = generateRepresentation(post, operators)
        document = generateDocument(post, representation)
        save_result = feluda.store.store(post.type, document)
        print(save_result)
        # return save_result
        report["id"] = data["post"]["id"]
        report["datasource"] = data["post"]["datasource_id"]
        report["status"] = "indexed"
        print(report)

        # try:
        #     print("Indexing data ...")
        #     index_id = index_data(es, data)

        #     print("Sending report to queue ...")
        #     report["index_timestamp"] = str(datetime.utcnow())
        #     report["index_id"] = index_id
        #     report["status"] = "indexed"

        #     queue_controller.add_data_to_report_queue(json.dumps(report))
        ch.basic_ack(delivery_tag=method.delivery_tag)

        # except Exception:
        #     log.exception("Error indexing media")
        #     report["status"] = "failed"

        #     # queue_controller.add_data_to_report_queue(json.dumps(report))
        #     print("Indexing failure report sent to report queue")
        #     try:
        #         os.remove("/tmp/vid.mp4")
        #     except:
        #         pass
        #     ch.basic_ack(delivery_tag=method.delivery_tag)

    return worker


try:
    feluda = Feluda("config-indexer.yml")
    # log.prettyprint(vars(feluda))
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
    feluda.queue.listen("tattle-search-index-queue", indexer(feluda))
except Exception as e:
    log.exception("Error Initializing Indexer")
