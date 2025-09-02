from enum import Enum


class EnvironmentNameEnum(str, Enum):
    APP_ENVIRONMENT = "APP_ENVIRONMENT"
    DATABASE_CONNECTION_STRING = "DATABASE_CONNECTION_STRING"
