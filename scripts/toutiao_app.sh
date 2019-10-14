#! /bin/bash
source ~/.bash_profile
export FLASK_ENV=production
cd /home/python/toutiao-backend/
workon toutiao
exec gunicorn -b 0.0.0.0:8000 --access-logfile /home/python/logs/access_app.log --error-logfile /home/python/logs/error_app.log toutiao.main:app