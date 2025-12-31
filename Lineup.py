# 11. 라인업 프로그램
from BatterProfile import BatterProfile
from PitcherProfile import PitcherProfile
from Team import Team
from Bases import Bases
class PositionError(Exception):
    pass
class Lineup:
    positions=('P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF',
               'DH')
# 이 라인업이 어떤 팀의 라인업인지 구분하기 위해 __init__ 함수의 인자로 팀 객체
# 이름을 매개변수 team으로 입력받도록 함. 이때 team이 Team의 객체가 아니면 오류
    def __init__(self, team:Team):
        if not isinstance(team, Team):
            raise TypeError('변수 team은 Team의 객체이어야 합니다.')
        self.team=team
        self.team_name=team.team_name

# 타순별 타자들을 저장한 리스트
# 앞에서부터 1번~9번
        self.batting_order=[None]*9
# 현재 타순을 표시하는 변수. 초기 값은 1번 타자를 가리키는 0
        self.current_index=0

# 포지션별 선수 객체를 저장한 딕셔너리
        self.players_by_position={'P':None, 'C':None, '1B':None, 
                                  '2B':None, '3B':None, 'SS':None,
                                  'LF':None, 'CF':None, 'RF':None, 
                                  'DH':None}

# 팀 내의 모든 선수들을 저장할 리스트를 생성. 이때 각 요소는 선수 객체
# 만들어진 Team 객체를 이용해 Lineup 객체를 만들면, Team 내의 모든 선수 객체를
# all에 저장.(이 기능은 아래에서 구현) 이후 라인업을 구성할 때는 이 all에
# 있는 선수 객체만 사용할 수 있도록 제한
        self.all_players=[]
# 모든 선수들을 all에 저장
        for pitcher in team.pitchers:
            self.all_players.append(pitcher)
        for catcher in team.catchers:
            self.all_players.append(catcher)
        for infielder in team.infielders:
            self.all_players.append(infielder)
        for outfielder in team.outfielders:
            self.all_players.append(outfielder)
# team의 모든 선수 객체를 저장한 리스트 all이 완성되면, 선수들을 모두 벤치로 배치
# 이후 all은 수정할 수 없도록 튜플로 변경
# 만약 선수단 엔트리에 변동이 있다면, Team 객체에서 수정한 후 Lineup 객체를 갱신
        self.bench=self.all_players.copy()
        self.all_players=tuple(self.all_players)
# 이렇게 하면 Lineup 객체의 초기화가 완료
# 벤치는 아직 해당 경기에 출전하지 않은 선수들이 있는 리스트
# 경기 중 한 번 출장한 선수는 벤치에서 빠짐(한 번 빠진 선수는 해당 경기 재출전 불가)

# 타자의 포지션과 타순을 설정하는 함수
# 선발 라인업을 구성할 때 사용
# 타자의 수는 정확히 9명
# 모든 타자는 팀의 엔트리(all)에 있어야 함
# 각 타자들은 모두 BatterProfile의 객체이어야 함
# 한 선수 객체는 한 번만 포함. 두 번 이상 포함되어서는 안 됨
# 주의: 타순 설정만으로는 벤치에서 제외되지 않음. 수비 위치가 설정되어야 비로소 벤치에서 제외됨
# 만약 대타로만 나오고 수비로 나오지 않는 상황이라면, 일단 그 대타에게 수비 위치를 부여했다가
# 곧바로 다른 선수를 그 대타의 대수비로 투입하면 됨
# 입력값은 길이가 9인 리스트. 이 리스트의 모든 원소는 BatterProfile 객체
    def set_batting_order(self, batters:list):
        if len(batters)!=9:
            raise ValueError(f'타순은 반드시 9명이어야 합니다. 입력 리스트의 길이: {len(batters)}')
# 한 번 라인업에 포함된 타자를 구분하기 위한 집합을 생성
        seen=set()
# 조건문과 반복문을 통한 입력 리스트의 유효성 검사
        for idx in range(len(batters)):
            batter=batters[idx]
# batters에서 타자 객체가 아닌 요소가 있다면 TypeError 발생
            if not isinstance(batter, BatterProfile):
                raise TypeError(f'타순에는 타자 객체만 들어갈 수 있습니다. batters[{idx}]의 데이터형은 {type(batter)}입니다.')
# batters에서 all에 없는 타자 객체가 있다면 ValueError 발생
            if batter not in self.all_players:
                raise ValueError(f'{batter.name}은(는) 팀 엔트리에 포함되어 있지 않습니다.')
# batters에서 중복된 타자 객체가 있다면 ValueError 발생
            if batter in seen:
                raise ValueError(f'{batter.name}이(가) 입력 리스트에 중복으로 포함되어 있습니다.')
            seen.add(batter)
# 유효성 검사가 끝나면 초기화해 둔 self.batting_order를 입력 리스트 batters로 덮어씀
# 선발 라인업이 확정되었으므로 현재 타순도 1번 타자를 가리키는 0으로 초기화
        self.batting_order=batters.copy()
        self.current_index=0

# 선발 수비 포지션을 설정하는 함수
# 투수는 PitcherProfile, 나머지 포지션은 BatterProfile의 객체
# 포지션은 중복 불가. 한 선수가 두 개 이상의 포지션을 배정받아서는 안 됨
# 모든 선수는 엔트리에 포함되어 있어야 함
# 요령: 이 함수는 선발 출장하는 선수들의 수비 포지션을 정할 때만 사용할 것.
# 대타, 대주자, 대수비로 교체되는 선수들의 경우에는 아래 change 계열 함수들을 사용할 것
    def assign_position(self, position, player, first_appearance=True):
# 조건문과 반복문을 통한 입력 매개변수들의 유효성 검사
# 포지션이 투, 포, 1, 2, 3, 유, 좌, 중, 우 중에 없으면 ValueError 발생
        if position not in self.players_by_position.keys():
            raise ValueError(f'{position}은(는) 올바른 포지션 이름이 아닙니다. {tuple(self.players_by_position.keys())} 중에서 입력하세요.')
# 만약 포지션이 투수인데 선수가 투수 객체가 아니면 TypeError 발생
        if position=='P':
            if not isinstance(player, PitcherProfile):
                raise TypeError(f'투수 포지션은 투수 객체만 배정할 수 있습니다. player의 데이터형은 {type(player)}입니다.')
# 포지션이 투수가 아니면 포수/야수
# 이때 선수가 타자 객체가 아니면 TypeError 발생
        else:
            if not isinstance(player, BatterProfile):
                raise TypeError(f'포수/야수 포지션은 타자 객체만 배정할 수 있습니다. player의 데이터형은 {type(player)}입니다.')
# 야수는 다시 보직별로 구분
# 해당 보직에 맞는 타자만 배정하도록 제한
            if position=='C':
                if player.position!='포수':
                    raise PositionError(f'포수 포지션에는 포수만 배정할 수 있습니다. {player.name}은(는) {player.position}입니다.')
            elif position in ('1B', '2B', '3B', 'SS'):
                if player.position!='내야수':
                    raise PositionError(f'내야수 포지션에는 내야수만 배정할 수 있습니다. {player.name}은(는) {player.position}입니다.')
            elif position in ('LF', 'CF', 'RF'):
                if player.position!='외야수':
                    raise PositionError(f'외야수 포지션에는 외야수만 배정할 수 있습니다. {player.name}은(는) {player.position}입니다.')
# 입력한 선수가 엔트리에 없으면 ValueError 발생
        if player not in self.all_players:
            raise ValueError(f'{player.name}은(는) 팀 엔트리에 포함되어 있지 않습니다.')
# 한 선수가 이미 한 포지션에 배정되어 있는 상태에서 또 다른 포지션에 배정하려 한다면
# ValueError 발생
        for pos, p in self.players_by_position.items():
# 오류 발생 조건: 추가하려는 선수가 딕셔너리의 value로 이미 있는데, 이때 그 선수의
# 포지션(key)가 현재 추가하려는 key와 서로 다른 상황
# 조건문을 이렇게 설정하면 수비 위치 이동을 구현할 수 있음. 수비 위치 이동은 벤치에서의
# 출장이 아니므로 first_appearance가 False. 따라서 벤치 검사를 하지 않음
            if p is player and pos!=position:
                raise PositionError(f'{player.name}은(는) 이미 {pos} 포지션에 배정되어 있습니다.')
# first_appearance는 이 호출로 인해 player가 처음으로 출장하는 것인지 구분하는 bool 값
# 선발 출장 또는 대수비 투입은 처음부터 수비로 출장하므로 True
# 대타/대주자 출장은 공격 때 먼저 출장하고 나중에 수비로 바뀌는 것이므로 False
# 벤치 유무 검사는 first_appearance가 True일 때만 실행. 대타/대주자 출장은 수비 포지션을
# 배정받기 전에 이미 출장한 것이므로 bench에의 유무를 따지지 않음
# first_appearance가 True일 때, 입력한 선수가 엔트리에는 있으나 벤치에 없다면 
# 이는 교체된 선수를 다시 배정하려는 상황이므로 ValueError 발생
        if first_appearance:
# first_appearance가 True일 때만 아래 조건문을 실행
# 대타/대주자로 출장한 선수에게 수비 포지션을 부여할 때는 first_appearance를 False로 설정
            if player not in self.bench:
                raise ValueError(f'{player.name}은(는) 이미 출장한 선수입니다.')
# 포지션을 배정받은 선수는 출장한 것이므로, 벤치에서 제거(교체된 후 재출장 불가)
# 벤치에서 출장하는 선발, 대수비는 이때 출장 처리됨
            self.bench.remove(player)
# 유효성 검사가 끝나면, 포지션 딕셔너리에서 해당 포지션의 value를 player로 설정
        self.players_by_position[position]=player

# 선수를 교체하는 함수(투수 교체, 대수비, 대타/대주자 출장 선수의 수비 포지션 배정)
# 어떤 포지션의 선수를 다른 선수로 교체
# 투수 교체 또는 대수비 투입 시에는 first_appearance를 True로 지정하여 벤치 유무를 검사
# 대타/대주자로 출장한 선수들은 이미 벤치에서 제거되었으므로 first_appearance를 False로
# 지정하여 벤치 유무 검사를 생략(이렇게 오류 방지)
    def change_defense(self, position, new_player, first_appearance=True):
        if position not in self.players_by_position.keys():
            raise ValueError(f'{position}은(는) 올바른 수비 포지션 이름이 아닙니다. {tuple(self.players_by_position.keys())} 중에서 입력하세요.')
        old_player=self.players_by_position[position]
# 만약 실수로 똑같은 선수를 다시 교체하는 상황이라면 아무것도 하지 않음
        if old_player is new_player:
            return old_player
# 먼저 기존의 선수를 제거
        self.players_by_position[position]=None
# 그 후 새로운 선수의 포지션을 배정
# 이때 같은 선수를 여러 번 교체하여 발생하는 버그 방지를 위해 예외 처리
# 한 번 교체 투입된 선수를 다시 교체 투입하려 하면 오류 발생
        try:
            self.assign_position(position, new_player, first_appearance)
        except Exception as e:
            self.players_by_position[position]=old_player
            raise e
# 기존의 선수 객체를 반환
        return old_player

# 타자를 교체하는 함수(대타)
# 대타 당시에는 수비를 교체하지 않음. 수비는 이닝 종료 후 교체
# 따라서 대타 상황에서 수비 교체는 발생하지 않음
# 수비 교체는 발생하지 않으나, 대타는 출장에 속함
# 따라서 대타로 나온 선수는 벤치에서 제거
# 대타로 출장한 선수에게 수비 포지션을 배정할 때는 first_appearance를 False로 지정할 것
# 이는 대주자도 마찬가지
    def pinch_hitter(self, order_idx:int, new_batter:BatterProfile):
# 입력값의 유효성 검사
# 타순 번호가 1~9의 정수가 아니라면 ValueError 발생
        if order_idx not in [x for x in range(1, 10)]:
            raise ValueError(f'타순은 1에서 9까지의 정수이어야 합니다. 현재 입력된 타순은 {order_idx}입니다.')
# 새로운 타자가 타자 객체가 아니면 TypeError 발생
        if not isinstance(new_batter, BatterProfile):
            raise TypeError(f'대타는 타자 객체만 출장할 수 있습니다. new_batter의 데이터형은 {type(new_batter)}입니다.')
# 새로운 타자 객체가 엔트리에 없으면 ValueError 발생
        if new_batter not in self.all_players:
            raise ValueError(f'{new_batter.name}은(는) 팀 엔트리에 포함되어 있지 않습니다.')
# 새로운 타자 객체가 엔트리에 있으나 벤치에 없으면 이미 출장한 것이므로 ValueError 발생
        if new_batter not in self.bench:
            raise ValueError(f'{new_batter.name}은(는) 이미 출장한 선수입니다.')
# 유효성 검사가 끝나면, 해당 타순의 기존 타자를 old_batter로 저장
        old_batter=self.batting_order[order_idx-1]
# 만약 기존 타자가 없으면 선발 타순 구성이 안 된 것이므로 ValueError 발생
        if old_batter is None:
            raise ValueError(f'{order_idx}번에 배정된 타자가 없습니다. set_batting_order 함수를 사용하여 선발 타순을 먼저 완성하세요.')
# 유효성 검사가 끝났다면 해당 타순의 기존 타자를 제거하고 새 타자로 교체
# 이후 대타로 나온 선수를 벤치에서 제거
        self.batting_order[order_idx-1]=new_batter
        self.bench.remove(new_batter)
# 주의: 대타 함수는 대타로 나온 타자의 수비 포지션에는 아무런 영향을 주지 않음
# 대타 타자의 수비 포지션 배정은 해당 이닝 공격이 끝나고 할 일
# 다만 교체되어 경기에서 빠진 기존 타자의 포지션은 제거해야 함. 이 선수는 이제 경기에
# 출전할 수 없게 됨
        for pos, player in self.players_by_position.items():
# 포지션 딕셔너리에서 교체된 기존 타자의 포지션을 찾음
            if player is old_batter:
# player가 기존 타자와 같은 객체이면 이때의 pos가 기존 타자의 포지션
# 따라서 이 포지션에 대한 value를 None으로 수정
# 이후 다른 요소는 볼 필요가 없으므로 즉시 반복문을 탈출
                self.players_by_position[pos]=None
                break
# 기존 타자 객체를 반환
        return old_batter

# 주자를 교체하는 함수(대주자)
# 대주자는 공격 출장
# 대주자로 나오는 즉시 출장 처리(벤치에서 제거)
# 대타와 마찬가지로 수비 포지션에는 영향을 주지 않음. 수비 교체는 공격이 끝나고 할 일
# 대주자로 출장한 선수가 수비 포지션을 배정받을 때는 first_appearance=False
# 현실 단순화를 위해 대주자는 타자로만 한정
    def pinch_runner(self, bases:Bases, base_idx:int, new_runner:BatterProfile):
# 입력값 유효성 검사
# bases가 베이스 객체가 아니면 오류 발생
# 진행 중인 경기에 사용되고 있는 베이스 객체가 들어갈 예정
        if not isinstance(bases, Bases):
            raise TypeError(f'bases에는 베이스 객체를 입력해야 합니다. 현재 bases의 데이터형은 {type(bases)}입니다.')
# 주자가 있을 수 있는 베이스는 1, 2, 3루이므로, base_idx는 1, 2, 3 중 하나
        if base_idx not in (1, 2, 3):
            raise ValueError(f'베이스의 번호는 1, 2, 3 중 하나이어야 합니다. 현재 입력된 값은 {base_idx} 입니다.')
# 새 주자가 타자가 아니면 TypeError 발생
        if not isinstance(new_runner, BatterProfile):
            raise TypeError(f'대주자로는 타자 객체만 배정할 수 있습니다. 현재 new_runner의 데이터형은 {type(new_runner)}입니다.')
# 새 주자가 될 타자 객체가 엔트리에 없다면 ValueError 발생
        if new_runner not in self.all_players:
            raise ValueError(f'{new_runner.name}은(는) 팀 엔트리에 포함되어 있지 않습니다.')
# 새 주자가 될 타자 객체가 엔트리에 있으나 벤치에 없다면 이미 출장한 선수이므로
# ValueError 발생
        if new_runner not in self.bench:
            raise ValueError(f'{new_runner.name}은(는) 이미 출장한 선수입니다.')
# 유효성 검사가 끝나면, 교체할 주자의 위치에 따라 함수를 구현
# 교체할 주자가 1루 주자라면 1루에 주자가 있는지 확인. 없으면 ValueError 발생
        if base_idx==1:
            if not bases.is_1B_loaded():
                raise ValueError('현재 1루에 주자가 없습니다.')
# 기존 주자를 삭제하고 그 주자를 old_runner로 저장
            old_state=bases.delete_1B_runner()
            if old_state is None:
                raise RuntimeError('1루 주자 상태를 가져오지 못했습니다.')
            bases.set_1B_runner(new_runner, 
                                old_state.resp_pitcher,
                                earned=old_state.earned)
# 교체할 주자의 위치가 2루나 3루일 때도 같은 방법으로 처리
        elif base_idx==2:
            if not bases.is_2B_loaded():
                raise ValueError('현재 2루에 주자가 없습니다.')
            old_state=bases.delete_2B_runner()
            if old_state is None:
                raise RuntimeError('2루 주자 상태를 가져오지 못했습니다.')
            bases.set_2B_runner(new_runner,
                                old_state.resp_pitcher,
                                earned=old_state.earned)
        else:
            if not bases.is_3B_loaded():
                raise ValueError('현재 3루에 주자가 없습니다.')
            old_state=bases.delete_3B_runner()
            if old_state is None:
                raise RuntimeError('3루 주자 상태를 가져오지 못했습니다.')
            bases.set_3B_runner(new_runner,
                                old_state.resp_pitcher,
                                earned=old_state.earned)
# 대주자 교체가 완료되면 새로운 주자(대주자로 출장한 선수)를 벤치에서 제거
        self.bench.remove(new_runner)
# 기존 주자가 수비 포지션을 갖고 있었다면, 그 포지션을 공석으로 만들어야 함
# 대주자로 출전한 선수의 수비 포지션 배정은 공격이 끝나고 할 일
        for pos, player in self.players_by_position.items():
            if player is old_state.runner:
                self.players_by_position[pos]=None
                break
# 기존 주자 객체를 반환
        return old_state.runner
# 참고: 대주자 투입 즉시 수비 교체를 자동으로 배정하지는 않지만, 기존 주자가 수비에 
# 배정되어 있던 경우 그 수비 포지션은 공석이 된다.
# 타자 교체가 아니라 주자 교체이기 때문
# 기존 주자가 다시 타석에 들어설 수 없는 것은 맞으나, 다음 타석에 이 대주자가 타석에
# 들어올지, 아니면 다른 타자가 들어올지(대타)는 감독의 선택

# 현재 타자를 반환하는 함수
    def get_current_batter(self):
        return self.batting_order[self.current_index]

# 타순을 이동하는 함수
# 9번 타자의 다음 타자는 1번 타자
# 나머지로 구현
    def next_batter(self):
        self.current_index=(self.current_index+1)%9

# 현재 타순을 반환하는 함수
    def get_current_batting_order(self):
        return self.batting_order

# 현재 투수를 반환하는 함수
    def get_current_pitcher(self):
        return self.players_by_position['P']

# 현재 타순을 출력하는 함수
    def print_current_batting_order(self):
        for idx in range(len(self.batting_order)):
            batter=self.batting_order[idx]
# None의 name 멤버 변수 값을 찾으려고 할 때 발생하는 AttributeError를 방지
            if batter is None:
                print(f'{idx+1}번 (공석)')
            else:
                print(f'{idx+1}번 {batter.name}')

# 현재 수비 위치를 출력하는 함수
    def print_current_defense(self):
# None의 name 멤버 변수 값을 찾으려고 할 때 발생하는 AttributeError를 방지
        for key in self.players_by_position.keys():
            player=self.players_by_position[key]
            if player is None:
                print(f'{key}: (공석)')
            else:
                print(f'{key}: {self.players_by_position[key].name}')

# 경기 시작 직후 또는 공수교대 후 수비 위치를 검증하는 함수
# (필요에 따라 대타, 대주자를 사용하고서) 팀의 공격이 끝났을 때, 현재 라인업이 다음
# 수비를 시작할 수 있는 라인업인지 검사하는 역할
# 만약 검증 결과 수비를 시작할 수 있는 라인업이 아니라면 즉시 경기는 중단되고, 감독은
# 수비 라인업을 조정해야 함
# 이 함수는 대타, 대주자 기용 시에는 실행되지 않음. 오직 이닝(초/말)이 끝날 때만 실행됨
    def validate_defense(self):
# 수비 포지션: 투, 포, 1, 2, 3, 유, 좌, 중, 우
# 지명타자는 수비를 나가지 않으므로 검증 대상이 아님
        required_positions=('P', 'C', '1B', '2B', '3B', 'SS', 'LF',
                            'CF', 'RF')
# 조건 1. 각 수비 포지션에 모두 선수가 있는가?
# 수비를 나가는 포지션에 한 명이라도 선수가 없다면 PositionError 발생
        for position in required_positions:
            if self.players_by_position[position] is None:
                raise PositionError(f'{position} 포지션에 배정된 선수가 없습니다.')
# 조건 2: 같은 선수가 두 개 이상의 포지션에 중복으로 배정되었는가?
# 이건 사실 assign/change 함수에서 이미 걸러지겠지만, 안전 장치로 설계
        seen=set()
        for pos in required_positions:
            player=self.players_by_position[pos]
            if player in seen:
                raise PositionError(f'{player.name}이(가) 두 개 이상의 포지션에 배정되어 있습니다.')
            seen.add(player)
# 조건 검사가 끝나면, True를 반환하고 경기 시작 or 재개
        return True

# 요약-상황별 first_appearance
# 선발 출장: True
# 대수비: True
# 투수 교체: True
# 대타, 대주자 출장 후 수비 투입: False
# 수비 위치 이동: False

# 테스트 프로그램
if __name__=='__main__':
    lotte=Team('롯데')
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
    jcw=PitcherProfile('정철원', '롯데', '불펜')
    kwj=PitcherProfile('김원중', '롯데', '불펜')
    jbk=BatterProfile('정보근', '롯데', '포수')
    hdh=BatterProfile('한동희', '롯데', '내야수')
    jds=BatterProfile('장두성', '롯데', '외야수', 'R', 'L')
    kms=BatterProfile('김민성', '롯데', '내야수')
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
    lotte.add_player(jbk)
    lotte.add_player(hdh)
    lotte.add_player(jds)
    lineup1=Lineup(lotte)
    lineup1.all_players
# 선발 타순 구성
    lineup1.set_batting_order([hsb, gsm, reyes, jjw, ydh, nsy, shy,
                               jbk, jmj])
# 수비 위치 결정(선발 출전 선수들의 출장 확정)
    lineup1.assign_position('CF', hsb)
    lineup1.assign_position('2B', gsm)
    lineup1.assign_position('LF', reyes)
    lineup1.assign_position('RF', ydh)
    lineup1.assign_position('1B', nsy)
    lineup1.assign_position('3B', shy)
    lineup1.assign_position('C', jbk)
    lineup1.assign_position('SS', jmj)
    lineup1.assign_position('P', psw)
    lineup1.assign_position('DH', jjw)
    lineup1.print_current_defense()
    lineup1.print_current_batting_order()
# 대타 유강남(정보근 타석)
# 유강남은 대타로 나온 시점에서 출장으로 처리되므로 first_appearance가 False
    lineup1.pinch_hitter(8, ykn)
    lineup1.print_current_batting_order()
# 대수비 출장, 투수 교체
# 대타로 투입됐던 유강남은 수비 투입 시 벤치에서 온 것이 아니므로 first_appearance가 False
# 유강남에게 수비 위치를 부여하지 않은 채 수비를 시작하려 하면 포수가 공석이므로 오류 발생
    lineup1.validate_defense()
    lineup1.change_defense('C', ykn, first_appearance=False)
    lineup1.print_current_batting_order()
    lineup1.print_current_defense()
    lineup1.validate_defense()
# 유강남에게 포수 위치를 부여하자 검증 함수가 True를 반환함
# 투수 박세웅: 투수 정철원으로 교체
    lineup1.change_defense('P', jcw)
# 정철원으로 이미 교체한 상태에서 또 정철원으로 교체하려고 하면 교체는 일어나지 않음
    lineup1.print_current_defense()
# 투수 정철원: 투수 김원중으로 교체
    lineup1.change_defense('P', kwj)
    lineup1.print_current_batting_order()
    lineup1.print_current_defense()
# 수비 위치 이동
# 고승민 제외, 손호영 3루->2루, 한동희 3루
# 한동희는 대수비 출장이므로 first_appearance가 True, 손호영은 수비 이동이므로
# first_appearance가 False
# 따라서 한동희는 대수비로 나오는 동시에 벤치에서 제거
# 손호영은 이미 벤치에 없었음
# 한동희를 먼저 3루에 넣고 손호영을 2루로 이동해야 오류가 발생하지 않음
# 손호영을 먼저 2루로 옮기려고 하면 3루와 2루에 동시에 손호영이 있기 때문에 오류 발생
    lineup1.print_current_defense()
    lineup1.change_defense('2B', shy, False)
    lineup1.change_defense('3B', hdh)
    lineup1.change_defense('2B', shy, False)
    lineup1.print_current_defense()
    lineup1.validate_defense()
# 이미 교체된 고승민을 다시 투입하려 하면 오류 발생
    lineup1.assign_position('2B', gsm)
# 1루 주자 레이예스: 대주자 장두성으로 교체
    lck=PitcherProfile('임찬규', 'LG', '선발', 'R', 'L')
    base1=Bases()
    base1.set_1B_runner(reyes, lck, earned=True)
    old=lineup1.pinch_runner(base1, 1, jds)
    new=base1.get_1B_runner()
    print(f'1루 주자 {old.name}: 대주자 {new.name}(으)로 교체')