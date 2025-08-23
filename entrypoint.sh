#!/bin/sh
set -e

. ./.venv/bin/activate

if [ "$RUN_MODE" = "dev" ]; then
    echo "RUN_MODE=dev → doing nothing, keeping container alive..."
    fastapi dev src/plum_chatbot/webserver/webserver.py --app app --host 0.0.0.0 --port 8000
    exec tail -f /dev/null
else
    echo "RUN_MODE=$RUN_MODE → starting fastapi..."
    exec fastapi run src/plum_chatbot/webserver/webserver.py --app app --host 0.0.0.0 --port 8000
fi
