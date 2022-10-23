import tensorflow.compat.v1 as tf
from glob import glob
from matplotlib import pyplot as plt
import numpy as np
import pickle
import os
import argparse
import seaborn as sns
# disable tensorflow-v2
tf.disable_v2_behavior()
"""
this is used for Mac M1 Chip
"""

METRICS = ['comps', 'reward', 'length', 'env_step']

parser = argparse.ArgumentParser()
parser.add_argument('--logdir', type=str, default='logs', help='the log path')
parser.add_argument('--env-id', type=int, default=1, help='ID of environment')
parser.add_argument('--task-id', type=int, default=1, help='Task ID of environment')
parser.add_argument('--plot', action='store_true', help='If plot the curves')
parser.add_argument('--plot-dir', type=str, default='plots')

def smooth_reward_curve(x, y, coef=60):
    halfwidth = int(np.ceil(len(x) / coef))  # Halfwidth of our smoothing convolution
    k = halfwidth
    xsmoo = x
    ysmoo = np.convolve(y, np.ones(2 * k + 1), mode='same') / np.convolve(np.ones_like(y), np.ones(2 * k + 1),
        mode='same')
    return xsmoo, ysmoo

def smooth_data(results, data_type='reward'):
    smooth_x, smooth_y = [], []
    for idx in range(results['env_step'].shape[0]):
        x_, y_ = smooth_reward_curve(results['env_step'][0], results[data_type][idx])
        smooth_x.append(x_)
        smooth_y.append(y_)
    smooth_x, smooth_y = np.array(smooth_x), np.array(smooth_y)
    results['env_step'] = smooth_x
    results[data_type] = smooth_y
    return results

def extract_info(logdir):
    results = {}
    seeds_dirs = sorted(os.listdir(logdir))
    for met in METRICS:
        results[met] = []
    for seed in seeds_dirs:
        if seed == '.DS_Store':
            continue
        cur_path = '{}/{}'.format(logdir, seed)
        event_path = glob('{}/events*'.format(cur_path))[0]
        for met in METRICS:
            target_tag = 'test/{}'.format(met)
            val_ = []
            for e in tf.train.summary_iterator(event_path):
                for v in e.summary.value:
                    if v.tag == target_tag:
                        val_.append(v.simple_value)
            results[met].append(val_)
    # convert them into numpy array
    for met in METRICS:
        results[met] = np.array(results[met])
    # check the shape
    assert results[METRICS[0]].shape == results[METRICS[1]].shape
    assert results[METRICS[0]].shape == results[METRICS[2]].shape
    assert results[METRICS[0]].shape == results[METRICS[3]].shape
    # smooth
    results = smooth_data(results)
    return results

if __name__ == '__main__':
    # save data as pkl files
    args = parser.parse_args()
    algos = ['dqn', 'ddqn', 'a2c', 'ppo']
    # get information
    statistics, metrics = {}, {}
    for algo in algos:
        statistics[algo] = extract_info('{}/{}_logs/env{}/scene{}'.format(args.logdir, algo, args.env_id, args.task_id))
    if args.plot:
        sns.set()
        # plot dqn
        for algo in algos:
            results = statistics[algo]
            plt.plot(results['env_step'][0], np.mean(results['reward'], axis=0), label=algo.upper())
            std_error = np.std(results['reward'], axis=0) / np.sqrt(results['reward'].shape[0])
            plt.fill_between(results['env_step'][0], np.mean(results['reward'], axis=0) - std_error, np.mean(results['reward'], axis=0) + std_error, alpha=0.25)
            metrics[algo] = {'mean': np.mean(results['reward'], axis=0)[-1], 'std_error': std_error[-1]}
        # labels
        plt.xlabel('Timesteps')
        plt.ylabel('Mean Rewards')
        plt.title('Env{}-S{}'.format(args.env_id, args.task_id))
        plt.legend()
        plt.tight_layout()
        if not os.path.exists('{}'.format(args.plot_dir)):
            os.makedirs(args.plot_dir, exist_ok=True)
        plt.savefig('{}/Env{}_S{}.pdf'.format(args.plot_dir, args.env_id, args.task_id))
        # print metrics
        for algo in metrics.keys():
            print('{}: mean: {:.2f}, std error: {:.2f}'.format(algo, metrics[algo]['mean'], metrics[algo]['std_error']))