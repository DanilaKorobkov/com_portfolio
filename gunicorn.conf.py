# pylint: disable=invalid-name
# pylint: disable=invalid-envvar-default

from multiprocessing import cpu_count
from os import getenv as env

from com_portfolio import log

# Internal setting that is adjusted for each type of application.
default_proc_name = "gunicorn:com_portfolio"

# Check the configuration and exit. The exit status is 0 if the configuration
# is correct, and 1 if the configuration is incorrect.
check_config = env("GUNICORN_CHECK_CONFIG", False)

# The socket to bind.
bind = env("GUNICORN_BIND", "0.0.0.0:8080")

# The number of worker processes that this server
# should keep alive for handling requests.
workers = env("GUNICORN_WORKERS", cpu_count() * 2 + 1)

# The type of workers to use.
worker_class = env("GUNICORN_WORKER_CLASS", "aiohttp.GunicornUVLoopWebWorker")

# The number of seconds to wait for the next
# request on a Keep-Alive HTTP connection.
keepalive = env("GUNICORN_KEEPALIVE", 10)

# The maximum number of pending connections. This refers to the number
# of clients that can be waiting to be served. Exceeding this number results
# in the client getting an error when attempting to connect
backlog = env("GUNICORN_BACKLOG", 2048)

# If a worker does not notify the master process in this number of
# seconds it is killed and a new worker is spawned to replace it.
timeout = env("GUNICORN_TIMEOUT", 60)

# The maximum number of requests a worker will process before restarting.
# Any value greater than zero will limit the number of requests a worker
# will process before automatically restarting.
# This is a simple method to help limit the damage of memory leaks.
max_requests = env("GUNICORN_MAX_REQUESTS", 1024)

# Timeout for graceful workers restart.
# After receiving a restart signal, workers have this much time to finish
# serving requests.
# Workers still alive after the timeout are force killed.
graceful_timeout = env("GUNICORN_GRACEFUL_TIMEOUT", 30)

# Install a trace function that spews every line of Python
# that is executed when running the server.
# This is the nuclear option.
spew = env("GUNICORN_SPEW", False)

# Daemonize the Gunicorn process.
# Detaches the server from the controlling terminal and enters the background.
daemon = env("GUNICORN_DAEMON", False)

_STDOUT = _STDERR = "-"

# The path to a log file to write to.
logfile = env("GUNICORN_LOGFILE", _STDOUT)

# The granularity of log output.
loglevel = env("GUNICORN_LOGLEVEL", log.LEVEL)

# Where to write error log.
errorlog = env("GUNICORN_ERRORLOG", _STDERR)

# Where to write access log.
accesslog = env("GUNICORN_ACCESSLOG", _STDOUT)

# The access log format.
access_log_format = log.GUNICORN_ACCESS_LOG_FORMAT

# The log config dictionary to use, using the standard Python
# logging module’s dictionary configuration format.
logconfig_dict = log.CONFIG
