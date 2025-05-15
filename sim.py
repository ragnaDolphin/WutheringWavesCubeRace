import cube_sim

total_match_num = 1000
result = {}
for i in range(0,total_match_num):
    match_result = cube_sim.main()
    j = 1
    for name in match_result:
        if name not in result.keys():
            result[name] = {}
        if j not in result[name].keys():
            result[name][j] = 0
        result[name][j] += 1
        j += 1

for key in result:
    print("%s的成绩："%key)
    rank = 1
    for rank in range(1,7):
        print("第%d名：%d次"%(rank,result[key][rank]))
    win_rate = (result[key][1] + result[key][2] + result[key][3] + result[key][4]) / total_match_num * 100
    print('晋级率：%.2f%%'%win_rate)