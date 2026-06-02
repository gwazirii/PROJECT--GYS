# gunicorn.conf.py
import multiprocessing
import os

# --- Network Socket Binding ---
# Use the PORT provided by the hosting environment (e.g. Render uses $PORT)
port = os.environ.get('PORT', '10000')
bind = f"0.0.0.0:{port}"

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