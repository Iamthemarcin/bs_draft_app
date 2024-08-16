#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import debugpy

    

def main():
    """Run administrative tasks."""
    #if you start the django with the docker compose up -f "docker-compose-debug.yml" command you'll have a debugger.
    #it slows down restarting a bit tho so only use in bigboi bugs
    if os.getenv('DEBUGPY_DJANGO') == 'true':
        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
            import debugpy
            debugpy.listen(("0.0.0.0", 3000))
            debugpy.wait_for_client()
            print('Attached!')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'power_draft.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    try:
        execute_from_command_line(sys.argv)
    except SystemExit as e:
        if e.code != 0: 
            raise
        sys.exit(0)
if __name__ == '__main__':
    main()
