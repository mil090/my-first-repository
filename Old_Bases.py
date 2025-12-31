# 6. 베이스 프로그램
# 타자와 투수 프로필을 사용하므로 이들을 호출
from BatterProfile import BatterProfile
from PitcherProfile import PitcherProfile
class Bases:
    first, second, third=-1, -2, -3
    def __init__(self):
        self.bases=[None, None, None]
# 왼쪽부터 3루, 2루, 1루
# 주자가 있을 때는 그 주자 객체가 들어가고, 없을 때는 None이 들어감
# 각 베이스에 주자가 있는지 확인하는 함수
    def is_1B_loaded(self):
        return self.bases[self.first] is not None
    def is_2B_loaded(self):
        return self.bases[self.second] is not None
    def is_3B_loaded(self):
        return self.bases[self.third] is not None
# 만루인지 확인하는 함수
    def is_loaded(self):
        return None not in self.bases
# 모든 베이스가 비었는지(주자가 없는지) 확인하는 함수
    def is_empty(self):
        return all(x is None for x in self.bases)
# self.base 내의 모든 요소가 None이어야 True를 반환
# 이외의 경우에는 False를 반환

# 각 베이스에 있는 주자를 반환하는 함수
    def get_1B_runner(self):
        return self.bases[self.first]
    def get_2B_runner(self):
        return self.bases[self.second]
    def get_3B_runner(self):
        return self.bases[self.third]
    def get_runners(self):
        first_runner=self.get_1B_runner()
        second_runner=self.get_2B_runner()
        third_runner=self.get_3B_runner()
        return first_runner, second_runner, third_runner
    
# 각 베이스에 있는 주자의 이름을 출력하는 함수
    def print_1B_runner(self):
        if not self.is_1B_loaded():
            print('1루 주자:')
        else:
            runner=self.bases[self.first]
            if isinstance(runner, (BatterProfile, PitcherProfile)):
                print(f'1루 주자: {runner.name}')
    def print_2B_runner(self):
        if not self.is_2B_loaded():
            print('2루 주자:')
        else:
            runner=self.bases[self.second]
            if isinstance(runner, (BatterProfile, PitcherProfile)):
                print(f'2루 주자: {runner.name}')
    def print_3B_runner(self):
        if not self.is_3B_loaded():
            print('3루 주자:')
        else:
            runner=self.bases[self.third]
            if isinstance(runner, (BatterProfile, PitcherProfile)):
                print(f'3루 주자: {runner.name}')
# 현재 주자 상황을 출력하는 함수
    def print_runners(self):
        self.print_3B_runner()
        self.print_2B_runner()
        self.print_1B_runner()
# 각 베이스의 주자를 설정/삭제하는 함수
# 이때 주자로 입력될 변수는 항상 BatterProfile 또는 PitcherProfile의 객체이어야 함
# 주자 삭제 함수는 그때 있던 주자의 객체를 반환함
    def set_1B_runner(self, runner):
        if not isinstance(runner, (BatterProfile, PitcherProfile)):
            raise TypeError(f'변수 runner에는 타자 또는 투수 객체가 입력되어야 합니다. 현재 runner의 데이터형은 {type(runner)}입니다.')
        self.bases[self.first]=runner
    def set_2B_runner(self, runner):
        if not isinstance(runner, (BatterProfile, PitcherProfile)):
            raise TypeError(f'변수 runner에는 타자 또는 투수 객체가 입력되어야 합니다. 현재 runner의 데이터형은 {type(runner)}입니다.')
        self.bases[self.second]=runner
    def set_3B_runner(self, runner):
        if not isinstance(runner, (BatterProfile, PitcherProfile)):
            raise TypeError(f'변수 runner에는 타자 또는 투수 객체가 입력되어야 합니다. 현재 runner의 데이터형은 {type(runner)}입니다.')
        self.bases[self.third]=runner
# 주자 삭제 함수는 그 베이스에 주자가 있을 때만 실행
    def delete_1B_runner(self):
        if not self.is_1B_loaded():
            raise Exception('현재 1루에 주자가 없습니다.')
        else:
            runner=self.get_1B_runner()
            self.bases[self.first]=None
            return runner
    def delete_2B_runner(self):
        if not self.is_2B_loaded():
            raise Exception('현재 2루에 주자가 없습니다.')
        else:
            runner=self.get_2B_runner()        
            self.bases[self.second]=None
            return runner
    def delete_3B_runner(self):
        if not self.is_3B_loaded():
            raise Exception('현재 3루에 주자가 없습니다.')
        else:
            runner=self.get_3B_runner()
            self.bases[self.third]=None
            return runner
# 베이스를 비우는 함수
# 현재 주자 상황에 관계없이 오류는 발생하지 않음
# 홈런이 나왔을 때 베이스를 비우는 용도로 사용
    def clear_bases(self):
        self.bases[self.first]=None
        self.bases[self.second]=None
        self.bases[self.third]=None
# 현재 주자가 있는 위치를 출력하는 함수
# 없음, 1루, 2루, 3루, 12루, 13루, 23루, 만루
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
# 득점권 상황(2, 3루에 주자 있음)인지 확인하는 함수
    def is_scoring_position(self):
        return self.is_2B_loaded() or self.is_3B_loaded()

# 추가 과제: 출루한 주자가 누구의 책임 주자인지 표시하는 기능을 구현해야 함
# 이에 더불어 이 주자의 출루 원인(자책/비자책)도 표시되어야 함
# 이후 실점/자책점 기록에 사용될 예정

# 테스트 프로그램
if __name__=="__main__":
    hsb=BatterProfile('황성빈', '롯데', '외야수', 'R', 'L')
    gsm=BatterProfile('고승민', '롯데', '내야수', 'R', 'L')
    rey=BatterProfile('레이예스', '롯데', '외야수', 'R', 'S')
    base1=Bases()
    base1.is_1B_loaded()
    base1.is_2B_loaded()
    base1.is_3B_loaded()
    base1.is_loaded()
    base1.is_empty()
    base1.get_1B_runner()
    base1.get_2B_runner()
    base1.get_3B_runner()
    base1.get_runners()
    base1.print_1B_runner()
    base1.print_2B_runner()
    base1.print_3B_runner()
    base1.print_runners()
    base1.print_status()
    base1.set_1B_runner(rey)
    base1.set_2B_runner(gsm)
    base1.set_3B_runner(hsb)
    base1.delete_1B_runner()
    base1.delete_3B_runner()
    base1.delete_2B_runner()
    base1.is_scoring_position()
    base1.clear_bases()
    print('Test End')