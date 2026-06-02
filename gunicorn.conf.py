# gunicorn.conf.py
import multiprocessing

# --- Network Socket Binding ---
bind = "0.0.0.0:10000"

# --- Process Concurrency Tuning ---
# Automatically scales worker count based on the assigned CPU core allocation formula (2 * Cores + 1)
workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = 'sync'

# --- Resource Lifespan Controls ---
timeout = 30
keepalive = 2

# --- Operational Logging Paths ---
errorlog = '-'
accesslog = '-'
loglevel = 'info'