'''
鸣潮团子赛跑模拟
'''
from enum import Enum
import random

DEBUG = (__name__ == "__main__")

def ability_active_notice(chara_name):
    if DEBUG:
        print("---%s技能发动！！---"%chara_name)

def main():
    # 在这里设置起始位置
    class CUBE_NAMES(Enum):
        守岸人 = ("守岸人", 1)
        卡卡罗 = ("卡卡罗", 1)
        今汐 = ("今汐", 1)
        长离 = ("长离", 1)
        椿 = ("椿", 1)
        小土豆 = ("小土豆", 1)
        洛可可 = ("洛可可", 1)
        船长 = ("船长", 1)
        坎特蕾拉 = ("坎特蕾拉", 1)
        赞妮 = ("赞妮", 1)
        卡提希亚 = ("卡提希亚", 1)
        菲比 = ("菲比", 1)

        def __init__(self, chara_name, start_position):
            self.chara_name = chara_name  # 存储人物名字
            self.start_position = start_position     # 存储起始位置

    # 在这里设置参赛选手
    match_cubes = [
        CUBE_NAMES.洛可可,
        CUBE_NAMES.船长,
        CUBE_NAMES.赞妮,
        CUBE_NAMES.菲比,
    ]

    class Paramaters():
        def __init__(self):
            self.TOTAL_LENGTH = 24
            self.CHANGLI_ABILITY = False
            self.ROCOCO_ABILITY = False
            self.CAPTAIN_ABILITY = False
            self.ZANI_ABILITY = False
            self.KATI_ABILITY = False
            self.CANTARELLA_ABILITY = True
            self.CUBE_GROUPS = []
            self.cur_turn = 1

        def get_cube_group(self,position):
            for cube_group in self.CUBE_GROUPS:
                if cube_group.position == position:
                    return cube_group
            return False

    class Match():
        def __init__(self):
            self.params = Paramaters()
            self.cube_list = []
            self.cube_dict = {}

        def init_cubes(self):
            for name in match_cubes:
                cube = Cube(name,self.params)
                self.cube_list.append(cube)
                self.cube_dict[name] = cube

        def update_rank(self):
            sorted_cube_list = sorted(self.cube_list, key=lambda x: (-x.position, -x.height))
            for cube in sorted_cube_list:
                cube.rank = sorted_cube_list.index(cube) + 1

        def turn_process(self):
            random.shuffle(self.cube_list)

            if self.params.CHANGLI_ABILITY:
                self.cube_list.remove(self.cube_dict[CUBE_NAMES.长离])
                self.cube_list.append(self.cube_dict[CUBE_NAMES.长离])
                self.params.CHANGLI_ABILITY = False

            if DEBUG:
                cube_order = []
                for cube in self.cube_list:
                    cube_order.append(cube.name.name)
                print("行动顺序为：",cube_order)

            if CUBE_NAMES.洛可可 in match_cubes and self.cube_list.index(self.cube_dict[CUBE_NAMES.洛可可]) == (len(match_cubes) - 1):
                self.params.ROCOCO_ABILITY = True

            if CUBE_NAMES.船长 in match_cubes and self.cube_list.index(self.cube_dict[CUBE_NAMES.船长]) == 0:
                self.params.CAPTAIN_ABILITY = True
                
            for cube in self.cube_list:
                cube.act()
                self.update_rank()
                if DEBUG and cube.name == CUBE_NAMES.卡提希亚 and not self.params.KATI_ABILITY:
                    print("卡提希亚当前排名：",cube.rank)

                if cube.name == CUBE_NAMES.卡提希亚 and not self.params.KATI_ABILITY and cube.rank == len(match_cubes):
                    ability_active_notice(cube.name.chara_name)
                    self.params.KATI_ABILITY = True

                if cube.position >= self.params.TOTAL_LENGTH:
                    result = []
                    cube_rank = sorted(self.cube_list, key=lambda x: (-x.position, -x.height))
                    for _cube in cube_rank:
                        result.append(_cube.name.name)
                    return result
                        
            if CUBE_NAMES.长离 in match_cubes and self.cube_dict[CUBE_NAMES.长离].height > 1 and random.random() <= 0.65:
                if DEBUG:
                    print("---长离技能发动！！---")
                self.params.CHANGLI_ABILITY = True

            return False

        def main(self):
            self.init_cubes()
            self.params.cur_turn = 1
            while True:
                if DEBUG:
                    print("-----第%d回合开始-----"%self.params.cur_turn)
                result = self.turn_process()
                
                self.params.CUBE_GROUPS.sort(key=lambda x: (-x.position))
                if DEBUG:
                    print("-----第%d回合结束，当前场况：-----"%self.params.cur_turn)
                    for cube_group in self.params.CUBE_GROUPS:
                        cube_list = []
                        for cube in cube_group.cubes:
                            cube_list.append(cube.name.name)
                        print("第%d格："%cube_group.position,cube_list)

                self.params.cur_turn += 1
                if result:
                    break
            if DEBUG:
                # print("冠军是%s"%winner.name)
                print("结果是",result)
            return result

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
        def __init__(self, chara_name,params:Paramaters):
            self.name = chara_name
            self.flower_ability = False
            self.rank = 0
            self.dice_point = 0
            self.position = chara_name.start_position
            # self.height = 1
            self.cube_group = CubeGroup(self,params)
            self.params = params

        @property
        def height(self):
            return self.cube_group.cubes.index(self)+1

        def move(self, cur_position, target_position):
            if DEBUG:
                print("%s团子从 %d 位置前进到 %d 位置"%(self.name.name,cur_position,target_position))
            cur_cube_group_member = []
            move_cube_group_mamber = []

            for cube in self.cube_group.cubes:
                cur_cube_group_member.append(cube.name.name)

            target_cube_group = self.params.get_cube_group(target_position)


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
                move_cube_group_mamber.append(cube.name.chara_name)

            self.cube_group.position = target_position
            for cube in self.cube_group.cubes:
                cube.position = target_position

            if target_cube_group:
                self.cube_group.combine(target_cube_group)
            final_cube_group_mamber = []

            for cube in self.cube_group.cubes:
                if CUBE_NAMES.今汐 in match_cubes and cube.name == CUBE_NAMES.今汐 and self.name != CUBE_NAMES.今汐:
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

            if self.name == CUBE_NAMES.赞妮:
                self.dice_point = random.choice([1,3])
                if self.cube_group.total_height > 1 and random.random() <= 0.4:
                    self.params.ZANI_ABILITY = True
                    ability_active_notice(self.name.chara_name)

            if DEBUG:
                print("%s团子 初始骰出 %d 点"%(self.name.name,self.dice_point))

            if self.name == CUBE_NAMES.赞妮 and self.params.ZANI_ABILITY:
                self.params.ZANI_ABILITY = False
                self.dice_point += 2

            if self.name == CUBE_NAMES.卡卡罗:
                if self.rank == len(match_cubes) and self.params.cur_turn != 1:
                    self.dice_point += 3
                    ability_active_notice(self.name.chara_name)

            if self.name == CUBE_NAMES.小土豆:
                if random.random() <= 0.28:
                    self.dice_point = self.dice_point*2
                    ability_active_notice(self.name.chara_name)

            if self.name == CUBE_NAMES.椿:
                if random.random() <= 0.5 and self.cube_group.total_height >1:
                    self.dice_point = self.dice_point + self.cube_group.total_height - 1
                    ability_active_notice(self.name.chara_name)
                    self.flower_ability = True

            if self.name == CUBE_NAMES.洛可可 and self.params.ROCOCO_ABILITY:
                self.params.ROCOCO_ABILITY = False
                self.dice_point += 2
                ability_active_notice(self.name.chara_name)

            if self.name == CUBE_NAMES.船长 and self.params.CAPTAIN_ABILITY:
                self.params.CAPTAIN_ABILITY = False
                self.dice_point += 2
                ability_active_notice(self.name.chara_name)

            if self.name == CUBE_NAMES.卡提希亚 and self.params.KATI_ABILITY and random.random() <= 0.6:
                ability_active_notice(self.name.chara_name)
                self.dice_point += 2

            if self.name == CUBE_NAMES.菲比 and random.random() <= 0.5:
                ability_active_notice(self.name.chara_name)
                self.dice_point += 1

            if self.name == CUBE_NAMES.坎特蕾拉 and self.params.CANTARELLA_ABILITY:
                canta_target_position = self.position + self.dice_point

                move_combine_group = False
                for cube_group in self.params.CUBE_GROUPS:
                    cur_move_combine_group_position = 99
                    if cube_group.position > self.position and cube_group.position < (self.position + self.dice_point) and cube_group.position < cur_move_combine_group_position:
                        cur_move_combine_group_position = cube_group.position
                        move_combine_group = cube_group

                if move_combine_group:
                    self.params.CANTARELLA_ABILITY = False
                    ability_active_notice(self.name.chara_name)

                    # if DEBUG:
                    #     if not self.params.get_cube_group(canta_target_position):
                    #         print('debug')

                    self.move(self.position, move_combine_group.position)
                    for cube in self.cube_group.cubes:
                        if cube.height == 1:
                            cube.move(cube.position, canta_target_position)
                            break
                    return
                
            self.move(self.position,self.position + self.dice_point)

        def move_to_top(self):
            self.cube_group.cubes.remove(self)
            self.cube_group.cubes.append(self)
    
    return Match().main()

if DEBUG:
    main()
