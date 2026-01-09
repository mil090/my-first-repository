from Team import Team
from BatterProfile import BatterProfile
from PitcherProfile import PitcherProfile
from Lineup import Lineup
from Stats import BattingEvent
from Game import Game
lg=Team('LG')
chi=PitcherProfile('치리노스', 'LG', '선발')
tol=PitcherProfile('톨허스트', 'LG', '선발')
lck=PitcherProfile('임찬규', 'LG', '선발', 'R', 'L')
pmk=PitcherProfile('박명근', 'LG', '불펜', 'Rside', 'R')
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
lg.add_player(pmk)
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
cjy=PitcherProfile('최준용', '롯데', '불펜')
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
lotte.add_player(cjy)
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

# 경기 game1을 초기화
game1=Game(lg_lineup, lotte_lineup)
# 초기 점수는 0:0
game1.get_current_score()

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
res_top1=game1.play_half_inning(top_1_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(top_1_events))
print(game1.get_current_score())
# 1회초 종료. 공수교대
game1.switch_sides()
# 1회말: 롯데 공격
# 황성빈 뜬공-고승민 안타-레이예스 2루타-전준우 희생플라이(1타점)-
# 윤동희 2점홈런-나승엽 삼진
bot_1_events=[
    BattingEvent.OUT,
    BattingEvent.SINGLE,
    BattingEvent.DOUBLE,
    BattingEvent.SAC_FLY,
    BattingEvent.HOMERUN,
    BattingEvent.STRIKEOUT
]
res_bot1=game1.play_half_inning(bot_1_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(bot_1_events))
print(game1.get_current_score())
# 1회말 종료. 공수교대
game1.switch_sides()
game1.inning
# 2회초: LG공격
# 박동원 사구-이주헌 2루타-박해민 땅볼(1타점)-홍창기 안타(1타점)-신민재 병살타
top_2_events=[
    BattingEvent.HBP,
    BattingEvent.DOUBLE,
    BattingEvent.GROUNDOUT_RBI,
    BattingEvent.SINGLE,
    BattingEvent.GIDP
]
res_top2=game1.play_half_inning(top_2_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(top_2_events))
game1.get_current_score()
game1.away.get_current_batter().name
# 2회초 종료. 공수교대
game1.switch_sides()
# 2회말: 롯데공격
# 손호영 2루타-유강남 안타-전민재 병살타(1득점)-황성빈 뜬공
bot_2_events=[
    BattingEvent.DOUBLE,
    BattingEvent.SINGLE,
    BattingEvent.GIDP_RUN,
    BattingEvent.OUT
]
res_bot2=game1.play_half_inning(bot_2_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(bot_2_events))
game1.get_current_score()
# 2회말 종료. 공수교대
game1.switch_sides()
# 3회초: LG공격
# 오스틴 2루타-문보경 진루타 뜬공-문성주 희생플라이(1타점)-오지환 삼진
top_3_events=[
    BattingEvent.DOUBLE,
    BattingEvent.FLYOUT_ADV,
    BattingEvent.SAC_FLY,
    BattingEvent.STRIKEOUT
]
res_top3=game1.play_half_inning(top_3_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(top_3_events))
game1.get_current_score()
# 3회초 종료. 공수교대
game1.switch_sides()
# 3회말: 롯데공격
# 고승민 땅볼-레이예스 삼진-전준우 삼진
bot_3_events=[
    BattingEvent.OUT,
    BattingEvent.STRIKEOUT,
    BattingEvent.STRIKEOUT
]
res_bot3=game1.play_half_inning(bot_3_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(bot_3_events))
game1.get_current_score()
# 3회말 종료. 공수교대
game1.is_top
game1.inning
game1.switch_sides()
# 4회초: LG공격
# 박동원 삼진-이주헌 땅볼-박해민 볼넷-홍창기 안타(1타점)-신민재 땅볼
top_4_events=[
    BattingEvent.STRIKEOUT,
    BattingEvent.OUT,
    BattingEvent.WALK,
    BattingEvent.SINGLE,
    BattingEvent.OUT
]
res_top4=game1.play_half_inning(top_4_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(top_4_events))
game1.get_current_score()
# 4회초 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
# 4회말: 롯데공격
game1.home.get_current_batter().name
# 윤동희 안타-나승엽 볼넷-손호영 번트-유강남 사구-전민재 직선타-황성빈 땅볼
bot_4_events=[
    BattingEvent.SINGLE,
    BattingEvent.WALK,
    BattingEvent.SAC_BUNT,
    BattingEvent.HBP,
    BattingEvent.OUT,
    BattingEvent.OUT
]
res_bot4=game1.play_half_inning(bot_4_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(bot_4_events))
game1.get_current_score()
# 4회말 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
# 5회초: LG공격
game1.away.get_current_batter().name
# 오스틴 2루타-문보경 삼진-문성주 진뜬-오지환 안타-박동원 삼진
top_5_events=[
    BattingEvent.DOUBLE,
    BattingEvent.STRIKEOUT,
    BattingEvent.FLYOUT_ADV,
    BattingEvent.SINGLE,
    BattingEvent.STRIKEOUT
]
res_top5=game1.play_half_inning(top_5_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(top_5_events))
game1.get_current_score()
# 5회초 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
# 5회말: 롯데공격
game1.home.get_current_batter().name
# 고승민 삼진-레이예스 2루타-전준우 진땅-윤동희 볼넷-나승엽 2루타(1타점)-
# 손호영 3점홈런-유강남 삼진
bot_5_events=[
    BattingEvent.STRIKEOUT,
    BattingEvent.DOUBLE,
    BattingEvent.GROUNDOUT_ADV,
    BattingEvent.WALK,
    BattingEvent.DOUBLE,
    BattingEvent.HOMERUN,
    BattingEvent.STRIKEOUT
]
res_bot5=game1.play_half_inning(bot_5_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(bot_5_events))
game1.get_current_score()
# 5회말 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
# 6회초: LG공격
game1.away.get_current_batter().name
# 이주헌 땅볼-박해민 땅볼-홍창기 뜬공
top_6_events=[
    BattingEvent.OUT,
    BattingEvent.OUT,
    BattingEvent.OUT
]
res_top6=game1.play_half_inning(top_6_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(top_6_events))
game1.get_current_score()
# 6회초 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
# 6회말: 롯데공격
game1.home.get_current_batter().name
# 전민재 삼진-황성빈 볼넷-고승민 볼넷-레이예스 병살타
bot_6_events=[
    BattingEvent.STRIKEOUT,
    BattingEvent.WALK,
    BattingEvent.WALK,
    BattingEvent.GIDP
]
res_bot6=game1.play_half_inning(bot_6_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(bot_6_events))
game1.get_current_score()
# 6회말 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
# 7회초: LG공격
game1.away.get_current_batter().name
# 투수 박세웅: 투수 정철원으로 교체
game1.home.get_current_pitcher().name
game1.home.change_defense('P', jcw)
game1.home.get_current_pitcher().name
# 신민재 직선타-오스틴 1점홈런-문보경 2루타-문성주 볼넷-오지환 안타-박동원 삼진-
# 이주헌 볼넷(1타점)-박해민 뜬공
top_7_events=[
    BattingEvent.OUT,
    BattingEvent.HOMERUN,
    BattingEvent.DOUBLE,
    BattingEvent.WALK,
    BattingEvent.SINGLE,
    BattingEvent.STRIKEOUT,
    BattingEvent.WALK,
    BattingEvent.OUT
]
res_top7=game1.play_half_inning(top_7_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(top_7_events))
game1.get_current_score()
# 7회초 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
# 7회말: 롯데공격
game1.home.get_current_batter().name
# 전준우 삼진-윤동희 삼진-나승엽 뜬공
bot_7_events=[
    BattingEvent.STRIKEOUT,
    BattingEvent.STRIKEOUT,
    BattingEvent.OUT
]
res_bot7=game1.play_half_inning(bot_7_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(bot_7_events))
game1.get_current_score()
# 7회말 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
game1.is_tie()
# 8회초: LG공격
game1.away.get_current_batter().name
# 홍창기 볼넷-신민재 2루타-오스틴 삼진-문보경 희생플라이(1타점)-문성주 땅볼
top_8_events=[
    BattingEvent.WALK,
    BattingEvent.DOUBLE,
    BattingEvent.STRIKEOUT,
    BattingEvent.SAC_FLY,
    BattingEvent.OUT
]
res_top8=game1.play_half_inning(top_8_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(top_8_events))
game1.get_current_score()
# 8회초 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
# 8회말: 롯데공격
game1.home.get_current_batter().name
# 투수 치리노스: 투수 김진성으로 교체
game1.away.change_defense('P', kjs)
game1.away.get_current_pitcher().name
# 손호영 뜬공-유강남 안타-전민재 볼넷-황성빈 삼진-고승민 뜬공
bot_8_events=[
    BattingEvent.OUT,
    BattingEvent.SINGLE,
    BattingEvent.WALK,
    BattingEvent.STRIKEOUT,
    BattingEvent.OUT
]
res_bot8=game1.play_half_inning(bot_8_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(bot_8_events))
game1.get_current_score()
# 8회말 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
# 9회초: LG공격
game1.away.get_current_batter().name
# 투수 정철원: 투수 김원중으로 교체
game1.home.get_current_pitcher().name
game1.home.change_defense('P', kwj)
# 오지환 2루타-박동원 번트-이주헌 희생플라이(1타점)-박해민 볼넷-홍창기 볼넷-
# 신민재 2루타(1타점)-오스틴 뜬공
top_9_events=[
    BattingEvent.DOUBLE,
    BattingEvent.SAC_BUNT,
    BattingEvent.SAC_FLY,
    BattingEvent.WALK,
    BattingEvent.WALK,
    BattingEvent.DOUBLE,
    BattingEvent.OUT
]
res_top9=game1.play_half_inning(top_9_events)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(top_9_events))
game1.get_current_score()
# 9회초 종료. 공수교대
game1.switch_sides()
game1.inning
game1.is_top
# 9회말: 롯데공격
game1.home.get_current_batter().name
# 투수 김진성: 투수 유영찬으로 교체
game1.away.change_defense('P', yyc)
game1.away.get_current_pitcher().name
# 레이예스 1점홈런-전준우 땅볼-윤동희 볼넷-나승엽 안타-손호영 삼진-유강남 3점홈런(끝내기)
bot_9_events=[
    BattingEvent.HOMERUN,
    BattingEvent.OUT,
    BattingEvent.WALK,
    BattingEvent.SINGLE,
    BattingEvent.STRIKEOUT,
    BattingEvent.HOMERUN
]
res_bot9=game1.play_half_inning(bot_9_events, allow_walkoff=True)
print(f'{game1.inning}회', '초' if game1.is_top else '말', f': {game1.away.team_name if game1.is_top else game1.home.team_name}공격')
game1.print_last_logs(len(bot_9_events))
game1.get_current_score()

lg_lineup=Lineup(lg)
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
lg_lineup.print_current_batting_order()
lg_lineup.print_current_defense()
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

game1=Game(lg_lineup, lotte_lineup)
game1.get_current_score()
events_by_inning_for_game1={1: (top_1_events, bot_1_events),
                            2: (top_2_events, bot_2_events),
                            3: (top_3_events, bot_3_events),
                            4: (top_4_events, bot_4_events),
                            5: (top_5_events, bot_5_events),
                            6: (top_6_events, bot_6_events),
                            7: (top_7_events, bot_7_events),
                            8: (top_8_events, bot_8_events),
                            9: (top_9_events, bot_9_events)}
game1.play_game(events_by_inning_for_game1, 9, 11)
game1.print_last_logs(len(game1.logs))

