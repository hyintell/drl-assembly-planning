from Construction3DEnv_h import Construct3DEnvObs
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--env-id", type=int, default=1, help="ID of the environment")
parser.add_argument("--task-id", type=int, default=1, help="ID of the environment")

if __name__ == "__main__":
    args = parser.parse_args()
    env = Construct3DEnvObs(env_id=args.env_id, task_id=args.task_id)
    obs = env.reset()
    print("After reset, observation shape: {}, action shape: {}".format(env.observation_space, env.action_space.n))
    ts = 0
    while True:
        obs, reward, done, _ = env.step(np.random.randint(env.action_space.n))
        print("timestep: {}, observation shape: {}, reward: {}, done: {}".format(ts, obs.shape, reward, done))
        ts += 1
        if done: break