import uvloop


worker_class = "uvicorn.workers.UvicornWorker"
workers = 4
bind = "0.0.0.0:8000"
timeout = 120
graceful_timeout = 30
keepalive = 5
accesslog = "/logs/app.log"
errorlog = "/logs/app.log"

uvloop.install()