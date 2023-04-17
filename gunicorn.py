import multiprocessing

command = '/home/ubuntu/wiseBackend/env/bin/gunicorn'
pythonpath = '/home/ubuntu/wiseBackend'
bind = '0.0.0.0:8000'
workers = (multiprocessing.cpu_count() * 2)