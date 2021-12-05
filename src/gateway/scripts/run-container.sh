#!/bin/bash
export PYTHONPATH="."

uvicorn --host 0.0.0.0 --port $PORT "gateway.asgi:app"
