# Developing Locally

Run the docker container with debugpy and then you can add breakpoint and inspect as API requests come in via curl or by running a test

For debugging, edit the docker-compose.yml file as target : debug

whats happening ?
python runs the debugger, which runs the app.
vscode can then listen on port 5678 to the debugger and intercept breakpoints.
debugpy --wait-for-client argument makes debugpy wait on executing the given command (starting the app), till a client is listening to it (vscode, in our case)
