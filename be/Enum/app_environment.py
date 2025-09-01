from enum import Enum


class AppEnvironmentEnum(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
