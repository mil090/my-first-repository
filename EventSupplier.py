from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import random

from BatterProfile import BatterProfile
from PitcherProfile import PitcherProfile
from Bases import Bases
from Stats import BattingEvent, PitchingEvent

from enum import Enum, auto
# 투구 결과를 반영하는 클래스
class PitchResult(Enum):
    BALL=auto()
    CALLED_STRIKE=auto()
    SWINGING_STRIKE=auto()
    FOUL=auto()
    IN_PLAY=auto()
    HBP=auto()
    WP=auto()
    BALK=auto()

# 볼 카운트 정보를 담고 있는 타석 상태 클래스
@dataclass
class PlateAppearanceState:
    balls: int=0
    strikes: int=0
    is_over: bool=False
    final_event: "BattingEvent|None"=None
    def apply_pitch(self, pr: PitchResult):
# 보크는 볼 카운트에 영향을 주지 않음. 폭투는 볼로 처리
        if pr==PitchResult.BALK:
            return None
# 투구 결과가 볼이면 볼이 1 증가. 폭투는 볼로 처리하며 주자 진루는 이후 구현
# 폭투가 발생하면 일괄적으로 모든 주자 1베이스씩 진루로 처리(3루 주자 득점)
# 볼이 4개가 되면 타석이 종료되고 결과는 볼넷
        if pr in (PitchResult.BALL, PitchResult.WP):
            self.balls+=1
            if self.balls>=4:
                self.is_over=True
                self.final_event=BattingEvent.WALK
# 투구 결과가 몸에 맞는 공이면 그 타석은 즉시 종료되고 결과는 사구
        elif pr==PitchResult.HBP:
            self.is_over=True
            self.final_event=BattingEvent.HBP
# 투구 결과가 스트라이크이면 스트라이크가 1 증가
# 스트라이크가 3개가 되면 타석이 종료되고 결과는 삼진 아웃
        elif pr in (PitchResult.CALLED_STRIKE, PitchResult.SWINGING_STRIKE):
            self.strikes+=1
            if self.strikes>=3:
                self.is_over=True
                self.final_event=BattingEvent.STRIKEOUT
# 투구 (이후 타격) 결과가 파울이면 스트라이크가 조건부로 증가
# 2스트라이크 이전에는 파울이면 스트라이크가 1 증가
# 2스트라이크 이후에는 파울로는 볼 카운트 변화 없음
        elif pr==PitchResult.FOUL:
            if self.strikes<2:
                self.strikes+=1
# 투구 (이후 타격) 결과가 인 플레이(타격)이면 타석이 종료되고 결과는 선수의 능력치에
# 따라 확률로 결정
        elif pr==PitchResult.IN_PLAY:
            self.is_over=True

# 타석 이벤트에 대한 확률 튜닝 클래스
@dataclass
class EventConfig:
# 기본값은 대략적인 기준점으로 놓고, 각 타자/투수의 능력치에 따라 가감을 진행
    base_walk: float=0.08
    base_hbp: float=0.008
    base_so: float=0.20
# 인플레이 타구(PitchResult.IN_PLAY)가 안타가 될 확률
    base_hit_on_ball_in_play: float=0.28
# 인플레이 타구가 안타가 되었을 때, 장타에 대한 확률분포
# 합이 1이 되도록 설정
    hit_single_share: float=0.70
    hit_double_share: float=0.22
    hit_triple_share: float=0.03
    hit_hr_share: float=0.05
# 특수 타격 이벤트(희생타/병살타/진루타 등)는 Game이 상황을 보고 호출하도록 설정
# OUT의 일부를 땅볼, (1사 이하이고 주자가 있다는 가정 하에서) 땅볼의 일부가
# 병살타로 연결된다고 가정
    gidp_given_groundball: float=0.10
    groundball_share_of_outs: float=0.45
# 투수 고유 이벤트 확률
    base_wp: float=0.01
    base_balk: float=0.002