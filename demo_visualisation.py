import argparse
from Construction3DEnv_h import Construct3DEnvObs
from BIMClass.drawSite import draw_site
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from tianshou.utils.net.common import Net
from tianshou.policy import DQNPolicy
import numpy as np 
import time
from datetime import datetime
import torch

"""
Script to visualise the policy
"""

parser = argparse.ArgumentParser()
parser.add_argument('--task-id', type=int, default=1, help='ID of the task')
parser.add_argument('--env-id', type=int, default=1, help='ID of the environment')
parser.add_argument('--algo', type=str, default='dqn', help='the name of algorithm')
parser.add_argument('--hidden-sizes', type=int, nargs='*', default=[64, 64])
parser.add_argument('--dueling-q-hidden-sizes', type=int, nargs='*', default=[64, 64])
parser.add_argument('--dueling-v-hidden-sizes', type=int, nargs='*', default=[64, 64])
parser.add_argument('--use-dueling', action='store_true', help='if use the dueling network for the training')
parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu')
parser.add_argument('--ckpt-path', type=str, default='saved_ckpt', help='The folder to save ckpt')
parser.add_argument('--num-test', type=int, default=5, help='The number of test time')
parser.add_argument('--render', action='store_true', help='if render the environment')
parser.add_argument('--eps', type=float, default=0.02, help='eps coef for the epsilon-greedy')

def setup_pygame():
    pygame.init()
    display = (1200, 800)
    # INIT PYGAME DISPLAY AND OPENGL
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(25, display[0] / display[1], 0.1, 50.0)
    glTranslate(1, 0, -5)
    glRotatef(35, 1, 0, 0)
    glOrtho(0, 1000, 0, 1000, 0, 1000)
    glEnable(GL_DEPTH_TEST)

def get_tensor(obs, device):
    return torch.tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)

if __name__ == '__main__':
    args = parser.parse_args()
    env = Construct3DEnvObs(env_id=args.env_id, task_id=args.task_id)
    state_shape = env.observation_space.shape or env.observation_space.n
    action_shape = env.action_space.shape or env.action_space.n
    # setup py game
    if args.render: setup_pygame()
    # build up the network
    if args.algo == 'dqn' or args.algo == 'ddqn':
        net = Net(
            state_shape,
            action_shape,
            hidden_sizes=args.hidden_sizes,
            device=args.device,
            dueling_param=(Q_param, V_param) if args.use_dueling else None,
            norm_layer=torch.nn.LayerNorm,
        ).to(args.device)
        policy = DQNPolicy(net, torch.optim.Adam(net.parameters(), lr=0.001), target_update_freq=10)
        policy.load_state_dict(torch.load('{}/{}/env{}/scene{}/policy.pth'.format(args.ckpt_path, args.algo, args.env_id, args.task_id), map_location=args.device))
    else:
        raise NotImplementedError
    # start to visualise the policy
    for test_id in range(args.num_test):
        obs = env.reset()
        episode_rewards, step = 0, 0
        while True:
            if args.render:
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # get the action
            obs_tensor = get_tensor(obs, args.device)
            with torch.no_grad():
                logits, _ = policy.model(obs_tensor)
            logits = logits.cpu().numpy().squeeze()
            if np.random.random() < args.eps:
                action = np.random.randint(action_shape)
            else:
                action = np.argmax(logits)
            # execute the action
            obs, reward, done, info = env.step(action)
            episode_rewards += reward
            step += 1
            if args.render:
                draw_site(env.state_render)
                time.sleep(0.09)
                pygame.display.flip()
            if done: break
        print('[{}] Episode: {}, Steps: {}, Rewards: {}, Success Components: {}'.format(datetime.now(), test_id, step, episode_rewards, info['count']))
    # quit pygame
    if args.render: pygame.quit()