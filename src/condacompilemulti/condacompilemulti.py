import argparse
import glob
import os
import pathlib
import subprocess
import sys
import uuid

parser = argparse.ArgumentParser(prog='conda-compile-multi')
parser.add_argument('path')
parser.add_argument('-f', '--format', default='txt')
parser.add_argument('-c', '--channel', action='append')


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


def write_txt_file(package_list, filename):
    with open(os.path.splitext(filename)[0] + '.txt', 'w') as f:
        for package in package_list:
            f.write(f'{package[0]}={package[1]}\n')


def write_yml_file(package_list, filename, channels):
    fileroot = os.path.splitext(filename)[0]
    with open(fileroot + '.yml', 'w') as f:
        f.write(f'name: {os.path.split(fileroot)[-1]}\n')
        f.write(f'channels:\n')
        for c in [channel for channel in channels if channel != '-c']:
            f.write(f'  - {c}\n')
        f.write(f'dependencies:\n')
        for package in package_list:
            f.write(f'  - {package[0]}={package[1]}\n')


def parse_mamba_output(output):
    return [
        l.lstrip(' +').split()[:2] for l in output.decode().split('\n')
        if l.strip().startswith('+')
    ]


def process_file(filename, channels, fmt):

    dependencies = parse_input_file(filename)
    channels = [item for channel in channels for item in ['-c', channel]]

    env_name = uuid.uuid4().hex
    out = subprocess.check_output(['mamba', 'create'] + channels +
                                  ['--dry-run', '-n', env_name] + dependencies,
                                  stderr=subprocess.STDOUT,
                                  shell=sys.platform == "win32")

    package_list = parse_mamba_output(output=out)

    if fmt == 'yml':
        write_yml_file(package_list=package_list,
                       filename=filename,
                       channels=channels)
    elif fmt == 'txt':
        write_txt_file(package_list=package_list, filename=filename)


if __name__ == '__main__':

    args = parser.parse_args()
    channels = args.channel
    if 'conda-forge' not in channels:
        channels.append('conda-forge')
    if 'nodefaults' not in channels:
        channels.append('nodefaults')

    for file in glob.glob(os.path.join(args.path, '*.in')):
        print('Locking dependencies in', file)
        process_file(filename=file, channels=channels, fmt=args.format)
