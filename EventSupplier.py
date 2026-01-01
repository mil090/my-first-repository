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

# 이벤트를 공급하는 클래스
# Game에서 다음 타석 결과를 물으면 그에 대한 이벤트를 뽑아 공급하는 역할
class EventSupplier:
    def __init__(self, seed: Optional[int]=None,
                 config: Optional[EventConfig]=None):
        self.rng=random.Random(seed)
        self.cfg=config or EventConfig()
# 내부 유틸: 확률 보정 함수
    @staticmethod
# _clamp: 각 확률의 최대/최솟값 조정
# 만약 보정된 확률이 이 범위를 넘어간다면 최댓값이나 최솟값으로 제한
# 현실성 보장을 위한 장치. 확률이 제멋대로 극단적인 값으로 튀는 것을 제한
    def _clamp(x: float, lo: float, hi: float) -> float:
        return lo if x<lo else hi if x>hi else x
# _ability_scale_0_1: 선수의 능력치에 대한 표준화
# 각 선수의 능력치 수치는 1부터 100까지 99개의 정수 중 하나
# 따라서 능력치 값에서 1을 뺀 다음 이를 99로 나누어 확률에 사용할 수 있게 보정
    def _ability_scale_0_1(self, x: int) -> float:
        return self._clamp((x-1)/99.0, 0.0, 1.0)
# _soft_adjust: 보정된 확률에 대한 범위 제한
# 앞에서 정의했던 기본 확률에 능력치로 보정한 값을 더해서 이 범위를 최대와 최소
# 사이로 제한
    def _soft_adjust(self, base: float, adj: float, lo: float=0.0,
                     hi: float=0.95) -> float:
        return self._clamp(base+adj, lo, hi)

# 투수 고유 이벤트에 대한 샘플링
    def sample_pitching_evnet(self, pitcher: PitcherProfile,
                              bases: Bases) -> Optional[PitchingEvent]:
        if not isinstance(pitcher, PitcherProfile):
            raise TypeError(f'pitcher에는 투수 객체를 입력해야 합니다. 현재 pitcher의 데이터형은 {type(pitcher)}입니다.')
        if not isinstance(bases, Bases):
            raise TypeError(f'bases에는 베이스 객체를 입력해야 합니다. 현재 bases의 데이터형은 {type(bases)}입니다.')
        runners=bases.count_runners()
# 폭투 및 보크는 주자가 없을 때만 발생하므로, 현재 주자가 없다면 None을 반환
        if runners==0:
            return None
# 투수 객체의 제구 능력치를 0부터 1 사이의 값으로 보정
        cmd=self._ability_scale_0_1(pitcher.command)
# (보정된) 제구 능력치가 낮을수록 폭투/보크 확률 상승
        wp_p=self.cfg.base_wp*(1.0+2.0*(1.0-cmd))*(1.0+0.25*(runners-1))
        balk_p=self.cfg.base_balk*(1.0+2.5*(1.0-cmd))*(1.0+0.25*(runners-1))
# 제구 능력치와 주자 수를 이용하여 폭투/보크 확률을 각각 계산하고, 이들을 각각의 범위 내로 제한
# 폭투 확률은 최대 0.05, 보크 확률은 최대 0.02
        wp_p=self._clamp(wp_p, 0.0, 0.05)
        balk_p=self._clamp(balk_p, 0.0, 0.02)
# 0부터 1까지의 난수를 하나 생성
        u=self.rng.random()
# 이 값이 폭투 확률 미만이면 폭투 결과 반환
        if u<wp_p:
            return PitchingEvent.WP
# 이 값이 폭투 확률보다 크고 폭투 확률+보크 확률보다 작으면 보크 결과 반환
        elif u<wp_p+balk_p:
            return PitchingEvent.BALK
# 이 값이 폭투 확률+보크 확률보다 크다면 None을 반환(폭투/보크 미발생)
        return None