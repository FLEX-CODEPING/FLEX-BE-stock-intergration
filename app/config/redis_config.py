import redis
from app.config.app_config import settings

def redis_client():
    return redis.StrictRedis(
        host=settings.redis_host, 
        port=settings.redis_port, 
        db=settings.redis_db,
        password=settings.redis_password 
        decode_responses=True)
