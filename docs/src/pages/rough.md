# Semantics

throughout the code you will read references to something called representation (occasionally shortened to rep), this
is supposed to mean some kind of simplification of a media item.
For instance an image may be **represented** by a string hash or a 512 dimensional vector. So, the word representation is a
generic way to encapsulate this idea. This allows us to write generic interfaces like store(rep) to store a representation
of a media item in a database (mongo, sql, elasticsearch) as opposed to creating functions like store(hash), store(vector) etc.

# Logging

there is a centralized logger that is passed from app.py to every module/component/feature.
modules should expect it as a dependency and use log.info(), log.debug(), log.error() as a way to log results.
During development these logs will be available for viewing to the developer in their terminal whereas in production, these will be collected by a log agent
and sent to a centralized dashboard like kibana or xyz
For exception handling, please use the log.exception() method. this ensures that the stack trace is printed along with the exception and is helpful in debugging.

it would be better to find out a way to remove logger as a dependency of every module. so you didn't have to pass it to every

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
