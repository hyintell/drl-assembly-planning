# create a 3D site, which can set width, len, height

import copy
from BIMClass.Site.SCO import *
import random


class site():
    def __init__(self, width, length, height):
        # all site
        self.s_wid = width
        self.s_len = length
        self.s_he = height

        #construction area
        self.construction_x = [ 8, 9, 10, 11, 12, 13, 14]
        self.construction_y = [ 8, 9, 10, 11, 12, 13, 14]
        self.site_list = []
        for i in self.construction_x:
            for j in self.construction_y:
                self.site_list.append([i,j])


        # Build Empty Array
        self.site_ground = []
        self.site_space = []
        self.site_3D = []
        self.scos = []
        self.sco_index = 0
        self.arrived_scos = []
        self.tar_list = [[9, 10, 4, 9, 12, 4], [9, 9, 1, 9, 9, 4], [9, 13, 1, 9, 13, 4],[13, 9, 1, 13, 9, 4,], [13, 13, 1, 13, 13, 4,], [10, 9, 4, 12, 9, 4,],[13, 10, 4, 13, 12, 4,], [10, 13, 4, 12, 13, 4,]]
        #count rotate times, limit rotate times
        # self.rotate_count = 0

        # create 2D ground
        for i in range(self.s_wid):
            self.site_ground.append([10 for j in range(self.s_len)])
        for i in range(self.s_wid):
            self.site_space.append([0 for j in range(self.s_len)])



        # create 3D env
        for i in range(self.s_he + 1):
            if i == 0:
                self.site_3D.append(self.site_ground)
            # create new space
            else:
                new_floor = copy.deepcopy(self.site_space)
                self.site_3D.append(new_floor)

        # create construction area
        for i in self.construction_x:
            for j in self.construction_y:
                self.site_3D[0][i][j] = 50



        # Print Results
        # print("Map init")
        # print("Map Initialized With Length:", self.s_len)
        # print("Map Initialized With Width:", self.s_wid)
        # print("Map Initialized With Height:", self.s_he)
        # self.site_3D[1][7][8] = 2
        self.init_component()
        # first component
        self.sco = self.scos[0]

        # set column action
        self.site_action = ['forward', 'back', 'left', 'right', 'up', 'down']

    def gene_point(self, type):
        if type == 'beam':
            rand_choice = random.choice([1, 2])
            x_1 = random.randint(3, 11)
            if x_1 < 6:
                if rand_choice == 1:
                    y_1 = random.randint(3, 11)
                    x_2 = x_1 - 2
                    y_2 = y_1
                elif rand_choice == 2:
                    y_1 = random.randint(3, 11)
                    y_2 = y_1 - 2
                    x_2 = x_1
            if x_1 >= 6:
                if rand_choice == 1:
                    y_1 = random.randint(3, 5)
                    x_2 = x_1 - 2
                    y_2 = y_1
                elif rand_choice == 2:
                    y_1 = random.randint(3, 5)
                    y_2 = y_1 - 2
                    x_2 = x_1
            if x_1 == x_2:
                return [[x_1, y_1], [x_1, y_1 - 1], [x_2, y_2]]
            else:
                return [[x_1, y_1], [x_1 - 1, y_1], [x_2, y_2]]
        elif type == 'column':
            rand_choice = random.choice([1, 2])
            x_1 = random.randint(3, 11)
            if x_1 < 6:
                if rand_choice == 1:
                    y_1 = random.randint(3, 11)
                    x_2 = x_1 - 3
                    y_2 = y_1
                elif rand_choice == 2:
                    y_1 = random.randint(3, 11)
                    y_2 = y_1 - 3
                    x_2 = x_1
            if x_1 >= 6:
                if rand_choice == 1:
                    y_1 = random.randint(3, 5)
                    x_2 = x_1 - 3
                    y_2 = y_1
                elif rand_choice == 2:
                    y_1 = random.randint(3, 5)
                    y_2 = y_1 - 3
                    x_2 = x_1
            if x_1 == x_2:
                return [[x_1, y_1], [x_1, y_1 - 1], [x_1, y_1 - 2], [x_2, y_2]]
            else:
                return [[x_1, y_1], [x_1 - 1, y_1], [x_1 - 2, y_1], [x_2, y_2]]

    # create component
    def init_component(self):

        self.site_3D[0][9][9] = 'foundation'
        self.site_3D[0][9][13] = 'foundation'
        self.site_3D[0][13][9] = 'foundation'
        self.site_3D[0][13][13] = 'foundation'

        n = 0
        count_round = 0
        comp = []
        while n <= 3:
            if len(comp) == 0:
                comp.append(self.gene_point('beam'))
                n += 1
            else:
                bad_node = True
                count = 0
                bad_count = 0
                while bad_node:
                    count_round += 1
                    if count_round < 100000:
                        node = self.gene_point('beam')
                        for i in comp:
                            count += 1
                            for j in i:
                                if j in node:
                                    bad_node = True
                                    bad_count += 1
                        if bad_count == 0 and count == len(comp):
                            bad_node = False
                            comp.append(node)
                            n += 1
                    elif count_round >= 1000:
                        n += 1
                        bad_node = False
                        comp = random.choice([[[[10, 4], [10, 3], [10, 2]], [[3, 7], [2, 7], [1, 7]],
                                               [[3, 10], [2, 10], [1, 10]], [[7, 3], [6, 3], [5, 3]]],
                                              [[[6, 4], [5, 4], [4, 4]], [[3, 6], [2, 6], [1, 6]],
                                               [[7, 3], [6, 3], [5, 3]], [[11, 3], [11, 2], [11, 1]]],
                                              [[[6, 5], [5, 5], [4, 5]], [[6, 3], [6, 2], [6, 1]],
                                               [[11, 5], [10, 5], [9, 5]], [[4, 9], [4, 8], [4, 7]]],
                                              [[[5, 7], [5, 6], [5, 5]], [[6, 5], [6, 4], [6, 3]],
                                               [[9, 5], [9, 4], [9, 3]], [[3, 5], [2, 5], [1, 5]]],
                                              [[[8, 5], [7, 5], [6, 5]], [[5, 7], [5, 6], [5, 5]],
                                               [[11, 3], [11, 2], [11, 1]], [[10, 3], [10, 2], [10, 1]]],
                                              [[[5, 7], [4, 7], [3, 7]], [[5, 3], [4, 3], [3, 3]],
                                               [[11, 3], [11, 2], [11, 1]], [[6, 5], [5, 5], [4, 5]]],
                                              [[[3, 10], [3, 9], [3, 8]], [[5, 3], [5, 2], [5, 1]],
                                               [[7, 5], [7, 4], [7, 3]], [[11, 3], [11, 2], [11, 1]]]])
        k = 0
        while k <= 3:
            if len(comp) == 0:
                comp.append(self.gene_point('column'))
                n += 1
            else:
                bad_node = True
                count = 0
                bad_count = 0
                while bad_node:
                    count_round += 1
                    if count_round < 10000:
                        node = self.gene_point('column')
                        for i in comp:
                            count += 1
                            for j in i:
                                if j in node:
                                    bad_node = True
                                    bad_count += 1
                        if bad_count == 0 and count == len(comp):
                            bad_node = False
                            comp.append(node)
                            n += 1
                    elif count_round >= 10000:
                        k += 1
                        bad_node = False
                        #print("not working")
                        comp

        #print(comp)

        comp = random.choice([
            [[[6, 3], [5, 3], [4, 3]], [[3, 8], [2, 8], [1, 8]], [[7, 3], [7, 2], [7, 1]], [[4, 10], [3, 10], [2, 10]],
             [[5, 4], [4, 4], [3, 4], [2, 4]], [[9, 3], [9, 2], [9, 1], [9, 0]], [[13, 5], [13, 4], [13, 3], [13, 2]],
             [[1, 12], [2, 12], [3, 12], [4, 12]]],
            [[[10, 4], [10, 3], [10, 2]], [[3, 7], [3, 6], [3, 5]], [[5, 8], [5, 7], [5, 6]], [[6, 3], [6, 2], [6, 1]],
             [[8, 4], [8, 3], [8, 2], [8, 1]], [[11, 3], [11, 2], [11, 1], [11, 0]], [[4, 3], [4, 2], [4, 1], [4, 0]],
             [[10, 4], [10, 3], [10, 2], [10, 1]]],
            [[[8, 5], [7, 5], [6, 5]], [[5, 7], [5, 6], [5, 5]], [[11, 3], [11, 2], [11, 1]],
             [[10, 3], [10, 2], [10, 1]], [[8, 4], [8, 3], [8, 2], [8, 1]], [[4, 3], [4, 2], [4, 1], [4, 0]],
             [[13, 5], [13, 4], [13, 3], [13, 2]], [[[9, 3], [9, 2], [9, 1], [9, 0]]],
             [[[8, 5], [7, 5], [6, 5]], [[5, 7], [5, 6], [5, 5]], [[11, 3], [11, 2], [11, 1]],
              [[10, 3], [10, 2], [10, 1]], [[3, 7], [2, 7], [1, 7], [0, 7]], [[4, 10], [3, 10], [2, 10], [1, 10]],
              [[3, 4], [3, 3], [3, 2], [3, 1]], [[1, 12], [2, 12], [3, 12], [4, 12]]]
             ]])



        x12 = comp[0][0][0]
        y12 = comp[0][0][1]
        x11 = comp[0][2][0]
        y11 = comp[0][2][1]

        x22 = comp[1][0][0]
        y22 = comp[1][0][1]
        x21 = comp[1][2][0]
        y21 = comp[1][2][1]

        x32 = comp[2][0][0]
        y32 = comp[2][0][1]
        x31 = comp[2][2][0]
        y31 = comp[2][2][1]

        x42 = comp[3][0][0]
        y42 = comp[3][0][1]
        x41 = comp[3][2][0]
        y41 = comp[3][2][1]



        x51 = comp[4][0][0]
        y51 = comp[4][0][1]
        x52 = comp[4][3][0]
        y52 = comp[4][3][1]

        x61 = comp[5][0][0]
        y61 = comp[5][0][1]
        x62 = comp[5][3][0]
        y62 = comp[5][3][1]

        x71 = comp[6][0][0]
        y71 = comp[6][0][1]
        x72 = comp[6][3][0]
        y72 = comp[6][3][1]

        x81 = comp[6][0][0]
        y81 = comp[6][0][1]
        x82 = comp[6][3][0]
        y82 = comp[6][3][1]

        # FRAME
        sco1 = SCO(1, 'beam', 4, 4, 1, 6, 4, 1, 9, 10, 4, 9, 12, 4, 3, [[2, 2, 1], [3, 2, 2]])
        self.scos.append(sco1)
        sco2 = SCO(2, 'column', 4, 3, 1, 7, 3, 1, 9, 9, 1, 9, 9, 4, 4, [[0, 1, 1], [1, 1, 2]])
        self.scos.append(sco2)
        sco3 = SCO(3, 'column', 7, 2, 1, 4, 2, 1, 9, 13, 1, 9, 13, 4, 4, [[0, 1, 1], [1, 2, 2]])
        self.scos.append(sco3)
        # #
        # # # ONE UNIT STRUCTURE
        self.site_3D[0][13][9] = 'foundation'
        self.site_3D[0][13][13] = 'foundation'
        sco4 = SCO(4, 'column', 8, 2, 1, 11, 2, 1, 13, 9, 1, 13, 9, 4, 4, [[0, 1, 1], [6, 1, 2]])
        self.scos.append(sco4)
        sco5 = SCO(5, 'column', 8, 3, 1, 11, 3, 1, 13, 13, 1, 13, 13, 4, 4, [[0, 1, 1], [7, 2, 2]])
        self.scos.append(sco5)
        sco6 = SCO(6, 'beam', 8, 4, 1, 10, 4, 1, 10, 9, 4, 12, 9, 4, 3, [[2, 2, 1], [4, 2, 2]])
        self.scos.append(sco6)
        sco7 = SCO(7, 'beam', 8, 5, 1, 10, 5, 1, 13, 10, 4, 13, 12, 4, 3, [[4, 2, 1], [5, 2, 2]])
        self.scos.append(sco7)
        sco8 = SCO(8, 'beam', 8, 6, 1, 10, 6, 1, 10, 13, 4, 12, 13, 4, 3, [[3, 2, 1], [5, 2, 2]])
        self.scos.append(sco8)




        # generate sco target
        for sco in self.scos:
            if sco.length == 2:
                self.site_3D[sco.z_1][sco.x_1][sco.y_1] = 1
                self.site_3D[sco.z_2][sco.x_2][sco.y_2] = 1
                self.site_3D[sco.z_tar_1][sco.x_tar_1][sco.y_tar_1] = 5
                self.site_3D[sco.z_tar_2][sco.x_tar_2][sco.y_tar_2] = 5
            elif sco.length > 2:
                # init state is flat, can't erect
                if sco.x_1 > sco.x_2:
                    for x_len in range(abs(sco.x_1 - sco.x_2) - 1):
                        self.site_3D[sco.z_2][sco.x_2 + x_len + 1][sco.y_2] = 1
                    self.site_3D[sco.z_1][sco.x_1][sco.y_1] = 1
                    self.site_3D[sco.z_2][sco.x_2][sco.y_2] = 1
                    self.site_3D[sco.z_tar_1][sco.x_tar_1][sco.y_tar_1] = 5
                    self.site_3D[sco.z_tar_2][sco.x_tar_2][sco.y_tar_2] = 5
                elif sco.x_2 > sco.x_1:
                    for x_len in range(abs(sco.x_2 - sco.x_1) - 1):
                        self.site_3D[sco.z_1][sco.x_1 + x_len + 1][sco.y_1] = 1
                    self.site_3D[sco.z_1][sco.x_1][sco.y_1] = 1
                    self.site_3D[sco.z_2][sco.x_2][sco.y_2] = 1
                    self.site_3D[sco.z_tar_1][sco.x_tar_1][sco.y_tar_1] = 5
                    self.site_3D[sco.z_tar_2][sco.x_tar_2][sco.y_tar_2] = 5
                elif sco.y_1 > sco.y_2:
                    for x_len in range(abs(sco.y_1 - sco.y_2) - 1):
                        self.site_3D[sco.z_2][sco.x_2][sco.y_2 + x_len + 1] = 1
                    self.site_3D[sco.z_1][sco.x_1][sco.y_1] = 1
                    self.site_3D[sco.z_2][sco.x_2][sco.y_2] = 1
                    self.site_3D[sco.z_tar_1][sco.x_tar_1][sco.y_tar_1] = 5
                    self.site_3D[sco.z_tar_2][sco.x_tar_2][sco.y_tar_2] = 5
                elif sco.y_2 > sco.y_1:
                    for x_len in range(abs(sco.y_2 - sco.y_1) - 1):
                        self.site_3D[sco.z_1][sco.x_1][sco.y_1 + x_len + 1] = 1
                    self.site_3D[sco.z_1][sco.x_1][sco.y_1] = 1
                    self.site_3D[sco.z_2][sco.x_2][sco.y_2] = 1
                    self.site_3D[sco.z_tar_1][sco.x_tar_1][sco.y_tar_1] = 5
                    self.site_3D[sco.z_tar_2][sco.x_tar_2][sco.y_tar_2] = 5
                self.create_target(sco)



    # switch the objects
    def switch_sco(self, switch):
        if self.sco.working == False or self.sco.arrived == True:
            if switch == 'switch':
                if self.sco_index < (len(self.scos) - 1):
                    self.sco_index += 1
                elif self.sco_index == (len(self.scos) - 1):
                    self.sco_index = 0
                self.sco = self.scos[self.sco_index]



    # sco action
    def sco_action(self,action):
        # write componet move and component clear as a single def
        #
        # # check direction
        # if self.sco.arrived == True:
        #     # beam assembly
        #     if self.sco.type == 'beam':
        #         check_arrive = 0
        #         for id in self.sco.relate_sco:
        #             for sco in self.scos:
        #                 if id[0] == sco.id:
        #                     if sco.node1_assembly is True:
        #                         check_arrive += 1
        #         if check_arrive < 2:
        #             self.sco.crash = True
        #         elif check_arrive == 2:
        #             self.sco.allow_assembly = True
        #         if self.sco.allow_assembly is True:
        #             if action == "assembly_node1":
        #                 if self.sco.node1_assembly is False:
        #                     self.sco.node1_assembly = True
        #                     self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 200
        #                     for i in self.sco.relate_sco:
        #                         if i[2] == 1:
        #                             for col in self.scos:
        #                                 if i[0] == col.id:
        #                                     col.node2_assembly = True
        #                                     self.site_3D[col.z_2][col.x_2][col.y_2] = 200
        #             # elif action == "assembly_node2":
        #                 if self.sco.node2_assembly is False:
        #                     self.sco.node2_assembly = True
        #                     self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 200
        #                     for i in self.sco.relate_sco:
        #                         if i[2] == 2:
        #                             for col in self.scos:
        #                                 if i[0] == col.id:
        #                                     col.node2_assembly = True
        #                                     self.site_3D[col.z_2][col.x_2][col.y_2] = 200
        #
        #     #  column assembly
        #     elif self.sco.type == 'column':
        #         if action == "assembly_node1":
        #             # print("here is node1 ")
        #             if self.sco.node1_assembly is False:
        #                 # print('I am arrived')
        #                 # print(self.site_3D[self.sco.z_1 - 1][self.sco.x_1][self.sco.y_1])
        #                 if self.site_3D[self.sco.z_1 - 1][self.sco.x_1][self.sco.y_1] == 10:
        #                     self.sco.node1_assembly = True
        #                     self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 200
        #         # elif action == "assembly_node2":
        #         #     # print("here is node2 ")
        #         #     if self.sco.node2_assembly is False:
        #         #         for i in self.scos:
        #         #             if self.sco.relate_sco[0] == i.id:
        #         #                 if i.allow_assembly is True:
        #         #                     self.sco.node2_assembly = True
        #         #                     self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 200
        #
        # else:
        #     if (self.sco.x_1 < self.construction_x[0] and self.sco.x_2 < self.construction_x[0]) or (self.sco.y_1 < self.construction_y[0] and self.sco.y_2 < self.construction_y[0]):
        #         if action == "assembly_node1" or action == "assembly_node2":
        #             self.sco.crash = True
        #         pass
        #     else:
        #         if action in self.site_action:
        #             if self.sco.arrived == False:
        #                 if action == "assembly_node1" or action == "assembly_node2":
        #                     self.sco.crash = True
        #         else:
        #             self.sco.crash = True
        self.check_init(self.sco)
        if self.sco.working == True:
            self.site_3D[self.sco.node1[0]][self.sco.node1[1]][self.sco.node1[2]] = 3
            self.site_3D[self.sco.node2[0]][self.sco.node2[1]][self.sco.node2[2]] = 3
            if self.sco.length > 2:
                if self.sco.node1[1] > self.sco.node2[1]:
                    for x_len in range(abs(self.sco.node1[1] - self.sco.node2[1])):
                        self.site_3D[self.sco.node2[0]][self.sco.node2[1] + x_len + 1][self.sco.node2[2]] = 3
                elif self.sco.node2[1] > self.sco.node1[1]:
                    for x_len in range(abs(self.sco.node2[1] - self.sco.node1[1])):
                        self.site_3D[self.sco.node2[0]][self.sco.node1[1] + x_len + 1][self.sco.node2[2]] = 3
                elif self.sco.node1[2] > self.sco.node2[2]:
                    for y_len in range(abs(self.sco.node1[2] - self.sco.node2[2])):
                        self.site_3D[self.sco.node2[0]][self.sco.node2[1]][self.sco.node2[2] + y_len + 1] = 3
                elif self.sco.node2[2] > self.sco.node1[2]:
                    for y_len in range(abs(self.sco.node2[2] - self.sco.node1[2])):
                        self.site_3D[self.sco.node2[0]][self.sco.node1[1]][self.sco.node1[2] + y_len + 1] = 3
                elif self.sco.node1[0] > self.sco.node2[0]:
                    for z_len in range(self.sco.length - 2):
                        self.site_3D[self.sco.node2[0] + z_len + 1][self.sco.node2[1]][self.sco.node2[2]] = 3
                elif self.sco.node2[0] > self.sco.node1[0]:
                    for z_len in range(abs(self.sco.node2[2] - self.sco.node1[2])):
                        self.site_3D[self.sco.node1[0] + z_len + 1][self.sco.node1[1]][self.sco.node1[2]] = 3



        if self.sco.type == 'beam':
            if self.sco.check_arrive < 2:
                self.sco.wrong_work = True
            elif self.sco.check_arrive == 2:
                self.sco.wrong_work = False
                self.sco.allow_assembly = True
        # check assembly
        if self.sco.arrived == True:
            # beam assembly
            pass
        else:

            self.check_above(self.sco)
            if self.sco.lock == True:
                pass
            elif self.sco.lock == False:
                # basic move
                if action == "forward":
                    # clear current position
                    self.clear_sco(self.sco)
                    # check collision
                    self.check_collision(self.sco, action)
                    if self.sco.collision_f == True:
                        self.sco.crash = True
                        pass
                    elif self.sco.collision_f == False:
                        for node in self.sco.scoNodes:
                            # check node id, node move
                            if node[3] == 1:
                                if self.sco.direction == 'NS':
                                    if self.sco.x_2 != 0:
                                        self.sco.move_forward(1)
                                    elif self.sco.x_2 == 0:
                                        self.sco.x_1 = self.sco.x_2 + self.sco.length - 1
                                elif self.sco.direction == 'EW' or 'V':
                                    self.sco.move_forward(1)
                                # Boundary check
                                if self.sco.x_1 < 0:
                                    self.sco.move_back(1)
                                    self.sco.crash = True
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 2
                            # check node id, node move
                            if node[3] == 2:
                                if self.sco.direction == 'NS':
                                    if self.sco.x_1 != 0:
                                        self.sco.move_forward(2)
                                    elif self.sco.x_1 == 0:
                                        self.sco.x_2 = self.sco.x_1 + self.sco.length - 1
                                elif self.sco.direction == 'EW' or 'V':
                                    self.sco.move_forward(2)
                                if self.sco.x_2 < 0:
                                    self.sco.move_back(2)
                                    self.sco.crash = True
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 2
                        self.move_sco(self.sco)
                        self.sco.steps += 1

                elif action == "back":
                    # clear current position
                    self.clear_sco(self.sco)
                    # check collision
                    self.check_collision(self.sco, action)
                    if self.sco.collision_b == True:
                        self.sco.crash = True
                        pass
                    elif self.sco.collision_b == False:
                        for node in self.sco.scoNodes:
                            if node[3] == 1:
                                if self.sco.direction == 'NS':
                                    if self.sco.x_2 != self.s_wid - 1:
                                        self.sco.move_back(1)
                                    elif self.sco.x_2 == self.s_wid - 1:
                                        self.sco.x_1 = self.sco.x_2 - self.sco.length + 1
                                elif self.sco.direction == 'EW' or 'V':
                                    self.sco.move_back(1)
                                if self.sco.x_1 > self.s_wid - 1:
                                    self.sco.move_forward(1)
                                    self.sco.crash = True
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 2
                            if node[3] == 2:
                                if self.sco.direction == 'NS':
                                    if self.sco.x_1 != self.s_wid - 1:
                                        self.sco.move_back(2)
                                    elif self.sco.x_1 == self.s_wid - 1:
                                        self.sco.x_2 = self.sco.x_1 - self.sco.length + 1
                                elif self.sco.direction == 'EW' or 'V':
                                    self.sco.move_back(2)
                                if self.sco.x_2 > self.s_wid - 1:
                                    self.sco.move_forward(2)
                                    self.sco.crash = True
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 2
                        # component move
                        self.move_sco(self.sco)
                        self.sco.steps += 1

                elif action == "left":
                    # clear current position
                    self.clear_sco(self.sco)
                    # check collision
                    self.check_collision(self.sco, action)
                    if self.sco.collision_l == True:
                        self.sco.crash = True
                        pass
                    elif self.sco.collision_l == False:
                        for node in self.sco.scoNodes:
                            if node[3] == 1:
                                if self.sco.direction == 'EW':
                                    if self.sco.y_2 != 0:
                                        self.sco.move_left(1)
                                    elif self.sco.y_2 == 0:
                                        self.sco.y_1 = self.sco.y_2 + self.sco.length - 1
                                elif self.sco.direction == 'NS' or 'V':
                                    self.sco.move_left(1)
                                if self.sco.y_1 < 0:
                                    self.sco.move_right(1)
                                    self.sco.crash = True
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 2
                            if node[3] == 2:
                                if self.sco.direction == 'EW':
                                    if self.sco.y_1 != 0:
                                        self.sco.move_left(2)
                                    elif self.sco.y_1 == 0:
                                        self.sco.y_2 = self.sco.y_1 + self.sco.length - 1
                                elif self.sco.direction == 'NS' or 'V':
                                    self.sco.move_left(2)
                                if self.sco.y_2 < 0:
                                    self.sco.move_right(2)
                                    self.sco.crash = True
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 2
                        # component move
                        self.move_sco(self.sco)
                        self.sco.steps += 1

                elif action == "right":
                    # clear current position
                    self.clear_sco(self.sco)
                    # check collision
                    self.check_collision(self.sco, action)
                    if self.sco.collision_r == True:
                        self.sco.crash = True
                        pass
                    elif self.sco.collision_r == False:
                        for node in self.sco.scoNodes:
                            if node[3] == 1:
                                if self.sco.direction == 'EW':
                                    if self.sco.y_2 != self.s_len - 1:
                                        self.sco.move_right(1)
                                    elif self.sco.y_2 == self.s_len - 1:
                                        self.sco.y_1 = self.sco.y_2 - self.sco.length + 1
                                elif self.sco.direction == 'NS' or 'V':
                                    self.sco.move_right(1)
                                if self.sco.y_1 > self.s_len - 1:
                                    self.sco.move_left(1)
                                    self.sco.crash = True
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 2
                            if node[3] == 2:
                                if self.sco.direction == 'EW':
                                    if self.sco.y_1 != self.s_len - 1:
                                        self.sco.move_right(2)
                                    elif self.sco.y_1 == self.s_len - 1:
                                        self.sco.y_2 = self.sco.y_1 - self.sco.length + 1
                                elif self.sco.direction == 'NS' or 'V':
                                    self.sco.move_right(2)
                                if self.sco.y_2 > self.s_len - 1:
                                    self.sco.move_left(2)
                                    self.sco.crash = True
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 2
                        # component move
                        self.move_sco(self.sco)
                        self.sco.steps += 1

                elif action == "up":
                    # clear current position
                    self.clear_sco(self.sco)
                    # check collision
                    self.check_collision(self.sco, action)
                    if self.sco.collision_u == True:
                        self.sco.crash = True
                        pass
                    elif self.sco.collision_u == False:
                        for node in self.sco.scoNodes:
                            if node[3] == 1:
                                if self.sco.direction == 'V':
                                    if self.sco.z_2 != self.s_he:
                                        self.sco.move_up(1)
                                    elif self.sco.z_2 == self.s_he:
                                        self.sco.z_1 = self.sco.z_2 - self.sco.length + 1
                                elif self.sco.direction == 'EW' or 'NS':
                                    self.sco.move_up(1)
                                if self.sco.z_1 > self.s_he:
                                    self.sco.crash = True
                                    self.sco.move_down(1)

                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 2
                            if node[3] == 2:
                                if self.sco.direction == 'V':
                                    if self.sco.z_1 != self.s_he:
                                        self.sco.move_up(2)
                                    elif self.sco.z_1 == self.s_he:
                                        self.sco.z_2 = self.sco.z_1 - self.sco.length + 1
                                elif self.sco.direction == 'EW' or 'NS':
                                    self.sco.move_up(2)
                                if self.sco.z_2 > self.s_he:
                                    self.sco.crash = True
                                    self.sco.move_down(2)

                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 2
                        # component move
                        self.move_sco(self.sco)
                        self.sco.steps += 1

                elif action == "down":
                    # clear current position
                    self.clear_sco(self.sco)
                    # check collision
                    self.check_collision(self.sco, action)
                    if self.sco.collision_d == True:
                        self.sco.crash = True
                        pass
                    elif self.sco.collision_d == False:
                        for node in self.sco.scoNodes:
                            if node[3] == 1:
                                if self.sco.direction == 'V':
                                    if self.sco.z_2 != 1:
                                        self.sco.move_down(1)
                                    elif self.sco.z_2 == 1:
                                        self.sco.z_1 = self.sco.z_2 + self.sco.length - 1
                                elif self.sco.direction == 'EW' or 'NS':
                                    self.sco.move_down(1)
                                if self.sco.z_1 < 1:
                                    self.sco.crash = True
                                    self.sco.move_up(1)

                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 2
                            if node[3] == 2:
                                if self.sco.direction == 'V':
                                    if self.sco.z_1 != 1:
                                        self.sco.move_down(2)
                                    elif self.sco.z_1 == 1:
                                        self.sco.z_2 = self.sco.z_1 + self.sco.length - 1
                                elif self.sco.direction == 'EW' or 'NS':
                                    self.sco.move_down(2)
                                if self.sco.z_2 < 1:
                                    self.sco.crash = True
                                    self.sco.move_up(2)

                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 2
                        # component move
                        self.move_sco(self.sco)
                        self.sco.steps += 1

                # erect
                if action == 'change_dir':
                    if self.sco.type == 'column':
                        if self.sco.z_tar_1 > self.sco.z_tar_2:
                            action == "erect1"
                            self.check_collision(self.sco, action)
                            if self.sco.collision_e == True:
                                self.sco.crash = True
                                pass
                            elif self.sco.collision_e == False:
                                if self.sco.z_1 <= self.s_he - self.sco.length + 1 and (self.site_3D[self.sco.z_2 - 1][self.sco.x_2][self.sco.y_2] == 1 or self.site_3D[self.sco.z_2 - 1][self.sco.x_2][self.sco.y_2] == 10): # if component on ground or has a other component under
                                    if self.sco.z_1 == self.sco.z_2:
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 0
                                        if self.sco.length > 2:
                                            if self.sco.x_1 > self.sco.x_2:
                                                for x_len in range(abs(self.sco.x_1 - self.sco.x_2)):
                                                    self.site_3D[self.sco.z_2][self.sco.x_2 + x_len + 1][self.sco.y_2] = 0
                                            elif self.sco.x_2 > self.sco.x_1:
                                                for x_len in range(abs(self.sco.x_2 - self.sco.x_1)):
                                                    self.site_3D[self.sco.z_2][self.sco.x_1 + x_len + 1][self.sco.y_2] = 0
                                            elif self.sco.y_1 > self.sco.y_2:
                                                for x_len in range(abs(self.sco.y_1 - self.sco.y_2) - 1):
                                                    self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2 + x_len + 1] = 0
                                            elif self.sco.y_2 > self.sco.y_1:
                                                for x_len in range(abs(self.sco.y_2 - self.sco.y_1) - 1):
                                                    self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1 + x_len + 1] = 0
                                        self.sco.erect1()
                                        self.sco.steps += 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                        if self.sco.length > 2:
                                            for len in range(self.sco.length - 2):
                                                self.site_3D[self.sco.z_2 + len + 1][self.sco.x_1][self.sco.y_1] = 1
                                else:
                                    self.sco.crash = True

                        elif self.sco.z_tar_2 > self.sco.z_tar_1:
                            action == "erect2"
                            self.check_collision(self.sco, action)
                            if self.sco.collision_e == True:
                                self.sco.crash = True
                                pass
                            elif self.sco.collision_e == False:
                                if self.sco.z_2 <= self.s_he - self.sco.length + 1 and (self.site_3D[self.sco.z_1 - 1][self.sco.x_1][self.sco.y_1] == 1 or self.site_3D[self.sco.z_1 - 1][self.sco.x_1][self.sco.y_1] == 10):
                                    if self.sco.z_1 == self.sco.z_2:
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 0
                                        if self.sco.length > 2:
                                            if self.sco.x_1 > self.sco.x_2:
                                                for x_len in range(abs(self.sco.x_1 - self.sco.x_2)):
                                                    self.site_3D[self.sco.z_2][self.sco.x_2 + x_len + 1][self.sco.y_2] = 0
                                            elif self.sco.x_2 > self.sco.x_1:
                                                for x_len in range(abs(self.sco.x_2 - self.sco.x_1)):
                                                    self.site_3D[self.sco.z_2][self.sco.x_1 + x_len + 1][self.sco.y_2] = 0
                                            elif self.sco.y_1 > self.sco.y_2:
                                                for x_len in range(abs(self.sco.y_1 - self.sco.y_2) - 1):
                                                    self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2 + x_len + 1] = 0
                                            elif self.sco.y_2 > self.sco.y_1:
                                                for x_len in range(abs(self.sco.y_2 - self.sco.y_1) - 1):
                                                    self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1 + x_len + 1] = 0
                                        self.sco.erect2()
                                        self.sco.steps += 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                        if self.sco.length > 2:
                                            for len in range(self.sco.length - 2):
                                                self.site_3D[self.sco.z_1 + len + 1][self.sco.x_1][self.sco.y_1] = 1
                                else:
                                    self.sco.crash = True

                    # elif self.sco.type == 'beam':


                # lay
                if action == "layf":
                    self.check_collision(self.sco, action)
                    if self.sco.collision_lay == True:
                        self.sco.crash = True
                        pass
                    elif self.sco.collision_lay == False:
                        if self.sco.z_1 != self.sco.z_2:
                            if self.sco.z_1 < self.sco.z_2:
                                z = self.sco.z_1
                            elif self.sco.z_2 < self.sco.z_1:
                                z = self.sco.z_2
                            if self.site_3D[z - 1][self.sco.x_2][self.sco.y_2] == 1 or self.site_3D[z - 1][self.sco.x_2][self.sco.y_2] == 10:
                                if self.sco.x_1 >= self.sco.length - 1 or self.sco.x_2 >= self.sco.length - 1:
                                    if self.sco.z_1 > self.sco.z_2:
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 0
                                        if self.sco.length > 2:
                                            for len in range(self.sco.length - 2):
                                                self.site_3D[self.sco.z_2 + len + 1][self.sco.x_1][self.sco.y_1] = 0
                                        self.sco.layf()
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                    elif self.sco.z_2 > self.sco.z_1:
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 0
                                        if self.sco.length > 2:
                                            for len in range(self.sco.length - 2):
                                                self.site_3D[self.sco.z_1 + len + 1][self.sco.x_1][self.sco.y_1] = 0
                                        self.sco.layf()
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    # component move
                                    self.move_sco(self.sco)
                                    self.sco.steps += 1
                                else:
                                    self.sco.crash = True

                elif action == "layb":
                    self.check_collision(self.sco, action)
                    if self.sco.collision_lay == True:
                        self.sco.crash = True
                        pass
                    elif self.sco.collision_lay == False:
                        if self.sco.z_1 != self.sco.z_2:
                            if self.sco.z_1 < self.sco.z_2:
                                z = self.sco.z_1
                            elif self.sco.z_2 < self.sco.z_1:
                                z = self.sco.z_2
                            if self.site_3D[z - 1][self.sco.x_2][self.sco.y_2] == 1 or self.site_3D[z - 1][self.sco.x_2][self.sco.y_2] == 10:
                                if self.sco.x_1 <= self.s_wid - self.sco.length:
                                    if self.sco.z_1 > self.sco.z_2:
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 0
                                        if self.sco.length > 2:
                                            for len in range(self.sco.length - 2):
                                                self.site_3D[self.sco.z_2 + len + 1][self.sco.x_1][self.sco.y_1] = 0
                                        self.sco.layb()
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                    elif self.sco.z_2 > self.sco.z_1:
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 0
                                        if self.sco.length > 2:
                                            for len in range(self.sco.length - 2):
                                                self.site_3D[self.sco.z_1 + len + 1][self.sco.x_1][self.sco.y_1] = 0
                                        self.sco.layb()
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    # component move
                                    self.move_sco(self.sco)
                                    self.sco.steps += 1
                                else:
                                    self.sco.crash = True

                elif action == "layl":
                    self.check_collision(self.sco, action)
                    if self.sco.collision_lay == True:
                        self.sco.crash = True
                        pass
                    elif self.sco.collision_lay == False:
                        if self.sco.z_1 != self.sco.z_2:
                            if self.sco.z_1 < self.sco.z_2:
                                z = self.sco.z_1
                            elif self.sco.z_2 < self.sco.z_1:
                                z = self.sco.z_2
                            if self.site_3D[z - 1][self.sco.x_2][self.sco.y_2] == 1 or self.site_3D[z - 1][self.sco.x_2][self.sco.y_2] == 10:
                                if self.sco.y_1 >= self.sco.length - 1 or self.sco.y_2 >= self.sco.length - 1:
                                    if self.sco.z_1 > self.sco.z_2:
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 0
                                        if self.sco.length > 2:
                                            for len in range(self.sco.length - 2):
                                                self.site_3D[self.sco.z_2 + len + 1][self.sco.x_1][self.sco.y_1] = 0
                                        self.sco.layl()
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                    elif self.sco.z_2 > self.sco.z_1:
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 0
                                        if self.sco.length > 2:
                                            for len in range(self.sco.length - 2):
                                                self.site_3D[self.sco.z_1 + len + 1][self.sco.x_1][self.sco.y_1] = 0
                                        self.sco.layl()
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    # component move
                                    self.move_sco(self.sco)
                                    self.sco.steps += 1
                                else:
                                    self.sco.crash = True

                elif action == "layr":
                    self.check_collision(self.sco, action)
                    if self.sco.collision_lay == True:
                        self.sco.crash = True
                        pass
                    elif self.sco.collision_lay == False:
                        if self.sco.z_1 != self.sco.z_2:
                            if self.sco.z_1 < self.sco.z_2:
                                z = self.sco.z_1
                            elif self.sco.z_2 < self.sco.z_1:
                                z = self.sco.z_2
                            if self.site_3D[z - 1][self.sco.x_2][self.sco.y_2] == 1 or self.site_3D[z - 1][self.sco.x_2][self.sco.y_2] == 10:
                                if self.sco.y_1 <= self.s_len - self.sco.length or self.sco.y_2 <= self.s_len - self.sco.length:
                                    if self.sco.z_1 > self.sco.z_2:
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 0
                                        if self.sco.length > 2:
                                            for len in range(self.sco.length - 2):
                                                self.site_3D[self.sco.z_2 + len + 1][self.sco.x_1][self.sco.y_1] = 0
                                        self.sco.layr()
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                    elif self.sco.z_2 > self.sco.z_1:
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 0
                                        if self.sco.length > 2:
                                            for len in range(self.sco.length - 2):
                                                self.site_3D[self.sco.z_1 + len + 1][self.sco.x_1][self.sco.y_1] = 0
                                        self.sco.layr()
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    # component move
                                    self.move_sco(self.sco)
                                    self.sco.steps += 1
                                else:
                                    self.sco.crash = True

                # rotate
                # if self.rotate_count > 1:
                #     self.sco.crash = True
                # else:
                if self.sco.direction != "V":
                    if action == 'rotate1':
                        self.clear_sco(self.sco)
                        if self.sco.direction == 'NS':
                            blank_count = 0
                            if self.sco.y_1 - self.sco.length + 2 > 0:
                                if self.sco.x_1 < self.sco.x_2:
                                    x1 = self.sco.x_1
                                    x2 = self.sco.x_2
                                elif self.sco.x_2 < self.sco.x_1:
                                    x1 = self.sco.x_2
                                    x2 = self.sco.x_1
                                for x_len in range(self.sco.length):
                                    for y_len in range(self.sco.length - 1):
                                        if self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 - y_len - 1] == 1 or self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 - y_len - 1] == 2:
                                            self.sco.collision_rotate1 = True
                                            self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                            self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                            self.move_sco(self.sco)
                                        if self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 - y_len - 1] == 0:
                                            blank_count += 1
                                            if blank_count == self.sco.length * (self.sco.length - 1):
                                                self.sco.collision_rotate1 = False
                                if self.sco.collision_rotate1 == False:
                                            if self.sco.x_1 < self.sco.x_2:
                                                self.sco.x_2 = self.sco.x_1
                                                self.sco.y_2 = self.sco.y_2 - self.sco.length + 1
                                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                            elif self.sco.x_2 < self.sco.x_1:
                                                self.sco.x_1 = self.sco.x_2
                                                self.sco.y_1 = self.sco.y_1 - self.sco.length + 1
                                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                            self.sco.direction = "EW"
                                            self.move_sco(self.sco)
                                            self.sco.steps += 1
                            else:
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                self.move_sco(self.sco)
                                self.sco.crash = True
                        elif self.sco.direction == 'EW':
                            blank_count = 0
                            if self.sco.x_1 + self.sco.length - 1 < self.s_wid:
                                if self.sco.y_1 < self.sco.y_2:
                                    y1 = self.sco.y_1
                                    y2 = self.sco.y_2
                                elif self.sco.y_2 < self.sco.y_1:
                                    y1 = self.sco.y_2
                                    y2 = self.sco.y_1
                                for y_len in range(self.sco.length):
                                    for x_len in range(self.sco.length - 1):
                                        if self.site_3D[self.sco.z_1][self.sco.x_1 + x_len + 1][y1 + y_len] == 1 or self.site_3D[self.sco.z_1][self.sco.x_1 + x_len + 1][y1 + y_len] == 2:
                                            self.sco.collision_rotate1 = True
                                            self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                            self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                            self.move_sco(self.sco)
                                        if self.site_3D[self.sco.z_1][self.sco.x_1 + x_len + 1][y1 + y_len] == 0:
                                            blank_count += 1
                                            if blank_count == self.sco.length * (self.sco.length - 1):
                                                self.sco.collision_rotate1 = False
                                if self.sco.collision_rotate1 == False:
                                    if self.sco.y_1 < self.sco.y_2:
                                        self.sco.y_2 = self.sco.y_1
                                        self.sco.x_2 = self.sco.x_2 + self.sco.length - 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    elif self.sco.y_2 < self.sco.y_1:
                                        self.sco.y_1 = self.sco.y_2
                                        self.sco.x_1 = self.sco.x_1 + self.sco.length - 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    self.sco.direction = "NS"
                                    self.move_sco(self.sco)
                                    self.sco.steps += 1
                            else:
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                self.move_sco(self.sco)
                                self.sco.crash = True
                        # self.rotate_count += 1
                    elif action == 'rotate2':
                        self.clear_sco(self.sco)
                        if self.sco.direction == 'NS':
                            blank_count = 0
                            if self.sco.y_1 + self.sco.length - 1 < self.s_len:
                                if self.sco.x_1 < self.sco.x_2:
                                    x1 = self.sco.x_1
                                    x2 = self.sco.x_2
                                elif self.sco.x_2 < self.sco.x_1:
                                    x1 = self.sco.x_2
                                    x2 = self.sco.x_1
                                for x_len in range(self.sco.length):
                                    for y_len in range(self.sco.length - 1):
                                        if self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 + y_len + 1] == 1 or self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 + y_len + 1] == 2:
                                            self.sco.collision_rotate2 = True
                                            self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                            self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                            self.move_sco(self.sco)
                                        if self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 + y_len + 1] == 0:
                                            blank_count += 1
                                            if blank_count == self.sco.length * (self.sco.length - 1):
                                                self.sco.collision_rotate2 = False
                                if self.sco.collision_rotate2 == False:
                                    if self.sco.x_1 < self.sco.x_2:
                                        self.sco.x_2 = self.sco.x_1
                                        self.sco.y_2 = self.sco.y_2 + self.sco.length - 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    elif self.sco.x_2 < self.sco.x_1:
                                        self.sco.x_1 = self.sco.x_2
                                        self.sco.y_1 = self.sco.y_1 + self.sco.length - 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    self.sco.direction = "EW"
                                    self.move_sco(self.sco)
                                    self.sco.steps += 1
                            else:
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                self.move_sco(self.sco)
                                self.sco.crash = True
                        elif self.sco.direction == 'EW':
                            blank_count = 0
                            if self.sco.x_1 - self.sco.length + 2 > 0:
                                for y_len in range(self.sco.length):
                                    for x_len in range(self.sco.length - 1):
                                        if self.sco.y_1 < self.sco.y_2:
                                            y1 = self.sco.y_1
                                            y2 = self.sco.y_2
                                        elif self.sco.y_2 < self.sco.y_1:
                                            y1 = self.sco.y_2
                                            y2 = self.sco.y_1
                                        if self.site_3D[self.sco.z_1][self.sco.x_1 - x_len - 1][y1 + y_len] == 1 or self.site_3D[self.sco.z_1][self.sco.x_1 - x_len - 1][y1 + y_len] == 2:
                                            self.sco.collision_rotate2 = True
                                            self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                            self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                            self.move_sco(self.sco)
                                        if self.site_3D[self.sco.z_1][self.sco.x_1 - x_len - 1][y1 + y_len] == 0:
                                            blank_count += 1
                                            if blank_count == self.sco.length * (self.sco.length - 1):
                                                self.sco.collision_rotate2 = False
                                if self.sco.collision_rotate2 == False:
                                    if self.sco.y_1 < self.sco.y_2:
                                        self.sco.y_2 = self.sco.y_1
                                        self.sco.x_2 = self.sco.x_2 - self.sco.length + 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    elif self.sco.y_2 < self.sco.y_1:
                                        self.sco.y_1 = self.sco.y_2
                                        self.sco.x_1 = self.sco.x_1 - self.sco.length + 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    self.sco.direction = "NS"
                                    self.move_sco(self.sco)
                                    self.sco.steps += 1
                            else:
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                self.move_sco(self.sco)
                                self.sco.crash = True
                        # self.rotate_count += 1
                    elif action == 'rotate3':
                        self.clear_sco(self.sco)
                        if self.sco.direction == 'NS':
                            blank_count = 0
                            if self.sco.y_1 - self.sco.length + 2 > 0:
                                if self.sco.x_1 < self.sco.x_2:
                                    x1 = self.sco.x_1
                                    x2 = self.sco.x_2
                                elif self.sco.x_2 < self.sco.x_1:
                                    x1 = self.sco.x_2
                                    x2 = self.sco.x_1
                                for x_len in range(self.sco.length):
                                    for y_len in range(self.sco.length - 1):
                                        if self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 - y_len - 1] == 1 or self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 - y_len - 1] == 2:
                                            self.sco.collision_rotate3 = True
                                            self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                            self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                            self.move_sco(self.sco)
                                        if self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 - y_len - 1] == 0:
                                            blank_count += 1
                                            if blank_count == self.sco.length * (self.sco.length - 1):
                                                self.sco.collision_rotate3 = False
                                if self.sco.collision_rotate3 == False:
                                    if self.sco.x_1 < self.sco.x_2:
                                        self.sco.x_1 = self.sco.x_2
                                        self.sco.y_1 = self.sco.y_1 - self.sco.length + 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    elif self.sco.x_2 < self.sco.x_1:
                                        self.sco.x_2 = self.sco.x_1
                                        self.sco.y_2 = self.sco.y_2 - self.sco.length + 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    self.sco.direction = "EW"
                                    self.move_sco(self.sco)
                                    self.sco.steps += 1
                            else:
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                self.move_sco(self.sco)
                                self.sco.crash = True
                        elif self.sco.direction == 'EW':
                            blank_count = 0
                            if self.sco.x_1 + self.sco.length - 1 < self.s_wid:
                                if self.sco.y_1 < self.sco.y_2:
                                    y1 = self.sco.y_1
                                    y2 = self.sco.y_2
                                elif self.sco.y_2 < self.sco.y_1:
                                    y1 = self.sco.y_2
                                    y2 = self.sco.y_1
                                for y_len in range(self.sco.length):
                                    for x_len in range(self.sco.length - 1):
                                        if self.site_3D[self.sco.z_1][self.sco.x_1 + x_len + 1][y1 + y_len] == 1 or self.site_3D[self.sco.z_1][self.sco.x_1 + x_len + 1][y1 + y_len] == 2:
                                            self.sco.collision_rotate3 = True
                                            self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                            self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                            self.move_sco(self.sco)
                                        if self.site_3D[self.sco.z_1][self.sco.x_1 + x_len + 1][y1 + y_len] == 0:
                                            blank_count += 1
                                            if blank_count == self.sco.length * (self.sco.length - 1):
                                                self.sco.collision_rotate3 = False
                                if self.sco.collision_rotate3 == False:
                                    if self.sco.y_1 < self.sco.y_2:
                                        self.sco.y_1 = self.sco.y_2
                                        self.sco.x_1 = self.sco.x_1 + self.sco.length - 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    elif self.sco.y_2 < self.sco.y_1:
                                        self.sco.y_2 = self.sco.y_1
                                        self.sco.x_2 = self.sco.x_2 + self.sco.length - 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    self.sco.direction = "NS"
                                    self.move_sco(self.sco)
                                    self.sco.steps += 1
                            else:
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                self.move_sco(self.sco)
                                self.sco.crash = True
                        # self.rotate_count += 1
                    # ? check
                    elif action == 'rotate4':
                        self.clear_sco(self.sco)
                        if self.sco.direction == 'NS':
                            blank_count = 0
                            if self.sco.y_1 + self.sco.length - 1 < self.s_len:
                                if self.sco.x_1 < self.sco.x_2:
                                    x1 = self.sco.x_1
                                    x2 = self.sco.x_2
                                elif self.sco.x_2 < self.sco.x_1:
                                    x1 = self.sco.x_2
                                    x2 = self.sco.x_1
                                for x_len in range(self.sco.length):
                                    for y_len in range(self.sco.length - 1):
                                        if self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 + y_len + 1] == 1 or self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 + y_len + 1] == 2:
                                            self.sco.collision_rotate4 = True
                                            self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                            self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                            self.move_sco(self.sco)
                                        if self.site_3D[self.sco.z_1][x1 + x_len][self.sco.y_1 + y_len + 1] == 0:
                                            blank_count += 1
                                            if blank_count == self.sco.length * (self.sco.length - 1):
                                                self.sco.collision_rotate4 = False
                                if self.sco.collision_rotate4 == False:
                                    if self.sco.x_1 < self.sco.x_2:
                                        self.sco.x_1 = self.sco.x_2
                                        self.sco.y_1 = self.sco.y_1 + self.sco.length - 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    elif self.sco.x_2 < self.sco.x_1:
                                        self.sco.x_2 = self.sco.x_1
                                        self.sco.y_2 = self.sco.y_2 + self.sco.length - 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    self.sco.direction = "EW"
                                    self.move_sco(self.sco)
                            else:
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                self.move_sco(self.sco)
                                self.sco.crash = True
                        elif self.sco.direction == 'EW':
                            blank_count = 0
                            if self.sco.x_1 - self.sco.length + 2 > 0:
                                for y_len in range(self.sco.length):
                                    for x_len in range(self.sco.length - 1):
                                        if self.sco.y_1 < self.sco.y_2:
                                            y1 = self.sco.y_1
                                            y2 = self.sco.y_2
                                        elif self.sco.y_2 < self.sco.y_1:
                                            y1 = self.sco.y_2
                                            y2 = self.sco.y_1
                                        if self.site_3D[self.sco.z_1][self.sco.x_1 - x_len - 1][y1 + y_len] == 1 or self.site_3D[self.sco.z_1][self.sco.x_1 - x_len - 1][y1 + y_len] == 2:
                                            self.sco.collision_rotate4 = True
                                            self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                            self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                            self.move_sco(self.sco)
                                        if self.site_3D[self.sco.z_1][self.sco.x_1 - x_len - 1][y1 + y_len] == 0:
                                            blank_count += 1
                                            if blank_count == self.sco.length * (self.sco.length - 1):
                                                self.sco.collision_rotate4 = False
                                if self.sco.collision_rotate4 == False:
                                    if self.sco.y_1 < self.sco.y_2:
                                        self.sco.y_1 = self.sco.y_2
                                        self.sco.x_1 = self.sco.x_1 - self.sco.length + 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    elif self.sco.y_2 < self.sco.y_1:
                                        self.sco.y_2 = self.sco.y_1
                                        self.sco.x_2 = self.sco.x_2 - self.sco.length + 1
                                        self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                        self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                    self.sco.direction = "NS"
                                    self.move_sco(self.sco)
                                    self.sco.steps += 1
                            else:
                                self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 1
                                self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 1
                                self.move_sco(self.sco)
                                self.sco.crash = True
                        # self.rotate_count += 1


                    elif self.sco.direction == "V":
                        if action == 'rotate1' or action == 'rotate2' or action == 'rotate3' or action == 'rotate4':
                            self.sco.crash = True



                if self.sco.collision_rotate1 or self.sco.collision_rotate2 or self.sco.collision_rotate3 or self.sco.collision_rotate4:
                    self.sco.crash = True

                self.check_arrived(self.sco)


    def print_map(self):
        for k in range(len(self.site_3D)):
            if k == 0:
                print("Current is ground")
            else:
                print("Current is {} meter".format(k))
            for i in range(len(self.site_3D[0])):
                for j in range(len(self.site_3D[0][0])):
                    print("[" + str(self.site_3D[k][i][j]) + "]", end="")
                print("")

    def clear_sco(self, sco):
        self.site_3D[sco.z_1][sco.x_1][sco.y_1] = 0
        self.site_3D[sco.z_2][sco.x_2][sco.y_2] = 0
        if sco.length > 2:
            if sco.x_1 > sco.x_2:
                for x_len in range(abs(sco.x_1 - sco.x_2)):
                    self.site_3D[sco.z_2][sco.x_2 + x_len + 1][sco.y_2] = 0
            elif sco.x_2 > sco.x_1:
                for x_len in range(abs(sco.x_2 - sco.x_1)):
                    self.site_3D[sco.z_2][sco.x_1 + x_len + 1][sco.y_2] = 0
            elif sco.y_1 > sco.y_2:
                for x_len in range(abs(sco.y_1 - sco.y_2) - 1):
                    self.site_3D[sco.z_2][sco.x_2][sco.y_2 + x_len + 1] = 0
            elif sco.y_2 > sco.y_1:
                for x_len in range(abs(sco.y_2 - sco.y_1) - 1):
                    self.site_3D[sco.z_1][sco.x_1][sco.y_1 + x_len + 1] = 0
            elif sco.z_1 > sco.z_2:
                for len in range(sco.length - 2):
                    self.site_3D[sco.z_2 + len + 1][sco.x_1][sco.y_1] = 0
            elif sco.z_2 > sco.z_1:
                for len in range(sco.length - 2):
                    self.site_3D[sco.z_1 + len + 1][sco.x_1][sco.y_1] = 0

    def create_target(self,sco):
        if sco.length > 2:
            if sco.x_tar_1 > sco.x_tar_2:
                for x_len in range(abs(sco.x_tar_1 - sco.x_tar_2) - 1):
                    self.site_3D[sco.z_tar_2][sco.x_tar_2 + x_len + 1][sco.y_tar_2] = 5
            elif sco.x_tar_2 > sco.x_tar_1:
                for x_len in range(abs(sco.x_tar_2 - sco.x_tar_1) - 1):
                    self.site_3D[sco.z_tar_2][sco.x_tar_1 + x_len + 1][sco.y_tar_2] = 5
            elif sco.y_tar_1 > sco.y_tar_2:
                for x_len in range(abs(sco.y_tar_1 - sco.y_tar_2) - 1):
                    self.site_3D[sco.z_tar_2][sco.x_tar_2][sco.y_tar_2 + x_len + 1] = 5
            elif sco.y_tar_2 > sco.y_tar_1:
                for x_len in range(abs(sco.y_tar_2 - sco.y_tar_1) - 1):
                    self.site_3D[sco.z_tar_1][sco.x_tar_1][sco.y_tar_1 + x_len + 1] = 5
            elif sco.z_tar_1 > sco.z_tar_2:
                for z_len in range(sco.length - 2):
                    self.site_3D[sco.z_tar_2 + z_len + 1][sco.x_tar_1][sco.y_tar_1] = 5
            elif sco.z_tar_2 > sco.z_tar_1:
                for z_len in range(sco.length - 2):
                    self.site_3D[sco.z_tar_1 + z_len + 1][sco.x_tar_1][sco.y_tar_1] = 5

    def move_sco(self, sco):
        if sco.length > 2:
            if sco.x_1 > sco.x_2:
                for x_len in range(abs(sco.x_1 - sco.x_2) - 1):
                    self.site_3D[sco.z_2][sco.x_2 + x_len + 1][sco.y_2] = 2
            elif sco.x_2 > sco.x_1:
                for x_len in range(abs(sco.x_2 - sco.x_1) - 1):
                    self.site_3D[sco.z_2][sco.x_1 + x_len + 1][sco.y_2] = 2
            elif sco.y_1 > sco.y_2:
                for x_len in range(abs(sco.y_1 - sco.y_2) - 1):
                    self.site_3D[sco.z_2][sco.x_2][sco.y_2 + x_len + 1] = 2
            elif sco.y_2 > sco.y_1:
                for x_len in range(abs(sco.y_2 - sco.y_1) - 1):
                    self.site_3D[sco.z_1][sco.x_1][sco.y_1 + x_len + 1] = 2
            elif sco.z_1 > sco.z_2:
                for len in range(sco.length - 2):
                    self.site_3D[sco.z_2 + len + 1][sco.x_1][sco.y_1] = 2
            elif sco.z_2 > sco.z_1:
                for len in range(sco.length - 2):
                    self.site_3D[sco.z_1 + len + 1][sco.x_1][sco.y_1] = 2

    def check_collision(self,sco,action):
        #if init position is NS
        collision_id = [1, 2, 10, 50, 'foundation',100, 200]
        for i in collision_id:
            if sco.direction == 'NS':
                if sco.x_1 < sco.x_2:
                    x1 = sco.x_1
                    x2 = sco.x_2
                elif sco.x_2 < sco.x_1:
                    x1 = sco.x_2
                    x2 = sco.x_1
                # check forward
                if action == 'forward':
                    if self.site_3D[sco.z_1][x1 - 1][sco.y_1] == i:
                        sco.collision_f = True
                        for x_len in range(abs(x2 - x1) + 1):
                            self.site_3D[sco.z_2][x1 + x_len][sco.y_2] = 2
                    elif self.site_3D[sco.z_1][x1 - 1][sco.y_1] == 0:
                        sco.collision_f = False
                # check back
                if action == 'back':
                    if x2 < self.s_wid - 1:
                        if self.site_3D[sco.z_1][x2 + 1][sco.y_1] == i:
                            sco.collision_b = True
                            for x_len in range(abs(x2 - x1) + 1):
                                self.site_3D[sco.z_2][x1 + x_len][sco.y_2] = 2
                        elif self.site_3D[sco.z_1][x2 + 1][sco.y_1] == 0:
                            sco.collision_b = False
                # check left
                if action == 'left':
                    blank_count = 0
                    for soc_len in range(abs(x2 - x1) + 1):
                        if self.site_3D[sco.z_1][x1 + soc_len][sco.y_1 - 1] == i:
                            sco.collision_l = True
                            for soc_len in range(abs(x2 - x1) + 1):
                                self.site_3D[sco.z_2][x1 + soc_len][sco.y_1] = 2
                    for soc_len in range(abs(x2 - x1) + 1):
                        if self.site_3D[sco.z_1][x1 + soc_len][sco.y_1 - 1] == 0:
                            blank_count += 1
                            if blank_count == sco.length:
                                sco.collision_l = False
                # check right
                if action == 'right':
                    if sco.y_1 < self.s_len - 1:
                        blank_count = 0
                        for soc_len in range(abs(x2 - x1) + 1):
                            if self.site_3D[sco.z_1][x1 + soc_len][sco.y_1 + 1] == i:
                                sco.collision_r = True
                                for soc_len in range(abs(x2 - x1) + 1):
                                    self.site_3D[sco.z_2][x1 + soc_len][sco.y_1] = 2
                        for soc_len in range(abs(x2 - x1) + 1):
                            if self.site_3D[sco.z_1][x1 + soc_len][sco.y_1 + 1] == 0:
                                blank_count += 1
                                if blank_count == sco.length:
                                    sco.collision_r = False
                # check up
                if action == 'up':
                    if sco.z_1 < self.s_he:
                        blank_count = 0
                        for soc_len in range(abs(x2 - x1) + 1):
                            if self.site_3D[sco.z_1 + 1][x1 + soc_len][sco.y_1] == i:
                                sco.collision_u = True
                                for soc_len in range(abs(x2 - x1) + 1):
                                    self.site_3D[sco.z_2][x1 + soc_len][sco.y_1] = 2
                        for soc_len in range(abs(x2 - x1) + 1):
                            if self.site_3D[sco.z_1 + 1][x1 + soc_len][sco.y_1] == 0:
                                blank_count += 1
                                if blank_count == sco.length:
                                    sco.collision_u = False
                # check down
                if action == 'down':
                    blank_count = 0
                    for soc_len in range(abs(x2 - x1) + 1):
                        if self.site_3D[sco.z_1 - 1][x1 + soc_len][sco.y_1] == i:
                            sco.collision_d = True
                            for soc_len in range(abs(x2 - x1) + 1):
                                self.site_3D[sco.z_2][x1 + soc_len][sco.y_1] = 2
                    for soc_len in range(abs(x2 - x1) + 1):
                        if self.site_3D[sco.z_1 - 1][x1 + soc_len][sco.y_1] == 0:
                            blank_count += 1
                            if blank_count == sco.length:
                                sco.collision_d = False
                        elif self.site_3D[sco.z_1 - 1][x1 + soc_len][sco.y_1] == 10:
                            sco.collision_d = False
                # check erect
                if action == 'erect1' or action == 'erect2':
                    if sco.z_1 < self.s_he - 1:
                        blank_count = 0
                        for z_len in range(abs(x2 - x1)):
                            for soc_len in range(abs(x2 - x1) + 1):
                                # print("it is z:", sco.z_1 + z_len + 1)
                                # print('it is x:', x1 + soc_len)
                                # print('it is y:', sco.y_1)
                                if self.site_3D[sco.z_1 + z_len + 1][x1 + soc_len][sco.y_1] == i:
                                    sco.collision_e = True
                                    for soc_len in range(abs(x2 - x1) + 1):
                                        self.site_3D[sco.z_2][x1 + soc_len][sco.y_1] = 2
                        for z_len in range(abs(x2 - x1)):
                            for soc_len in range(abs(x2 - x1) + 1):
                                if self.site_3D[sco.z_1 + z_len + 1][x1 + soc_len][sco.y_1] == 0:
                                    blank_count += 1
                                    if blank_count == sco.length * (sco.length-1):
                                        sco.collision_e = False
            # if init position is EW
            if sco.direction == 'EW':
                if sco.y_1 < sco.y_2:
                    y1 = sco.y_1
                    y2 = sco.y_2
                elif sco.y_2 < sco.y_1:
                    y1 = sco.y_2
                    y2 = sco.y_1
                # check forward
                if action == 'forward':
                    blank_count = 0
                    for soc_len in range(abs(y2 - y1) + 1):
                        if self.site_3D[sco.z_1][sco.x_1 - 1][y1 + soc_len] == i:
                            sco.collision_f = True
                            for soc_len in range(abs(y2 - y1) + 1):
                                self.site_3D[sco.z_1][sco.x_1][y1 + soc_len] = 2
                    for soc_len in range(abs(y2 - y1) + 1):
                        if self.site_3D[sco.z_1][sco.x_1 - 1][y1 + soc_len] == 0:
                            blank_count += 1
                            if blank_count == sco.length:
                                sco.collision_f = False
                # check back
                if action == 'back':
                    if sco.x_1 < self.s_wid - 1:
                        blank_count = 0
                        for soc_len in range(abs(y2 - y1) + 1):
                            if self.site_3D[sco.z_1][sco.x_1 + 1][y1 + soc_len] == i:
                                sco.collision_b = True
                                for soc_len in range(abs(y2 - y1) + 1):
                                    self.site_3D[sco.z_2][sco.x_1][y1 + soc_len] = 2
                        for soc_len in range(abs(y2 - y1) + 1):
                            if self.site_3D[sco.z_1][sco.x_1 + 1][y1 + soc_len] == 0:
                                blank_count += 1
                                if blank_count == sco.length:
                                    sco.collision_b = False
                # check left
                if action == 'left':
                    if self.site_3D[sco.z_1][sco.x_1][y1 - 1] == i:
                        sco.collision_l = True
                        for y_len in range(abs(y2 - y1) + 1):
                            self.site_3D[sco.z_2][sco.x_2][y1 + y_len] = 2
                    elif self.site_3D[sco.z_1][sco.x_1][y1 - 1] == 0:
                        sco.collision_l = False
                # check right
                if action == 'right':
                    if y2 < self.s_len - 1:
                        if self.site_3D[sco.z_1][sco.x_1][y2 + 1] == i:
                            sco.collision_r = True
                            for y_len in range(abs(y2 - y1) + 1):
                                self.site_3D[sco.z_2][sco.x_2][y1 + y_len] = 2
                        elif self.site_3D[sco.z_1][sco.x_1][y2 + 1] == 0:
                            sco.collision_r = False
                # check up
                if action == 'up':
                    if sco.z_1 < self.s_he:
                        blank_count = 0
                        for soc_len in range(abs(y2 - y1) + 1):
                            if self.site_3D[sco.z_1 + 1][sco.x_1][y1 + soc_len] == i:
                                sco.collision_u = True
                                for soc_len in range(abs(y2 - y1) + 1):
                                    self.site_3D[sco.z_1][sco.x_1][y1 + soc_len] = 2
                        for soc_len in range(abs(y2 - y1) + 1):
                            if self.site_3D[sco.z_1 + 1][sco.x_1][y1 + soc_len] == 0:
                                blank_count += 1
                                if blank_count == sco.length:
                                    sco.collision_u = False
                # check down
                if action == 'down':
                    blank_count = 0
                    for soc_len in range(abs(y2 - y1) + 1):
                        if self.site_3D[sco.z_1 - 1][sco.x_1][y1 + soc_len] == i:
                            sco.collision_d = True
                            for soc_len in range(abs(y2 - y1) + 1):
                                self.site_3D[sco.z_1][sco.x_1][y1 + soc_len] = 2
                    for soc_len in range(abs(y2 - y1) + 1):
                        if self.site_3D[sco.z_1 - 1][sco.x_1][y1 + soc_len] == 0:
                            blank_count += 1
                            if blank_count == sco.length:
                                sco.collision_d = False
                        elif self.site_3D[sco.z_1 - 1][sco.x_1][y1 + soc_len] == 10:
                            sco.collision_d = False
                # check erect
                if action == 'erect1' or action == 'erect2':
                    if sco.z_1 + sco.length - 1 < self.s_he:
                        if sco.z_1 < self.s_he - 1:
                            blank_count = 0
                            for z_len in range(abs(y2 - y1)):
                                for soc_len in range(abs(y2 - y1) + 1):
                                    if self.site_3D[sco.z_1 + z_len + 1][sco.x_1][y1 + soc_len] == i:
                                        sco.collision_e = True
                                        for soc_len in range(abs(y2 - y1) + 1):
                                            self.site_3D[sco.z_2][sco.x_1][y1 + soc_len] = 2
                            for z_len in range(abs(y2 - y1)):
                                for soc_len in range(abs(y2 - y1) + 1):
                                    if self.site_3D[sco.z_1 + z_len + 1][sco.x_1][y1 + soc_len] == 0:
                                        blank_count += 1
                                        if blank_count == sco.length * (sco.length-1):
                                            sco.collision_e = False
                    elif sco.z_1 + sco.length - 1 == self.s_he:
                        blank_count = 0
                        for z_len in range(abs(y2 - y1)):
                            for soc_len in range(abs(y2 - y1) + 1):
                                if self.site_3D[sco.z_1 + z_len + 1][sco.x_1][y1 + soc_len] == i:
                                    #print('e2 true')
                                    sco.collision_e = True
                                    for soc_len in range(abs(y2 - y1) + 1):
                                        self.site_3D[sco.z_2][sco.x_1][y1 + soc_len] = 2
                        for z_len in range(abs(y2 - y1)):
                            for soc_len in range(abs(y2 - y1) + 1):
                                if self.site_3D[sco.z_1 + z_len + 1][sco.x_1][y1 + soc_len] == 0:
                                    blank_count += 1
                                    if blank_count == sco.length * (sco.length - 1):
                                        sco.collision_e = False

            # if position is V
            if sco.direction == 'V':
                if sco.z_1 < sco.z_2:
                    z1 = sco.z_1
                    z2 = sco.z_2
                elif sco.z_2 < sco.z_1:
                    z1 = sco.z_2
                    z2 = sco.z_1
                    # check forward
                if action == 'forward':
                    blank_count = 0
                    for soc_len in range(abs(z2 - z1) + 1):
                        if self.site_3D[z1 + soc_len][sco.x_1 - 1][sco.y_1] == i:
                            sco.collision_f = True
                            for soc_len in range(abs(z2 - z1) + 1):
                                self.site_3D[z1 + soc_len][sco.x_1][sco.y_1] = 2
                    for soc_len in range(abs(z2 - z1) + 1):
                        if self.site_3D[z1 + soc_len][sco.x_1 - 1][sco.y_1] == 0:
                            blank_count += 1
                            if blank_count == sco.length:
                                sco.collision_f = False
                # check back
                if action == 'back':
                    if self.sco.x_1 <= self.s_wid - 2:
                        blank_count = 0
                        for soc_len in range(abs(z2 - z1) + 1):
                            if self.site_3D[z1 + soc_len][sco.x_1 + 1][sco.y_1] == i:
                                sco.collision_b = True
                                for soc_len in range(abs(z2 - z1) + 1):
                                    self.site_3D[z1 + soc_len][sco.x_1][sco.y_1] = 2
                        for soc_len in range(abs(z2 - z1) + 1):
                            if self.site_3D[z1 + soc_len][sco.x_1 + 1][sco.y_1] == 0:
                                blank_count += 1
                                if blank_count == sco.length:
                                    sco.collision_b = False
                # check left
                if action == 'left':
                    blank_count = 0
                    for soc_len in range(abs(z2 - z1) + 1):
                        if self.site_3D[z1 + soc_len][sco.x_1][sco.y_1 - 1] == i:
                            sco.collision_l = True
                            for soc_len in range(abs(z2 - z1) + 1):
                                self.site_3D[z1 + soc_len][sco.x_1][sco.y_1] = 2
                    for soc_len in range(abs(z2 - z1) + 1):
                        if self.site_3D[z1 + soc_len][sco.x_1][sco.y_1 - 1] == 0:
                            blank_count += 1
                            if blank_count == sco.length:
                                sco.collision_l = False
                # check right
                if action == 'right':
                    if sco.y_1 <= self.s_len - 2:
                        blank_count = 0
                        for soc_len in range(abs(z2 - z1) + 1):
                            if self.site_3D[z1 + soc_len][sco.x_1][sco.y_1 + 1] == i:
                                sco.collision_r = True
                                for soc_len in range(abs(z2 - z1) + 1):
                                    self.site_3D[z1 + soc_len][sco.x_1][sco.y_1] = 2
                        for soc_len in range(abs(z2 - z1) + 1):
                            if self.site_3D[z1 + soc_len][sco.x_1][sco.y_1 + 1] == 0:
                                blank_count += 1
                                if blank_count == sco.length:
                                    sco.collision_r = False
                # check up
                if action == 'up':
                    if z2 < self.s_he:
                        if self.site_3D[z2 + 1][sco.x_1][sco.y_1] == i:
                            sco.collision_u = True
                            for z_len in range(abs(z2 - z1) + 1):
                                self.site_3D[z1 + z_len][sco.x_2][sco.y_2] = 2
                        elif self.site_3D[z2 + 1][sco.x_1][sco.y_1] == 0:
                            sco.collision_u = False
                # check back
                if action == 'down':
                    if self.site_3D[z1 - 1][sco.x_1][sco.y_1] == i:
                        sco.collision_d = True
                        for z_len in range(abs(z2 - z1) + 1):
                            self.site_3D[z1 + z_len][sco.x_2][sco.y_2] = 2
                    elif self.site_3D[z1 - 1][sco.x_1][sco.y_1] == 0:
                        sco.collision_d = False
                    if self.site_3D[z1 - 1][sco.x_1][sco.y_1] == 10:
                        sco.collision_d = False
                # check layf
                if action == 'layf':
                    blank_count = 0
                    if self.sco.x_1 >= self.sco.length - 1:
                        for z_len in range(sco.length):
                            for sco_len in range(sco.length - 1):
                                if self.site_3D[z1 + z_len][sco.x_1 - sco_len - 1][sco.y_1] == i:
                                    sco.collision_lay = True
                                    for z_len in range(abs(z2 - z1) + 1):
                                        self.site_3D[z1 + z_len][sco.x_2][sco.y_2] = 2
                        for z_len in range(sco.length):
                            for sco_len in range(sco.length - 1):
                                if self.site_3D[z1 + z_len][sco.x_1 - sco_len - 1][sco.y_1] == 0:
                                    blank_count += 1
                                    if blank_count == sco.length * (sco.length - 1):
                                        sco.collision_lay = False

                # check layb
                if action == 'layb':
                    blank_count = 0
                    if self.sco.x_1 <= self.s_wid - self.sco.length:
                        for z_len in range(sco.length):
                            for sco_len in range(sco.length - 1):
                                if self.site_3D[z1 + z_len][sco.x_2 + sco_len + 1][sco.y_1] == i:
                                    sco.collision_lay = True
                                    for z_len in range(abs(z2 - z1) + 1):
                                        self.site_3D[z1 + z_len][sco.x_2][sco.y_2] = 2
                        for z_len in range(sco.length):
                            for sco_len in range(sco.length - 1):
                                if self.site_3D[z1 + z_len][sco.x_2 + sco_len + 1][sco.y_1] == 0:
                                    blank_count += 1
                                    if blank_count == sco.length * (sco.length - 1):
                                        sco.collision_lay = False

                # check layl
                if action == 'layl':
                    blank_count = 0
                    if self.sco.y_1 >= self.sco.length - 1:
                        for z_len in range(sco.length):
                            for sco_len in range(sco.length - 1):
                                if self.site_3D[z1 + z_len][sco.x_1][sco.y_1 - sco_len - 1] == i:
                                    sco.collision_lay = True
                                    for z_len in range(abs(z2 - z1) + 1):
                                        self.site_3D[z1 + z_len][sco.x_2][sco.y_2] = 2
                        for z_len in range(sco.length):
                            for sco_len in range(sco.length - 1):
                                if self.site_3D[z1 + z_len][sco.x_1][sco.y_1  - sco_len - 1] == 0:
                                    blank_count += 1
                                    if blank_count == sco.length * (sco.length - 1):
                                        sco.collision_lay = False
                # check layr
                if action == 'layr':
                    blank_count = 0
                    if self.sco.y_1 <= self.s_len - self.sco.length:
                        for z_len in range(sco.length):
                            for sco_len in range(sco.length - 1):
                                if self.site_3D[z1 + z_len][sco.x_2][sco.y_1 + sco_len + 1] == i:
                                    sco.collision_lay = True
                                    for z_len in range(abs(z2 - z1) + 1):
                                        self.site_3D[z1 + z_len][sco.x_2][sco.y_2] = 2
                        for z_len in range(sco.length):
                            for sco_len in range(sco.length - 1):
                                if self.site_3D[z1 + z_len][sco.x_2][sco.y_1  + sco_len + 1] == 0:
                                    blank_count += 1
                                    if blank_count == sco.length * (sco.length - 1):
                                        sco.collision_lay = False

    def check_above(self,sco):
        if sco.x_1 < sco.x_2:
            x1 = sco.x_1
            x2 = sco.x_2
        elif sco.x_2 < sco.x_1:
            x1 = sco.x_2
            x2 = sco.x_1
        if sco.y_1 < sco.y_2:
            y1 = sco.y_1
            y2 = sco.y_2
        elif sco.y_2 < sco.y_1:
            y1 = sco.y_2
            y2 = sco.y_1
        if sco.z_1 < sco.z_2:
            z = sco.z_2
        elif sco.z_2 < sco.z_1:
            z = sco.z_1
        if sco.direction == "NS":
            if sco.z_1 < self.s_he - 1:
                blank_count = 0
                for x_len in range(abs(x2 - x1) + 1):
                    if self.site_3D[sco.z_1 + 1][x1 + x_len][sco.y_2] == 1:
                        sco.lock = True
                    if self.site_3D[sco.z_1 + 1][x1 + x_len][sco.y_2] == 0:
                        blank_count += 1
                        if blank_count == sco.length:
                            sco.lock = False
        if sco.direction == "EW":
            if sco.z_1 < self.s_he - 1:
                blank_count = 0
                for sco_len in range(abs(y2 - y1) + 1):
                    if self.site_3D[sco.z_1 + 1][sco.x_1][y1 + sco_len] == 1:
                        sco.lock = True
                    if self.site_3D[sco.z_1 + 1][sco.x_1][y1 + sco_len] == 0:
                        blank_count += 1
                        if blank_count == sco.length:
                            sco.lock = False
        if sco.direction == "V":
            if z < self.s_he - 1:
                if self.site_3D[z + 1][sco.x_1][sco.y_1] == 1:
                    sco.lock = True
                if self.site_3D[z + 1][sco.x_1][sco.y_1] == 0:
                    sco.lock = False

    def check_arrived(self, sco):
        for tar in self.tar_list:
            if sco.x_1 == tar[0] and sco.y_1 == tar[1] and sco.z_1 == tar[2] \
                    and sco.x_2 == tar[3] and sco.y_2 == tar[4] and sco.z_2 == tar[5]:

                self.site_3D[sco.z_1][sco.x_1][sco.y_1] = 100
                self.site_3D[sco.z_2][sco.x_2][sco.y_2] = 100

                sco.arrived = True
                sco.working = False
                self.arrived_scos.append(sco)


                if sco.length > 2:
                    if sco.x_1 > sco.x_2:
                        for x_len in range(abs(sco.x_1 - sco.x_2) - 1):
                            self.site_3D[sco.z_2][sco.x_2 + x_len + 1][sco.y_2] = 100
                    elif sco.x_2 > sco.x_1:
                        for x_len in range(abs(sco.x_2 - sco.x_1) - 1):
                            self.site_3D[sco.z_2][sco.x_1 + x_len + 1][sco.y_2] = 100
                    elif sco.y_1 > sco.y_2:
                        for x_len in range(abs(sco.y_1 - sco.y_2) - 1):
                            self.site_3D[sco.z_2][sco.x_2][sco.y_2 + x_len + 1] = 100
                    elif sco.y_2 > sco.y_1:
                        for x_len in range(abs(sco.y_2 - sco.y_1) - 1):
                            self.site_3D[sco.z_1][sco.x_1][sco.y_1 + x_len + 1] = 100
                    elif sco.z_1 > sco.z_2:
                        for len in range(sco.length - 2):
                            self.site_3D[sco.z_2 + len + 1][sco.x_1][sco.y_1] = 100
                    elif sco.z_2 > sco.z_1:
                        for len in range(sco.length - 2):
                            self.site_3D[sco.z_1 + len + 1][sco.x_1][sco.y_1] = 100

                if self.sco.type == 'beam':
                    if self.sco.allow_assembly is True:
                        if self.sco.node1_assembly is False:
                            self.sco.node1_assembly = True
                            self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 200
                            for i in self.sco.relate_sco:
                                if i[2] == 1:
                                    for col in self.scos:
                                        if i[0] == col.id:
                                            col.node2_assembly = True
                                            self.site_3D[col.z_2][col.x_2][col.y_2] = 200
                        # elif action == "assembly_node2":
                        if self.sco.node2_assembly is False:
                            self.sco.node2_assembly = True
                            self.site_3D[self.sco.z_2][self.sco.x_2][self.sco.y_2] = 200
                            for i in self.sco.relate_sco:
                                if i[2] == 2:
                                    for col in self.scos:
                                        if i[0] == col.id:
                                            col.node2_assembly = True
                                            self.site_3D[col.z_2][col.x_2][col.y_2] = 200

                #  column assembly
                elif self.sco.type == 'column':
                    if self.sco.node1_assembly is False:
                        # print('I am arrived')
                        # print(self.site_3D[self.sco.z_1 - 1][self.sco.x_1][self.sco.y_1])
                        if self.site_3D[self.sco.z_1 - 1][self.sco.x_1][self.sco.y_1] == 'foundation':
                            self.sco.node1_assembly = True
                            self.site_3D[self.sco.z_1][self.sco.x_1][self.sco.y_1] = 200

        # print("sco.arrived is: ", sco.arrived)
        # # print("sco.crash is: ", sco.crash)
        # print("sco's x1 : {}, y1 : {}, z1 : {}".format(sco.x_1, sco.y_1, sco.z_1))
        # print("sco's x2 : {}, y2 : {}, z2 : {}".format(sco.x_2, sco.y_2, sco.z_2))
        # print("sco's x1 tar : {}, y1 tar : {}, z1 tar : {}".format(sco.x_tar_1, sco.y_tar_1, sco.z_tar_1))
        # print("sco's x2 tar : {}, y2 tar : {}, z2 tar : {}".format(sco.x_tar_2, sco.y_tar_2, sco.z_tar_2))

    def check_direction(self,sco):
        if sco.direction != sco.tar_direction:
            if sco.tar_direction == 'EW':
                if sco.x_tar_1 < sco.x_tar_2:
                    pass
                elif sco.x_tar_1 > sco.x_tar_2:
                    pass

            elif sco.tar_direction == 'NS':
                if sco.y_tar_1 < sco.y_tar_2:
                    pass
                elif sco.y_tar_1 > sco.y_tar_2:
                    pass
                pass
            elif sco.tar_direction == 'V':
                if sco.z_tar_1 < sco.z_tar_2:
                    pass
                elif sco.z_tar_1 > sco.z_tar_2:
                    pass

    def check_init(self, sco):
        if sco.lock == False and sco.not_working == True and sco.arrived == False and sco.crash == False:
            # print('Ready to work')
            # sco.working = True

            up_count = 0
            if sco.type == 'column':
                if sco.z_tar_1 > sco.z_tar_2:
                    sco.erect1()
                    sco.move_up(1)
                    sco.move_up(2)
                else:
                    sco.erect2()
                    sco.move_up(1)
                    sco.move_up(2)
            elif sco.type == 'beam':
                if sco.direction == sco.tar_direction:
                    while up_count < sco.z_tar_1 - 1:
                        sco.move_up(1)
                        sco.move_up(2)
                        up_count += 1
                    if sco.direction == 'NS':
                        if sco.x_tar_1 - sco.x_tar_2 != sco.x_1 - sco.x_2:
                            x= sco.x_1
                            sco.x_1 = sco.x_2
                            sco.x_2 = x
                    if sco.direction == 'EW':
                        if sco.x_tar_1 - sco.x_tar_2 != sco.x_1 - sco.x_2:
                            x= sco.x_1
                            sco.x_1 = sco.x_2
                            sco.x_2 = x
                elif sco.direction != sco.tar_direction:
                    while up_count < sco.z_tar_1 - 1:
                        sco.move_up(1)
                        sco.move_up(2)
                        up_count += 1
                    if sco.direction == 'NS':
                        sco.direction = 'EW'
                        x_center = int(abs(sco.x_1 + sco.x_2)/2)
                        sco.x_1 = x_center
                        sco.x_2 = x_center
                        y_center = int(abs(sco.y_1 + sco.y_2)/2)
                        if sco.y_tar_1 > sco.y_tar_2:
                            sco.y_1 = y_center + 1
                            sco.y_2 = y_center - 1
                        elif sco.y_tar_2 > sco.y_tar_1:
                            sco.y_1 = y_center - 1
                            sco.y_2 = y_center + 1
                    elif sco.direction == 'EW':
                        sco.direction = 'NS'
                        x_center = int(abs(sco.x_1 + sco.x_2) / 2)
                        y_center = int(abs(sco.y_1 + sco.y_2) / 2)
                        sco.y_1 = y_center
                        sco.y_2 = y_center
                        if sco.x_tar_1 > sco.x_tar_2:
                            sco.x_1 = x_center + 1
                            sco.x_2 = x_center - 1
                        elif sco.x_tar_2 > sco.x_tar_1:
                            sco.x_1 = x_center - 1
                            sco.x_2 = x_center + 1


                sco.check_arrive = 0
                for id in sco.relate_sco:
                    for o_sco in self.scos:
                        if id[0] == o_sco.id:
                            if o_sco.type == 'column':
                                if o_sco.node1_assembly is True:
                                    sco.check_arrive += 1
                if sco.check_arrive < 2:
                    sco.wrong_work = True
                elif sco.check_arrive == 2:
                    sco.wrong_work = False
                    sco.allow_assembly = True

            if sco.working == True:
                sco.not_working = False








if __name__ == "__main__":
    site = site(15, 20, 4)
    site.print_map()
    print(site.site_3D)


