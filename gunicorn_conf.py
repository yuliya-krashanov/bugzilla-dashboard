import os

TMP = os.path.expanduser("~/tmp/")


def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

port = os.environ.get('GUNICORN_PORT', 9006)

bind = "127.0.0.1:%s" % port
workers = 3
worker_class = "gevent"
max_requests = 1000
daemon = True
pidfile = TMP + "dash_stats_g.pid"
accesslog = TMP + "dash_stats_g.access.log"
errorlog = TMP + "dash_stats_g.error.log"
graceful_timeout = 60
timeout = 300
keepalive = 0
