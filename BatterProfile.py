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
import plotly.graph_objects as go
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
        self.single=0 # 단타
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
            self.sb=0 # 도루 허용
            self.cs=0 # 도루 저지
            self.cs_rate=0 # 도루 저지율
            self.pb=0 # 포일
        print(f'Batter {self.name}({self.team}, {self.position}, {self.pitch_hand}{self.bat_hand})\'s profile is created')
        print(f'파워: {self.power}, 주력: {self.speed}, 컨택: {self.contact}, 수비: {self.defense}, 선구안: {self.eye}')
        self.status_chart()

# 타자별 능력치를 설정하는 함수
# 각 능력치는 1~100 사이의 정수 값을 가짐
# 수치가 높을수록 그 부문에서 뛰어난 선수
# 파워: 수치가 높을수록 장타가 나오기 쉬움. 타격 결과가 안타일 때 그 안타가 장타가
# 될 확률에 영향. 타격 결과가 홈런일 때 그 비거리에 영향
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
# 테스트 프로그램
if __name__=='__main__':
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
    print('Test End')