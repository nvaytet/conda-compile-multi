import glob
import os
import pathlib
import subprocess
import sys
import uuid


def parse_input_file(filename):
    with open(filename, 'r') as f:
        content = f.readlines()
    out = []
    for line in content:
        if line.startswith('-r'):
            out += parse_input_file(line.split()[-1])
        else:
            out.append(line.strip())
    return out


def process_file(filename):

    dependencies = parse_input_file(filename)

    env_name = uuid.uuid4().hex
    out = subprocess.check_output(
        ['mamba', 'create', '-c', 'conda-forge', '--dry-run', '-n', env_name] +
        dependencies,
        stderr=subprocess.STDOUT,
        shell=sys.platform == "win32")

    with open(os.path.splitext(filename)[0] + '.txt', 'w') as f:
        for l in out.decode().split('\n'):
            if l.strip().startswith('+'):
                to_write = l.lstrip(' +').split()[:2]
                f.write(f'{to_write[0]}={to_write[1]}\n')


if __name__ == '__main__':

    for file in glob.glob('*.in'):
        print('Locking dependencies in', file)
        process_file(file)
