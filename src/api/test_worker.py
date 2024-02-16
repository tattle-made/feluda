from core import config
from core.feluda import ComponentType, Feluda

feluda = Feluda("config-indexer.yml")
feluda.setup()


print(feluda)
