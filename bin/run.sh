#/bin/bash

set -eo pipefail

alembic upgrade head
gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker 