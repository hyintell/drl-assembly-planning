import random

class SCO:
    def __init__(self, id, type, x_node1, y_node1, z_node1, x_node2, y_node2, z_node2, x_target1, y_target1, z_target1, x_target2, y_target2, z_target2, length, relate_sco, train_on = False):
        self.id = id
        self.type = type
        self.x_1 = x_node1
        self.y_1 = y_node1
        self.z_1 = z_node1
        self.x_2 = x_node2
        self.y_2 = y_node2
        self.z_2 = z_node2
        self.x_tar_1 = x_target1
        self.y_tar_1 = y_target1
        self.z_tar_1 = z_target1
        self.x_tar_2 = x_target2
        self.y_tar_2 = y_target2
        self.z_tar_2 = z_target2
        #node x,y,z and node id
        self.node1 = [self.z_1, self.x_1, self.y_1, 1]
        self.node2 = [self.z_2, self.x_2, self.y_2, 2]
        self.scoNodes = [self.node1, self.node2]
        self.length = length
        self.node1_assembly = False
        self.node2_assembly = False
        self.relate_sco = relate_sco
        if self.x_1 == self.x_2:
            self.direction = 'EW'
        elif self.y_1 == self.y_2:
            self.direction = 'NS'
        elif self.z_1 != self.z_2:
            self.direction = 'V'
        if self.x_tar_1 == self.x_tar_2:
            self.tar_direction = 'EW'
        elif self.y_tar_1 == self.y_tar_2:
            self.tar_direction = 'NS'
        elif self.z_tar_1 != self.z_tar_2:
            self.tar_direction = 'V'
        self.steps = 0
        self.collision_f = False
        self.collision_b = False
        self.collision_l = False
        self.collision_r = False
        self.collision_u = False
        self.collision_d = False
        self.collision_e = False
        self.collision_lay = False
        self.collision_rotate1 = False
        self.collision_rotate2 = False
        self.collision_rotate3 = False
        self.collision_rotate4 = False
        self.not_working = True
        self.lock = False
        self.arrived = False
        self.crash = False
        self.working = False
        self.wrong_work = False
        self.init_place = True
        self.train = train_on

        if self.type == 'beam':
            self.allow_assembly = False
            self.check_arrive = 0
        else:
            pass


        if self.train and self.init_place:
            self.init_place = False
            # if self.type == 'column':
            #     rand_choice = random.choice([1, 2])
            #     if rand_choice == 1:
            #         self.x_1 = random.randint(3, 8)
            #         # self.y_1 = random.randint(3, 8)
            #         self.y_1 = random.choice([random.randint(3, 8),random.randint(10,12),13])
            #         self.x_2 = self.x_1 - 3
            #         self.y_2 = self.y_1
            #     elif rand_choice == 2:
            #         self.x_1 = random.choice([random.randint(3, 8),random.randint(10,12),13])
            #         # self.x_1 = random.randint(3, 8)
            #         self.y_1 = random.randint(3, 8)
            #         self.y_2 = self.y_1 - 3
            #         self.x_2 = self.x_1
            # elif self.type == 'beam':
            #     rand_choice = random.choice([1, 2])
            #     if rand_choice == 1:
            #         self.x_1 = random.choice([random.randint(2, 8),12])
            #         self.y_1 = random.choice([random.randint(2, 8),random.randint(10,12),13])
            #         # self.x_1 = random.randint(3, 8)
            #         # self.y_1 = random.randint(3, 8)
            #         self.x_2 = self.x_1 - 2
            #         self.y_2 = self.y_1
            #     elif rand_choice == 2:
            #         self.x_1 = random.choice([random.randint(2, 8),random.randint(10,12),13])
            #         self.y_1 = random.choice([random.randint(2, 8),12])
            #         # self.x_1 = random.randint(3, 8)
            #         # self.y_1 = random.randint(3, 8)
            #         self.y_2 = self.y_1 - 2
            #         self.x_2 = self.x_1

            if self.type == 'column':
                rand_choice = random.choice([1, 2])
                self.x_1 = random.randint(3, 11)
                if self.x_1 < 6:
                    if rand_choice == 1:
                        # change range
                        #self.y_1 = random.randint(3, 12)
                        self.y_1 = random.randint(3, 7)
                        self.x_2 = self.x_1 - 3
                        self.y_2 = self.y_1
                    elif rand_choice == 2:
                        #self.y_1 = random.randint(3, 12)
                        self.y_1 = random.randint(3, 7)
                        self.y_2 = self.y_1 - 3
                        self.x_2 = self.x_1
                if self.x_1 >= 6:
                    if rand_choice == 1:
                        self.y_1 = random.randint(3, 5)
                        self.x_2 = self.x_1 - 3
                        self.y_2 = self.y_1
                    elif rand_choice == 2:
                        self.y_1 = random.randint(3, 5)
                        self.y_2 = self.y_1 - 3
                        self.x_2 = self.x_1

            elif self.type == 'beam':
                rand_choice = random.choice([1, 2])
                self.x_1 = random.randint(3, 11)
                if self.x_1 < 6:
                    if rand_choice == 1:
                        #self.y_1 = random.randint(3, 11)
                        self.y_1 = random.randint(3, 7)
                        self.x_2 = self.x_1 - 2
                        self.y_2 = self.y_1
                    elif rand_choice == 2:
                        #self.y_1 = random.randint(3, 11)
                        self.y_1 = random.randint(3, 7)
                        self.y_2 = self.y_1 - 2
                        self.x_2 = self.x_1
                if self.x_1 >= 6:
                    if rand_choice == 1:
                        self.y_1 = random.randint(3, 5)
                        self.x_2 = self.x_1 - 2
                        self.y_2 = self.y_1
                    elif rand_choice == 2:
                        self.y_1 = random.randint(3, 5)
                        self.y_2 = self.y_1 - 2
                        self.x_2 = self.x_1
            self.node1 = [self.z_1, self.x_1, self.y_1, 1]
            self.node2 = [self.z_2, self.x_2, self.y_2, 2]

        
        
        # print("SCO Initialized")

    def move_forward(self, nodeId):
        if nodeId == 1:
            self.x_1 -= 1
        elif nodeId == 2:
            self.x_2 -= 1

    def move_back(self, nodeId):
        if nodeId == 1:
            self.x_1 += 1
        elif nodeId == 2:
            self.x_2 += 1

    def move_left(self, nodeId):
        if nodeId == 1:
            self.y_1 -= 1
        elif nodeId == 2:
            self.y_2 -= 1

    def move_right(self, nodeId):
        if nodeId == 1:
            self.y_1 += 1
        elif nodeId == 2:
            self.y_2 += 1

    def move_up(self, nodeId):
        if nodeId == 1:
            self.z_1 += 1
        elif nodeId == 2:
            self.z_2 += 1

    def move_down(self, nodeId):
        if nodeId == 1:
            self.z_1 -= 1
        elif nodeId == 2:
            self.z_2 -= 1

    def erect1(self):
        self.x_1 = self.x_2
        self.y_1 = self.y_2
        self.z_1 = self.z_2 + self.length - 1
        self.direction = 'V'


    def erect2(self):
        self.x_2 = self.x_1
        self.y_2 = self.y_1
        self.z_2 = self.z_1 + self.length - 1
        self.direction = 'V'

    def layf(self):
        if self.z_1 > self.z_2:
            self.x_1 = self.x_2 - self.length + 1
            self.y_1 = self.y_2
            self.z_1 = self.z_2
        elif self.z_2 > self.z_1:
            self.x_2 = self.x_1 - self.length + 1
            self.y_2 = self.y_1
            self.z_2 = self.z_1
        self.direction = 'NS'

    def layb(self):
        if self.z_1 > self.z_2:
            self.x_1 = self.x_2 + self.length -1
            self.y_1 = self.y_2
            self.z_1 = self.z_2
        elif self.z_2 > self.z_1:
            self.x_2 = self.x_1 + self.length -1
            self.y_2 = self.y_1
            self.z_2 = self.z_1
        self.direction = 'NS'


    def layl(self):
        if self.z_1 > self.z_2:
            self.x_1 = self.x_2
            self.y_1 = self.y_2 - self.length + 1
            self.z_1 = self.z_2
        elif self.z_2 > self.z_1:
            self.x_2 = self.x_1
            self.y_2 = self.y_1 - self.length + 1
            self.z_2 = self.z_1
        self.direction = 'EW'


    def layr(self):
        if self.z_1 > self.z_2:
            self.x_1 = self.x_2
            self.y_1 = self.y_2 + self.length -1
            self.z_1 = self.z_2
        elif self.z_2 > self.z_1:
            self.x_2 = self.x_1
            self.y_2 = self.y_1 + self.length -1
            self.z_2 = self.z_1
        self.direction = 'EW'

    # def asseble_node1(self):
    #     pass
    #
    # def asseble_node2(self):
    #     pass


if __name__ == "__main__":
    pass
