
GYS — deployment notes

- Start command (Procfile):

```
web: gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

- Render notes:
	- Ensure the service start command matches the Procfile or is set to use `gunicorn wsgi:app`.
	- If Render shows an error mentioning `unicorn.conf.py` (missing "g"), check your Render service settings for a typo in any supervisor/command configuration and replace it with `gunicorn.conf.py` or use the Procfile start command above.

