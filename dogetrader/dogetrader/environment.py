import os
import re
import subprocess


VARIABLE_PREFIX = 'DOGETRADER_'


def source_environment_vars(file_path='/etc/default/dogetrader', key_regex=re.compile('^(%s|DJANGO_).*' % VARIABLE_PREFIX)):
    """
    Sources environment variables from the specified bash script.
    """

    command = ['bash', '-c', 'source %s && env' % file_path]
    proc = subprocess.Popen(command, stdout = subprocess.PIPE)

    for line in proc.stdout:
        key, _, value = line.rstrip('\r\n').partition('=')
        if key_regex is None or key_regex.match(key):
            os.environ[key] = value

    proc.communicate()
