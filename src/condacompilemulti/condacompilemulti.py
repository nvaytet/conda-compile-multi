import argparse
import os
import pathlib
import subprocess
import sys
import uuid

parser = argparse.ArgumentParser(description='')
parser.add_argument('--file')

if __name__ == '__main__':

    args = parser.parse_args()

    env_name = uuid.uuid4().hex

    out = subprocess.check_output(
        ['conda', 'create', '--dry-run', '--file', args.file, '-n', env_name],
        stderr=subprocess.STDOUT,
        shell=sys.platform == "win32")

    print(out)
