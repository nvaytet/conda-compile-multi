import argparse
import os
import pathlib
import subprocess
import sys
import uuid

parser = argparse.ArgumentParser(description='')
parser.add_argument('-i', '--input-file')
parser.add_argument('-o', '--output-file')

if __name__ == '__main__':

    args = parser.parse_args()

    env_name = uuid.uuid4().hex

    out = subprocess.check_output([
        'mamba', 'create', '-c', 'conda-forge', '--dry-run', '--file',
        args.input_file, '-n', env_name
    ],
                                  stderr=subprocess.STDOUT,
                                  shell=sys.platform == "win32")

    with open(args.output_file, 'w') as f:
        for l in out.decode().split('\n'):
            if l.strip().startswith('+'):
                to_write = l.lstrip(' +').split()[:2]
                f.write(f'{to_write[0]}={to_write[1]}\n')
