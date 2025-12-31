from BatterProfile import BatterProfile
from PitcherProfile import PitcherProfile
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
    team_set=('LG', '한화', 'SSG', '삼성', 'NC', 'KT', '롯데',
              'KIA', '두산', '키움')
    def __init__(self, team_name):
        if team_name not in self.team_set:
            raise ValueError(f'구단은 {self.team_set} 중에서 선택해야 합니다.')
        self.team_name=team_name
# 각 포지션별 선수 객체를 저장할 집합
# 같은 선수가 여러 번 추가되는 것을 막기 위해 집합을 사용
# 동명이인은 선수 이름을 만들 때 구분되도록 해야 함
        self.pitchers=set()
        self.catchers=set()
        self.infielders=set()
        self.outfielders=set()
# 선수(객체)를 팀(클래스)에 추가하는 함수
        print(f'Team {self.team_name} is created')
    def add_player(self, player):
# 변수 player에는 타자나 투수 클래스 객체만 오도록 설정
        if not isinstance(player, (BatterProfile, PitcherProfile)):
            raise TypeError('추가할 선수는 BatterProfile 또는 PitcherProfile의 객체이어야 합니다.')
# player의 팀과 Team의 팀명이 같을 때에만 추가하도록 설정
        if player.team!=self.team_name:
            raise TeamError(f'추가할 선수의 소속 구단은 해당 팀의 구단과 같아야 합니다. 선수 소속 구단: {player.team}, 팀 구단: {self.team_name}')
# 포지션에 따라 알맞은 리스트에 이름을 추가
        if player.position=='포수':
            self.catchers.add(player)
        elif player.position=='내야수':
            self.infielders.add(player)
        elif player.position=='외야수':
            self.outfielders.add(player)
        else:
            self.pitchers.add(player)
        print(f'Player {player.name}({player.position}) is added')
# 소속 선수들의 명단을 출력하는 함수
# 포지션별 출력, 전체 출력
    def print_pitchers(self):
        for i in self.pitchers:
            print(i.name, end=' ')
    def print_catchers(self):
        for i in self.catchers:
            print(i.name, end=' ')
    def print_infielders(self):
        for i in self.infielders:
            print(i.name, end=' ')
    def print_outfielders(self):
        for i in self.outfielders:
            print(i.name, end=' ')
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
if __name__=='__main__':
    lotte=Team('롯데')
    sas=BatterProfile('손아섭', '한화', '외야수', 'R', 'L')
    # lotte.add_player(sas)
    # lotte.add_player('')
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