# workout
An AI-driven Personal Training

## INSTALL
### RUN REDIS
```bash
source source/redis.py
```

### RUN CELERY WORKER
celery -A features.server.app.celery worker --loglevel=info
