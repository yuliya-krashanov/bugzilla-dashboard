import os

TMP = os.path.expanduser("~/tmp/")


def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")


# bind = "unix:/tmp/gunicorn.sock"

port = os.environ.get('GUNICORN_PORT', 9003)

bind = "127.0.0.1:%s" % port
workers = 4
worker_class = "gevent"
max_requests = 1000
daemon = True
pidfile = TMP + "dash_stats_g.pid"
accesslog = TMP + "dash_stats_g.access.log"
errorlog = TMP + "dash_stats_g.error.log"
graceful_timeout = 60
timeout = 500
keepalive = 0
