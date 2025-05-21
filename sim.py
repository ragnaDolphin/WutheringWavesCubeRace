import cube_sim

total_match_num = 10000
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
    print("---%s的成绩：---"%key)
    rank = 1
    max_rank = len(result[key].keys())
    for rank in range(1,max_rank + 1):
        print("第%d名：%d次"%(rank,result[key][rank]))
    no1_rate = result[key][1] / total_match_num * 100
    win_rate = (result[key][1] + result[key][2]) / total_match_num * 100
    print('夺冠率：%.2f%%'%no1_rate)
    print('晋级率：%.2f%%'%win_rate)