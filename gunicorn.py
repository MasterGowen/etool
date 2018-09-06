import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "softskills.settings")
preload_app = False
timeout = 300
bind = "0.0.0.0:9999"
pythonpath = "/projects/softskills"

settings_file = "softskills.settings"
errorlog = "/projects/var/log/softskills/error.log"
loglevel = 'debug'
accesslog = "/projects/var/log/softskills/access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

workers = 1
