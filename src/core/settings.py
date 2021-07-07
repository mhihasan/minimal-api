import os

MONGODB_HOST = os.environ.get("MONGODB_HOST", "localhost")
MONGODB_PORT = int(os.environ.get("MONGODB_PORT", 27017))

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

STAGE = os.environ.get("STAGE", "test")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

config = {
    "databases": {
        "mongodb": {
            "name": f"webapp-{STAGE}",
            "host": MONGODB_HOST,
            "port": MONGODB_PORT,
        }
    },
    "redis": {"host": REDIS_HOST, "port": REDIS_PORT},
    "env": {"stage": STAGE, "log_level": LOG_LEVEL},
}
