import cube_sim

result = {}
for i in range(0,1000):
    name = cube_sim.main()
    if name not in result.keys():
        result[name] = 0
    result[name] += 1

for key in result:
    print("%s获得了%d次冠军"%(key,result[key]))