#!/bin/bash
export PYTHONPATH="."

alembic --name=alembic_${TARGET_ALEMBIC_APP} upgrade head

uvicorn --host 0.0.0.0 --port $PORT "rental.asgi:app"
