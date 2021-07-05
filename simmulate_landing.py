import simpy as si
import time as ti
import numpy as np


#변수 ################################################################
endcode = 0
climate = 0
dron_hp = []
dron_sen_hp = []
#일반 객체 ##########################################################

def ran_cl() :
    global climate
    print('날씨 확인중')
    ti.sleep(0.1)
    climate = np.random.randint(1,11)
    if climate < 4 :
        climate = 'rain'
        #print('rain')
    else :
        #print('clean')
        print('')

def falling(hight) :
    global dama,hp,endcode
    hp = 200 #드론 내구도
    dama = np.random.randint(0,hight)
    hp = hp - dama
    #print(f'추락! 남은 내구도 : {hp}')
    endcode = 1
    

def warning(hight, percent=11) :
    #rint('현재 높이 :' + str(hight))
    fall = np.random.randint(1,percent)
    if fall < 2 :
        falling(hight)

def parachute(env, hight) :
    yield env.timeout(np.random.randint(0,3))
    print('낙하산')
    warning(hight,percent=16)
    hight = hight - 0.5
    return hight

#시뮬레이션 객체 ######################################################

def dron_sen(env):
    hight = 100 #드론 높이
    sensor = int(0) #자이로 센서
    while climate != 'rain'  :
        ran_cl()
    while True :    
        if climate == 'rain' :
            sensor = int(np.random.randint(-5,6))

            if sensor <3 or sensor >-3 and sensor != 0 :
                #print('자이로센서 값 :' + str(sensor))
                hight = hight - 1
                warning(hight)
        
            elif sensor <=5 or sensor >=-5 :
                #print('자이로센서 값 :' + str(sensor))
                hight = parachute(env,hight)
            
        if endcode != 0 :
            break
        #ti.sleep(0.2)
        

        

        
    yield env.timeout(1)

def dron(env):
    hight = 100 #드론 높이
    while climate != 'rain'  :
        ran_cl()
    while True :    
        if climate == 'rain' :
            warning(hight)

        if endcode != 0 :
            break
        #ti.sleep(0.2)

        
    yield env.timeout(1)




#시뮬래이션 시작 #######################################################

print('''
상황 : 날씨가 좋지 않은날 비상착륙이 장비된 드론과 일반드론의 파손률 비교
(3초 후 시뮬레이션 시작)
''')
ti.sleep(3)

ans = int(input('반복 횟수 입력 >>>'))

for i in range(ans) :

    ti.sleep(1)

    print('일반 드론')
    env = si.Environment()
    env.process(dron(env))
    env.run()
    endcode = 0
    dron_hp.append(hp)

    ti.sleep(1)

    print('자이로센서 탑제 드론')
    env = si.Environment()
    env.process(dron_sen(env))
    env.run()
    endcode = 0
    dron_sen_hp.append(hp)

    print(f'반복 횟수 : {i+1}')

print(f'''
일반드론 추락 후 내구도 > 
{dron_hp}
''')
print(f'''
자이로센서 드론 추락 후 내구도 >
{dron_sen_hp}
''')

ans = input()