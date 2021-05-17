web: PYTHONUNBUFFERED=1 python -Wall manage.py runserver 0.0.0.0:$PORT
mailhog: bash -c 'if [[ ! $(pgrep mailhog) ]]; then mailhog; else while true; do sleep 99999; done; fi'