import simpy as si
import numpy as np


#변수 ################################################################
endcode = 0
#기타 코드 ###########################################################
climate = np.random.randint(1,11)
if climate < 4 :
    climate = 'rain'


#일반 객체 ##########################################################

def falling(hight) :
    global dama,hp,endcode
    hp = 200 #드론 내구도
    dama = np.random.randint(0,hight)
    hp = hp - dama
    print(f'추락! 남은 내구도 : {hp}')
    endcode = 1
    

def warning(hight, percent=11) :
    print('현재 높이 :' + str(hight))
    fall = np.random.randint(1,percent)
    if fall < 2 :
        falling(hight)

def parachute(env, hight) :
    yield env.timeout(np.random.randint(0,3))
    warning(hight,percent=16)
    hight = hight - 0.5
    return hight

#시뮬레이션 객체 ######################################################
def dron_sen(env):
    hight = 100 #드론 높이
    sensor = int(0) #자이로 센서
    while True :    
        if climate == 'rain' :
            sensor = int(np.random.randint(-5,6))

            if sensor <3 or sensor >-3 and sensor != 0 :
                print('자이로센서 값 :' + str(sensor))
                hight = hight - 1
                warning(hight)
        
            elif sensor <5 or sensor >-5 :
                print('자이로센서 값 :' + str(sensor))
                hight = parachute(env,hight)
            
        if endcode != 0 :
            break

        
    yield env.timeout(1)

def dron(env):
    hight = 100 #드론 높이
    while True :    
        if climate == 'rain' :
            warning()

        if endcode != 0 :
            break

        
    yield env.timeout(1)




#시뮬래이션 시작 #######################################################
ans = int(input('반복 횟수 입력 >>>'))
for i in range(ans) :
    env = si.Environment()
    # cl_list = si.Store(env, capacity=2)
    # cli_re = env.process(cl_list)
    env.process(dron_sen(env))
    env.run()

ans = input()