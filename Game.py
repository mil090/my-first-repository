# 14. 야구 경기 프로그램
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Dict, Tuple, Mapping, List

from BatterProfile import BatterProfile
from PitcherProfile import PitcherProfile
from Team import Team
from Lineup import Lineup
from Bases import Bases, RunnerState
from Stats import Stats, BattingEvent

# 반 이닝 클래스
@dataclass
class HalfInningResult:
    runs: int
    outs: int
    walkoff: bool=False

# 한 이닝 클래스
@dataclass
class InningResult:
    inning: int
    top: HalfInningResult
# (9회)말은 생략될 수 있음
    bottom: Optional[HalfInningResult]
    score_after: Dict[str, int]
# 경기 종료 여부
# 홈 팀이 리드 중인 상태로 9회 초가 끝나면 그대로 경기 종료
    ended: bool=False

# 타석 로그
@dataclass
class PAlog:
    inning: int
    is_top: bool
    outs_before: int
    batter: str
    pitcher: str
    event: BattingEvent
    runs_scored: int
    outs_added: int
    score_after: Dict[str, int]
    walkoff: bool=False

class Game:
# 최소 목표
# 반 이닝(3아웃) 동안 타석을 진행
# 그동안 Stats로 타자와 투수의 기록을 반영
# Bases로 주자 배치/진루/득점을 반영
# 스코어보드(팀 득점) 반영
    def __init__(self, away: Lineup, home: Lineup):
# Game 객체는 생성될 때 두 팀(원정 팀, 홈 팀)에 대한 라인업 객체를 입력받음
# 입력값 유효성 검사
# 두 객체가 Lineup 객체가 아니면 TypeError 발생
        if not isinstance(away, Lineup) or not isinstance(home, Lineup):
            raise TypeError(f'away와 home에는 각각 Lineup 객체를 입력해야 합니다. 현재 away의 데이터형은 {type(away)}, home의 데이터형은 {type(home)}입니다.')
# 원정 팀과 홈 팀의 라인업 객체를 각각 멤버 변수로 저장
        self.away=away
        self.home=home
# 경기 상태를 나타내는 변수들을 생성 및 초기화
        self.inning: int=1
        self.is_top: bool=True
        self.bases=Bases()
# 점수판: 딕셔너리 형태
        self.score: Dict[str, int]={
            self.away.team: 0,
            self.home.team: 0
        }
        self.logs: List[PAlog]=[]
# 공수 라인업 선택 헬퍼
# is_top이 True이면 이닝 초이므로 원정 팀 공격, 홈 팀 수비
# is_top이 False이면 이닝 말이므로 홈 팀 공격, 원정 팀 수비
    def _offense(self) -> Lineup:
        return self.away if self.is_top else self.home
    def _defense(self) -> Lineup:
        return self.home if self.is_top else self.away
# 타석 로그 출력 헬퍼
# 최근 n개의 기록을 출력. 기본값은 10
    def print_last_logs(self, n: int=10):
        for row in self.logs[-n:]:
            half='초' if row.is_top else '말'
            print(f'{row.inning}회 {half} outs:{row.outs_before} '
                  f'{row.batter} vs {row.pitcher} -> {row.event.name} '
                  f'(R+{row.runs_scored}, O+{row.outs_added}) '
                  f'{"WALKOFF" if row.walkoff else ""}')

# "판정" 공급
    def play_half_inning(self, events: Iterable[BattingEvent],
                         allow_walkoff: bool=False) -> HalfInningResult:
# offense: 공격 팀, defense: 수비 팀
# 각각은 라인업 객체
        offense=self._offense()
        defense=self._defense()
# 이닝 시작 전 수비 팀의 수비 위치 유효성 검사
        defense.validate_defense()
# 이닝 시작 전 베이스, 아웃 카운트, 득점 초기화
        self.bases.clear_bases()
        outs=0
        runs_total=0
        runs_scored=0
# 끝내기 가능 여부를 나타내는 bool 값을 생성
        walkoff=False
# 끝내기 판정에 필요한 기준 점수(이 반이닝 시작 시점 기준)
        away_before=self.score[self.away.team]
        home_before=self.score[self.home.team]
        for event in events:
# 3아웃이 되면 이닝 교대
            if outs>=3:
                break
            batter=offense.get_current_batter()
            pitcher=defense.get_current_pitcher()
            if batter is None or pitcher is None:
                raise ValueError('타자 또는 투수 객체가 없습니다. 라인업/수비 배정을 확정하세요.')
# 타석 시작 전 득점권 여부 확인
            is_risp=self.bases.is_scoring_position()
# 대타 여부는 아직 Game에서 결정하지 않으니, 우선은 False로 설정
            stat=Stats(batter, pitcher)
            stat.record_plate_appearance(event, is_risp=is_risp, is_ph=False)
            outs_before_pa=outs
            add_outs, add_runs=self._apply_batting_event(event, batter, pitcher, outs_before=outs)
            outs+=add_outs
            runs_scored+=add_runs
            runs_total+=add_runs
# 타석의 결과를 로그에 추가
# 반이닝 내 누적 득점(runs_scored)을 반영한 score 스냅샷을 생성
            score_snapshot=self.get_current_score()
            if offense is self.away:
                score_snapshot[self.away.team_name]+=runs_scored
            else:
                score_snapshot[self.home.team_name]+=runs_scored
            self.logs.append(PAlog(
                inning=self.inning,
                is_top=self.is_top,
                outs_before=outs_before_pa,
                batter=batter.name,
                pitcher=pitcher.name,
                event=event,
                runs_scored=add_runs,
                outs_added=add_outs,
                score_after=score_snapshot,
                walkoff=False
            ))
# 끝내기 상황 확인
# 홈 공격(말)이고 9회 이상이면 끝내기가 가능한 상황
            if allow_walkoff:
                if not self.is_top and self.inning>=9:
# 이 반이닝(9회 이상 말 공격)에서 홈 팀이 얻는 점수는 runs_scored
# 끝내기 가능 이닝에서 홈 팀의 점수가 원정 팀 점수를 앞서는 순간 그대로 경기 종료
                    if home_before+runs_scored>away_before:
                        walkoff=True
                        self.score[offense.team]+=runs_scored
# 만약 끝내기로 경기가 종료되었다면 로그의 맨 마지막에 최종 점수를 최신화하고, walkoff
# bool 값을 True로 변경
                        if self.logs:
                            self.logs[-1].walkoff=True
                            self.logs[-1].score_after=self.get_current_score()
                        runs_scored=0
                        break
# 타석 결과에 따라 아웃과 득점을 처리한 후 타순을 이동
            offense.next_batter()
# 끝내기 상황이 아닐 때, 이벤트 반복문이 끝났는데 3아웃이 채워지지 않았다면 오류 발생
        if outs<3 and not walkoff:
            raise RuntimeError('제시된 이벤트가 3아웃이 되기 전에 모두 소진되었습니다. 3아웃이 채워지도록 추가 이벤트를 작성하세요.')
        self.score[offense.team]+=runs_scored
        return HalfInningResult(runs=runs_total, outs=outs, walkoff=walkoff)
# 공수를 교대하는 함수
# 이닝의 초가 끝나면 말로 이동, 말이 끝나면 다음 이닝 초로 이동
    def switch_sides(self):
        if self.is_top:
            self.is_top=False
        else:
            self.is_top=True
            self.inning+=1
    def _apply_batting_event(self, event: BattingEvent, batter: BatterProfile, 
                             current_pitcher: PitcherProfile, outs_before: int) -> Tuple[int, int]:
# 특정 베이스의 주자 득점을 처리하는 함수
        def score_from(base: int) -> int:
            if base==3 and self.bases.is_3B_loaded():
                self.bases.score_from_3B(current_pitcher)
                return 1
            if base==2 and self.bases.is_2B_loaded():
                self.bases.score_from_2B(current_pitcher)
                return 1
            if base==1 and self.bases.is_1B_loaded():
                self.bases.score_from_1B(current_pitcher)
                return 1
            return 0
        runs=0
        outs_added=0
# 진루타 땅볼(타자 아웃, 주자는 1베이스 진루, 1/2루 주자 한정)
        if event==BattingEvent.GROUNDOUT_ADV:
            outs_added=1
# 2아웃 이후라면 진루타는 의미가 없으므로 땅볼(OUT)과 같은 효과(이후 잔루에 반영)
            if outs_before<=1:
                if self.bases.is_2B_loaded() and not self.bases.is_3B_loaded():
                    self.bases.move_2B_to_3B()
                if self.bases.is_1B_loaded() and not self.bases.is_2B_loaded():
                    self.bases.move_1B_to_2B()
            return outs_added, 0
# 땅볼 타점이 발생했을 때
# 3루 주자 득점, 다른 주자들은 1베이스씩 진루
        if event==BattingEvent.GROUNDOUT_RBI:
            outs_added=1
            runs=0
# 만약 2아웃이라면 땅볼 아웃으로는 득점이 이루어질 수 없음
            if outs_before>=2:
                return outs_added, runs
# 만약 3루에 주자가 없으면 득점이 이루어질 수 없음
# 이후 이벤트를 공급하는 파일에서 땅볼 타점은 3루에 주자가 있고 2사가 아닐 때만
# 발생하도록 구현(그렇게 되면 아래 조건문은 의미가 없어짐)
            if not self.bases.is_3B_loaded():
                return outs_added, runs
# 먼저 3루 주자 득점
            runs+=score_from(3)            
            batter.rbi+=1
# 이후 다른 주자들의 강제 진루
# 2루 주자는 3루로, 1루 주자는 2루로 진루
# 3루는 반드시 비어 있으므로 조건문으로 또 확인할 필요가 없음
            if self.bases.is_2B_loaded():
                self.bases.move_2B_to_3B()
# 위 조건문이 실행되든 되지 않든 여기까지 왔으면 2루는 비어 있음
            if self.bases.is_1B_loaded():
                self.bases.move_1B_to_2B()
            return outs_added, runs
# 아웃 이벤트가 발생했을 때
# 지금은 어떤 아웃이든 득점이 인정되지 않도록 설정되어 있음
# 그러나 실제로는 아웃 이벤트에서도 득점은 발생할 수 있음(주자 3루에서 땅볼 등)
# 이는 추후에 수정하도록 하자
        if event in (BattingEvent.STRIKEOUT, BattingEvent.OUT):
            outs_added=1
            return outs_added, 0
# 병살타가 발생했을 때
        if event==BattingEvent.GIDP:
# 병살타는 무사 또는 1사에 1루 주자가 있을 때에만 발생 가능
# 위 조건을 만족하지 않는다면 그냥 OUT과 같은 방법으로 처리
            if outs_before<=1 and self.bases.is_1B_loaded():
                first_state=self.bases.delete_1B_runner()
                outs_added=2
            else:
                outs_added=1
            return outs_added, 0
# 득점이 나오는 병살타가 발생했을 때
# 득점이 기록되더라도 타자에게 타점은 인정되지 않음
        if event==BattingEvent.GIDP_RUN:
# 2아웃이면 병살타가 성립하지 않으므로 그냥 아웃만 하나 늘어남
# 추후 이벤트 공급 파일에서 2사 이후에는 병살타가 아예 나오지 않도록 설계
            if outs_before>=2:
                outs_added=1
                return outs_added, 0
# 1아웃이면 병살타와 동시에 (반)이닝 종료
# 득점은 발생할 수 없음
            elif outs_before==1:
                if self.bases.is_1B_loaded():
                    first_state=self.bases.delete_1B_runner()
                    outs_added=2
                else:
                    outs_added=1
                return outs_added, 0
# 0아웃이면 병살타로도 득점은 발생하나 타자의 타점은 올라가지 않음
# 다만 투수의 실점(상황에 따라 자책점까지)은 올라감(이는 Bases에서 이미 구현)
# 주자가 1/3루였다면 모든 주자가 사라지고, 만루였다면 2루 주자가 3루로 진루
            elif outs_before==0:
                if not self.bases.is_1B_loaded():
                    outs_added=1
                    return outs_added, 0
                outs_added=2
                if self.bases.is_3B_loaded():
                    runs+=score_from(3)
                if self.bases.is_2B_loaded():
                    self.bases.move_2B_to_3B()
                if self.bases.is_1B_loaded():
                    first_state=self.bases.delete_1B_runner()
                return outs_added, runs
# 희생번트가 발생했을 때
# 편의상 스퀴즈는 생각하지 않기로 함(일단 1루->2루 진루, 2루->3루 진루, 또는 둘 다 동시만)
        if event==BattingEvent.SAC_BUNT:
            outs_added=1
# 희생번트가 나왔을 때 2루에 주자가 있었다면 3루로 이동
            if self.bases.is_2B_loaded() and (not self.bases.is_3B_loaded()):
                self.bases.move_2B_to_3B()
# 그 다음으로 1루에 주자가 있었다면 2루로 이동
            if self.bases.is_1B_loaded() and (not self.bases.is_2B_loaded()):
                self.bases.move_1B_to_2B()
            return outs_added, 0
# 희생플라이가 발생했을 때
        if event==BattingEvent.SAC_FLY:
            outs_added=1
# 2사가 아니고 3루에 주자가 있었다면 3루 주자 득점
# 이후 희생플라이를 친 타자에게 타점을 추가
            if outs_before<=1 and self.bases.is_3B_loaded():
                runs+=score_from(3)
                batter.rbi+=1
            return outs_added, runs
# 안타가 아닌 출루 이벤트가 발생했을 때
        if event in (BattingEvent.WALK, BattingEvent.IBB, BattingEvent.HBP):
            add_runs=self.bases.force_advance_on_walk(batter, current_pitcher, earned=True)
            runs+=add_runs
# 만약 밀어내기로 득점이 발생했다면 타자에게 타점을 부여
            if add_runs:
                batter.rbi+=add_runs
            return 0, runs
# 안타 이벤트가 발생했을 때
# 우선 최소 규칙에 따라 처리하고 이후 변경
# 단타: 모든 주자 1베이스 진루(3루 주자만 득점)
        if event==BattingEvent.SINGLE:
            if self.bases.is_3B_loaded():
                runs+=score_from(3)
                batter.rbi+=1
            if self.bases.is_2B_loaded() and not self.bases.is_3B_loaded():
                self.bases.move_2B_to_3B()
            if self.bases.is_1B_loaded() and not self.bases.is_2B_loaded():
                self.bases.move_1B_to_2B()
            self.bases.set_1B_runner(batter, current_pitcher, earned=True)
            return 0, runs
# 2루타: 2/3루 주자 득점, 1루 주자는 3루까지
        if event==BattingEvent.DOUBLE:
            if self.bases.is_3B_loaded():
                runs+=score_from(3)
                batter.rbi+=1
            if self.bases.is_2B_loaded():
                runs+=score_from(2)
                batter.rbi+=1
            if self.bases.is_1B_loaded():
                if not self.bases.is_3B_loaded():
                    self.bases.move_1B_to_3B()
# 그럴 일은 없겠지만, 만약 위 조건문 처리 후 3루에 주자가 있다면 1루 주자는 일단
# 2루까지만 이동
                else:
                    if not self.bases.is_2B_loaded():
                        self.bases.move_1B_to_2B()
            self.bases.set_2B_runner(batter, current_pitcher, earned=True)
            return 0, runs
# 3루타: 모든 주자 득점
        if event==BattingEvent.TRIPLE:
            if self.bases.is_3B_loaded():
                runs+=score_from(3)
                batter.rbi+=1
            if self.bases.is_2B_loaded():
                runs+=score_from(2)
                batter.rbi+=1
            if self.bases.is_1B_loaded():
                runs+=score_from(1)
                batter.rbi+=1
            self.bases.set_3B_runner(batter, current_pitcher, earned=True)
            return 0, runs
# 홈런: 모든 주자 득점 후 타자까지 득점
        if event==BattingEvent.HOMERUN:
            if self.bases.is_3B_loaded():
                runs+=score_from(3)
                batter.rbi+=1
            if self.bases.is_2B_loaded():
                runs+=score_from(2)
                batter.rbi+=1
            if self.bases.is_1B_loaded():
                runs+=score_from(1)
                batter.rbi+=1
            batter.run+=1
            batter.rbi+=1
            current_pitcher.run+=1
            current_pitcher.erun+=1
            runs+=1
            return 0, runs
        raise ValueError(f'아직 처리되지 않은 이벤트: {event}')

# 초 공격과 말 공격을 하나로 묶어 한 이닝을 진행하는 함수
    def play_inning(self, top_events: Iterable[BattingEvent],
                    bot_events: Iterable[BattingEvent]) -> InningResult:
        cur_inning=self.inning
# 초(원정 팀 공격)
        self.is_top=True
        top_res=self.play_half_inning(top_events)
# 홈 팀이 리드하는 상황에서 9회초가 끝나면 9회말 없이 경기 종료
# 추후 경기 종료/연장전 진행 규칙 구현
        if cur_inning>=9:
            away_score=self.score[self.away.team]
            home_score=self.score[self.home.team]
            if home_score>away_score:
                return InningResult(
                    inning=cur_inning,
                    top=top_res,
                    bottom=None,
                    score_after=self.get_current_score(),
                    ended=True
                )
# 공수교대
        self.switch_sides()
# 말(홈 팀 공격)
# 말 공격은 allow_walkoff가 True. 따라서 끝내기 상황에 대한 조건문 검사가 이루어짐
# allow_walkoff가 True라고 해서 무조건 끝내기 상황이 되는 것은 아님(혼동 금지)
# 끝내기 상황으로 판별되면 ended를 True로 설정하여 바로 경기 종료
# 다음 이닝으로 넘어가지 않음
        bot_res=self.play_half_inning(bot_events, allow_walkoff=True)
        if bot_res.walkoff:
            return InningResult(
                inning=cur_inning,
                top=top_res,
                bottom=bot_res,
                score_after=self.get_current_score(),
                ended=True
            )
# 다음 이닝 초로 이동
        self.switch_sides()
# 만약 9회 말 도중 홈 팀이 앞서면 끝내기 상황(이는 추후 구현)
        ended=False
        if cur_inning>=9:
            away_score=self.score[self.away.team]
            home_score=self.score[self.home.team]
            if home_score!=away_score:
                ended=True
# 이닝 결과를 반환
        return InningResult(
            inning=cur_inning,
            top=top_res,
            bottom=bot_res,
            score_after=self.get_current_score(),
            ended=ended
        )

# 경기 진행 루프
# 정규 이닝은 9회, 연장 최대 이닝은 (KBO 기준) 11회
    def play_game(
            self,
            events_by_inning: Mapping[int, Tuple[Iterable[BattingEvent], Iterable[BattingEvent]]],
            regulation_innings: int=9, max_innings: int=11
    ) -> List[InningResult]:
# {이닝 번호: (초 이벤트, 말 이벤트)}
# 최대 이닝: 기본적으로 9회. 연장은 추후 구현
# 반환값은 이닝별 결과를 저장한 리스트
        results: List[InningResult]=[]
# 항상 1회초부터 시작하도록 초기화
        self.inning=1
        self.is_top=True
        while self.inning<=max_innings:
            inn=self.inning
            if inn not in events_by_inning:
                raise RuntimeError(f"{inn}회 이벤트가 제공되지 않았습니다.")
            top_events, bot_events=events_by_inning[inn]
            res=self.play_inning(top_events, bot_events)
            results.append(res)
# 만약 res의 ended가 True이면 경기 종료
            if res.ended:
                return results
# 만약 현재 이닝이 정규이닝(기본 9회) 미만이면 반복문을 계속 진행
            if inn<regulation_innings:
                continue
# 현재 이닝이 정규이닝(기본 9회) 이상인데 동점이면 계속해서 연장전 진행
# 동점이 아니라면 (홈팀의 끝내기 승리로) 경기 종료
            if not self.is_tie():
                return results
# 동점이라면 while 반복문에 의해 다음 이닝으로 자동 이동(play_inning 함수 내에
# 이닝 교대 함수가 들어 있음)
        raise RuntimeError(f'{max_innings}회까지 진행했으나 승부가 나지 않았습니다.')

# 현재 팀별 점수를 반환하는 함수
    def get_current_score(self) -> Dict[str, int]:
        score_by_team={self.away.team_name: self.score[self.away.team],
                       self.home.team_name: self.score[self.home.team]}
        return score_by_team

# 연장전 구현을 위한 환경 구축
# 동점 상황인지 반환하는 함수
    def is_tie(self) -> bool:
        return self.score[self.away.team]==self.score[self.home.team]

# 테스트 프로그램
if __name__=='__main__':
# LG:롯데 in 사직야구장
# LG 엔트리
# 투수: 치리노스, 톨허스트, 임찬규, 김진성, 유영찬
# 포수: 박동원, 이주헌
# 내야수: 오스틴, 문보경, 오지환, 신민재, 구본혁
# 외야수: 홍창기, 문성주, 박해민, 송찬의
# 롯데 엔트리
# 투수: 로드리게스, 비슬리, 박세웅, 정철원, 김원중
# 포수: 유강남, 정보근
# 내야수: 고승민, 나승엽, 손호영, 전민재, 이호준
# 외야수: 황성빈, 레이예스, 전준우, 윤동희

# LG 라인업
# 홍창기(RF)-신민재(2B)-오스틴(1B)-문보경(3B)-문성주(LF)-오지환(SS)-박동원(DH)-
# 이주헌(C)-박해민(CF)
# 선발 투수: 치리노스
# 롯데 라인업
# 황성빈(CF)-고승민(2B)-레이예스(LF)-전준우(DH)-윤동희(RF)-나승엽(1B)-손호영(3B)-
# 유강남(C)-전민재(SS)
# 선발 투수: 박세웅
    lg=Team('LG')
    chi=PitcherProfile('치리노스', 'LG', '선발')
    tol=PitcherProfile('톨허스트', 'LG', '선발')
    lck=PitcherProfile('임찬규', 'LG', '선발', 'R', 'L')
    kjs=PitcherProfile('김진성', 'LG', '불펜', 'R', 'L')
    yyc=PitcherProfile('유영찬', 'LG', '불펜', 'R', 'L')
    pdw=BatterProfile('박동원', 'LG', '포수')
    ljh=BatterProfile('이주헌', 'LG', '포수')
    aus=BatterProfile('오스틴', 'LG', '내야수')
    mbk=BatterProfile('문보경', 'LG', '내야수', 'R', 'L')
    ojh=BatterProfile('오지환', 'LG', '내야수', 'R', 'L')
    kbh=BatterProfile('구본혁', 'LG', '내야수')
    smj=BatterProfile('신민재', 'LG', '내야수', 'R', 'L')
    hck=BatterProfile('홍창기', 'LG', '외야수', 'R', 'L')
    msj=BatterProfile('문성주', 'LG', '외야수', 'L', 'L')
    phm=BatterProfile('박해민', 'LG', '외야수', 'R', 'L')
    sce=BatterProfile('송찬의', 'LG', '외야수')
    lg.add_player(chi)
    lg.add_player(tol)
    lg.add_player(lck)
    lg.add_player(kjs)
    lg.add_player(yyc)
    lg.add_player(pdw)
    lg.add_player(ljh)
    lg.add_player(aus)
    lg.add_player(mbk)
    lg.add_player(ojh)
    lg.add_player(kbh)
    lg.add_player(smj)
    lg.add_player(hck)
    lg.add_player(msj)
    lg.add_player(phm)
    lg.add_player(sce)
    lg.print_all_players()
    lg_lineup=Lineup(lg)
# LG 선발 타순 및 수비 위치 설정
    lg_lineup.set_batting_order([hck, smj, aus, mbk, msj, ojh, 
                                 pdw, ljh, phm])
    lg_lineup.assign_position('RF', hck)    
    lg_lineup.assign_position('2B', smj)
    lg_lineup.assign_position('1B', aus)
    lg_lineup.assign_position('3B', mbk)
    lg_lineup.assign_position('LF', msj)
    lg_lineup.assign_position('SS', ojh)
    lg_lineup.assign_position('C', ljh)
    lg_lineup.assign_position('CF', phm)
    lg_lineup.assign_position('P', chi)
    lg_lineup.assign_position('DH', pdw)
    lg_lineup.bench

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
    rod=PitcherProfile('로드리게스', '롯데', '선발')
    bea=PitcherProfile('비슬리', '롯데', '선발')
    lhj=BatterProfile('이호준', '롯데', '내야수', 'R', 'L')
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
    lotte.add_player(rod)
    lotte.add_player(bea)
    lotte.add_player(lhj)
    lotte_lineup=Lineup(lotte)
    lotte_lineup.set_batting_order([hsb, gsm, reyes, jjw, ydh, nsy,
                                    shy, ykn, jmj])
    lotte_lineup.assign_position('CF', hsb)
    lotte_lineup.assign_position('2B', gsm)
    lotte_lineup.assign_position('LF', reyes)
    lotte_lineup.assign_position('DH', jjw)
    lotte_lineup.assign_position('RF', ydh)
    lotte_lineup.assign_position('1B', nsy)
    lotte_lineup.assign_position('3B', shy)
    lotte_lineup.assign_position('C', ykn)
    lotte_lineup.assign_position('SS', jmj)
    lotte_lineup.assign_position('P', psw)
    lotte_lineup.print_current_defense()
    lotte_lineup.validate_defense()
    lotte_lineup.bench

# 1회초: LG 공격
# 홍창기 안타-신민재 볼넷-오스틴 진루타 땅볼-문보경 2루타(2타점)-문성주 삼진-오지환 땅볼
    top_1_events=[
        BattingEvent.SINGLE,
        BattingEvent.WALK,
        BattingEvent.GROUNDOUT_ADV,
        BattingEvent.DOUBLE,
        BattingEvent.STRIKEOUT,
        BattingEvent.OUT
    ]
# 1회말: 롯데 공격
# 황성빈 뜬공-고승민 안타-레이예스 2루타-전준우 희생플라이-윤동희 홈런-나승엽 삼진
    bot_1_events=[
        BattingEvent.OUT,
        BattingEvent.SINGLE,
        BattingEvent.DOUBLE,
        BattingEvent.SAC_FLY,
        BattingEvent.HOMERUN,
        BattingEvent.STRIKEOUT
    ]
# 2회초: LG공격
# 박동원 사구-이주헌 2루타-박해민 땅볼(1타점)-홍창기 안타(1타점)-신민재 병살타
    top_2_events=[
        BattingEvent.HBP,
        BattingEvent.DOUBLE,
        BattingEvent.GROUNDOUT_RBI,
        BattingEvent.SINGLE,
        BattingEvent.GIDP
    ]
# 2회말: 롯데공격
# 손호영 2루타-유강남 안타-전민재 병살타(1득점)-황성빈 뜬공
    bot_2_events=[
        BattingEvent.DOUBLE,
        BattingEvent.SINGLE,
        BattingEvent.GIDP_RUN,
        BattingEvent.OUT
    ]
# 경기 game1을 초기화
    game1=Game(lg_lineup, lotte_lineup)
# 초기 점수는 0:0
    game1.get_current_score()
# 1회초 LG공격
    res_top1=game1.play_half_inning(top_1_events)
    print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
    for event in top_1_events:
        print(event)
    print(res_top1)
    print(game1.get_current_score())
    game1.print_last_logs(len(game1.logs))
# 1회초 종료. 공수교대
    game1.switch_sides()
# 1회말 롯데공격
    res_bot1=game1.play_half_inning(bot_1_events)
    print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
    for event in bot_1_events:
        print(event)
    print(res_bot1)
    print(game1.get_current_score())
    game1.print_last_logs(len(game1.logs))
# 1회말 종료. 공수교대
    game1.switch_sides()
    game1.inning
# 2회초 LG공격
    res_top2=game1.play_half_inning(top_2_events)
    print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
    game1.print_last_logs(len(game1.logs))
    game1.get_current_score()
    game1.away.get_current_batter().name
    ydh.print_stats()
    chi.print_stats()
# 2회초 종료. 공수교대
    game1.switch_sides()
    game1.inning
    game1.is_top
    res_bot2=game1.play_half_inning(bot_2_events)
    game1.print_last_logs(len(game1.logs))
    game1.get_current_score()
    jmj.print_stats()

# 1이닝 진행 프로그램으로 병합
# 아래를 실행하기 전에 라인업을 초기화할 것
    events_by_inning1={1: (top_1_events, bot_1_events)}
    game1=Game(lg_lineup, lotte_lineup)
    results1=game1.play_game(events_by_inning1, regulation_innings=1)
    game1.score
    game1.is_tie()
    for r in results1:
        print(f"{r.inning}회 종료: {r.score_after}")
    game1.logs
    game1.print_last_logs(len(game1.logs))
    game1.get_current_score()
    game1.away.get_current_batter().name
    game1.home.get_current_batter().name

# 또 다른 경기: 끝내기 테스트
# 아래를 실행하기 전에 두 팀의 라인업을 초기화할 것
    game2=Game(lg_lineup, lotte_lineup)
    three_outs=[BattingEvent.OUT, BattingEvent.OUT, BattingEvent.OUT]
    events_by_inning2={inn: (three_outs, three_outs)
                       for inn in range(1, 10)}
# 10회 초: 삼자범퇴
    top_10_events=three_outs
# 10회 말: 2아웃 이후 볼넷, 홈런
    bot_10_events=[BattingEvent.OUT, BattingEvent.OUT, BattingEvent.WALK, BattingEvent.HOMERUN]
    events_by_inning2[10]=(top_10_events, bot_10_events)
    results2=game2.play_game(events_by_inning2, regulation_innings=9,
                             max_innings=11)
    for r in results2:
        print(r.inning, r.score_after, 'ended' if r.ended else "", 
              'walkoff' if (r.bottom and r.bottom.walkoff) else "")