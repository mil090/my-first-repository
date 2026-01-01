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