import argparse
import os
import pprint
import gym
import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter
#from tianshou.utils import WandbLogger
from utils.wandb_logger import WandbLogger
import wandb
# other necessary data
from tianshou.data import VectorReplayBuffer, PrioritizedVectorReplayBuffer
from utils.customize_collector import Collector
from tianshou.env import DummyVectorEnv, SubprocVectorEnv
from tianshou.policy import DQNPolicy
from tianshou.trainer import offpolicy_trainer
from tianshou.utils import TensorboardLogger
from tianshou.utils.net.common import Net
# our BIM environment
from Construction3DEnv_h import Construct3DEnvObs

"""
This script is used to run the DQN and Dueling DQN
"""

def get_args():
    parser = argparse.ArgumentParser()
    # the parameters are found by Optuna
    parser.add_argument('--task', type=str, default='bim-benchmark')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--eps-test', type=float, default=0.00)
    parser.add_argument('--eps-train', type=float, default=1)
    parser.add_argument('--eps-train-final', type=float, default=0.02)
    parser.add_argument('--buffer-size', type=int, default=50000)
    parser.add_argument('--explore-frac', type=float, default=0.1)
    parser.add_argument('--lr', type=float, default=5e-4)
    parser.add_argument('--gamma', type=float, default=0.9)
    parser.add_argument('--n-step', type=int, default=1)
    parser.add_argument('--target-update-freq', type=int, default=500)
    parser.add_argument('--epoch', type=int, default=200)
    parser.add_argument('--step-per-epoch', type=int, default=10000)
    parser.add_argument('--step-per-collect', type=int, default=1)
    parser.add_argument('--update-per-step', type=float, default=1)
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--hidden-sizes', type=int, nargs='*', default=[64, 64])
    parser.add_argument('--dueling-q-hidden-sizes', type=int, nargs='*', default=[64, 64])
    parser.add_argument('--dueling-v-hidden-sizes', type=int, nargs='*', default=[64, 64])
    parser.add_argument('--training-num', type=int, default=1)
    parser.add_argument('--test-num', type=int, default=20)
    parser.add_argument('--logdir', type=str, default='log')
    parser.add_argument('--render', type=float, default=0.)
    parser.add_argument('--use-dueling', action='store_true', help='if use the dueling network for the training')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu')
    parser.add_argument('--env-id', type=int, default=1, help='ID of environments')
    parser.add_argument('--task-id', type=int, default=1, help='Task ID of the current environment')
    parser.add_argument('--use-priority', action='store_true', help='If use PER')
    parser.add_argument('--alpha', type=float, default=0.6, help='PER coef')
    parser.add_argument('--beta', type=float, default=0.4, help='PER coef')
    parser.add_argument("--beta-final", type=float, default=1.)
    parser.add_argument("--beta-anneal-step", type=int, default=2000000)
    parser.add_argument("--save-ckpt", action='store_true', help='If save checkpoints')
    return parser.parse_args()


def test_dqn(args=get_args()):
    # create the environment
    env = Construct3DEnvObs(env_id=args.env_id, task_id=args.task_id)
    #env = gym.make(args.task)
    args.state_shape = env.observation_space.shape or env.observation_space.n
    args.action_shape = env.action_space.shape or env.action_space.n
    # you can also use tianshou.env.SubprocVectorEnv
    train_envs = DummyVectorEnv(
        [lambda: Construct3DEnvObs(env_id=args.env_id, task_id=args.task_id) for _ in range(args.training_num)]
    )
    # test_envs = gym.make(args.task)
    test_envs = SubprocVectorEnv(
        [lambda: Construct3DEnvObs(env_id=args.env_id, task_id=args.task_id) for _ in range(args.test_num)]
    )
    # seed
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    #train_envs.seed(args.seed)
    #test_envs.seed(args.seed)
    # model
    Q_param = {"hidden_sizes": args.dueling_q_hidden_sizes}
    V_param = {"hidden_sizes": args.dueling_v_hidden_sizes}
    net = Net(
        args.state_shape,
        args.action_shape,
        hidden_sizes=args.hidden_sizes,
        device=args.device,
        dueling_param=(Q_param, V_param) if args.use_dueling else None,
        norm_layer=torch.nn.LayerNorm,
    ).to(args.device)
    # optimizer
    optim = torch.optim.Adam(net.parameters(), lr=args.lr)
    policy = DQNPolicy(
        net,
        optim,
        args.gamma,
        args.n_step,
        target_update_freq=args.target_update_freq
    )
    # define buffer
    if args.use_priority:
        buffer = PrioritizedVectorReplayBuffer(args.buffer_size, len(train_envs), alpha=args.alpha, beta=args.beta)
    else: 
        buffer = VectorReplayBuffer(args.buffer_size, len(train_envs))
    # collector
    train_collector = Collector(
        policy,
        train_envs,
        buffer,
        exploration_noise=True
    )
    test_collector = Collector(policy, test_envs, exploration_noise=False)
    # policy.set_eps(1)
    train_collector.collect(n_step=args.batch_size * args.training_num)
    # log
    log_path = '{}/{}_logs/env{}/scene{}/seed{}'.format(args.logdir, 'ddqn' if args.use_dueling else 'dqn', \
                                                        args.env_id, args.task_id, args.seed)
    # setup the wandb
    logger = WandbLogger(project="bim-benchmark", entity=None, \
                        group='Env_{}_Scene_{}'.format(args.env_id, args.task_id), \
                        name='e{}s{}_{}_{}'.format(args.env_id, args.task_id, 'ddqn' if args.use_dueling else 'dqn', args.seed))
    writer = SummaryWriter(log_path)
    writer.add_text("args", str(args))
    logger.load(writer)

    def save_best_fn(policy):
        torch.save(policy.state_dict(), os.path.join(log_path, 'policy.pth'))

    def train_fn(epoch, env_step):  # exp decay
        # nature DQN setting, linear decay in the first 1M steps
        if env_step <= int(args.epoch * args.step_per_epoch * args.explore_frac):
            eps = args.eps_train - env_step / int(args.epoch * args.step_per_epoch * args.explore_frac) * \
                (args.eps_train - args.eps_train_final)
        else:
            eps = args.eps_train_final
        policy.set_eps(eps)
        # set beta
        if args.use_priority:
            if env_step <= args.beta_anneal_step:
                beta = args.beta - env_step / args.beta_anneal_step * \
                    (args.beta - args.beta_final)
            else:
                beta = args.beta_final
            buffer.set_beta(beta)
        # write eps
        if env_step % 1000 == 0:
            logger.write("train/env_step", env_step, {"train/eps": eps})

    def test_fn(epoch, env_step):
        policy.set_eps(args.eps_test)

    # trainer
    result = offpolicy_trainer(
        policy,
        train_collector,
        test_collector,
        args.epoch,
        args.step_per_epoch,
        args.step_per_collect,
        args.test_num,
        args.batch_size,
        save_best_fn=save_best_fn if args.save_ckpt else None,
        update_per_step=args.update_per_step,
        train_fn=train_fn,
        test_fn=test_fn,
        logger=logger
    )
    pprint.pprint(result)

if __name__ == '__main__':
    test_dqn(get_args())