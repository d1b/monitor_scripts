#!/usr/bin/python3
import os
import subprocess


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    stats_dir = os.path.join(here, 'stats')
    path = '/dev/disk/by-id/'
    for i in os.listdir(path):
        full_path = os.path.join(path, i)
        if ('part' not in i.split('-')[-1] and 
            i.startswith('ata-') and not i.lower().endswith('.py')):
            proc = subprocess.Popen(['smartctl', '-a', full_path], 
                stdout=subprocess.PIPE)
            output = proc.communicate()[0]
            with open(os.path.join(stats_dir, i), 'w+') as f:
                f.write(output.decode('utf-8'))  
                for line in output.decode('utf-8').split('\n'):
                    if 'Power_On_Hours' in line:
                        hours = int(line.split(' ')[-1].split('h')[0])
                        print(full_path, 'Years online', ((hours / 24) / 365.25) )
                        if 'h' in line:
                            print('\tReported as', line.split(' ')[-1])


if __name__ == '__main__':
  main()

