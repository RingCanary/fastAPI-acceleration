# fastAPI-acceleration
Profiling sample use case api to check and optimize production FastAPI apps

## Setup

Install `uv` from https://docs.astral.sh/uv/getting-started/installation/

(macOS and Linux)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation cd to the repo (`git clone https://github.com/RingCanary/fastAPI-acceleration.git`)
and run the following commands

```bash
uv sync
# let the packages download, takes a short time | uv is quite fast

source .venv/bin/activate
# activates python virtual env, install if it fails,
# "sudo apt update && sudo apt install python3-venv"

uvicorn main:app --reload --workers 1
# this serves the api on 127.0.0.1:8000 or http://localhost,
# which you can cUrl to via browser
```

Leave the app running and now, to time the I/O test with following command on another shell

```bash
time curl http://127.0.0.1:8000/is-io-async-good
```
