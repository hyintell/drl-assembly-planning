import argparse
import datetime
import os
import pprint

import numpy as np
import torch
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.tensorboard import SummaryWriter
from tianshou.data import VectorReplayBuffer
from utils.customize_collector import Collector
from tianshou.policy import A2CPolicy
#from utils.customize_policy import A2CPolicy
from tianshou.utils.net.common import Net
from tianshou.trainer import onpolicy_trainer
from tianshou.utils.net.common import ActorCritic
from tianshou.utils.net.discrete import Actor, Critic
from tianshou.env import DummyVectorEnv, SubprocVectorEnv, ShmemVectorEnv
# our BIM environment
from utils.wandb_logger import WandbLogger
from Construction3DEnv_h import Construct3DEnvObs


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--scale-obs", type=int, default=0)
    parser.add_argument("--buffer-size", type=int, default=100000)
    parser.add_argument("--lr", type=float, default=7e-4)
    parser.add_argument("--gamma", type=float, default=0.9)
    parser.add_argument("--epoch", type=int, default=200)
    parser.add_argument("--step-per-epoch", type=int, default=10000)
    parser.add_argument("--step-per-collect", type=int, default=80)
    parser.add_argument("--repeat-per-collect", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument('--hidden-sizes', type=int, nargs='*', default=[256, 256])
    parser.add_argument("--training-num", type=int, default=16)
    parser.add_argument("--test-num", type=int, default=20)
    parser.add_argument("--rew-norm", type=int, default=False)
    parser.add_argument("--vf-coef", type=float, default=0.5)
    parser.add_argument("--ent-coef", type=float, default=0.01)
    parser.add_argument("--gae-lambda", type=float, default=0)
    parser.add_argument("--lr-decay", type=int, default=True)
    parser.add_argument("--max-grad-norm", type=float, default=0.5)
    parser.add_argument("--value-clip", type=int, default=0)
    parser.add_argument("--norm-adv", type=int, default=1)
    parser.add_argument("--recompute-adv", type=int, default=0)
    parser.add_argument("--logdir", type=str, default="log")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument('--env-id', type=int, default=1, help='ID of environments')
    parser.add_argument('--task-id', type=int, default=1, help='Task ID of the current environment')
    parser.add_argument('--norm-obs', action='store_true', help='If normalise the observation')
    parser.add_argument("--save-ckpt", action='store_true', help='If save checkpoints')
    return parser.parse_args()

def test_a2c(args=get_args()):
    # create the dummy environment
    env = Construct3DEnvObs(env_id=args.env_id, task_id=args.task_id)
    args.state_shape = env.observation_space.shape or env.observation_space.n
    args.action_shape = env.action_space.shape or env.action_space.n
    # create the training and test environment
    train_envs = ShmemVectorEnv(
        [lambda: Construct3DEnvObs(env_id=args.env_id, task_id=args.task_id, normalise=args.norm_obs) for _ in range(args.training_num)]
    )
    # test_envs = gym.make(args.task)
    test_envs = ShmemVectorEnv(
        [lambda: Construct3DEnvObs(env_id=args.env_id, task_id=args.task_id, normalise=args.norm_obs) for _ in range(args.test_num)]
    )
    # should be N_FRAMES x H x W
    print("Observations shape:", args.state_shape)
    print("Actions shape:", args.action_shape)
    # seed
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    # define model
    actor_net = Net(
        args.state_shape,
        hidden_sizes=args.hidden_sizes,
        device=args.device,
    ).to(args.device)
    
    critic_net = Net(
        args.state_shape,
        hidden_sizes=args.hidden_sizes,
        device=args.device,
    ).to(args.device)
    # actor critic
    actor = Actor(actor_net, args.action_shape, device=args.device, softmax_output=False)
    critic = Critic(critic_net, device=args.device)
    optim = torch.optim.RMSprop(ActorCritic(actor, critic).parameters(), lr=args.lr, eps=1e-5, alpha=0.99)
    #optim = torch.optim.Adam(ActorCritic(actor, critic).parameters(), lr=args.lr)
    lr_scheduler = None
    if args.lr_decay:
        # decay learning rate to 0 linearly
        max_update_num = np.ceil(
            args.step_per_epoch / args.step_per_collect
        ) * args.epoch

        lr_scheduler = LambdaLR(
            optim, lr_lambda=lambda epoch: 1 - epoch / max_update_num
        )

    # define policy
    def dist(p):
        return torch.distributions.Categorical(logits=p)
    
    policy = A2CPolicy(
        actor,
        critic,
        optim,
        dist,
        discount_factor=args.gamma,
        gae_lambda=args.gae_lambda,
        max_grad_norm=args.max_grad_norm,
        vf_coef=args.vf_coef,
        ent_coef=args.ent_coef,
        reward_normalization=args.rew_norm,
        action_scaling=False,
        lr_scheduler=lr_scheduler,
        action_space=env.action_space,
    ).to(args.device)
    # when you have enough RAM
    buffer = VectorReplayBuffer(
        args.buffer_size,
        buffer_num=len(train_envs),
    )
    # collector
    train_collector = Collector(policy, train_envs, buffer, exploration_noise=True)
    test_collector = Collector(policy, test_envs, exploration_noise=False)
    # log
    log_path = '{}/{}_logs/env{}/scene{}/seed{}'.format(args.logdir, 'a2c', args.env_id, args.task_id, args.seed)
    # setup the wandb
    logger = WandbLogger(project="bim-benchmark", entity=None, \
                        group='Env_{}_Scene_{}'.format(args.env_id, args.task_id), \
                        name='e{}s{}_{}_{}'.format(args.env_id, args.task_id, 'a2c', args.seed))
    writer = SummaryWriter(log_path)
    writer.add_text("args", str(args))
    logger.load(writer)
    
    def save_best_fn(policy):
        torch.save(policy.state_dict(), os.path.join(log_path, "policy.pth"))

    # trainer
    result = onpolicy_trainer(
        policy,
        train_collector,
        test_collector,
        args.epoch,
        args.step_per_epoch,
        args.repeat_per_collect,
        args.test_num,
        args.batch_size,
        save_best_fn=save_best_fn if args.save_ckpt else None,
        step_per_collect=args.step_per_collect,
        logger=logger,
        test_in_train=False,
    )
    pprint.pprint(result)
if __name__ == "__main__":
    test_a2c(get_args())