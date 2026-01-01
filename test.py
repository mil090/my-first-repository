from Bases import Bases
a=Bases()
a.print_runners()
from BatterProfile import BatterProfile
win_g=BatterProfile('윈지', '롯데', '외야수', 'S', 'S')
from PitcherProfile import PitcherProfile
win_g2=PitcherProfile('윈지2', '롯데', '선발', 'S', 'S')
from Team import Team
lotte=Team('꼴데')
lotte.add_player(win_g)
lotte.add_player(win_g2)
lotte.print_all_players()

import random
a=random.Random(1)
a.randrange(10, 20)