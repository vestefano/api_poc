#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import coverage


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_poc.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    cov = coverage.coverage(
        source=['.'],
        branch=True,
        omit=[
            '*/migrations/*',
            '*/test/*',
            '*/__init__.py',
            'api_poc/wsgi.py',
            '*/urls.py',
            'manage.py',
            '*_dev.*',
            '*/admin',
            '*/apps.py',
            'api_poc/*',
            'seeder_script.py'
        ]
    )
    cov.erase()
    cov.start()

    execute_from_command_line(sys.argv)

    cov.stop()
    cov.save()
    cov.report()

    cov.xml_report(outfile='./cov/coverage.xml')
    cov.html_report(directory='./cov')


if __name__ == '__main__':
    main()
