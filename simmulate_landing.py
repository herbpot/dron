import simpy as si
import time as ti
import random


#변수 ################################################################
endcode = 0
climate = 0
dron_hp = []
dron_sen_hp = []
key_M = []
l = {}
windtime = 0
windforce = 0
hp = 0
dron_gps = [0,0] #드론 위치(GPS)
end_gps = [130,0] #목적지 위치
a = 0
#일반 객체 ##########################################################

def dic(x):
    return l[x]


def ran_cl() :
    global climate
    #print('날씨 확인중')
    #ti.sleep(0.1)
    climate = random.randint(1,11)
    if climate <= 4 :
        climate = 'rain'
        #print('rain')
    else :
        climate = 'clean'
        #print('clean')
        

def falling(hight, m) :
    global dama,hp,endcode
    
    g = 9.8
    dama = int(m*hight * random.randint(8, 10)/10)
    # print(f'받은 충격량 {dama}')

    # try :
    #     dama = random.randint(5,hight)
    # except ValueError :
    #     dama = random.randint(hight,5)
    
    
    hp = hp - dama
    endcode = 1
    #print(f'추락! 남은 내구도 : {hp}')


def wind():
    global windforce,windtime
    if windtime < 5 :
        windforce = int(random.randint(1,6))
    elif windtime < 8 :
        windforce = int(random.randint(5,11))
    elif windtime < 12 :
        windforce = int(random.randint(10,16))
    elif windtime < 15 :
        windforce = int(random.randint(15,21))
    elif windtime < 17 :
        windforce = int(random.randint(20,26))
    else : 
        windforce = int(random.randint(25,31))

    # print(f'바람 세기 {windforce}')


def parachute(env, hight) :
    global endcode,windtime
    #print(hight)
    #print('낙하산')
    while True :
        hight = hight - 0.5
        wind()
        sensor = windforce/4
        windtime = windtime + 1
        if sensor >= 6 or sensor <= -6 :
            # print('senor3')
            falling(hight,m=220)
            endcode = 1
            break

        if hight <= 0 :
            # print('land with parachute')
            endcode = 1
            break
            
    
def dron_sen_start():
    global endcode,windtime
    env = si.Environment()
    env.process(dron_sen(env))
    env.run()
    endcode = 0
    windtime = 0
    dron_sen_hp.append(hp)
    l[2] = hp


def dron_start() :
    global endcode,windtime
    env = si.Environment()
    env.process(dron(env))
    env.run()
    endcode = 0
    windtime = 0
    dron_hp.append(hp)
    l[1] = hp

def go():
    global end_gps,dron_gps
    print('이동중')
    dron_gps[0] = dron_gps[0] + 10
    print(f'남은 거리{end_gps[0] - dron_gps[0]}')

def back():
    global end_gps,dron_gps
    print('귀환중')
    dron_gps[0] = dron_gps[0] - 10
    print(f'남은 거리{dron_gps[0]}')

def move() :
    global a
    if a == 0 :
        go()
    if a == 1 :
        back()

#시뮬레이션 객체 ######################################################

def dron_sen(env):
    global windtime,windforce,hp,endcode,end_gps,dron_gps,a
    hight = 10 #드론 높이
    sensor = int(0) #자이로 센서
    hp = 2200
    dron_gps = [0,0] #드론 위치(GPS)
    end_gps = [130,0] #목적지 위치

    while endcode == 0 :    
        # print(f'받은 코드 {endcode}')
        if endcode != 0 :
            break
        ran_cl()
        # print(f'날씨 {climate}')

        if climate == 'rain' :
            wind()
            # print(f'바람세기 {windforce}')
            sensor = windforce/4
            windtime = windtime + 1
            # print(f'센서 {sensor}')

            if hight == 0 :
                # print('land')
                break

            if sensor <2 or sensor >-2 :
                # print('senor1')
                # print('자이로센서 값 :' + str(sensor))
                hight = hight - 1
                # print(f'높이 {hight}')

            if sensor <=4 or sensor >=-4 :
                # print('senor2')
                # print('자이로센서 값 :' + str(sensor))
                parachute(env, hight)
                #print('센서값 이상')
                # print(f'높이 {hight}')

            if sensor >= 5 or sensor <= -5 :
                # print('senor3')
                falling(hight,m=220)
                endcode = 1
                break
        '''목적지까지 이동'''
        move()
        if end_gps[0] == dron_gps[0] :
            print('목적지 도착, 물품 수령중')
            yield env.timeout(10)
            a = 1
        if 0 == dron_gps[0] :
            print('귀환 완료')
            a = 0
            break
        


        #ti.sleep(0.2)
        
    yield env.timeout(1)

def dron(env):
    global windforce,windtime,hp,a
    hight = 10 #드론 높이
    hp = 2200
    while endcode == 0 :    
        ran_cl()
        if climate == 'rain' :
            wind()
            windtime = windtime + 1
            if windforce  <= 15 :
                falling(hight,m=200)
                break
        
        move()
        if end_gps[0] == dron_gps[0] :
            print('목적지 도착, 물품 수령중')
            yield env.timeout(10)
            a = 1
            
        if 0 == dron_gps[0] :
            print('귀환 완료')
            a = 0
            yield env.timeout(10)
            break

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

    #ti.sleep(1)
    #print('일반 드론')
    dron_start()

    #ti.sleep(1)
    #print('자이로센서 탑제 드론')
    dron_sen_start()


    m = max(l.keys(), key=dic)
    key_M.append(m)
    m = 0

    # print(l)
    # print(m)
    # print(key_M)

    #print(f'반복 횟수 : {i+1}')
    l = {}
    print(f'반복횟수 {i}')

print(f'''
일반드론 추락 후 내구도 > 
{dron_hp}
''')

print(f'''
자이로센서 드론 추락 후 내구도 >
{dron_sen_hp}
''')

print('결과')
print('일반드론', str(key_M.count(1)), '번' ,'최대체력',str(max(dron_hp)))
print('센서 탑제 드론', str(key_M.count(2)), '번','최대체력',str(max(dron_sen_hp)))



'''목적지 갔다가 오는 프로그램 만드는 중'''