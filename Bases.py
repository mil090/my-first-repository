# 13. 확장된 베이스 프로그램
# 실점/자책점/승계주자를 구현하려면 Bases 클래스가 책임투수, 자책 여부를 기억
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from BatterProfile import BatterProfile
from PitcherProfile import PitcherProfile

@dataclass
# 베이스 위 주자 상태를 표현하는 클래스
class RunnerState:
# runner: 타자 객체
    runner: BatterProfile
# resp_pitcher: 책임 투수(runner를 내보낸 투수)
    resp_pitcher: PitcherProfile
# earned: 자책 여부(자책인 경우 True, 비자책인 경우 False)
# 기본값은 True, 이후 실책, 야수선택, 포일 등의 비자책 상황을 구현할 때 False로
# 바뀌도록 구현하는 것이 후속 과제
    earned: bool=True

class Bases:
# 베이스의 위치는 왼쪽부터 3루-2루-1루
    third, second, first=0, 1, 2
    def __init__(self):
        self.bases: list[Optional[RunnerState]]=[None, None, None]
# 주자 상태를 확인하는 함수
    def is_1B_loaded(self) -> bool:
        return self.bases[self.first] is not None
    def is_2B_loaded(self) -> bool:
        return self.bases[self.second] is not None
    def is_3B_loaded(self) -> bool:
        return self.bases[self.third] is not None
    def is_loaded(self) -> bool:
        return None not in self.bases
    def is_empty(self) -> bool:
        return all(x is None for x in self.bases)
# 현재 주자 수를 반환하는 함수
    def count_runners(self) -> int:
        return sum(1 for x in self.bases if x is not None)
# 득점권 여부를 반환하는 함수
    def is_scoring_position(self) -> bool:
        return self.is_2B_loaded() or self.is_3B_loaded()
# 각 베이스의 주자 상태를 반환하는 함수
    def get_1B_state(self) -> Optional[RunnerState]:
        return self.bases[self.first]
    def get_2B_state(self) -> Optional[RunnerState]:
        return self.bases[self.second]
    def get_3B_state(self) -> Optional[RunnerState]:
        return self.bases[self.third]
# 기존 코드 호환: runner 객체만 반환
    def get_1B_runner(self):
        state=self.get_1B_state()
        return None if state is None else state.runner
    def get_2B_runner(self):
        state=self.get_2B_state()
        return None if state is None else state.runner
    def get_3B_runner(self):
        state=self.get_3B_state()
        return None if state is None else state.runner
    def get_runners(self) -> Tuple[Optional[BatterProfile], 
                                   Optional[BatterProfile],
                                   Optional[BatterProfile]]:
        return self.get_1B_runner(), self.get_2B_runner(), self.get_3B_runner()
# 각 베이스에 있는 주자의 이름을 출력하는 함수
    def print_1B_runner(self):
        state=self.get_1B_state()
        if state is None:
            print('1루 주자:')
        else:
            print(f'1루 주자: {state.runner.name}')
    def print_2B_runner(self):
        state=self.get_2B_state()
        if state is None:
            print('2루 주자:')
        else:
            print(f'2루 주자: {state.runner.name}')
    def print_3B_runner(self):
        state=self.get_3B_state()
        if state is None:
            print('3루 주자:')
        else:
            print(f'3루 주자: {state.runner.name}')
    def print_runners(self):
        self.print_3B_runner()
        self.print_2B_runner()
        self.print_1B_runner()
# 현재 주자 상태를 출력하는 함수
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
# 투수 교체 시 호출하는 함수
# 승계주자 관련 기록 작성에 이용
    def register_pitcher_change(self, new_pitcher: PitcherProfile):
        if not isinstance(new_pitcher, PitcherProfile):
            raise TypeError(f'new_pitcher에는 투수 객체를 입력해야 합니다. 현재 new_pitcher의 데이터형은 {type(new_pitcher)}입니다.')
        new_pitcher.ir+=self.count_runners()

# 주자를 설정하고 삭제하는 함수
# 먼저 입력값의 유효성을 검사하는 함수를 생성
    def _validate_runner(self, runner):
        if not isinstance(runner, BatterProfile):
            raise TypeError(f'runner에는 타자 객체를 입력해야 합니다. 현재 runner의 데이터형은 {type(runner)}입니다.')
    def _validate_pitcher(self, pitcher):
        if not isinstance(pitcher, PitcherProfile):
            raise TypeError(f'pitcher에는 투수 객체를 입력해야 합니다. 현재 pitcher의 데이터형은 {type(pitcher)}입니다.')
# 베이스에 주자를 배치할 때에는 반드시 책임 투수 객체를 입력하도록 설계
    def set_1B_runner(self, runner, resp_pitcher: PitcherProfile,
                      earned: bool=True):
        self._validate_runner(runner)
        self._validate_pitcher(resp_pitcher)
        self.bases[self.first]=RunnerState(runner=runner, 
                                           resp_pitcher=resp_pitcher,
                                           earned=earned)
    def set_2B_runner(self, runner, resp_pitcher: PitcherProfile,
                      earned: bool=True):
        self._validate_runner(runner)
        self._validate_pitcher(resp_pitcher)
        self.bases[self.second]=RunnerState(runner=runner,
                                            resp_pitcher=resp_pitcher,
                                            earned=earned)
    def set_3B_runner(self, runner, resp_pitcher: PitcherProfile,
                      earned: bool=True):
        self._validate_runner(runner)
        self._validate_pitcher(resp_pitcher)
        self.bases[self.third]=RunnerState(runner=runner,
                                           resp_pitcher=resp_pitcher,
                                           earned=earned)
    def delete_1B_runner(self) -> RunnerState:
        if not self.is_1B_loaded():
            raise Exception('현재 1루에 주자가 없습니다.')
        state=self.bases[self.first]
        assert state is not None
        self.bases[self.first]=None
        return state
    def delete_2B_runner(self) -> RunnerState:
        if not self.is_2B_loaded():
            raise Exception('현재 2루에 주자가 없습니다.')
        state=self.bases[self.second]
        assert state is not None
        self.bases[self.second]=None
        return state
    def delete_3B_runner(self) -> RunnerState:
        if not self.is_3B_loaded():
            raise Exception('현재 3루에 주자가 없습니다.')
        state=self.bases[self.third]
        assert state is not None
        self.bases[self.third]=None
        return state
    def clear_bases(self):
        self.bases[self.first]=None
        self.bases[self.second]=None
        self.bases[self.third]=None

# 주자의 득점을 처리하는 함수
# runner_state가 득점에 성공했을 때 호출
    def score_runner(self, runner_state: RunnerState, current_pitcher:
                     PitcherProfile):
        if runner_state is None:
            raise ValueError(f'현재 runner_state가 None입니다.')
        self._validate_pitcher(current_pitcher)
# 타자와 투수 객체에 모두 멤버 변수 run이 존재하나, 그 의미가 다름
# 타자 객체의 run은 득점, 투수 객체의 run은 실점을 의미
# 그러니 (대)주자로는 타자 객체만 사용하는 것을 원칙으로 하자
# 투수 객체를 주자로 사용할 경우 득/실점이 섞여 기록이 무너짐

# 득점한 주자의 득점을 1 증가
        runner_state.runner.run+=1
# 득점한 주자의 책임투수의 실점을 1 증가
        runner_state.resp_pitcher.run+=1
# 만약 그 실점이 자책점일 경우 자책점을 1 증가
        if runner_state.earned:
            runner_state.resp_pitcher.erun+=1
# 만약 현재 마운드의 투수와 득점한 주자의 책임 투수가 서로 다르다면 이는 승계주자
# 실점 상황(분식)이므로 irs를 1 증가
# 자신의 책임 주자가 아니므로 실점 및 자책점은 증가하지 않음
        if current_pitcher is not runner_state.resp_pitcher:
            current_pitcher.irs+=1

# 각 베이스의 주자를 득점으로 처리하는 함수
    def score_from_1B(self, current_pitcher: PitcherProfile):
        state=self.delete_1B_runner()
        self.score_runner(state, current_pitcher)
    def score_from_2B(self, current_pitcher: PitcherProfile):
        state=self.delete_2B_runner()
        self.score_runner(state, current_pitcher)
    def score_from_3B(self, current_pitcher:PitcherProfile):
        state=self.delete_3B_runner()
        self.score_runner(state, current_pitcher)

# 주자의 진루를 표현하는 함수
    def move_1B_to_2B(self):
        if not self.is_1B_loaded():
            raise Exception('현재 1루에 주자가 없습니다.')
        if self.is_2B_loaded():
            raise Exception('현재 2루에 이미 주자가 있습니다.')
        self.bases[self.second]=self.bases[self.first]
        self.bases[self.first]=None
    def move_2B_to_3B(self):
        if not self.is_2B_loaded():
            raise Exception('현재 2루에 주자가 없습니다.')
        if self.is_3B_loaded():
            raise Exception('현재 3루에 이미 주자가 있습니다.')
        self.bases[self.third]=self.bases[self.second]
        self.bases[self.second]=None
    def move_1B_to_3B(self):
        if not self.is_1B_loaded():
            raise Exception('현재 1루에 주자가 없습니다.')
        if self.is_3B_loaded():
            raise Exception('현재 3루에 이미 주자가 있습니다.')
        self.bases[self.third]=self.bases[self.first]
        self.bases[self.first]=None

# 사사구로 인한 주자의 강제 진루 함수
    def force_advance_on_walk(self, batter: BatterProfile,
                              pitcher: PitcherProfile, 
                              earned: bool=True) -> int:
# 사사구로 타자가 1루에 나가면서 강제로 주자의 진루가 발생할 때 처리
# 반환값은 득점 수(밀어내기면 1, 아니면 0)
        runs=0
# 1루에 주자가 없다면 강제 진루는 발생하지 않음. 따라서 득점도 발생하지 않음
        if not self.is_1B_loaded():
            self.set_1B_runner(batter, pitcher, earned=earned)
            return 0
# 1루에 주자가 있으면 밀어내기 체인 시작
# 1루에 주자가 있는 상황 중 만루이면 밀어내기로 3루 주자 득점
        if self.is_loaded():
            self.score_from_3B(pitcher)
            runs+=1
        if self.is_2B_loaded():
# 1루에 주자가 있는 상태에서 2루에 주자가 있는 상황
# 만약 3루에도 주자가 있다면 만루
# 만루 상황은 위 로직에서 밀어내기로 처리되므로, 이 조건문에서 3루는 비어 있어야 정상
# 만약 3루가 비어 있지 않다면 에러로 잡기
# 즉 처음 주자 상황이 12루든 만루든, 이 조건문이 실행될 때 3루는 비어 있어야 정상
            if self.is_3B_loaded():
                raise RuntimeError('밀어내기 처리 후에도 3루가 비어 있지 않습니다.')
            self.move_2B_to_3B()
# 위 조건문을 처리한 후 2루는 비어 있어야 함
        if self.is_2B_loaded():
            raise RuntimeError('2루가 비워지지 않았습니다. move_2B_to_3B 구현을 확인하세요.')
# 1루 주자는 항상 2루로 강제 진루
        self.move_1B_to_2B()
        if not self.is_2B_loaded():
            raise RuntimeError('1루 주자를 2루로 옮기지 못했습니다. move_1B_to_2B 구현을 확인하세요.')
# 강제 진루가 끝나고 나면 1루는 비어 있어야 함
        if self.is_1B_loaded():
            raise RuntimeError('1루가 비워지지 않았습니다. move_1B_to_2B 구현을 확인하세요.')
        self.set_1B_runner(batter, pitcher, earned=earned)
        return runs

# 테스트 프로그램
if __name__=="__main__":
    hsb=BatterProfile('황성빈', '롯데', '외야수', 'R', 'L')
    gsm=BatterProfile('고승민', '롯데', '내야수', 'R', 'L')
    rey=BatterProfile('레이예스', '롯데', '외야수', 'R', 'S')
    jjw=BatterProfile('전준우', '롯데', '외야수')
    base1=Bases()
# LG와의 대결. 선발 투수는 임찬규
    lck=PitcherProfile('임찬규', 'LG', '선발', 'R', 'L')
# 선두 타자 황성빈이 안타로 1루에 출루
    base1.set_1B_runner(hsb, lck)
    base1.get_1B_runner()
    base1.print_1B_runner()
    base1.print_runners()
    base1.is_1B_loaded()
    base1.is_empty()
    base1.is_loaded()
    base1.is_scoring_position()
    base1.print_status()
# 고승민의 연속 안타로 황성빈이 3루까지 진루, 고승민은 1루
    base1.move_1B_to_3B()
    base1.set_1B_runner(gsm, lck)
    base1.print_status()
    base1.print_runners()
# 레이예스의 볼넷으로 3루 주자 황성빈은 그대로, 고승민은 2루까지 진루, 레이예스는
# 1루로 출루
    base1.move_1B_to_2B()
    base1.set_1B_runner(rey, lck)    
    base1.print_runners()
    base1.print_status()
    base1.is_scoring_position()
# 선발 투수 임찬규의 폭투로 모든 주자가 한 베이스씩 이동
    base1.score_from_3B(lck)
    base1.move_2B_to_3B()
    base1.move_1B_to_2B()
    base1.print_runners()
    base1.print_status()
    hsb.print_stats()
    lck.print_stats()
# 내야수의 땅볼 실책으로 전준우가 출루, 고승민 득점, 레이예스는 3루까지
# 모든 주자가 비자책으로 변경된 후 출루 및 진루
    base1.get_3B_state().earned=False
    base1.get_2B_state().earned=False    
    base1.score_from_3B(lck)
    base1.move_2B_to_3B()
    base1.set_1B_runner(jjw, lck, False)
    base1.print_runners()
    base1.print_status()
    lck.print_stats()
    gsm.print_stats()