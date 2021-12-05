# 2021-12-05 이종은 작성

class Seat: # 좌석 클래스
    def __init__(self, num, group): # Seat의 parameter: num(좌석 번호), group(분단 번호)
        # Seat의 멤버변수
        self.num = num
        self.state = False # 멤버변수 state # 디폴트 값은 False(사용 안 하는 중)
        self.sign = 'x'
        self.group = group # 속한 분단

    # 멤버함수 목록
    def use(self): # 좌석 이용 시작
        self.state = True
        self.sign = 'o'

    def end(self): # 좌석 이용 종료
        self.state = False
        self.sign = 'x'

class Prefer: # 선호 정보 클래스
    def __init__(self, distance, acheater, window, door): # parameter는 True나 False 값으로 주어져야 함.
        self.distance = distance # 거리두기 # True면 거리두기를 원함
        self.acheater = acheater # AC or 히터 # True면 AC/히터 먼 좌석을 원함 
        self.window = window # 창문 # True면 창문 먼 좌석을 원함
        self.door = door # 문 # True면 출입구 먼 좌석을 원함

def res(seat, time): # 좌석 예약
    # 주어진 time이 되면 자동으로 use 함수 쓸 수 있도록 설계
    seat.use()
    # 개발 중

def recommend(entireSeat, prefer): # 좌석 추천 # parameter 중 prefer는 Prefer 클래스 # entireSeat는 좌석 현황(parameter로 안 주어지고 전역 변수 바로 변경하도록 수정할 수도 있음)
    reclist = [x for x in range(1, 25)]

    if prefer.distance: # 거리두기(기준 좌석 근처의 state가 True면 추천 안 함)
        # 개발 중
        print(1)

    if prefer.acheater:
        for k in [19, 20, 23, 24]:
            if k in reclist:
                reclist.remove(k)

    if perfer.window:
        for k in [1, 2, 3, 4, 8, 12, 16, 20, 24]:
            if k in reclist:
                reclist.remove(k)
    
    if perfer.door:
        for k in [17, 18, 21, 22]:
            if k in reclist:
                reclist.remove(k)

    return reclist # 추천하는 seat의 num 리스트를 return

for i in range(1, 25):
    if 8 >= i and i >= 1: 
        globals()['seat{}'.format(i)] = Seat(i, 1)
    elif 16 >= i and i >= 9: 
        globals()['seat{}'.format(i)] = Seat(i, 2)
    elif 24 >= i and i >= 17: 
        globals()['seat{}'.format(i)] = Seat(i, 3)

# 알고리즘 만들면서 시각적으로 확인하기 위해
seat1.use()
seat3.use()
print(f"{seat1.sign}{seat1.num}{seat1.sign} {seat5.sign}{seat5.num}{seat5.sign}   {seat9.sign}{seat9.num}{seat9.sign}  {seat13.sign}{seat13.num}{seat13.sign}   {seat17.sign}{seat17.num}{seat17.sign} {seat21.sign}{seat21.num}{seat21.sign}")
print(f"{seat2.sign}{seat2.num}{seat2.sign} {seat6.sign}{seat6.num}{seat6.sign}   {seat10.sign}{seat10.num}{seat10.sign} {seat14.sign}{seat14.num}{seat14.sign}   {seat18.sign}{seat18.num}{seat18.sign} {seat22.sign}{seat22.num}{seat22.sign}")
print(f"{seat3.sign}{seat3.num}{seat3.sign} {seat7.sign}{seat7.num}{seat7.sign}   {seat11.sign}{seat11.num}{seat11.sign} {seat15.sign}{seat15.num}{seat15.sign}   {seat19.sign}{seat19.num}{seat19.sign} {seat23.sign}{seat23.num}{seat23.sign}")
print(f"{seat4.sign}{seat4.num}{seat4.sign} {seat8.sign}{seat8.num}{seat8.sign}   {seat12.sign}{seat12.num}{seat12.sign} {seat16.sign}{seat16.num}{seat16.sign}   {seat20.sign}{seat20.num}{seat20.sign} {seat24.sign}{seat24.num}{seat24.sign}")

### 메모
# 거리두기 등 고려하는 알고리즘 설계 시 규칙 이용 가능
# ex) 기준 좌석 k의 왼쪽은 k-4 오른쪽은 k+4
# ex) 위에서 1번째 줄은 k % 4 == 1. 2번째 줄은 k % 4 == 2.
# ex) k % 4 == 0이면 위에서 마지막 줄(if k % 4 ==인 경우 밑에 좌석(5번)과의 거리두기를 신경 안 써도 되게 설계)