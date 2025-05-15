'''
鸣潮团子赛跑模拟
'''
from enum import Enum
import random

DEBUG = (__name__ == "__main__")

def main():
    
    # CUBE_GROUPS = []

    class CUBE_NAMES(Enum):
        守岸人 = 1
        卡卡罗 = 2
        今汐 = 3
        长离 = 4
        椿 = 5
        小土豆 = 6

    class Paramaters():
        def __init__(self):
            self.TOTAL_LENGTH = 24
            self.CHANGLI_ABILITY = False
            self.CUBE_GROUPS = []

        def get_cube_group(self,position):
            for cube_group in self.CUBE_GROUPS:
                if cube_group.position == position:
                    return cube_group
            return False

    class Match():
        def __init__(self):
            self.params = Paramaters()

        def init_cubes(self):
            self.cube_list = []
            self.cube_dict = {}
            for name in CUBE_NAMES:
                # print("初始化%s团子"%name.name)
                cube = Cube(name,self.params)
                self.cube_list.append(cube)
                self.cube_dict[name] = cube

        def update_rank(self):
            sorted_cube_list = sorted(self.cube_list, key=lambda x: (-x.position, -x.height))
            for cube in sorted_cube_list:
                cube.rank = sorted_cube_list.index(cube) + 1

        def turn_process(self):
            random.shuffle(self.cube_list)
            if DEBUG:
                cube_order = []
                for cube in self.cube_list:
                    cube_order.append(cube.name.name)
                print("行动顺序为：",cube_order)
            if self.params.CHANGLI_ABILITY:
                self.cube_list.remove(self.cube_dict[CUBE_NAMES.长离])
                self.cube_list.append(self.cube_dict[CUBE_NAMES.长离])
                self.params.CHANGLI_ABILITY = False
                
            for cube in self.cube_list:
                cube.act()
                self.update_rank()
                if cube.position >= self.params.TOTAL_LENGTH:
                    for _cube in self.cube_list:
                        if _cube.rank == 1:
                            return _cube.name
                        
            if self.cube_dict[CUBE_NAMES.长离].height > 1 and random.random() <= 0.65:
                if DEBUG:
                    print("---长离技能发动！！---")
                self.params.CHANGLI_ABILITY = True

            return False

        def main(self):
            # print("初始化团子")
            self.init_cubes()
            turn_num = 1
            while True:
                if DEBUG:
                    print("-----第%d回合开始-----"%turn_num)
                winner = self.turn_process()
                turn_num += 1
                self.params.CUBE_GROUPS.sort(key=lambda x: (-x.position))
                if DEBUG:
                    print("-----第%d回合结束，当前场况：-----"%turn_num)
                    for cube_group in self.params.CUBE_GROUPS:
                        cube_list = []
                        for cube in cube_group.cubes:
                            cube_list.append(cube.name.name)
                        print("第%d格："%cube_group.position,cube_list)
                if winner:
                    break
            if DEBUG:
                print("冠军是%s"%winner.name)
            return winner.name

    class CubeGroup():
        def __init__(self,cubes,params):
            self.cubes = []
            if type(cubes) == list:
                for cube in cubes:
                    self.cubes.append(cube)
                # self.total_height = len(cubes)
                self.position = cubes[0].position
            else:
                self.cubes.append(cubes)
                # self.total_height = 1
                self.position = cubes.position
            self.params = params
            self.params.CUBE_GROUPS.append(self)
        
        def get_upper_cubes(self,height):
            upper_cubes = self.cubes[height-1:]
            if len(upper_cubes) > 1:
                return upper_cubes
            return upper_cubes[0]

        @property
        def total_height(self):
            return len(self.cubes)
        
        def combine(self, target_cube_group):
            self.cubes = target_cube_group.cubes + self.cubes
            for cube in target_cube_group.cubes:
                cube.cube_group = self
            self.params.CUBE_GROUPS.remove(target_cube_group)




    class Cube():
        def __init__(self, chara_name,params):
            self.name = chara_name
            self.flower_ability = False
            self.rank = 0
            self.dice_point = 0
            self.position = 1
            # self.height = 1
            self.cube_group = CubeGroup(self,params)
            self.params = params

        @property
        def height(self):
            return self.cube_group.cubes.index(self)+1

    # random.randint
    # random.random

        def move(self):
            if DEBUG:
                print("%s团子 骰出 %d 点，从 %d 位置前进到 %d 位置"%(self.name.name,self.dice_point,self.position,self.position + self.dice_point))
            cur_cube_group_member = []
            move_cube_group_mamber = []
            for cube in self.cube_group.cubes:
                cur_cube_group_member.append(cube.name.name)

            target_cube_group = self.params.get_cube_group(self.position + self.dice_point)


            if self.flower_ability:
                self.cube_group.cubes.remove(self)
                if len(self.cube_group.cubes) == 0:
                    self.params.CUBE_GROUPS.remove(self.cube_group)
                self.cube_group = CubeGroup(self,self.params)
                self.flower_ability = False
            else:
                upper_cube_group = CubeGroup(self.cube_group.get_upper_cubes(self.height),self.params)
                original_cube_group = self.cube_group
                for cube in upper_cube_group.cubes:
                    original_cube_group.cubes.remove(cube)
                    if len(original_cube_group.cubes) == 0:
                        self.params.CUBE_GROUPS.remove(original_cube_group)
                    cube.cube_group = upper_cube_group

            for cube in self.cube_group.cubes:
                move_cube_group_mamber.append(cube.name.name)

            self.cube_group.position += self.dice_point
            for cube in self.cube_group.cubes:
                cube.position += self.dice_point

            if target_cube_group:
                self.cube_group.combine(target_cube_group)
            final_cube_group_mamber = []

            for cube in self.cube_group.cubes:
                if cube.name == CUBE_NAMES.今汐 and self.name != CUBE_NAMES.今汐:
                    if cube.have_top() and (random.random() <= 0.4):
                        original_height = cube.height
                        cube.move_to_top()
                        cur_height = cube.height
                        if DEBUG:
                            print("---%s技能发动！！，高度从%d移动到%d---"%(cube.name.name,original_height,cur_height))

            for cube in self.cube_group.cubes:
                final_cube_group_mamber.append(cube.name.name)

            

            if DEBUG:
                print("当前组: ",cur_cube_group_member)
                print("移动组: ",move_cube_group_mamber)
                print("最终组: ",final_cube_group_mamber)

                

        def have_top(self):
            if self.height < self.cube_group.total_height:
                return True
            return False

        def act(self):
            self.dice_point = random.randint(1,3)

            if self.name == CUBE_NAMES.守岸人:
                self.dice_point = random.randint(2,3)

            if DEBUG:
                print("%s团子 初始骰出 %d 点"%(self.name.name,self.dice_point))
            
            if self.name == CUBE_NAMES.卡卡罗:
                if self.rank == 6 and self.position != 1:
                    self.dice_point += 3
                    if DEBUG:
                            print("---卡卡罗技能发动！！---")

            if self.name == CUBE_NAMES.小土豆:
                if random.random() <= 0.28:
                    self.dice_point = self.dice_point*2
                    if DEBUG:
                        print("---小土豆技能发动！！---")

            if self.name == CUBE_NAMES.椿:
                if random.random() <= 0.5 and self.cube_group.total_height >1:
                    self.dice_point = self.dice_point + self.cube_group.total_height - 1
                    if DEBUG:
                        print("---椿技能发动！！---")
                    self.flower_ability = True

            self.move()

        def move_to_top(self):
            self.cube_group.cubes.remove(self)
            self.cube_group.cubes.append(self)

    
    return Match().main()

if DEBUG:
    main()
