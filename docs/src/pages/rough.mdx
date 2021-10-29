---
title: Rough Notes
---

# Semantics

throughout the code you will read references to something called representation (occasionally shortened to rep), this
is supposed to mean some kind of simplification of a media item.
For instance an image may be **represented** by a string hash or a 512 dimensional vector. So, the word representation is a
generic way to encapsulate this idea. This allows us to write generic interfaces like store(rep) to store a representation
of a media item in a database (mongo, sql, elasticsearch) as opposed to creating functions like store(hash), store(vector) etc.

# Logging

within every module, inject the following code

```python
import logging
log = logging.getLogger(__name__)
```

Continue to use log.info(), log.warning() and log.error() as a way to log results.
During development these logs will be available for viewing to the developer in their terminal whereas in production, these will be collected by a log agent
and sent to a centralized dashboard like kibana or xyz

For exception handling, please use the `log.exception()` method instead of `log.error()`. this ensures that the stack trace is printed along with the exception and is helpful in debugging.

```python
log.info("hello")
log.warning("missing field : age")
log.error("somethign terrible happened")
log.exception("Error Initializing App")
```

to pretty print dict, use this `log.info(json.dumps(my_dict, indent=4))`

# TODO

- [ ] write helper scripts for day to day operations, monitoring and debugging. eg : show pending items in a queue, flush the queue etc
- [ ] Create a UI to demonstrate and test the server

# Making Changes

for any changes to how API endpoints are handled, look for corresponding functions in the handlers function
todo : collocate handler functions and the mapping between API endpoints and the handler functions

# Caveats

Ensure that the operators you need are enabled in the config.yml and that only those operators are reffered to within your code base.

# API definitions are defined in features

elements of a feature :
controllers, routes, model

# Pretty print while debugging

a lot of the config and payloads are dicts. pprint is a handy way to see them in a formatted way.
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(my_dict)

in the request payload, either look for the media item in the files OR look for a media_url or text field in the post_data

# Python and pip related things

pip list
pip install <package_name> -U // upgrades the package to its latest version.

RESUME
Open code in vscode
open 3 terminals 1. docker-compose up 2. docker exec -it <container_id> /bin/sh -> python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py 3. docker exec -it <container_id> /bin/sh -> nose2 feature.index.test_index.TestIndex.testRepresetnVideo
