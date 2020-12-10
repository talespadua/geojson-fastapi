from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix=False,
    merge_enabled=True,
    load_dotenv=True,
    environments=True,
    validators=[
        Validator("DB_CONNECTION_STRING", must_exist=True),
        Validator("ENVIRONMENT", is_type_of=str, default="production"),
        Validator("HOSTNAME", is_type_of=str, default=""),
        Validator("ACCESS_LOG", is_type_of=bool, default=False),
        Validator("PORT", is_type_of=int, default=5000),
        Validator("HOST", is_type_of=str, default="0.0.0.0"),
        Validator("LOGGING_LEVEL", is_type_of=str, default="INFO"),
    ],
)

settings.INSTANCE = settings.HOSTNAME
settings.DEBUG = settings.ENVIRONMENT == "development"

settings.LOGGING = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)-15s %(levelname)s %(message)s",
        }
    },
    "filters": {
        "container": {
            "()": "project.libs.monitoring.logging.filters.Container",
            "environment": settings.ENVIRONMENT,
            "instance": settings.INSTANCE,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "json",
            "filters": ["container"],
        },
    },
    "loggers": {
        "lore": {
            "level": settings.LOGGING_LEVEL,
            "handlers": ["console"],
        },
        "alembic": {
            "level": "INFO",
            "qualname": "alembic",
            "handlers": ["console"],
        },
        "sqlalchemy": {
            "level": "WARN",
            "qualname": "sqlalchemy.engine",
            "handlers": ["console"],
        },
    },
}
