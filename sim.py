import cube_sim

result = {}
for i in range(0,1000):
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