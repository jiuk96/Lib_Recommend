# 2021-11-15 이종은 작성
# 2021-11-16 ~ 2021-12-07 이종은 수정

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
        self.sign = '@'

    def end(self): # 좌석 이용 종료
        self.state = False
        self.sign = 'x'

class Prefer: # 선호 정보 클래스
    def __init__(self, distance, acheater, window, door): # parameter는 True나 False 값으로 주어져야 함.
        self.distance = distance # 거리두기 # True면 거리두기를 원함
        self.acheater = acheater # AC or 히터 # True면 AC/히터 먼 좌석을 원함 
        self.window = window # 창문 # True면 창문 먼 좌석을 원함
        self.door = door # 문 # True면 출입구 먼 좌석을 원함

def recommend(prefer): # 좌석 추천 # parameter 중 prefer는 Prefer 클래스
    reclist = [x for x in range(1, 25)]

    if prefer.distance: # Prefer 클래스의 distance가 True면 조건문이 실행됨
        for i in range(1, 25):
            if (i==1) and (seatlist[i].state == True):
                for k in [i, i+1, i+4, i+5]:
                    if k in reclist: reclist.remove(k)

            if (i==2 or i==3) and (seatlist[i].state == True):
                for k in [i-1, i, i+1, i+3, i+4, i+5]:
                    if k in reclist: reclist.remove(k)

            if (i==4) and (seatlist[i].state == True):
                for k in [i-1, i, i+3, i+4]:
                    if k in reclist: reclist.remove(k)

            if (i==5 or i==9 or i==13 or i==17) and (seatlist[i].state == True):
                for k in [i-4, i-3, i, i+1, i+4, i+5]:
                    if k in reclist: reclist.remove(k)

            if (i==6 or i==7 or i==10 or i==11 or i==14 or i==15 or i==18 or i==19) and (seatlist[i].state == True):
                for k in [i-5, i-4, i-3, i-1, i, i+1, i+3, i+4, i+5]:
                    if k in reclist: reclist.remove(k)

            if (i==8 or i==12 or i==16 or i==20) and (seatlist[i].state == True):
                for k in [i-5, i-4, i-1, i, i+3, i+4]:
                    if k in reclist: reclist.remove(k)
                
            if (i==21) and (seatlist[i].state == True):
                for k in [i-4, i-3, i+1]:
                    if k in reclist: reclist.remove(k)
            
            if (i==22 or i==23) and (seatlist[i].state == True):
                for k in [i-5, i-4, i-3, i-1, i, i+1]:
                    if k in reclist: reclist.remove(k)

            if (i==24) and (seatlist[i].state == True):
                for k in [i-5, i-4, i-1, i]:
                    if k in reclist: reclist.remove(k)
               
    if prefer.acheater:
        for k in [19, 20, 23, 24]:
            if k in reclist:
                reclist.remove(k)

    if prefer.window:
        for k in [1, 2, 3, 4, 8, 12, 16, 20, 24]:
            if k in reclist:
                reclist.remove(k)
    
    if prefer.door:
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
seat6.use()
seat15.use()
seat21.use()
print(f"{seat1.sign}{seat1.num}{seat1.sign} {seat5.sign}{seat5.num}{seat5.sign}   {seat9.sign}{seat9.num}{seat9.sign}  {seat13.sign}{seat13.num}{seat13.sign}   {seat17.sign}{seat17.num}{seat17.sign} {seat21.sign}{seat21.num}{seat21.sign}")
print(f"{seat2.sign}{seat2.num}{seat2.sign} {seat6.sign}{seat6.num}{seat6.sign}   {seat10.sign}{seat10.num}{seat10.sign} {seat14.sign}{seat14.num}{seat14.sign}   {seat18.sign}{seat18.num}{seat18.sign} {seat22.sign}{seat22.num}{seat22.sign}")
print(f"{seat3.sign}{seat3.num}{seat3.sign} {seat7.sign}{seat7.num}{seat7.sign}   {seat11.sign}{seat11.num}{seat11.sign} {seat15.sign}{seat15.num}{seat15.sign}   {seat19.sign}{seat19.num}{seat19.sign} {seat23.sign}{seat23.num}{seat23.sign}")
print(f"{seat4.sign}{seat4.num}{seat4.sign} {seat8.sign}{seat8.num}{seat8.sign}   {seat12.sign}{seat12.num}{seat12.sign} {seat16.sign}{seat16.num}{seat16.sign}   {seat20.sign}{seat20.num}{seat20.sign} {seat24.sign}{seat24.num}{seat24.sign}")
seatlist = [0, seat1, seat2, seat3, seat4, seat5, seat6, seat7, seat8, seat9, seat10, seat11, seat12, seat13, seat14, seat15, seat16, seat17, seat18, seat19, seat20, seat21, seat22, seat23, seat24]
prefer1 = Prefer(distance=True, acheater=False, window=False, door=True)
print(f"추천 좌석: {recommend(prefer1)}")