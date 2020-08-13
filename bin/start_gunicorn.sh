source /home/nikita/code/tennis_env/bin/activate
exec gunicorn -c "/home/nikita/code/TennisBot/tennis_bot/tennis_bot/tennis_bot/gunicorn_config.py" tennis_bot.wsgi

