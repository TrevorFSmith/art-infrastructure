import multiprocessing

preload_app = True
pidfile = 'ai-gunicorn.pid'
debug = True
proc_name = 'ai' # requires setproctitle module to be installed
workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2
bind = '0.0.0.0:8000'
logfile = 'ai-gunicorn.log'
user = 'art'
group = 'art'
#loglevel = 'debug'
