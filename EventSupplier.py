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
    def sample_pitching_event(self, pitcher: PitcherProfile,
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

# 투구 결과 샘플링 함수
    def sample_pitch_result(self, batter: BatterProfile,
                            pitcher: PitcherProfile,
                            bases: Optional[Bases],
                            state: PlateAppearanceState) -> PitchResult:
# 폭투/보크는 주자가 있을 때에만 발생 가능
        if not bases.is_empty():
            pe=self.sample_pitching_event(pitcher, bases)
            if pe==PitchingEvent.WP:
                return PitchResult.WP
            elif pe==PitchingEvent.BALK:
                return PitchResult.BALK
# 타자 객체의 컨택, 선구안, 파워 능력치를 각각 0~1 값으로 보정
        con=self._ability_scale_0_1(batter.contact)
        eye=self._ability_scale_0_1(batter.eye)
        power=self._ability_scale_0_1(batter.power)
# 투수 객체의 구위, 구속, 제구 능력치를 각각 0~1 값으로 보정
        stuff=self._ability_scale_0_1(pitcher.power)
        velo=self._ability_scale_0_1(pitcher.speed)
        cmd=self._ability_scale_0_1(pitcher.command)
# zone_p: 투수가 던진 공이 스트라이크존에 들어올 확률
# 투수의 제구 능력치가 높을수록 증가함
# 타자의 선구안 능력치가 높을수록 감소함
# 하나의 투구가 스트라이크존에 들어올 확률은 최대 0.8, 최소 0.2
        zone_p=self._clamp(0.45+0.25*cmd-0.10*eye, 0.20, 0.80)
# in_zone: 투수가 던진 공이 스트라이크존에 들어왔는지 판별하는 bool 값
        in_zone=self.rng.random()<zone_p

# swing_p: 타자가 스윙할 확률
# 1. 존에 들어온 공일 경우
# 투수의 구속이 높을수록 증가, 타자의 선구안이 높을수록 감소
# 존에 들어온 공을 스윙할 확률은 최대 0.9, 최소 0.2
        if in_zone:
            swing_p=self._clamp(0.55+0.15*(1.0-eye)+0.10*velo,
                                0.20, 0.90)
# 2. 존을 벗어난 공일 경우
# 투수의 제구가 높을수록 증가, 타자의 선구안이 높을수록 감소
# 존을 벗어난 공을 스윙할 확률은 최대 0.7, 최소 0.05
        else:
            swing_p=self._clamp(0.20+0.20*(1.0-eye)+0.05*cmd,
                                0.05, 0.70)
# swung: 타자가 공에 스윙했는지 판별하는 bool 값
        swung=self.rng.random()<swing_p

# 사구: 볼일 때 낮은 확률로 발생
# 제구가 높을수록 사구 확률이 감소
        if not in_zone and not swung and self.rng.random()<0.002*(1.0+1.5*(1.0-cmd)):
            return PitchResult.HBP

# 타자가 스윙을 하지 않은 경우
# 존에 들어왔으면 스트라이크, 벗어났으면 볼
        if not swung:
            return PitchResult.CALLED_STRIKE if in_zone else PitchResult.BALL

# 타자가 스윙을 한 경우
# 컨택에 성공했다면 파울 or 정타(인플레이), 실패했다면 헛스윙
# contact_p: 타자가 컨택에 성공할 확률
# 투수의 구속, 구위가 높을수록 컨택 성공 확률이 감소
# 타자의 컨택이 높을수록 컨택 성공 확률이 증가
# 컨택 성공 확률은 최대 0.95, 최소 0.1
        elif swung:
            contact_p=self._clamp(0.72+0.18*con-0.20*(0.6*stuff+0.4*velo), 
                                  0.10, 0.95)
# 만약 난수 값이 컨택 확률보다 높다면 실패(헛스윙)
            if self.rng.random()>contact_p:
                return PitchResult.SWINGING_STRIKE
# 만약 컨택에 성공했다면 파울 or 정타(인플레이)
# 스트라이크 카운트가 늘어날수록 정타보다는 파울이 좀 더 많이 나온다고 가정
# foul_p: 타자가 친 공이 파울이 될 확률
# 타자의 컨택이 높을수록 파울 확률이 감소, 정타 확률이 증가
# 투수의 구위가 높을수록 파울 확률이 증가, 정타 확률이 감소
# 파울이 될 확률은 최대 0.6, 최소 0.1
            else:
                foul_p=self._clamp(0.30-0.10*con+0.05*state.strikes+0.15*stuff)
                if self.rng.random()<foul_p:
                    return PitchResult.FOUL
                else:
                    return PitchResult.IN_PLAY

# 안타 타구의 비율 분포 설정 함수
# 안타가 났을 때 1/2/3/홈 분포를 파워, 구위로 보정
# 타자의 파워가 높을수록 홈런/2루타 비중이 증가
# 타자의 주력이 높을수록 3루타 비중이 증가
    def _sample_hit_type(self, pow01: float, spe01: float) -> BattingEvent:
# 기본 분포
        s=self.cfg.hit_single_share
        d=self.cfg.hit_double_share
        t=self.cfg.hit_triple_share
        hr=self.cfg.hit_hr_share
# 파워 보정
        hr_adj=0.06*(pow01-0.5)
        d_adj=0.04*(pow01-0.5)
        hr=self._clamp(hr+hr_adj, 0.01, 0.20)
        d=self._clamp(d+d_adj, 0.10, 0.35)
# 주력 보정
        t_adj=0.05*(spe01-0.5)
        t=self._clamp(t+t_adj, 0.0, 0.08)
# 안타 타구가 단타일 확률: 1-장타 확률
        s=1.0-(d+t+hr)
# 단타 확률이 0.4 미만으로 작아지면 보정
        if s<0.40:
            s=0.40
            rem=1.0-(s+t)
            dh=d+hr
            if dh<=1e-9:
                d, hr=rem*0.8, rem*0.2
            else:
                d=rem*(d/dh)
                hr=rem*(hr/dh)
        u=self.rng.random()
        if u<s:
            return BattingEvent.SINGLE
        elif u<s+d:
            return BattingEvent.DOUBLE
        elif u<s+d+t:
            return BattingEvent.TRIPLE
        else:
            return BattingEvent.HOMERUN

# 인플레이 타구의 결과 처리 함수
    def sample_ball_in_play_outcome(
            self, batter: BatterProfile, pitcher: PitcherProfile,
            bases: Optional[Bases], outs: int=0
    ) -> BattingEvent:
# 타자 객체의 컨택, 파워/투수 객체의 구위 수치를 0부터 1 사이의 값으로 보정
        con=self._ability_scale_0_1(batter.contact)
        power=self._ability_scale_0_1(batter.power)
        stuff=self._ability_scale_0_1(pitcher.power)
