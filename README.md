# Deep Reinforcement Learning For Assembly Planning
This is the official code for our paper "Deep Reinforcement Learning for Real-time Assembly Planning in Robot-based Prefabricated Construction" (Under Review).

## Requirements
- pygame==2.1.2
- PyOpenGL==3.1.6
- tianshou==0.4.9.post1
- wandb

## Install Packages
1. Use `requirements.txt` to install packages:
```bash
pip install -r requirements.txt
```
2. Use `environment.yml` to install conda environment:
```bash
conda env create -f environment.yml
```

## Training Models
Users can use `--env-id` and `--task-id` to select the correspodning environments and scenarios:
```bash
# login wandb
wandb login
# train the agent with DQN
python run_dqn_script.py --env-id 1 --task-id 1 --epoch 100 --gamma 0.9 --seed 0
# train the agent with DDQN
python run_dqn_script.py --env-id 1 --task-id 1 --epoch 100 --gamma 0.9 --use-dueling --seed 0
# train the agent with A2C
python run_a2c_script.py --env-id 1 --task-id 1 --epoch 100 --gamma 0.9 --seed=0
# train the agent with PPO
python run_ppo_script.py --env-id 1 --task-id 1 --epoch 100 --gamma 0.9 --norm-obs --seed=0
```

## Visualizing the Trained Agent
```bash
python demo_visualisation.py --env-id 1 --test-id 1 --algo dqn --ckpt-path <your-ckpt-path> --render
```

## Plot Training Curves
The log files used in this paper can be downloaded from [[link]](https://github.com/hyintell/drl-assembly-planning/releases/tag/v1.0.0).
```bash
# 1. enter the plot_tools/ folder
cd plot_tools
# 2. download all log files from Env1 - Scene1
python download_data.py --user-name <wandb-user-name> --group-name Env_1_Scene_1
# 3. plot the corresponding learning curve
python extract_info.py --env-id 1 --task-id 1 --plot --logdir <path-to-save-logs>
```