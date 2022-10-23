import wandb
import os
import argparse
import tqdm
from datetime import datetime

"""
download tfevents / log files from wandb server
"""

parser = argparse.ArgumentParser()
parser.add_argument('--group-name', type=str, default='Env_1_Scene_1', help='the group name')
parser.add_argument('--project-name', type=str, default='bim-benchmark', help='the name of the project')
parser.add_argument('--user-name', type=str, default='your wandb username', help='the name of wandb user')

if __name__ == '__main__':
    api = wandb.Api()
    args = parser.parse_args()
    cur_group = args.group_name
    # please change to personal wandb account
    runs = api.runs('{}/{}'.format(args.user_name, args.project_name))
    for run in runs:
        if run.group == cur_group:
            file_name = run.name
            if run.state != 'finished' and run.state != 'running':
                print('[{}] {}: {}'.format(datetime.now(), file_name, run.state))