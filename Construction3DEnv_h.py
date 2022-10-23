# IMPORT PYGAME AND OPENGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
#from drawSite import draw_site

# IMPORT CLASSES
import BIMClass.Site.siteOnly_multi_tar as Site
from BIMClass.Site import env_1, env_2, env_3, env_4

envs = {1: env_1, 2: env_2, 3: env_3, 4: env_4}

#IMPORT GYM
import gym
from gym import spaces
import numpy as np

#IMPORT RENDER
# import renderSite
# convert all map to obs
class Construct3DEnvObs:
    def __init__(self, env_id=1, task_id=1, normalise=False):
        self.env_id = env_id
        self.task_id = task_id
        # select environment and tasks
        if self.task_id == 1:
            self.siteEnv = envs[self.env_id].setting_1.site(15, 15, 8)
        elif self.task_id == 2:
            self.siteEnv = envs[self.env_id].setting_2.site(15, 15, 8)
        elif self.task_id == 3:
            self.siteEnv = envs[self.env_id].setting_3.site(15, 15, 8)
        elif self.task_id == 4:
            self.siteEnv = envs[self.env_id].setting_4.site(15, 15, 8)
        self.action_space = spaces.Discrete(6)
        # self.observation_space = spaces.Box(
        #     low=0,
        #     high=2,
        #     shape=(self.siteEnv.s_wid, self.siteEnv.s_len, 3),
        #     dtype='int32'
        # )
        timesteps_dict = {1: 100, 2: 100, 3: 300, 4: 600}
        self.normalise = normalise
        self.observation_space = spaces.Box(self.get_obs(self.siteEnv.site_3D), self.get_obs(self.siteEnv.site_3D))
        self.reward_range = None
        self.metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 2}
        self.state = None
        self.max_timestep = timesteps_dict[env_id]
        self.step_n = 0
        self.train_time = 0
        self.success_time = 0
        self.success_rate = []
        # self.arrived_count = 0

    def get_obs(self, state):
        obs = np.zeros((self.siteEnv.s_wid, self.siteEnv.s_len, 6), dtype='int32')
        index_z = -1
        index_x = -1
        index_y = -1
        for i in state:
            if index_z <= self.siteEnv.s_he:
                index_z += 1
            else:
                index_z = 0
            # print("z ",index_z)
            for j in state[0]:
                if index_x < self.siteEnv.s_wid - 1:
                    index_x += 1
                else:
                    index_x = 0
                # print("x ",index_x)
                for k in state[0][0]:
                    if index_y < self.siteEnv.s_len - 1:
                        index_y += 1
                    else:
                        index_y = 0
                    # print("y ",index_y)

                    if state[index_z][index_x][index_y] == 1:
                        obs[index_x, index_y, 1] = index_z
                    elif self.siteEnv.sco.steps < 15 and state[index_z][index_x][index_y] == 2:
                        obs[index_x, index_y, 1] = 0
                        obs[index_x, index_y, 2] = index_z
                    elif state[index_z][index_x][index_y] == 5:
                        obs[index_x, index_y, 0] = 1
                        obs[index_x, index_y, 3] = index_z
                    elif state[index_z][index_x][index_y] == 100:
                        obs[index_x, index_y, 0] = 1
                        obs[index_x, index_y, 2] = index_z
                        obs[index_x, index_y, 3] = index_z
                        obs[index_x, index_y, 5] = len(self.siteEnv.arrived_scos)
                    elif self.siteEnv.sco.steps > 15 and state[index_z][index_x][index_y] == 2:
                        obs[index_x, index_y, 1] = 0
                        obs[index_x, index_y, 2] = index_z
                        obs[index_x, index_y, 4] = 1
        
        return obs.flatten() / 4 if self.normalise else obs.flatten()

    def step(self, action):
        # if self.siteEnv.sco.steps == 0 and action == np.int(6):
        #     self.siteEnv.sco.working = False
        if self.siteEnv.sco.type == 'beam':
            self.siteEnv.sco.check_arrive = 0
            for id in self.siteEnv.sco.relate_sco:
                for o_sco in self.siteEnv.scos:
                    if id[0] == o_sco.id:
                        if o_sco.type == 'column':
                            if o_sco.node1_assembly is True:
                                self.siteEnv.sco.check_arrive += 1
            if self.siteEnv.sco.check_arrive < len(self.siteEnv.sco.relate_sco):
                self.siteEnv.switch_sco("switch")
            elif self.siteEnv.sco.check_arrive == len(self.siteEnv.sco.relate_sco):
                self.siteEnv.sco.allow_assembly = True

        if action in np.array([0,1,2,3,4,5]) and self.siteEnv.sco.arrived == False:
            self.siteEnv.sco.working = True


        assert self.action_space.contains(action), "%r (%s) invalid" %(action, type(action))
        if action == 0:
            self.siteEnv.sco_action("forward")
        elif action == 1:
            self.siteEnv.sco_action("left")
        elif action == 2:
            self.siteEnv.sco_action("back")
        elif action == 3:
            self.siteEnv.sco_action("right")
        elif action == 4:
            self.siteEnv.sco_action("up")
        elif action == 5:
            self.siteEnv.sco_action("down")

        # if self.siteEnv.sco.wrong_work == True:
        #     reward = -100
        #     done = False

        if self.siteEnv.sco.arrived == True:
            # method 1, remove successful component
            # add reward
            count = 0
            for _ in self.siteEnv.scos:
                if _.arrived == True:
                    count += 1
            reward = 1 * count
            done = False
            self.siteEnv.switch_sco("switch")
        elif self.siteEnv.sco.steps > 15:
            done = False
            reward = -2
        else:
            done = False
            reward = -1/(len(self.siteEnv.arrived_scos) + 1)

        #count for total
        arrived_count = 0
        for _ in self.siteEnv.scos:
            if _.arrived == True:
                arrived_count += 1
                if arrived_count == len(self.siteEnv.scos):
                    # here we define the final sucess reward
                    reward = 10
                    done = True
        self.state = self.siteEnv.site_3D
        obs = self.get_obs(self.state)
        self.step_n += 1

        if self.step_n == self.max_timestep:
            self.step_n = 0
            done = True

        if done is True:
            self.train_time += 1
            success_rate = self.success_time/self.train_time
            self.success_rate.append(success_rate)
            #if len(self.siteEnv.arrived_scos) != 0:
            #    print('it is arrived number', len(self.siteEnv.arrived_scos))
        return obs, reward, done, {'count': arrived_count}

    def reset(self):
        if self.task_id == 1:
            self.siteEnv = envs[self.env_id].setting_1.site(15, 15, 8)
        elif self.task_id == 2:
            self.siteEnv = envs[self.env_id].setting_2.site(15, 15, 8)
        elif self.task_id == 3:
            self.siteEnv = envs[self.env_id].setting_3.site(15, 15, 8)
        elif self.task_id == 4:
            self.siteEnv = envs[self.env_id].setting_4.site(15, 15, 8)
        #self.siteEnv = Site.site(15, 15, 8)
        # self.observation_space = spaces.Box(
        #     low=0,
        #     high=3,
        #     shape=(self.siteEnv.s_wid, self.siteEnv.s_len, 3),
        #     dtype='int32'
        # )
        self.observation_space = spaces.Box(self.get_obs(self.siteEnv.site_3D), self.get_obs(self.siteEnv.site_3D))
        self.state = self.siteEnv.site_3D
        self.state_render = self.siteEnv
        obs = self.get_obs(self.state)
        return obs

    def render(self):
        return None

    def close(self):
        return None


if __name__ == '__main__':
    env = Construct3DEnvObs()
    # env.reset()
    # while True:
    #     obs, reward, done, list = env.step(env.action_space.sample())
    #     print(obs)
    #     print('it is reward', reward)
    #     print('it is done', done)

    obs = env.reset()
    # INIT PYGAME
    pygame.init()
    display = (1200, 800)
    # INIT PYGAME DISPLAY AND OPENGL
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(25, display[0] / display[1], 0.1, 50.0)
    glClearColor(1, 1, 1, 0.7)
    glTranslate(1, 0, -5)
    glRotatef(35, 1, 0, 0)
    glOrtho(0, 1000, 0, 1000, 0, 1000)
    glEnable(GL_DEPTH_TEST)

    # RENDER POSITION
    rotate_x = 0
    rotate_y = 0
    translate_x = 0
    translate_y = 0
    z_position = 0

    # MOUSE INPUTS
    mouse_rotate = False
    mouse_move = False

    # MAIN GAME LOOP
    pygame.key.set_repeat(16, 100)
    in_game = True
    open_map = False
    show_steps = True

    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_rotate = True
                elif event.button == 3:
                    mouse_move = True
                elif event.button == 5:
                    translate_y -= 50
                elif event.button == 4:
                    translate_y += 50
            elif event.type == MOUSEBUTTONUP:
                mouse_rotate = False
                mouse_move = False
            elif event.type == MOUSEMOTION:
                i, j = event.rel
                if mouse_move:
                    translate_x += i
                    translate_y += j
                elif mouse_rotate:
                    rotate_x += i
                    rotate_y += j
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    z_position -= 50
                elif event.key == K_DOWN:
                    z_position += 50
                elif event.key == K_LEFT:
                    translate_x -= 50
                elif event.key == K_RIGHT:
                    translate_x += 50
                elif event.key == 113:
                    rotate_x -= 50
                elif event.key == 101:
                    rotate_x += 50

        if in_game:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # action, _states = model.predict(obs)
            # print('it is action', action)

            obs, rewards, dones, info = env.step(np.int(input("please input action")))
            print('reward', rewards)
            print(len(env.siteEnv.arrived_scos))
            print(obs)
            # print('it is crash', env.siteEnv.sco.crash)
            # print('it is done', dones)
            if env.siteEnv.sco.type == 'beam':
                print(
                    "SCO id: {}, step is {}, component crash is {}, component arrive is {}, component node 1 assembly is {}, component node 2 assembly is {}, componenet working is {}, component wrong work is {}, check arrive is  {}, check lock is {}, allow_assembly is {}".format(
                        env.siteEnv.sco.id, env.siteEnv.sco.steps, env.siteEnv.sco.crash, env.siteEnv.sco.arrived,
                        env.siteEnv.sco.node1_assembly, env.siteEnv.sco.node2_assembly, env.siteEnv.sco.working,
                        env.siteEnv.sco.wrong_work, env.siteEnv.sco.check_arrive, env.siteEnv.sco.lock, env.siteEnv.sco.allow_assembly))
            elif env.siteEnv.sco.type == 'column':
                print(
                    "SCO id: {}, step is {}, component crash is {}, component arrive is {}, component node 1 assembly is {}, component node 2 assembly is {}, componenet working is {}, component wrong work is {}, check lock is {}".format(
                        env.siteEnv.sco.id, env.siteEnv.sco.steps, env.siteEnv.sco.crash, env.siteEnv.sco.arrived,
                        env.siteEnv.sco.node1_assembly, env.siteEnv.sco.node2_assembly, env.siteEnv.sco.working,
                        env.siteEnv.sco.wrong_work, env.siteEnv.sco.lock))
            # print('node1 is {}, node2 is {}'.format(siteEnv.sco.node1, siteEnv.sco.node2,))
            draw_site(env.siteEnv)
            if dones is True:
                # time.sleep(1)
                obs = env.reset()
            # time.sleep(0.5)
            # TRANSLATE OBJECT IF MOUSE MOVED
            glTranslatef(translate_x, translate_y, -z_position)
            glRotatef(rotate_y / 20., 1, 0, 0)
            glRotatef(rotate_x / 20., 0, 1, 0)

            # RESET ROTATE
            rotate_x = 0
            rotate_y = 0
            translate_x = 0
            translate_y = 0
            z_position = 0
            pygame.display.flip()

        else:
            pygame.quit()
