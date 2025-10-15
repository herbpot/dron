# dron

Arduino 기반 드론 제어 시스템 및 착륙 시뮬레이션 프로젝트입니다.

## 개요

dron은 Arduino와 MPU6050 센서를 사용한 드론 하드웨어 제어와 Python simpy를 이용한 배터리 성능 및 착륙 시뮬레이션 프로젝트입니다. 실제 하드웨어 제어와 시뮬레이션을 결합하여 드론의 다양한 비행 시나리오를 분석합니다.

## 주요 기능

### 하드웨어 (Arduino)
- **MPU6050 센서**: 6축 관성 측정 (가속도계 + 자이로스코프)
- **시리얼 통신**: PC와 실시간 데이터 송수신
- **모터 제어**: 정방향/역방향/정지
- **온도 측정**: MPU6050 내장 온도 센서
- **실시간 각도/가속도 출력**: X, Y, Z축 데이터

### 시뮬레이션 (Python)
- **배터리 시뮬레이션**: 3가지 충전 방식 비교
- **착륙 시뮬레이션**: 안전 착륙 알고리즘
- **비행 거리 계산**: 배터리 수명 기반

## 기술 스택

- **Arduino C++** - 펌웨어
- **MPU6050** - 6축 IMU 센서
- **Python 3.x** - 시뮬레이션
- **SimPy** - 이산 사건 시뮬레이션
- **numpy** - 수치 계산

## 프로젝트 구조

```
dron/
├── dron.ino                    # Arduino 펌웨어
├── simmulate_battery.py        # 배터리 시뮬레이션
└── simmulate_landing.py        # 착륙 시뮬레이션
```

## 하드웨어 구성

### 회로 연결

```
Arduino Uno
├── MPU6050 (I2C 통신)
│   ├── VCC → 5V
│   ├── GND → GND
│   ├── SDA → A4 (Arduino Uno)
│   └── SCL → A5 (Arduino Uno)
└── 모터 드라이버
    ├── IN1 → Pin 9  (정방향)
    ├── IN2 → Pin 6  (역방향)
    ├── IN3 → Pin 10
    └── IN4 → Pin 11
```

## 설치 및 실행

### Arduino 설정

1. **Arduino IDE 설치**

2. **라이브러리 설치**
   - 스케치 → 라이브러리 포함 → 라이브러리 관리
   - `Wire` (기본 라이브러리)

3. **펌웨어 업로드**
```
1. dron.ino 열기
2. 보드: Arduino Uno
3. 포트 선택
4. 업로드
```

### Python 설정

```bash
pip install simpy numpy
```

## 사용 방법

### 1. 드론 제어 (시리얼 통신)

**시리얼 모니터 열기:**
- 도구 → 시리얼 모니터
- Baud rate: 9600

**명령어:**
- `1` - 모터 정방향 (1초)
- `2` - 모터 역방향 (1초)
- `3` - 모터 정지 (1초)

**센서 데이터 출력:**
```
AcX = 1024 | AcY = 2048 | AcZ = 16384 | Tmp = 36.53 | GyX = 12 | GyY = 34 | GyZ = 56
```

### 2. 배터리 시뮬레이션

```bash
python simmulate_battery.py
반복횟수 입력 >>> 100
```

**드론 종류:**
1. **일반 배터리 드론**: 3100 mAh
2. **레이저 충전 드론**: 3100 mAh + 지속 충전
3. **태양광 충전 드론**: 3000 mAh + 가변 충전

**결과:**
```
결과
1번드론 8 번
2번드론 87 번
3번드론 5 번
```

### 3. 착륙 시뮬레이션

```bash
python simmulate_landing.py
```

착륙 알고리즘을 시뮬레이션하여 안전한 착륙 경로를 계산합니다.

## 핵심 코드 구현

### Arduino - MPU6050 초기화

```cpp
#include<Wire.h>
const int MPU_addr = 0x68;  // I2C 주소
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;

void setup() {
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 레지스터
  Wire.write(0);     // 0으로 설정 (웨이크업)
  Wire.endTransmission(true);
  Serial.begin(9600);

  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
}
```

### Arduino - 센서 데이터 읽기

```cpp
void loop() {
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // ACCEL_XOUT_H 레지스터
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr, 14, true);  // 14 바이트 요청

  // 가속도 데이터
  AcX = Wire.read() << 8 | Wire.read();
  AcY = Wire.read() << 8 | Wire.read();
  AcZ = Wire.read() << 8 | Wire.read();

  // 온도 데이터
  Tmp = Wire.read() << 8 | Wire.read();

  // 자이로 데이터
  GyX = Wire.read() << 8 | Wire.read();
  GyY = Wire.read() << 8 | Wire.read();
  GyZ = Wire.read() << 8 | Wire.read();

  // 온도 변환: Tmp/340.00 + 36.53
  Serial.print("Tmp = ");
  Serial.print(Tmp / 340.00 + 36.53);

  delay(333);
}
```

### Arduino - 모터 제어

```cpp
if(Serial.available() > 0) {
  read1 = Serial.parseInt();
}

if(read1 == 1) {
  digitalWrite(in1, HIGH);  // 정방향
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  delay(1000);
}
if(read1 == 2) {
  digitalWrite(in1, LOW);  // 역방향
  digitalWrite(in2, HIGH);
}
if(read1 == 3) {
  digitalWrite(in1, LOW);  // 정지
  digitalWrite(in2, LOW);
  delay(1000);
}
```

### Python - 배터리 시뮬레이션

```python
import simpy as si
import numpy as np

def dron_1(env):
    """일반 배터리 드론"""
    battery_1 = 620 * 5  # 3100 mAh
    dron_gps_1 = [0, 0]
    use_b_1 = 2300 * 5
    timer_1 = battery_1 / use_b_1 * 60

    while timer_1 > 1:
        timer_1 = timer_1 - 1
        dron_gps_1[0] = dron_gps_1[0] + 10
        yield env.timeout(1)

# 환경 생성 및 실행
env = si.Environment()
env.process(dron_1(env))
env.run()
```

## MPU6050 센서 데이터

### 가속도 데이터 (AcX, AcY, AcZ)

- **범위**: ±2g, ±4g, ±8g, ±16g (설정 가능)
- **단위**: LSB (Least Significant Bit)
- **사용**: 기울기, 진동, 충격 감지

### 자이로 데이터 (GyX, GyY, GyZ)

- **범위**: ±250°/s, ±500°/s, ±1000°/s, ±2000°/s
- **단위**: °/s (degrees per second)
- **사용**: 회전 속도, 각속도 측정

### 온도 데이터 (Tmp)

- **공식**: `Temperature = Tmp/340.00 + 36.53`
- **단위**: °C (섭씨)
- **정확도**: ±1°C

## 센서 데이터 해석

### 수평 상태

```
AcX ≈ 0
AcY ≈ 0
AcZ ≈ 16384 (1g)
```

### 45도 기울임 (X축)

```
AcX ≈ 11585 (0.707g)
AcY ≈ 0
AcZ ≈ 11585 (0.707g)
```

## 시뮬레이션 결과

### 배터리 비교 (100회 실행)

| 드론 종류 | 평균 비행 거리 | 우승 횟수 |
|-----------|---------------|-----------|
| 일반 배터리 | 162m | 8회 |
| 레이저 충전 | 무한 | 87회 |
| 태양광 충전 | 180m | 5회 |

**결론**: 레이저 무선충전이 가장 효율적

## 캘리브레이션

### 오프셋 조정

```cpp
// 평평한 곳에 놓고 측정
int16_t ax_offset = 0;
int16_t ay_offset = 0;
int16_t az_offset = 16384;  // 1g

AcX_calibrated = AcX - ax_offset;
AcY_calibrated = AcY - ay_offset;
AcZ_calibrated = AcZ - az_offset;
```

## 트러블슈팅

### MPU6050 연결 실패

```
I2C device not found
```

해결:
- VCC, GND 연결 확인
- SDA, SCL 연결 확인 (A4, A5)
- I2C 스캐너 실행하여 주소 확인

### 데이터 값이 이상함

```
AcX = -1 | AcY = -1 | AcZ = -1
```

해결:
- 센서 초기화 실패
- `Wire.beginTransmission()`에서 오류
- 센서 불량 가능성

### 모터가 작동하지 않음

- 모터 드라이버 전원 확인
- PWM 핀 사용 여부 확인
- 모터 드라이버 연결 확인

## 개선 방향

- [ ] PID 제어 알고리즘
- [ ] 칼만 필터 (센서 노이즈 제거)
- [ ] Complementary Filter (각도 계산)
- [ ] 무선 조종 (RF 모듈)
- [ ] 고도 유지 (기압 센서)
- [ ] FPV 카메라 스트리밍

## PID 제어 예시

```cpp
float kp = 1.0, ki = 0.1, kd = 0.05;
float error, prev_error = 0, integral = 0;

void pidControl(float target, float current) {
  error = target - current;
  integral += error;
  float derivative = error - prev_error;

  float output = kp * error + ki * integral + kd * derivative;
  prev_error = error;

  // output을 모터에 적용
  analogWrite(motorPin, constrain(output, 0, 255));
}
```

## 참고 자료

- [MPU6050 레지스터 맵](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf)
- [SimPy 문서](https://simpy.readthedocs.io/)
- [드론 물리학](https://www.youtube.com/watch?v=FmS4_FJ4Fmo)

## 라이선스

교육 목적으로 작성된 프로젝트입니다.
