#/bin/bash

set -eo pipefail

alembic upgrade head
python -m app.main