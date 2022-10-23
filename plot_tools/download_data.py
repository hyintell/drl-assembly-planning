import wandb
import os
import argparse
import tqdm

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
        if run.state == 'finished':
            if run.group == cur_group:
                file_name = run.name
                env_info = file_name.split('_')[0]
                algo_name = file_name.split('_')[1]
                seed_num = file_name.split('_')[2]
                save_path = 'logs/{}_logs/env{}/scene{}/seed_{}'.format(algo_name, env_info[1], env_info[3], seed_num)
                if os.path.exists(save_path):
                    continue
                print(save_path)
                os.makedirs(save_path, exist_ok=True)
                for file in run.files():
                    if 'events' in file.name:
                        file.download(save_path)