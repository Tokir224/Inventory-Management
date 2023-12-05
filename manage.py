#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def get_env():
    ENVIRONMENT_TYPE = os.getenv("ENVIRONMENT_TYPE", default="development")

    if ENVIRONMENT_TYPE == "development":
        return os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings.development')
    elif ENVIRONMENT_TYPE == "staging":
        return os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings.staging')
    elif ENVIRONMENT_TYPE == "production":
        return os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings.production')


def main():
    """Run administrative tasks."""
    get_env()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
