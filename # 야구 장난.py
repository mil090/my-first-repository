# 야구 장난
import random
import numpy as np
from math import isclose
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# 1. 기록 측정 프로그램
import random
def batterStats(pa=500):
    ab=0
    hit=0
    single=0
    double=0
    triple=0
    hr=0
    bb=0
    hbp=0
    so=0
    gdp=0
    sac=0
    sf=0
    for _ in range(pa):
        a=random.uniform(0, 80)
        if a<12:
            print('삼진')
            so+=1
            ab+=1
        elif a<27:
            print('땅볼')
            ab+=1
        elif a<42:
            print('뜬공')
            ab+=1
        elif a<45:
            print('직선타')
            ab+=1
        elif a<50:
            print('병살타')
            gdp+=1
            ab+=1
        elif a<56:
            print('볼넷')
            bb+=1
        elif a<58:
            print('몸에 맞는 공')
            hbp+=1
        elif a<66:
            print('1루타')
            ab+=1
            hit+=1
            single+=1
        elif a<70.8:
            print('2루타')
            ab+=1
            hit+=1
            double+=1
        elif a<71.3:
            print('3루타')
            ab+=1
            hit+=1
            triple+=1
        elif a<74:
            print('홈런')
            ab+=1
            hit+=1
            hr+=1
        elif a<77:
            print('희생번트')
            sac+=1
        else:
            print('희생플라이')
            sf+=1
    print(f'{ab}타수 {hit}안타 2루타 {double} 3루타 {triple} {hr}홈런 {bb}볼넷 {hbp}사구 {so}삼진 {sac}희생번트 {sf}희생플라이')
    avg=round(hit/ab, 3)
    obp=round((hit+bb+hbp)/(ab+bb+hbp+sf), 3)
    slg=round((single*1+double*2+triple*3+hr*4)/ab, 3)
    ops=round(obp+slg, 3)
    print(f'타율: {avg} 출루율: {obp}, 장타율: {slg}, OPS: {ops}')
batterStats(600)

# 2. 타석 프로그램
# 투구별 결과: 스트라이크, 헛스윙, 파울, 볼, 타격, 몸에 맞는 볼
# 타격 결과
# 아웃: 땅볼, 뜬공, 직선타, 병살타
# 안타: 1루타, 2루타, 3루타, 홈런
# 희생타: 희생번트, 희생플라이
# 투구 결과
# 삼진, 볼넷, 몸에 맞는 볼
import numpy as np
def batting(batterName):
    ball=0
    strike=0
    pitches=0
    pitch_results=['스트라이크', '헛스윙', '파울', '볼', '타격']
    pitch_weights=[0.1, 0.1, 0.2, 0.3, 0.3]
    while True:
        pitches+=1
        pitch_result=np.random.choice(pitch_results, p=pitch_weights)
        if pitch_result=='스트라이크' or pitch_result=='헛스윙':
            print(f'{pitches}구 {pitch_result}')
            strike+=1
            if strike==3:
                print(f'{batterName}: 삼진 아웃')
                break
        elif pitch_result=='파울':
            print(f'{pitches}구 {pitch_result}')
            if strike<2:
                strike+=1
        elif pitch_result=='볼':
            print(f'{pitches}구 {pitch_result}')
            ball+=1
            ball_list=['볼', '몸에 맞는 볼']
            ball_weight=[0.9, 0.1]
            blnhbp=random.choices(ball_list, ball_weight)
            if blnhbp==['몸에 맞는 볼']:
                print(f'{batterName}: 몸에 맞는 볼')
                break
            elif ball==4:
                print(f'{batterName}: 볼넷')
                break
        elif pitch_result=='타격':
            batting_results=['땅볼', '뜬공', '직선타', '병살타', 
                             '1루타', '2루타', '3루타', '홈런',
                             '희생번트', '희생플라이']
            batting_result=random.choice(batting_results)
# 쓰리 번트 없이
            if strike==2 and batting_result=='희생번트':
                pitches-=1
                continue
            print(f'{pitches}구 {pitch_result}')
            print(f'{batterName}: {batting_result}')
            break
batting('윤동희')


# 3. 홈런 방향 정하기
def hrDirection(batterName, hand='R'):
    directionList=['좌익수', '좌중간', '중견수', '우중간', '우익수']
    if hand=='R':
        directionWeight=[0.45, 0.45, 1/30, 1/30, 1/30]
    elif hand=='L':
        directionWeight=[1/30, 1/30, 1/30, 0.45, 0.45]
    else:
        return None
    direction=np.random.choice(directionList, p=directionWeight)
    print(f'{batterName}: {direction} 뒤 홈런')
hrDirection('최형우', 'L')

# 4. 주자 없을 때 타구별 세부 결과 정하기
# 4-1. 땅볼
# 투수 땅볼, 포수 땅볼, 1루수 땅볼, 2루수 땅불, 3루수 땅볼, 유격수 땅볼
# 투수 땅볼 아웃 (투수->1루수 송구아웃)
# 포수 땅볼 아웃 (포수->1루수 송구아웃)
# 1루수 땅볼 아웃 (1루수->투수 1루 터치아웃)
# 1루수 땅볼 아웃 (1루수 1루 터치아웃)
# 2루수 땅볼 아웃 (2루수->1루수 송구아웃)
# 3루수 땅볼 아웃 (3루수->1루수 송구아웃)
# 유격수 땅볼 아웃 (유격수->1루수 송구아웃)
from math import isclose
def groundBall_noRunner(batterName, left=1/3, mid=1/3, right=1/3):
# 타구 비율
# 3루수 쪽: 2/3*left
# 유격수 쪽: 1/3*left+1/2*mid
# 2루수 쪽: 1/2*mid+1/3*right
# 1루수 쪽: 2/3*right
# 투수 쪽: (1-left-mid-right)*0.9
# 포수 쪽: (1-left-mid-right)*0.1
    rate_3B=(2/3*left)*0.9
    rate_SS=(1/3*left+1/2*mid)*0.9
    rate_2B=(1/2*mid+1/3*right)*0.9
    rate_1B=(2/3*right)*0.9
    rate_P=(1-rate_1B-rate_2B-rate_3B-rate_SS)*0.9
    rate_C=(1-rate_1B-rate_2B-rate_3B-rate_SS)*0.1
    direction_weight=[rate_P, rate_C, rate_1B, 
                      rate_2B, rate_3B, rate_SS]
    direction_list=['투수', '포수', '1루수', '2루수', '3루수', '유격수']
    direction=np.random.choice(direction_list, p=direction_weight)
    if direction=='1루수':
        rv_1B=random.uniform(0, 1)
        if rv_1B<=0.7:
            print(f'{batterName}: {direction} 땅볼 아웃 ({direction} 1루 터치아웃)')
        else:
            print(f'{batterName}: {direction} 땅볼 아웃 ({direction}->투수 1루 터치아웃)')
    else:
        print(f'{batterName}: {direction} 땅볼 아웃 ({direction}->1루수 송구아웃)')
groundBall_noRunner('전준우', 0.6, 0.2, 0.2)
groundBall_noRunner('나승엽', 0.15, 0.2, 0.65)
groundBall_noRunner('레이예스')

# 4-2. 뜬공
# 외야 플라이(70%)
# 좌익수 파울플라이, 좌익수 플라이, 중견수 플라이, 우익수 플라이, 우익수 파울플라이
# 내야 플라이(30%)
# 3루수 파울플라이, 3루수 플라이, 유격수 플라이, 2루수 플라이, 1루수 플라이,
# 1루수 파울플라이, 포수 플라이, 포수 파울플라이
def flyBall_noRunner(batterName, left=1/3, mid=1/3, right=1/3):
    out_or_in=random.random()
# 외야 플라이 비율
# 좌파플: left*0.2
# 좌플: left*0.5
# 중플: left*0.3+mid+right*0.3
# 우플: right*0.5
# 우파플: right*0.2
    if out_or_in<=0.7:
        rate_LF_foul=left*0.2
        rate_LF=left*0.5
        rate_CF=left*0.3+mid+right*0.3
        rate_RF=right*0.5
        rate_RF_foul=right*0.2
        direction_list=['좌익수 파울', '좌익수', '중견수', '우익수', 
                      '우익수 파울']
        direction_weight=[rate_LF_foul, rate_LF, rate_CF, rate_RF, 
                          rate_RF_foul]
        direction=np.random.choice(direction_list, p=direction_weight)
        print(f'{batterName}: {direction} 플라이 아웃')
# 내야 플라이는 잘 맞은 타구가 아니므로 방향을 타자의 성향에 관계없이 나오도록 설정
# 투수 플라이 아웃은 제외
    else:
        direction_list=['3루수 파울', '3루수', '유격수', '2루수', '1루수',
                        '1루수 파울', '포수', '포수 파울']
        direction=random.choice(direction_list)
        print(f'{batterName}: {direction} 플라이 아웃')
flyBall_noRunner('전준우', 0.6, 0.2, 0.2)

# 4-3. 직선타
# 내야 직선타만 표시
# 직선타는 주자 진루 확률이 거의 없으므로 주자 있을 때와 없을 때 동일하게
# 직선타 병살은 주자 시스템을 만든 후 구현하기
# 투수, 1루수, 2루수, 3루수, 유격수
# 비율: 0.08, 0.23, 0.23, 0.23, 0.23
def lineDrive(batterName):
    direction_list=['투수', '1루수', '2루수', '3루수', '유격수']
    direction_weight=[0.08, 0.23, 0.23, 0.23, 0.23]
    direction=np.random.choice(direction_list, p=direction_weight)
    print(f'{batterName}: {direction} 라인드라이브 아웃')
lineDrive('정훈')

# 4-4. 1루타
# 좌익수 앞, 좌중간, 중견수 앞, 우중간, 우익수 앞
# 방향 비율
# 좌익수 앞: left*0.7
# 좌중간: left*0.3+mid*0.15
# 중견수 앞: mid*0.7
# 우중간: mid*0.15+right*0.3
# 우익수 앞: right*0.7
def single_noRunner(batterName, left=1/3, mid=1/3, right=1/3):
    direction_list=['좌익수 앞', '좌중간', '중견수 앞', '우중간', 
                    '우익수 앞']
    rate_LF=left*0.7
    rate_LCF=left*0.3+mid*0.15
    rate_CF=mid*0.7
    rate_RCF=mid*0.15+right*0.3
    rate_RF=right*0.7
    direction_weight=[rate_LF, rate_LCF, rate_CF, rate_RCF, rate_RF]
    direction=np.random.choice(direction_list, p=direction_weight)
    print(f'{batterName}: {direction} 1루타')
single_noRunner('손호영', 0.7, 0.2, 0.1)

# 4-5. 2루타
# 좌익수 왼쪽, 좌익수 뒤, 좌중간, 중견수 뒤, 우중간, 우익수 뒤, 우익수 오른쪽
# 방향 비율
# 좌익수 왼쪽: left*0.4
# 좌익수 뒤: left*0.4
# 좌중간: left*0.2+mid*0.3
# 중견수 뒤: mid*0.4
# 우중간: mid*0.3+right*0.2
# 우익수 뒤: right*0.4
# 우익수 오른쪽: right*0.4
def double_noRunner(batterName, left=1/3, mid=1/3, right=1/3):
    direction_list=['좌익수 왼쪽', '좌익수 뒤', '좌중간', '중견수 뒤',
                    '우중간', '우익수 뒤', '우익수 오른쪽']
    direction_weight=[left*0.4, left*0.4, left*0.2+mid*0.3,
                      mid*0.4, mid*0.3+right*0.2, right*0.4,
                      right*0.4]
    direction=np.random.choice(direction_list, p=direction_weight)
    print(f'{batterName}: {direction} 2루타')
double_noRunner('유강남', 0.65, 0.2, 0.15)

# 4-6. 3루타
# 3루타 방향 비율은 좌우타자에 관계없이 우익수 쪽 비율이 높음
# 좌익수 왼쪽, 좌익수 뒤, 좌중간, 중견수 뒤, 우중간, 우익수 뒤, 우익수 오른쪽
def triple_noRunner(batterName):
    direction_list=['좌익수 왼쪽', '좌익수 뒤', '좌중간', '중견수 뒤',
                    '우중간', '우익수 뒤', '우익수 오른쪽']
    direction_weight=[0.05, 0.05, 0.05, 0.07, 0.26, 0.26, 0.26]
    direction=np.random.choice(direction_list, p=direction_weight)
    print(f'{batterName}: {direction} 3루타')
triple_noRunner('황성빈')

# 4-7. 홈런
# 매우 낮은 확률로 그라운드 홈런 포함
# 좌익수, 좌중간, 중견수, 우중간, 우익수
# 방향 비율
# 좌익수: left*0.7
# 좌중간: left*0.3+mid*0.3
# 중견수: mid*0.4
# 우중간: mid*0.3+right*0.3
# 우익수: right*0.7
# 홈런 비거리: 105, 110, 115, 120, 125, 130, 135, 140, 145
# 당겨 친 홈런: 110~145
# 중월 홈런: 125~145
# 밀어 친 홈런: 105~120
def hr_noRunner(batterName, left=1/3, mid=1/3, right=1/3, hand='R'):
    direction_list=['좌익수', '좌중간', '중견수', '우중간', '우익수']
    rate_LF=left*0.7
    rate_LCF=left*0.3+mid*0.3
    rate_CF=mid*0.4
    rate_RCF=mid*0.3+right*0.3
    rate_RF=right*0.7
    direction_weight=[rate_LF, rate_LCF, rate_CF, rate_RCF, rate_RF]
    direction=np.random.choice(direction_list, p=direction_weight)
    rv_groundHR=random.random()
    if rv_groundHR<=0.001:
        print(f'{batterName}: {direction} 그라운드 홈런')
    else:
        distance_list=[105, 110, 115, 120, 125, 130, 135, 140, 145]
        if hand=='R':
            if direction==direction_list[0]:
                distance=random.choice(distance_list[1:])
            elif direction==direction_list[1]:
                distance=random.choice(distance_list[3:])
            elif direction==direction_list[2]:
                distance=random.choice(distance_list[4:])
            elif direction==direction_list[3]:
                distance=random.choice(distance_list[3:6])
            else:
                distance=random.choice(distance_list[:4])
            print(f'{batterName}: {direction} 뒤 홈런 (홈런거리: {distance}m)')
        elif hand=='L':
            if direction==direction_list[4]:
                distance=random.choice(distance_list[1:])
            elif direction==direction_list[3]:
                distance=random.choice(distance_list[3:])
            elif direction==direction_list[2]:
                distance=random.choice(distance_list[4:])
            elif direction==direction_list[1]:
                distance=random.choice(distance_list[3:6])
            else:
                distance=random.choice(distance_list[:4])
            print(f'{batterName}: {direction} 뒤 홈런 (홈런거리: {distance}m)')
        else:
            print('Invalid input: variable \'hand\' should be \'L\' or \'R\'')
hr_noRunner('한동희', 0.8, 0.1, 0.1, 'R')
hr_noRunner('나승엽', 0.1, 0.2, 0.7, 'L')

# 5. 주자 배치 프로그램
# 리스트를 이용
bases=[None, None, None]
# 왼쪽부터 3루, 2루, 1루
# 타자가 출루에 성공하여 주자가 되면 해당 위치의 값을 타자의 이름으로 변경
single_noRunner('황성빈', 0.5, 0.25, 0.25)
bases[-1]='황성빈'
print(bases)

# 6. 베이스 프로그램
class Bases:
    def __init__(self):
        self.bases=[None, None, None]
# 왼쪽부터 3루, 2루, 1루
# 주자가 있을 때는 그 주자의 이름이 들어가고, 없을 때는 None이 들어감
# 각 베이스에 주자가 있는지 확인하는 함수
    def is_1B_loaded(self):
        return self.bases[-1] is not None
    def is_2B_loaded(self):
        return self.bases[-2] is not None
    def is_3B_loaded(self):
        return self.bases[-3] is not None
# 만루인지 확인하는 함수
    def is_loaded(self):
        return None not in self.bases
# 모든 베이스가 비었는지(주자가 없는지) 확인하는 함수
    def is_empty(self):
        return all(x is None for x in self.bases)
# self.base 내의 모든 요소가 None이어야 True를 반환
# 이외의 경우에는 False를 반환

# 각 베이스에 있는 주자의 이름을 출력하는 함수
    def print_1B_runner(self):
        if not self.is_1B_loaded():
            print('1루 주자:')
        else:
            print(f'1루 주자: {self.bases[-1]}')
    def print_2B_runner(self):
        if not self.is_2B_loaded():
            print('2루 주자:')
        else:
            print(f'2루 주자: {self.bases[-2]}')
    def print_3B_runner(self):
        if not self.is_3B_loaded():
            print('3루 주자:')
        else:
            print(f'3루 주자: {self.bases[-3]}')
# 현재 주자 상황을 출력하는 함수
    def print_runners(self):
        self.print_3B_runner()
        self.print_2B_runner()
        self.print_1B_runner()
# 각 베이스의 주자를 설정하는 함수
    def set_1B_runner(self, runnerName=None):
        self.bases[-1]=runnerName
    def set_2B_runner(self, runnerName=None):
        self.bases[-2]=runnerName
    def set_3B_runner(self, runnerName=None):
        self.bases[-3]=runnerName
# 현재 주자가 있는 위치를 출력하는 함수
# 없음, 1루, 2루, 3루, 12루, 13루, 23루, 만루
    def print_status(self):
        if self.is_empty():
            print('주자 없음')
        elif self.is_loaded():
            print('주자 만루')
        elif self.is_1B_loaded():
            if (not self.is_2B_loaded()) and (not self.is_3B_loaded()):
                print('주자 1루')
            elif self.is_2B_loaded():
                print('주자 1, 2루')
            else:
                print('주자 1, 3루')
        elif self.is_2B_loaded():
            if self.is_3B_loaded():
                print('주자 2, 3루')
            else:
                print('주자 2루')
        else:
            print('주자 3루')
# 득점권 상황(2, 3루에 주자 있음)인지 확인하는 함수
    def is_scoring_position(self):
        return self.is_2B_loaded() or self.is_3B_loaded()

base1=Bases()    
base1.bases
base1.is_empty()
base1.print_runners()
base1.set_3B_runner('황성빈')
base1.set_2B_runner('고승민')
base1.print_2B_runner()
base1.is_loaded()
base1.is_empty()
base1.set_1B_runner('레이예스')
base1.is_1B_loaded()
base1.is_loaded()
base1.print_runners()
base1.set_1B_runner()
base1.print_runners()
base1.print_status()
base1.is_scoring_position()

# 7. 라인업 프로그램
# 각 포지션별 선수 이름을 저장, 변경 및 출력
# 수비 위치 및 라인업을 출력
class LineUp:
# 클래스를 생성할 때 각 포지션을 생성하고 None으로 초기화
# 각 타순별 선수를 저장할 리스트를 생성(투수까지 포함해서 10칸)
    def __init__(self):
        self.pitcher=None
        self.catcher=None
        self.first=None
        self.second=None
        self.third=None
        self.shortstop=None
        self.leftfielder=None
        self.centerfielder=None
        self.rightfielder=None
        self.designatedhitter=None
        self.pinchhitter=None
        self.pinchrunner=None
        self.lineup_list=[None for _ in range(10)]
        self.lineup_list[-1]=self.pitcher
# 각 포지션 선수명과 포지션 약칭을 key:value로 저장할 딕셔너리
        self.name_position_dict={}
        self.position_name_dict={}
# 각 포지션별 선수는 한 명씩만 있어야 함. 이렇게 관리하기 위한 함수를 구현
    def unique_position(self, name, position):
# 만약 해당 포지션을 가진 선수가 이미 있었다면 이를 삭제하고 덮어써야 함
        if position in self.position_name_dict:
            old_name=self.position_name_dict[position]
            self.name_position_dict.pop(old_name, None)
        if name in self.name_position_dict:
            old_position=self.name_position_dict[name]
            self.position_name_dict.pop(old_position, None)
        self.name_position_dict[name]=position
        self.position_name_dict[position]=name

# 각 포지션별 선수의 이름을 출력하는 함수
    def print_pitcher(self):
        print(self.pitcher)
    def print_catcher(self):
        print(self.catcher)
    def print_first(self):
        print(self.first)
    def print_second(self):
        print(self.second)
    def print_third(self):
        print(self.third)
    def print_shortstop(self):
        print(self.shortstop)
    def print_leftfielder(self):
        print(self.leftfielder)
    def print_centerfielder(self):
        print(self.centerfielder)
    def print_rightfielder(self):
        print(self.rightfielder)
    def print_designatedhitter(self):
        print(self.designatedhitter)
# 전체 포지션별 선수를 출력하는 함수
    def print_all_fielders(self):
        print(f'투수 {self.pitcher}')
        print(f'포수 {self.catcher}')
        print(f'1루수 {self.first}')
        print(f'2루수 {self.second}')
        print(f'3루수 {self.third}')
        print(f'유격수 {self.shortstop}')
        print(f'좌익수 {self.leftfielder}')
        print(f'중견수 {self.centerfielder}')
        print(f'우익수 {self.rightfielder}')
        print(f'지명타자 {self.designatedhitter}')
# 각 포지션별 선수를 설정하는 함수
# 포지션에 선수 이름을 지정한 후, 선수이름:포지션 약칭 쌍을 self.position_dict
# 에 추가. 이때 이미 해당 포지션의 선수가 있는 상황이라면 그 선수는 삭제
    def set_pitcher(self, name):
        self.pitcher=name
        self.lineup_list[-1]=self.pitcher
        self.unique_position(self.pitcher, 'P')
    def set_catcher(self, name):
        self.catcher=name
        self.unique_position(self.catcher, 'C')
    def set_first(self, name):
        self.first=name
        self.unique_position(self.first, '1B')
    def set_second(self, name):
        self.second=name
        self.unique_position(self.second, '2B')
    def set_third(self, name):
        self.third=name
        self.unique_position(self.third, '3B')
    def set_shortstop(self, name):
        self.shortstop=name
        self.unique_position(self.shortstop, 'SS')
    def set_leftfielder(self, name):
        self.leftfielder=name
        self.unique_position(self.leftfielder, 'LF')
    def set_centerfielder(self, name):
        self.centerfielder=name
        self.unique_position(self.centerfielder, 'CF')
    def set_rightfielder(self, name):
        self.rightfielder=name
        self.unique_position(self.rightfielder, 'RF')
    def set_designatedhitter(self, name):
        self.designatedhitter=name
        self.unique_position(self.designatedhitter, 'DH')
    def set_pinchhitter(self, name):
        self.pinchhitter=name
    def set_pinchrunner(self, name):
        self.pinchrunner=name
# 타순을 설정하는 함수
    def set_batting_order(self, order, name=None):
# 투수 자리에는 못 넣도록 함
        if order==10:
            print('Cannot change pitcher\'s order')
        else:
            self.lineup_list[order-1]=name
# 라인업 구성이 완료되었는지 검사하는 함수
    def is_complete_lineup(self):
        return None not in self.lineup_list
# 완성된 라인업을 출력하는 함수
# 라인업이 미완성이면 완성하라는 메시지를 출력
    def print_batting_order(self):
        if not self.is_complete_lineup():
            print('Complete lineup list first')
            empty_list=[]
            for num in range(len(self.lineup_list)-1):
                if self.lineup_list[num]==None:
                    empty_list.append(num+1)
            print(f'Empty batter nums={empty_list}')
            if self.lineup_list[-1]==None:
                print('No pitcher in lineup')
        else:
            for i in range(len(self.lineup_list)-1):
                print(f'{i+1}번 타자 {self.lineup_list[i]} {self.name_position_dict[self.lineup_list[i]]}')
            print(f'선발 투수 {self.pitcher} {self.name_position_dict[self.pitcher]}')

lineup1=LineUp()
lineup1.print_pitcher()
lineup1.set_pitcher('박세웅')
lineup1.set_catcher('유강남')
lineup1.set_first('나승엽')
lineup1.set_second('고승민')
lineup1.set_third('손호영')
lineup1.set_shortstop('전민재')
lineup1.set_leftfielder('레이예스')
lineup1.set_centerfielder('황성빈')
lineup1.set_rightfielder('윤동희')
lineup1.set_designatedhitter('전준우')
lineup1.set_designatedhitter('레이예스')
lineup1.name_position_dict
lineup1.position_name_dict
lineup1.lineup_list
lineup1.print_all_fielders()
lineup1.print_batting_order()
lineup1.set_batting_order(1, lineup1.centerfielder)
lineup1.lineup_list[0]
lineup1.set_batting_order(2, lineup1.second)
lineup1.lineup_list[1]
lineup1.set_batting_order(3, lineup1.leftfielder)
lineup1.lineup_list[2]
lineup1.set_batting_order(4, lineup1.designatedhitter)
lineup1.lineup_list[3]
lineup1.set_batting_order(5, lineup1.rightfielder)
lineup1.lineup_list[4]
lineup1.set_batting_order(6, lineup1.first)
lineup1.lineup_list[5]
lineup1.set_batting_order(7, lineup1.third)
lineup1.lineup_list[6]
lineup1.set_batting_order(8, lineup1.catcher)
lineup1.lineup_list[7]
lineup1.set_batting_order(9, lineup1.shortstop)
lineup1.lineup_list[8]
lineup1.lineup_list
lineup1.print_all_fielders()
lineup1.print_batting_order()

# 8. 타자 프로필 프로그램
# 출신 관련 정보
# 이름, 생년월일, 출신학교(고교, 대학만), 포지션(포/내/외), 현재 소속팀, 투타
# 타격 관련 기록
# 경기, 타석, 타수, 안타, 2루타, 3루타, 홈런, 루타, 타점, 득점, 희생번트,
# 희생플라이, 볼넷, 고의4구, 사구, 삼진, 병살타, 타율, 출루율, 장타율, OPS, 
# 멀티히트, 득점권 타율, 대타 타율
# 수비 관련 기록
# 선발 경기, 실책
# 주루 관련 기록
# 도루 시도, 도루 성공, 도루 실패
# (포수 한정) 도루 허용, 도루 저지, 도루 저지율, 포일
# 소속팀과 포지션을 제한
import matplotlib.pyplot as plt
class BatterProfile:
    team_set={'LG', '한화', 'SSG', '삼성', 'NC', 'KT', '롯데',
              'KIA', '두산', '키움'}
    position_set={'포수', '내야수', '외야수'}
    hand_set={'R', 'L', 'S'}
    def __init__(self, name, team, position, pitch_hand='R', bat_hand='R'):
        if team not in self.team_set:
            raise ValueError(f'팀명은 {self.team_set} 중에서 입력해야 합니다.')
        if position not in self.position_set:
            raise ValueError(f'포지션명은 {self.position_set} 중에서 입력해야 합니다.')
        if pitch_hand not in self.hand_set or bat_hand not in self.hand_set:
            raise ValueError(f'투타는 {self.hand_set} 중에서 입력해야 합니다.')
# 능력치 설정이 정상적으로 완료되어야 기록지가 생성됨
        self.labels, self.values=self.set_status()
# self.labels는 능력치 이름, self.values는 각 능력치별 수치를 담은 리스트
# 프로필이 생성되면 이들을 이용하여 레이더 차트로 나타내자
        self.name=name
        self.team=team
        self.position=position
        if pitch_hand=='R':
            self.pitch_hand='우투'
        elif pitch_hand=='S':
            self.pitch_hand='양투'
        else:
            self.pitch_hand='좌투'
        if bat_hand=='R':
            self.bat_hand='우타'
        elif bat_hand=='S':
            self.bat_hand='양타'
        else:
            self.bat_hand='좌타'
        self.game=0
        self.game_starting=0
# 타격 지표
        self.pa=0 # 타석
        self.ab=0 # 타수
        self.hit=0 # 안타
        self.double=0 # 2루타
        self.triple=0 # 3루타
        self.hr=0 # 홈런
        self.totalbase=0 # 루타
        self.rbi=0 # 타점
        self.run=0 # 득점
        self.sac=0 # 희생번트
        self.sf=0 # 희생플라이
        self.walk=0 # 볼넷
        self.ibb=0 # 고의4구
        self.hbp=0 # 사구
        self.so=0 # 삼진
        self.gdp=0 # 병살타
        self.avg=0 # 타율
        self.obp=0 # 출루율
        self.slg=0 # 장타율
        self.ops=0 # OPS
        self.mh=0 # 멀티히트
        self.ab_isp=0 # 득점권 타수
        self.pa_hit=0 # 득점권 안타
        self.risp=0 # 득점권 타율
        self.ph_ab=0 # 대타 타수
        self.ph_hit=0 # 대타 안타
        self.phba=0 # 대타 타율
# 수비 지표
        self.error=0 # 실책
# 주루 지표
        self.attempt=0 # 도루 시도
        self.steal=0 # 도루 성공
        self.caught=0 # 도루 실패
# 포수 전용 지표
        if self.position=='포수':
            self.sb=0
            self.cs=0
            self.cs_rate=0
            self.pb=0
        print(f'Batter {self.name}({self.team}, {self.position}, {self.pitch_hand}{self.bat_hand})\'s profile is created')
        print(f'파워: {self.power}, 주력: {self.speed}, 컨택: {self.contact}, 수비: {self.defense}, 선구안: {self.eye}')
        self.status_chart()

# 타자별 능력치를 설정하는 함수
# 각 능력치는 1~100 사이의 정수 값을 가짐
# 수치가 높을수록 그 부문에서 뛰어난 선수
# 파워: 수치가 높을수록 장타가 나오기 쉬움. 타격 결과가 안타일 때 그 안타가 장타가
# 될 확률에 영향
# 스피드: 수치가 높을수록 도루 성공, 내야 안타가 나오기 쉬움. 출루해 있는 상태에서
# 도루 시도 확률과 그때의 성공 확률, 땅볼 타구 발생 시 내야 안타 확률, 1루에 출루한
# 상태에서 후속 타자의 2루타가 나왔을 때 홈인할 가능성 등에 영향
# 컨택: 수치가 높을수록 헛스윙이 줄어들고 파울과 정타가 나오기 쉬움. 타격 결과가
# 헛스윙이 될 확률에 영향
# 수비: 수치가 높을수록 실책이 나오기 어려움. 외야수의 경우 희생 플라이성 타구에 대한
# 홈 보살 확률에 영향. 포수의 경우 도루 저지 성공 확률에 영향
# 선구안: 수치가 높을수록 타석에서 볼의 비율이 늘어남.

# 먼저 1부터 100까지의 숫자인지 확인하는 함수를 생성
# 1에서 100까지의 정수임이 확인되면 이를 반환
    def is_1_to_100(self, prompt):
        try:
            value=int(input(prompt))
        except:
            raise ValueError('정수를 입력해야 합니다.')
        if not (1<=value<=100):
            raise ValueError(f'능력치 수치로는 1부터 100까지의 정수만 입력할 수 있습니다. 입력된 값: {value}')
        return value
# 능력치 설정 함수
# 정상적으로 1~100의 정수 5개를 입력받으면, 이를 이용해 레이더 차트로 나타내자
    def set_status(self):
        self.power=self.is_1_to_100('이 타자의 파워 수치를 1부터 100까지의 정수로 입력하세요.')
        self.speed=self.is_1_to_100('이 타자의 주력 수치를 1부터 100까지의 정수로 입력하세요.')
        self.contact=self.is_1_to_100('이 타자의 컨택 수치를 1부터 100까지의 정수로 입력하세요.')
        self.defense=self.is_1_to_100('이 타자의 수비 수치를 1부터 100까지의 정수로 입력하세요.')
        self.eye=self.is_1_to_100('이 타자의 선구안 수치를 1부터 100까지의 정수로 입력하세요.')
        labels=['파워', '주력', '컨택', '수비', '선구안']
        values=[self.power, self.speed, self.contact, self.defense,
                self.eye]
        return labels, values
# 기록 출력 함수
    def print_stats(self):
        print(f'{self.name} 시즌 기록')
        print('----------타격 지표----------')
        print(f'경기 수 {self.game}')
        print(f'선발 경기 수 {self.game_starting}')
        print(f'타석 {self.pa}')
        print(f'타수 {self.ab}')
        print(f'안타 {self.hit}')
        print(f'2루타 {self.double}')
        print(f'3루타 {self.triple}')
        print(f'홈런 {self.hr}')
        print(f'루타 {self.totalbase}')
        print(f'타점 {self.rbi}')
        print(f'득점 {self.run}')
        print(f'희생번트 {self.sac}')
        print(f'희생플라이 {self.sf}')
        print(f'볼넷 {self.walk}')
        print(f'고의4구 {self.ibb}')
        print(f'사구 {self.hbp}')
        print(f'삼진 {self.so}')
        print(f'병살타 {self.gdp}')
        print(f'타율 {self.avg}')
        print(f'출루율 {self.obp}')
        print(f'장타율 {self.slg}')
        print(f'OPS {self.ops}')
        print(f'멀티히트 {self.mh}')
        print(f'득점권 타율 {self.risp}')
        print(f'대타 타율 {self.phba}')
        print('----------주루/수비 지표----------')
        print(f'도루 시도 {self.attempt}')
        print(f'도루 성공 {self.steal}')
        print(f'도루 실패 {self.caught}')
        print(f'실책 {self.error}')
        if self.position=='포수':
            print(f'도루 허용 {self.sb}')
            print(f'도루 저지 {self.cs}')
            print(f'도루 저지율 {self.cs_rate}')
# 타자의 능력치를 레이더 차트로 나타내기
    def status_chart(self):
        v=self.values.copy()
        l=self.labels.copy()
        v.append(v[0])
        l.append(l[0])
        fig=go.Figure(go.Scatterpolar(r=v,
                                      theta=l,
                                      fill='toself'))
        fig.update_layout(title=f'{self.name}의 능력치', 
                          polar=dict(radialaxis=dict(visible=True, 
                                                     range=[0, 100])),
                                                     showlegend=False)
        fig.show()

l=['a', 'b', 'c', 'd', 'e', 'a']
r=[80, 55, 70, 40, 65, 80]
f=go.Figure(go.Scatterpolar(r=r, theta=l, fill='toself'))
f.update_layout(
    title='능력치 레이더 차트',
    polar=dict(radialaxis=dict(
        visible=True,
        range=[0, 100])), showlegend=False
)

jjw=BatterProfile('전준우', '롯데', '외야수')
jjw.print_stats()
jjw.status_chart()
jjw.position
ykn=BatterProfile('유강남', '롯데', '포수')
ykn.print_stats()
ykn.position
nsy=BatterProfile('나승엽', '롯데', '내야수', 'R', 'L')
nsy.print_stats()
nsy.position
reyes=BatterProfile('레이예스', '롯데', '외야수', 'R', 'S')
reyes.print_stats()
win_g=BatterProfile('윈지', '롯데', '외야수', 'S', 'S')

# 9. 투수 프로필 프로그램
# 출신 관련 정보
# 이름, 생년월일, 출신학교(고교, 대학만), 보직(선발/불펜), 현재 소속팀, 투타
# 경기, 승, 패, 홀드, 세이브, 이닝, 피안타, 피홈런, 볼넷, 사구, 탈삼진, 실점,
# 자책점, ERA, WHIP, 완투, 완봉, 퀄스, 블론, 보크, 투구수, 상대 타수, 피안타율,
# 피희생번트, 피희생플라이, 폭투, 실책
# 투수의 능력치: 구속, 구위, 제구, 지구력, 수비
# 구속: 수치가 높을수록 헛스윙 확률이 높아짐
# 구위: 수치가 높을수록 헛스윙 확률이 높아지고 정타 확률이 낮아짐. 정타(인플레이 타구)
# 가 나왔을 때 안타 확률과 안타가 되었을 때 장타가 될 확률에 영향
# 제구: 수치가 높을수록 볼의 비율이 감소하고 스트라이크의 비율이 늘어남
# 지구력: 수치가 높을수록 한계 투구수가 증가함. 한계 투구수가 늘어나면 다른 모든 능력치
# 수치가 20% 저하 (한계 투구수: 선발은 int(지구력*1.15), 불펜은 int(지구력*0.3))
# 수비: 수치가 높을수록 실책이 나오기 어려움(투수 땅볼 시)

# 실점, 자책점, 비자책점, 승계주자 실점 구분
# 출루한 주자가 득점하면, 그 주자를 출루시킨 투수의 실점 증가
# 만약 해당 이닝 중 실책이 없었다면, 그때까지 나온 실점은 모두 자책점
# 만약 이닝 진행 중 실책이 한 번이라도 나오면, 이후 그 이닝에서 나온 실점은 모두
# 비자책점으로 처리
class PitcherProfile:
    team_set={'LG', '한화', 'SSG', '삼성', 'NC', 'KT', '롯데',
              'KIA', '두산', '키움'}
    position_set={'선발', '불펜'}
    hand_set={'R', 'L', 'S', 'Rside', 'Lside', 'Sside',
              'Runder', 'Lunder', 'Sunder'}
    def __init__(self, name, team, position, pitch_hand='R', bat_hand='R'):
        if team not in self.team_set:
            raise ValueError(f'팀명은 {self.team_set} 중에서 입력해야 합니다.')
        if position not in self.position_set:
            raise ValueError(f'보직명은 {self.position_set} 중에서 입력해야 합니다.')
        if pitch_hand not in self.hand_set or bat_hand not in self.hand_set:
            raise ValueError(f'투타는 {self.hand_set} 중에서 입력해야 합니다.')
        self.labels, self.values=self.set_status()
        self.name=name
        self.team=team
        self.position=position
        if pitch_hand=='R':
            self.pitch_hand='우투'
        elif pitch_hand=='S':
            self.pitch_hand='양투'
        elif pitch_hand=='L':
            self.pitch_hand='좌투'
        elif pitch_hand=='Rside':
            self.pitch_hand='우사'
        elif pitch_hand=='Sside':
            self.pitch_hand='양사'
        elif pitch_hand=='Lside':
            self.pitch_hand='좌사'
        elif pitch_hand=='Runder':
            self.pitch_hand='우언'
        elif pitch_hand=='Sunder':
            self.pitch_hand='양언'
        else:
            self.pitch_hand='좌언'
        if bat_hand=='R':
            self.bat_hand='우타'
        elif bat_hand=='S':
            self.bat_hand='양타'
        else:
            self.bat_hand='좌타'
        self.game=0 # 경기
# 투구 관련 지표
        self.win=0 # 승
        self.lose=0 # 패
        self.hold=0 # 홀드
        self.save=0 # 세이브
        self.ip=0 # 이닝
        self.hit=0 # 피안타
        self.hr=0 # 피홈런
        self.bb=0 # 볼넷
        self.hbp=0 # 사구
        self.so=0 # 탈삼진
        self.run=0 # 실점
        self.erun=0 # 자책점
        self.era=0 # 평균자책점
        self.whip=0 # 이닝당 출루허용률
        self.cg=0 # 완투
        self.sho=0 # 완봉
        self.qs=0 # 퀄리티 스타트
        self.bsv=0 # 블론세이브
        self.balk=0 # 보크
        self.num_pitch=0 # 투구수
        self.ab=0 # 상대 타수
        self.avg=0 # 피안타율
        self.sac=0 # 피희생번트
        self.sf=0 # 피희생플라이
        self.wp=0 # 폭투
# 한계 투구수는 보직과 지구력에 따라 결정됨
# 선발: int(지구력*1.2), 불펜: int(지구력*0.4)
# 경기 도중 투수가 한계 투구수를 넘어설 경우 그 타자까지만 승부하고 교체 기회 부여
        if self.position=='선발':
            self.limit=int(self.hp*1.2)
        else:
            self.limit=int(self.hp*0.4)
# 수비 관련 지표
        self.error=0 # 실책
        print(f'Pitcher {self.name}({self.team}, {self.position}, {self.pitch_hand}{self.bat_hand})\'s profile is created')
        print(f'구속: {self.speed}, 구위: {self.power}, 제구: {self.command}, 지구력: {self.hp}, 수비: {self.defense}')
        self.status_chart()
        
# 각 능력치 값으로 1부터 100까지의 정수만 입력되도록 제한하는 함수(타자에서와 동일)
    def is_1_to_100(self, prompt):
        try:
            value=int(input(prompt))
        except:
            raise ValueError('정수를 입력해야 합니다.')
        if not (1<=value<=100):
            raise ValueError(f'능력치 수치로는 1부터 100까지의 정수만 입력할 수 있습니다. 입력된 값: {value}')
        return value
# 능력치 설정 함수-투수
    def set_status(self):
        self.speed=self.is_1_to_100('이 투수의 구속 수치를 1부터 100까지의 정수로 입력하세요.')
        self.power=self.is_1_to_100('이 투수의 구위 수치를 1부터 100까지의 정수로 입력하세요.')
        self.command=self.is_1_to_100('이 투수의 제구 수치를 1부터 100까지의 정수로 입력하세요.')
        self.hp=self.is_1_to_100('이 투수의 지구력 수치를 1부터 100까지의 정수로 입력하세요.')
        self.defense=self.is_1_to_100('이 타자의 수비 수치를 1부터 100까지의 정수로 입력하세요.')
        labels=['구속', '구위', '제구', '지구력', '수비']
        values=[self.speed, self.power, self.command, self.hp,
                self.defense]
        return labels, values
# 기록 출력 함수
    def print_stats(self):
        print(f'{self.name} 시즌 기록')
        print('----------투구 지표----------')
        print(f'경기 수 {self.game}')
        print(f'승 {self.win}')
        print(f'패 {self.lose}')
        print(f'홀드 {self.hold}')
        print(f'세이브 {self.save}')
        print(f'이닝 {self.ip}')
        print(f'피안타 {self.hit}')
        print(f'피홈런 {self.hr}')
        print(f'볼넷 {self.bb}')
        print(f'사구 {self.hbp}')
        print(f'탈삼진 {self.so}')
        print(f'실점 {self.run}')
        print(f'자책점 {self.erun}')
        print(f'평균자책점 {self.era}')
        print(f'이닝당 출루허용률(WHIP) {self.whip}')
        print(f'완투 {self.cg}')
        print(f'완봉 {self.sho}')
        print(f'퀄리티 스타트 {self.qs}')
        print(f'블론세이브 {self.bsv}')
        print(f'투구수 {self.num_pitch}')
        print(f'상대 타수 {self.ab}')
        print(f'피안타율 {self.avg}')
        print(f'피희생번트 {self.sac}')
        print(f'피희생플라이 {self.sf}')
        print(f'폭투 {self.wp}')
        print(f'보크 {self.balk}')
        print(f'한계 투구수 {self.limit}')
        print('----------수비 지표----------')
        print(f'실책 {self.error}')
# 투수의 능력치를 레이더 차트로 나타내기
    def status_chart(self):
        v=self.values.copy()
        l=self.labels.copy()
        v.append(v[0])
        l.append(l[0])
        fig=go.Figure(go.Scatterpolar(r=v,
                                      theta=l,
                                      fill='toself'))
        fig.update_layout(title=f'{self.name}의 능력치', 
                          polar=dict(radialaxis=dict(visible=True, 
                                                     range=[0, 100])),
                                                     showlegend=False)
        fig.show()
psw=PitcherProfile('박세웅', '롯데', '선발')
psw.print_stats()
psw.position
kwj=PitcherProfile('김원중', '롯데', '불펜')
kwj.print_stats()
kwj.position
jhs=PitcherProfile('정현수', '롯데', '불펜', 'L', 'L')
jhs.print_stats()

# 10. 야구단 프로그램
# 팀에 타자와 투수를 추가하는 함수를 구현
# 팀 이름과 선수의 소속팀이 같아야 추가 가능
# 현재 팀에 소속되어 있는 모든 선수들의 이름을 출력하는 함수
# 이때 타자와 투수를 각 포지션별로 분리해서 출력
# 타자는 포수, 내야수, 외야수
# 투수는 선발, 불펜

# 추가할 선수의 소속팀과 팀명이 같지 않을 때 발생시킬 오류명
class TeamError(Exception):
    pass
class Team:
    team_set={'LG', '한화', 'SSG', '삼성', 'NC', 'KT', '롯데',
              'KIA', '두산', '키움'}
    def __init__(self, team_name):
        self.team_selection=input('구단을 선택하세요.')
        if self.team_selection not in self.team_set:
            raise ValueError(f'구단은 {self.team_set} 중에서 선택해야 합니다.')
        self.team_name=team_name
# 각 포지션별 선수의 이름을 저장할 집합
# 같은 선수가 여러 번 추가되는 것을 막기 위해 집합을 사용
# 동명이인은 선수 이름을 만들 때 구분되도록 해야 함
        self.pitchers=set()
        self.catchers=set()
        self.infielders=set()
        self.outfielders=set()
# 선수(객체)를 팀(클래스)에 추가하는 함수
        print(f'Team {self.team_name}({self.team_selection}) is created')
    def add_player(self, player):
# 변수 player에는 타자나 투수 클래스 객체만 오도록 설정
        if not isinstance(player, (BatterProfile, PitcherProfile)):
            raise TypeError('추가할 선수는 BatterProfile 또는 PitcherProfile의 객체이어야 합니다.')
# player의 팀과 Team의 팀명이 같을 때에만 추가하도록 설정
        if player.team!=self.team_selection:
            raise TeamError(f'추가할 선수의 소속 구단은 해당 팀의 구단과 같아야 합니다. 선수 소속 구단: {player.team}, 팀 구단: {self.team_selection}')
# 포지션에 따라 알맞은 리스트에 이름을 추가
        if player.position=='포수':
            self.catchers.add(player.name)
        elif player.position=='내야수':
            self.infielders.add(player.name)
        elif player.position=='외야수':
            self.outfielders.add(player.name)
        else:
            self.pitchers.add(player.name)
        print(f'Player {player.name}({player.position}) is added')
# 소속 선수들의 명단을 출력하는 함수
# 포지션별 출력, 전체 출력
    def print_pitchers(self):
        for i in self.pitchers:
            print(i, end=' ')
    def print_catchers(self):
        for i in self.catchers:
            print(i, end=' ')
    def print_infielders(self):
        for i in self.infielders:
            print(i, end=' ')
    def print_outfielders(self):
        for i in self.outfielders:
            print(i, end=' ')
    def print_all_players(self):
        print(f'{self.team_name} 선수단 전체 명단')
        print()
        print('-'*10+'투수 명단'+'-'*10)
        self.print_pitchers()
        print()
        print('-'*10+'포수 명단'+'-'*10)
        self.print_catchers()
        print()
        print('-'*10+'내야수 명단'+'-'*10)
        self.print_infielders()
        print()
        print('-'*10+'외야수 명단'+'-'*10)
        self.print_outfielders()
# 테스트 프로그램
lotte=Team('꼴데 테스트')
sas=BatterProfile('손아섭', '한화', '외야수', 'R', 'L')
lotte.add_player(sas)
lotte.add_player('')
hsb=BatterProfile('황성빈', '롯데', '외야수', 'R', 'L')
gsm=BatterProfile('고승민', '롯데', '내야수', 'R', 'L')
reyes=BatterProfile('레이예스', '롯데', '외야수', 'R', 'S')
jjw=BatterProfile('전준우', '롯데', '외야수')
ydh=BatterProfile('윤동희', '롯데', '외야수')
nsy=BatterProfile('나승엽', '롯데', '내야수', 'R', 'L')
shy=BatterProfile('손호영', '롯데', '내야수')
ykn=BatterProfile('유강남', '롯데', '포수')
jmj=BatterProfile('전민재', '롯데', '내야수')
psw=PitcherProfile('박세웅', '롯데', '선발')
psw.print_stats()
jcw=PitcherProfile('정철원', '롯데', '불펜')
jcw.print_stats()
kwj=PitcherProfile('김원중', '롯데', '불펜')
kwj.print_stats()
lotte.add_player(hsb)
lotte.add_player(gsm)
lotte.add_player(reyes)
lotte.add_player(jjw)
lotte.add_player(ydh)
lotte.add_player(nsy)
lotte.add_player(shy)
lotte.add_player(ykn)
lotte.add_player(jmj)
lotte.add_player(psw)
lotte.add_player(jcw)
lotte.add_player(kwj)
lotte.pitchers
lotte.catchers
lotte.infielders
lotte.outfielders
lotte.print_pitchers()
lotte.print_catchers()
lotte.print_infielders()
lotte.print_outfielders()
lotte.print_all_players()
hhh=PitcherProfile('한현희')

# 2. 공수 프로그램
# inning=1
# away='LG'
# home='롯데'
# away_score=0
# home_score=0
# away_batter_num=1
# home_batter_num=1

# print(f'{inning}회 초-{away}공격')
# out=0
# b1=None
# b2=None
# b3=None
# while out<3:
#     if b1==None and b2==None and b3==None:
#         runner_posititon='주자 없음'
#     elif b1!=None and b2==None and b3==None:
#         runner_posititon='주자 1루'
#     elif b1==None and b2!=None and b3==None:
#         runner_posititon='주자 2루'
#     elif b1==None and b2==None and b3!=None:
#         runner_posititon='주자 3루'
#     elif b1!=None and b2!=None and b3==None:
#         runner_posititon='주자 1, 2루'
#     elif b1!=None and b2==None and b3!=None:
#         runner_posititon='주자 1, 3루'
#     elif b1==None and b2!=None and b3!=None:
#         runner_posititon='주자 2, 3루'
#     elif b1!=None and b2!=None and b3!=None:
#         runner_posititon='주자 만루'
#     print(f'{out}아웃 | {runner_posititon}')
#     print(f'{away_batter_num}번타자')
#     batter_result_value=random.uniform(0, 80)
#     if batter_result_value<12:
#         batter_result='삼진 아웃'
#         out+=1
#         print(f'{away_batter_num}: {batter_result}')
#     elif batter_result_value<27:
#         batter_result='땅볼 아웃'
#         out+=1
#         if out<3:
            