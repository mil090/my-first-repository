# 12. 기록 프로그램
# 야구에서 기록원 역할을 담당할 클래스
# 주의: Stats는 이미 결정된 판정을 보고 이를 기록하는 역할만 함
# 결과를 정하는 것은 실제 경기를 진행하는 Game에서 할 일
# 이미 판정된 이벤트 결과(아웃, 안타 등)를 받아 타자/투수 객체 내의 멤버 변수를
# 적절히 누적/갱신하는 역할

from BatterProfile import BatterProfile
from PitcherProfile import PitcherProfile
# 먼저 타자 or 투수별로 발생할 수 있는 이벤트들을 설계
# Enum을 이용
from enum import Enum, auto
# 12-1. 타자 이벤트 설계
# 오로지 최종 판정 결과만 저장
# 타구 방향, 수비 위치, 주자 진루 등은 반영되지 않음
# KBO 공식 기록에 남는 결과만
# 계열 분리: 안타, 아웃, (안타가 아닌)출루, 특수
class BattingEvent(Enum):
# 안타 계열: 단타, 2루타, 3루타, 홈런
    SINGLE=auto()
    DOUBLE=auto()
    TRIPLE=auto()
    HOMERUN=auto()
# (안타가 아닌) 출루 계열: 볼넷, 고의4구, 사구
    WALK=auto()
    IBB=auto()
    HBP=auto()
# 아웃 계열: 삼진, (삼진이 아닌) 아웃
    STRIKEOUT=auto()
    OUT=auto()
# 진루타 땅볼: 타자는 땅볼로 아웃되나 그 사이 주자가 한 베이스 진루하는 상황
# 진루타 땅볼은 1, 2루 주자에만 해당됨. 3루 주자가 땅볼로 득점하는 것은 따로 구현
    GROUNDOUT_ADV=auto()
# 진루타 타점: 타자는 땅볼로 아웃되나 그 사이 3루 주자가 득점하는 상황
# 진루타 타점은 3루 주자에만 해당됨
    GROUNDOUT_RBI=auto()
# 특수 계열: 병살타, 희생번트, 희생플라이, 득점이 있는 병살타
    GIDP=auto()
    SAC_BUNT=auto()
    SAC_FLY=auto()
    GIDP_RUN=auto()
# 야수선택, 타격방해, 인필드 플라이 등은 추후 처리

# 12-2. 투수 이벤트 설계
# 오로지 최종 판정 결과만 저장
# 타구 방향, 수비 위치, 주자 진루 등은 반영되지 않음
# KBO 공식 기록에 남는 결과만
# 투수 이벤트는 대부분 타자 이벤트와 결과 기준으로 대응
# 타자-안타<->투수-피안타 등
# 여기에 투수만의 고유 이벤트도 존재. 폭투, 보크, 블론세이브 등
# 그러나 타자 이벤트와 연결되는 이벤트는 사용되지 않으므로, 모두 삭제하고 투수 고유
# 이벤트만 남김
class PitchingEvent(Enum):
# 투수의 고유 이벤트
    WP=auto() # 폭투
    BALK=auto() # 보크
# 블론세이브는 나중에 실점 매커니즘을 설계한 후 구현

# 12-3. Stats 클래스 설계
class Stats:
# 기록 클래스는 생성 시 타자, 투수 객체를 입력받음
    def __init__(self, batter:BatterProfile, pitcher:PitcherProfile):
# 입력값 유효성 검사
# batter와 pitcher가 각각 타자/투수 객체가 아니면 TypeError 발생
        if not isinstance(batter, BatterProfile) or not isinstance(pitcher, PitcherProfile):
            raise TypeError(f'batter에는 타자 객체, pitcher에는 투수 객체만 입력할 수 있습니다. 현재 batter의 데이터형은 {type(batter)}, pitcher의 데이터형은 {type(pitcher)}입니다.')
# 입력받은 타자, 투수 객체를 각각 멤버 변수로 저장
        self.batter=batter
        self.pitcher=pitcher
# 현재 투수의 누적 아웃 개수를 저장하는 변수
# 나중에 이닝 계산에 사용(이닝=아웃 수/3)
        self.outs=0

# 타석에서의 기록 처리 함수
# 타자의 결과(BattingEvent)를 입력받아 타자, 투수 기록을 동시에 갱신
# 득점권 여부, 대타 여부는 bool 인자로 받음
# 득점권 여부는 Bases가 알고 있음
# 대타 여부는 Game에서 구현하기
# 처리 순서
# 1. 타자 기록 갱신
# 2. 투수 기록 갱신
# 3. 아웃 수 증가
# 4. 이닝 계산
    def record_plate_appearance(self, event:BattingEvent,
                                is_risp:bool=False, is_ph:bool=False):
# 0. 입력값 유효성 검사
# event가 타자 이벤트가 아니면 TypeError 발생
        if not isinstance(event, BattingEvent):
            raise TypeError(f'event에는 타자의 결과만 입력할 수 있습니다. 현재 event의 데이터형은 {type(event)}입니다.')
        is_hit_event=event in (BattingEvent.SINGLE, BattingEvent.DOUBLE,
                               BattingEvent.TRIPLE, BattingEvent.HOMERUN)
        is_ab_event=event in (BattingEvent.SINGLE, BattingEvent.DOUBLE,
                              BattingEvent.TRIPLE, BattingEvent.HOMERUN,
                              BattingEvent.STRIKEOUT, BattingEvent.OUT,
                              BattingEvent.GIDP, BattingEvent.GROUNDOUT_ADV)
# 1. 타자의 결과가 어떻게 되든, 타석 수는 반드시 1 증가
        self.batter.pa+=1
# 득점권/대타 여부는 타석 시작 시점을 기준으로 판단하므로, 모든 이벤트보다 먼저 
# 분류해 두어야 함
# 득점권 상황이고 event의 결과가 타수 증가 이벤트라면 득점권 타수 1 증가
        if is_risp and is_ab_event:
            self.batter.ab_isp+=1
# 득점권 상황이고 event의 결과가 안타 이벤트라면 득점권 안타 1 증가
        if is_risp and is_hit_event:
            self.batter.pa_hit+=1
# 대타 상황이고 event의 결과가 타수 증가 이벤트라면 대타 타수 1 증가
        if is_ph and is_ab_event:
            self.batter.ph_ab+=1
# 대타 상황이고 event의 결과가 안타 이벤트라면 대타 안타 1 증가
        if is_ph and is_hit_event:
            self.batter.ph_hit+=1

# 2. 이후 이벤트의 종류에 따라 구분
        if event==BattingEvent.SINGLE:
            self._handle_single()
        elif event==BattingEvent.DOUBLE:
            self._handle_double()
        elif event==BattingEvent.TRIPLE:
            self._handle_triple()
        elif event==BattingEvent.HOMERUN:
            self._handle_homerun()

        elif event in (BattingEvent.WALK, BattingEvent.IBB,
                       BattingEvent.HBP):
            self._handle_reach(event)

        elif event==BattingEvent.STRIKEOUT:
            self._handle_strikeout()
        elif event==BattingEvent.OUT:
            self._handle_out()

        elif event==BattingEvent.GIDP:
            self._handle_gidp()
        elif event==BattingEvent.SAC_BUNT:
            self._handle_sac_bunt()
        elif event==BattingEvent.SAC_FLY:
            self._handle_sac_fly()
        elif event==BattingEvent.GROUNDOUT_ADV:
            self._handle_groundout_adv()
        elif event==BattingEvent.GROUNDOUT_RBI:
            self._handle_groundout_rbi()
        elif event==BattingEvent.GIDP_RUN:
            self._handle_gidp_run()
        else:
            raise ValueError(f'Unhandled BattingEvent: {event}')
# 3. 투수가 잡은 아웃카운트 계산
        self._update_outs()
# 4. 매 타석마다 타자와 투수의 비율 스탯 갱신
        self.__class__.update_rate_stats_batter(self.batter)
        self.__class__.update_rate_stats_pitcher(self.pitcher)

# 각 이벤트별 _handle_ 함수 구현
# 1. 단타(SINGLE)
# 타자: ab+1, hit+1, single+1, totalbase+1
# 투수: ab+1, hit+1, out+0(주루사 등의 특수한 상황이 없는 한 아웃은 늘어나지 않음)
    def _handle_single(self):
        self.batter.ab+=1
        self.batter.hit+=1
        self.batter.single+=1
        self.batter.totalbase+=1
        self.pitcher.ab+=1
        self.pitcher.hit+=1
# 2. 2루타(DOUBLE), 3루타(TRIPLE)
# 2루타와 3루타는 각각 single 대신 double과 triple이 1씩 증가
# 루타 수는 2루타에서 2, 3루타에서 3 증가
    def _handle_double(self):
        self.batter.ab+=1
        self.batter.hit+=1
        self.batter.double+=1
        self.batter.totalbase+=2
        self.pitcher.ab+=1
        self.pitcher.hit+=1
    def _handle_triple(self):
        self.batter.ab+=1
        self.batter.hit+=1
        self.batter.triple+=1
        self.batter.totalbase+=3
        self.pitcher.ab+=1
        self.pitcher.hit+=1
# 3. 홈런(HOMERUN)
# 점수 반영은 지금 하지 않음
# 주자 상황을 모르기 때문. 사실 점수는 홈런 이외 다른 안타로도 날 수 있음
# 자책/비자책 구분도 불가능
# 따라서 타점/득점/실점/자책점은 외부 시스템에서 따로 처리
# 이 기능은 추후 Bases 클래스에 추가
# Bases는 누가 어디에 출루해 있고, 그 주자가 어떤 원인으로(자책/비자책) 출루해
# 있는지, 누구의 책임 주자인지 알 수 있기 때문에 Bases에 구현하는 것이 적절
# 추가 과제: Bases 클래스에서 출루한 주자가 누구의 책임 주자인지 알 수 있도록 하는
# 기능을 구현해야 함
# 타자: ab+1, hit+1, hr+1, totalbase+4
# 투수: ab+1, hit+1, hr+1
    def _handle_homerun(self):
        self.batter.ab+=1
        self.batter.hit+=1
        self.batter.hr+=1
        self.batter.totalbase+=4
        self.pitcher.ab+=1
        self.pitcher.hit+=1
        self.pitcher.hr+=1
# 4. 삼진(STRIKEOUT)
# 타자: ab+1, so+1
# 투수: ab+1, so+1, out+1
    def _handle_strikeout(self):
        self.batter.ab+=1
        self.batter.so+=1
        self.pitcher.ab+=1
        self.pitcher.so+=1
        self.outs+=1
# 5. 삼진이 아닌 아웃(OUT)
# 타자: ab+1
# 투수: ab+1, out+1
    def _handle_out(self):
        self.batter.ab+=1
        self.pitcher.ab+=1
        self.outs+=1
# 6. 병살타(GIDP)
# 타자: ab+1, gdp+1
# 투수: ab+1, out+2
# 실점 관련 계산은 역시 Bases와 같은 외부에서 처리
# ex) 1사 만루에서 병살타가 나오면 3루 주자가 홈으로 이동해도 득점 없이 이닝 종료
# ex) 2사 상황에서는 병살타가 성립하지 않음
# 병살타가 될 수 있는 상황에 대한 설정은 Game에서
    def _handle_gidp(self):
        self.batter.ab+=1
        self.batter.gdp+=1
        self.pitcher.ab+=1
        self.outs+=2
# 7. 안타가 아닌 출루(WALK, IBB, HBP)
# 볼넷, 고의4구, 사구는 타수가 올라가지 않음
# 볼넷-타자: walk+1 투수: bb+1
# 고의4구-타자: walk+1, ibb+1 투수: bb+1, ibb+1
# 사구-타자: hbp+1, 투수: hbp+1
    def _handle_reach(self, event:BattingEvent):
# 입력값 유효성 검사
        if event not in (BattingEvent.WALK, BattingEvent.IBB, 
                         BattingEvent.HBP):
            raise ValueError(f'Invalid reach event: {event}')
# 타자 이벤트 중 볼넷, 고의4구, 사구를 위 공식대로 처리
        if event==BattingEvent.WALK:
            self.batter.walk+=1
            self.pitcher.bb+=1
        elif event==BattingEvent.IBB:
            self.batter.walk+=1
            self.batter.ibb+=1
            self.pitcher.bb+=1
            self.pitcher.ibb+=1
        elif event==BattingEvent.HBP:
            self.batter.hbp+=1
            self.pitcher.hbp+=1
        else:
            raise ValueError(f'Invalid reach event: {event}')
# 8. 희생번트, 희생플라이(SAC_BUNT, SAC_FLY)
# 타자: sac+1(희생번트) sf+1(희생플라이)
# 투수: sac+1(피희생번트) sf+1(피희생플라이), out+1
# 참고: 타점/득점/실점/자책점이나 주자 이동은 여기서 구현하지 않음
# 현재 상황이 희번/희플 상황인지 판단하는 것도 여기서는 하지 않음
# 이는 Bases나 Game 등의 외부에서 처리
    def _handle_sac_bunt(self):
        self.batter.sac+=1
        self.pitcher.sac+=1
        self.outs+=1
    def _handle_sac_fly(self):
        self.batter.sf+=1
        self.pitcher.sf+=1
        self.outs+=1
# 9. 득점 없는 진루타 땅볼(GROUNDOUT_ADV)
# 일반 아웃과 똑같이 처리됨(타자는 타수만 증가, 투수는 상대 타수와 아웃 증가)
    def _handle_groundout_adv(self):
        self._handle_out()
# 10. 땅볼 타점(GROUNDOUT_RBI)
# 일반 아웃과 똑같이 처리됨(타자는 타수만 증가, 투수는 상대 타수와 아웃 증가)
    def _handle_groundout_rbi(self):
        self._handle_out()
# 11. 득점이 나오는 병살타(GIDP_RUN)
# Stats에서 처리하는 기록은 병살타와 동일
# 타자: 타수+1, 병살타+1
# 투수: 상대타수+1, 아웃+2
# 득점, 실점은 Game에서 구현
    def _handle_gidp_run(self):
        self._handle_gidp()

# 투수의 고유 이벤트에 대한 기록 처리 함수
# 폭투나 보크는 타석의 결과로 발생하는 결과가 아니기 때문에, record_plate_appearance
# 에 넣어서는 안 됨
# 이들은 타석 도중에서, 또는 타석과 타석 사이에서도 발생 가능(ex. 3볼 이후 폭투)
# 주자 이동과 실점 가능성이 있으며, 이는 Bases에서 구현
    def record_pitching_event(self, event:PitchingEvent):
# 0. 입력값 유효성 검사
# event가 투수 이벤트 객체가 아니면 TypeError 발생
        if not isinstance(event, PitchingEvent):
            raise TypeError(f'event에는 투수의 결과만 입력할 수 있습니다. 현재 event의 데이터형은 {type(event)}입니다.')
# 1. (투수 고유 이벤트의) 분기
        if event==PitchingEvent.WP:
            self._handle_wp()
        elif event==PitchingEvent.BALK:
            self._handle_balk()
        else:
            raise ValueError(f'Unhandled PitchingEvent: {event}')
# 2. 폭투, 보크 함수 구현
    def _handle_wp(self):
        self.pitcher.wp+=1
    def _handle_balk(self):
        self.pitcher.balk+=1

# 투수의 누적 아웃카운트를 계산하는 함수
# 사실 이 기능은 아래 update_rate_stats_pitcher 함수에서 실행
# 이 함수에서는 해당 투수가 잡은 누적 아웃카운트를 그 투수 객체의 멤버 변수 self.out으로
# 옮기는 역할만 함
    def _update_outs(self):
# 만약 잡은 아웃카운트가 없다면 아무것도 하지 않음
        if self.outs==0:
            return
# 해당 경기에서 투수가 잡은 아웃 카운트 수를 개인 누적 아웃 카운트 수에 더함
        self.pitcher.out+=self.outs
# 아웃카운트 수를 투수 객체의 멤버 변수 self.out으로 옮긴 후, self.outs는 다시
# 0으로 초기화해야 함
        self.outs=0

# 카운트 스탯을 통해 비율 스탯을 갱신하는 함수
# 타자 비율 스탯: 타출장, 옵스, 득타율, 대타타율
# 타율(avg): hit/ab
# 출루율(obp): (hit+walk+hbp)/(ab+bb+hbp+sf)
# 장타율(slg): totalbase/ab
# OPS: obp+slg
# 득점권 타율: pa_hit/ab_isp
# 대타 타율: ph_hit/ph_ab
# 투수 비율 스탯: 피안타율, 평균자책점, 이닝당 출루허용률
# 피안타율(avg): hit/ab
# 평균자책점(era): er*9/ip=er*27/out
# 이닝당 출루허용률(WHIP): (hit+bb)/ip=3*(hit+bb)/out
# 0으로 나누는 오류를 방지하는 함수
    @staticmethod
    def _safe_div(number:float, denom:float) -> float:
        return 0.0 if denom==0 else number/denom
# 투수의 이닝을 야구 관례 표기로 바꾸는 함수
# (ex) 잡은 아웃카운트가 17개이면 이닝은 5.2
    @staticmethod
    def _outs_to_ip_decimal(outs:int) -> float:
        full_innings=outs//3
        remainder=outs%3
        return float(f'{full_innings}.{remainder}')
# 내부 계산용 진짜 이닝(아웃카운트/3)을 반환하는 함수
    @staticmethod
    def _outs_to_ip_real(outs:int) -> float:
        return outs/3.0
# 타자의 비율 스탯을 갱신하는 함수
    @staticmethod
    def update_rate_stats_batter(batter):
# 입력값 유효성 검사: batter가 타자 객체가 아니면 TypeError 발생
        if not isinstance(batter, BatterProfile):
            raise TypeError(f'batter에는 타자 객체를 입력해야 합니다. 현재 batter의 데이터형은 {type(batter)}입니다.')
        batter.avg=round(Stats._safe_div(batter.hit, batter.ab), 3)
        obp_denom=batter.ab+batter.walk+batter.hbp+batter.sf
        batter.obp=round(Stats._safe_div(batter.hit+batter.walk+
                                         batter.hbp, obp_denom), 3)
        batter.slg=round(Stats._safe_div(batter.totalbase, batter.ab), 3)
        batter.ops=round(batter.obp+batter.slg, 3)
        batter.risp=round(Stats._safe_div(batter.pa_hit, batter.ab_isp), 3)
        batter.phba=round(Stats._safe_div(batter.ph_hit, batter.ph_ab), 3)
# 투수의 비율 스탯을 갱신하는 함수
    @staticmethod
    def update_rate_stats_pitcher(pitcher):
        if not isinstance(pitcher, PitcherProfile):
            raise TypeError(f'pitcher에는 투수 객체를 입력해야 합니다. 현재 pitcher의 데이터형은 {type(pitcher)}입니다.')
        ip_real=Stats._outs_to_ip_real(pitcher.out)
        pitcher.ip=Stats._outs_to_ip_decimal(pitcher.out)
        pitcher.avg=round(Stats._safe_div(pitcher.hit, pitcher.ab), 3)
        pitcher.era=round(Stats._safe_div(pitcher.erun*9.0, ip_real), 2)
        pitcher.whip=round(Stats._safe_div(pitcher.hit+pitcher.bb, ip_real), 2)
        pitcher.ira=round(Stats._safe_div(pitcher.irs, pitcher.ir), 3)


# 테스트 프로그램
# 외이스와 윤동희의 맞대결 상황
if __name__=='__main__':
    ydh=BatterProfile('윤동희', '롯데', '외야수')
    wei=PitcherProfile('와이스', '한화', '선발')
    stat1=Stats(ydh, wei)
# 2025 와이스 vs 윤동희 맞대결 기록
# 12타석 11타수 5안타 2루타 2 1타점 1볼넷 6삼진
# (가상) 와이스는 윤동희와의 맞대결 도중 폭투와 보크를 한 번씩 저지른 적이 있음
# 단타 3개, 2루타 2개
    for _ in range(3):
        stat1.record_plate_appearance(BattingEvent.SINGLE)
    for _ in range(2):
        stat1.record_plate_appearance(BattingEvent.DOUBLE)
    for _ in range(6):
        stat1.record_plate_appearance(BattingEvent.STRIKEOUT)
    stat1.record_plate_appearance(BattingEvent.WALK)
    stat1.record_pitching_event(PitchingEvent.BALK)
    stat1.record_pitching_event(PitchingEvent.WP)
    ydh.print_stats()
    wei.print_stats()