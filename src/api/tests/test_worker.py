from core import config
from core.feluda import ComponentType, Feluda

feluda = Feluda("config-indexer.yml")
feluda.setup()


# start queue
# # writing a message
# waiting on the listener


print(feluda)
