#!/usr/bin/env python
import sys

from dogetrader.environment import source_environment_vars

if __name__ == "__main__":
    source_environment_vars()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
