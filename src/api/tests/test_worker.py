from core import config
from core.feluda import ComponentType, Feluda
import json

# start queue
# # writing a message
# waiting on the listener

def make_report(data, status):
    report = {}
    report["indexer_id"] = 1
    report["post_id"] = data["post"]["id"]
    report["status"] = status
    report["status_code"] = 200
    return json.dumps(report)



try:
    feluda = Feluda("config-indexer.yml")
    feluda.setup()
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
except Exception as e:
    print("Error Initializing Indexer")
