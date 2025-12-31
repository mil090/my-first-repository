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
import plotly.graph_objects as go
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
        self.out=0 # 아웃카운트 수
        self.ip=0 # 이닝
        self.hit=0 # 피안타
        self.hr=0 # 피홈런
        self.bb=0 # 볼넷
        self.ibb=0 # 고의사구
        self.hbp=0 # 사구
        self.so=0 # 탈삼진
        self.run=0 # 실점
        self.erun=0 # 자책점
        self.ir=0 # 승계주자 수
        self.irs=0 # 승계주자 실점
        self.ira=0 # 승계주자 실점률
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
# 테스트 프로그램
if __name__=='__main__':
    psw=PitcherProfile('박세웅', '롯데', '선발')
    psw.print_stats()
    psw.position
    kwj=PitcherProfile('김원중', '롯데', '불펜')
    kwj.print_stats()
    kwj.position
    jhs=PitcherProfile('정현수', '롯데', '불펜', 'L', 'L')
    jhs.print_stats()
    print('Test End')