import simpy as si
import time as ti
import numpy as np

l_np = np.array([0,0,0])
l = {}
key_M = []

'''하나의 드론은 일반 배터리 내장 다른 드론은 지속적인 충전을 구현 '''

#드론 객체 ###################################################################

def dron_1(env) :
    global battery_1,hight_1,inertia_1,dron_gps_1,restricted_area_1
    battery_1 = 620 * 5 #드론 배터리 용량
    dron_gps_1 = [0,0] #드론 위치(GPS)
    use_b_1 = 2300 * 5 # 배터리 사용량
    timer_1 = battery_1/use_b_1 * 60 #운행시간(분단위)

    """
    1번 드론 일반적인 베터리 충전 방식
    """
    while timer_1 > 1 :
        timer_1 = timer_1 -1
        dron_gps_1[0] = dron_gps_1[0] + 10
        # print('드론 1이 간 거리' + str(dron_gps_1))
        # print('남은 운행시간 :' + str(timer_1))
        yield env.timeout(1)


def dron_2(env) :
    global battery_2,hight_2,inertia_2,dron_gps_2,restricted_area_2
    battery_2 = 620 * 5 #드론 배터리 용량 mAh
    dron_gps_2 = [0,0] #드론 위치(GPS)
    use_b_2 = 2300 * 5 # 배터리 사용량
    timer_2 = battery_2/use_b_2 * 60 #운행시간(분단위)
    charge_t_1 = 45/use_b_2 * 60 #충전 구현

    """
    2번 드론 지속적인 레이져 충전 방식
    """
    while timer_2 > 1 :
        timer_2 = timer_2 -1
        timer_2 = timer_2 + charge_t_1
        dron_gps_2[0] = dron_gps_2[0] + 10
        # print('드론 2가 간 거리' + str(dron_gps_2))
        # print('남은 운행 시간 :' + str(timer_2))
        yield env.timeout(1)


def dron_3(env) :
    global battery_3,hight_3,inertia_3,dron_gps_3,restricted_area_3
    battery_3 = 600 * 5 #드론 배터리 용량
    use_b_3 = 2300 * 5 # 배터리 사용량
    charge_t_3 = np.random.randint(3,7)/10 * 0.5#충전 구현(태양광)
    timer_3 = (battery_3 + charge_t_3)/use_b_3 * 60 #운행시간(분단위)
    dron_gps_3 = [0,0] #드론 위치(GPS)
    """
    3번 드론 태양광 충전 방식
    """
    while timer_3 > 1 :
        timer_3 = timer_3 - 1
        timer_3 = timer_3 + charge_t_3
        dron_gps_3[0] = dron_gps_3[0] + 10
        # print('드론 3가 간 거리' + str(dron_gps_3))
        # print('남은 배터리 :' + str(timer_3))
        yield env.timeout(1)

#일반 객체 ###################################################################
def dic(x):
    return l[x]

#시작 ###################################################################

print('''
상황 : 일반적인 배터리를 사용하는 드론과 지속적인 래이져 충전을 사용하는 드론과 태양광 충전을 사용하는 드론 비교

태양광 사용이 불가능한 날씨가 좋지 않은 날은 드론 운행 불가
(3초 후 시뮬레이션 시작)
''')

ti.sleep(3)

#시뮬래이션 ###################################################################

env = si.Environment()

i = int(input('반복횟수 입력 >>>'))

for a in range(i) :
    print('일반 드론 - 1번 드론')
    # ti.sleep(1)
    env.process(dron_1(env))
    env.run()

    env = si.Environment()

    print('''
    레이져 무선충전 드론
    (에너지 전송량은 초당 1, 거리에 따른 효율감소 실질적으로 없음) - 2번드론''')
    # ti.sleep(1.2)
    env.process(dron_2(env))
    env.run()

    env = si.Environment()

    print('''
    태양광 충전 드론 
    (초당 0.1에서 0.5의 충전 효율)- 3번드론''')
    # ti.sleep(1.2)
    env.process(dron_3(env))
    env.run()


    print(f'''
    최종 이동 거리
    드론1이 간 거리 : {dron_gps_1}
    드론2가 간 거리 : {dron_gps_2}
    드론3이 간 거리 : {dron_gps_3}

    ''')
    l = {}
    l['1번'] = dron_gps_1[0]
    l['2번'] = dron_gps_2[0]
    l['3번'] = dron_gps_3[0]

    print(l)

    m = max(l.keys(), key=dic)
    key_M.append(m)
    gps_np = np.array([dron_gps_1[0], dron_gps_2[0], dron_gps_3[0]])
    l_np = np.vstack((l_np, gps_np))

# print(l)
# l = pd.DataFrame(l)
# print(l)
np.set_printoptions(threshold=np.inf, linewidth=np.inf)
print(l_np)
print('결과')
print('1번드론', str(key_M.count('1번')), '번')
print('2번드론', str(key_M.count('2번')), '번')
print('3번드론', str(key_M.count('3번')), '번')

ans = input()