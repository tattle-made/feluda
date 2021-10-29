# Developing Locally

Run the docker container with debugpy and then you can add breakpoint and inspect as API requests come in via curl or by running a test

For debugging, edit the docker-compose.yml file as target : debug

whats happening ?
python runs the debugger, which runs the app.
vscode can then listen on port 5678 to the debugger and intercept breakpoints.
debugpy --wait-for-client argument makes debugpy wait on executing the given command (starting the app), till a client is listening to it (vscode, in our case)

If you ensure that the FLASK_ENV environment variable is set to development
`export FLASK_ENV=development`
and run
`python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py`
it will make sure that any changes you make to your source code will trigger an automatic reload
of the server. As long as there's a client like VScode attached to the debug server, you'll be able
to iterate on the codebase and test quickly.
