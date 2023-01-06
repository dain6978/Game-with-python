from cmath import sqrt
import tkinter as tk
import random
import numpy as np

class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [1, -1]
        self.speed = 10
        
        self.ballImage = tk.PhotoImage(file = 'ball.png')
        item = canvas.create_image(x, y, anchor=tk.CENTER, image = self.ballImage)
       
        super(Ball, self).__init__(canvas, item)

    def get_position(self):
        #self.canvas.coords(self.item) = [x-self.radius, y-self.radius, x+self.radius, y+self.radius]
        #[left, top, right, bottom]
        coords = self.canvas.coords(self.item) * 2 
        coords[0] -= self.radius #마지막에 변하는 x, y 값에서 원의 coords 반영해서 충돌 판정
        coords[1] -= self.radius
        coords[2] += self.radius
        coords[3] += self.radius
        return coords

    
    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)


    def makeInterPoint(self, a, b, game_objects, coordX, coordY): #a, b는 공의 중심 좌표
        game_object = game_objects[0]
        coords = game_object.get_position() # brick, paddle의 x1(left), y1(top), x2(right), y2(bottom)

       # 판별식 > 0 인 경우에만 교점 존재하니까 교점 구하기 
        interList = []# 교점의 좌표 담을 리스트

        # 오른쪽 아래인 경우
        if (coordX == coords[2]) and (coordY == coords[3]):
            y = coords[3]
            D = - pow(y, 2) + 2*b*y - pow(b, 2) + self.radius + y
            if (D > 0):
                x1 = a - sqrt(D)
                x2 = a + sqrt(D)
                if coords[0] < abs(x1) < coords[2]:
                    if coords[0] < abs(x2) < coords[2]:
                        pass
                    else:
                        interList.append([x1, y])
                        x = coords[2]
                        D = - pow(x, 2) + 2*a*x - pow(a, 2) + self.radius + x
                        y1 = a - sqrt(D)
                        y2 = a + sqrt(D)
                        if coords[1] < abs(y1) < coords[3]:
                            if (coords[1] < abs(y2) < coords[3]):
                                pass
                            else:
                                interList.append([x, y1])
        # 오른쪽 위인 경우
        if (coordX == coords[2]) and (coordY == coords[1]):
            y = coords[1]
            D = - pow(y, 2) + 2*b*y - pow(b, 2) + self.radius + y
            if (D > 0):
                x1 = a - sqrt(D)
                x2 = a + sqrt(D)
                if coords[0] < abs(x1) < coords[2]:
                    if coords[0] < abs(x2) < coords[2]:
                        pass
                    else:
                        interList.append([x1, y])
                        x = coords[2]
                        D = - pow(x, 2) + 2*a*x - pow(a, 2) + self.radius + x
                        y1 = a - sqrt(D)
                        y2 = a + sqrt(D)
                        if coords[1] < abs(y2) < coords[3]:
                            if (coords[1] < abs(y1) < coords[3]):
                                pass
                            else:
                                interList.append([x, y2])
        # 왼쪽 아래인 경우
        if (coordX == coords[0]) and (coordY == coords[3]):
            y = coords[3]
            D = - pow(y, 2) + 2*b*y - pow(b, 2) + self.radius + y
            if (D > 0):
                x1 = a - sqrt(D)
                x2 = a + sqrt(D)
                if coords[0] < abs(x2) < coords[2]:
                    if coords[0] < abs(x1) < coords[2]:
                        pass
                    else:
                        interList.append([x2, y])
                        x = coords[0]
                        D = - pow(x, 2) + 2*a*x - pow(a, 2) + self.radius + x
                        y1 = a - sqrt(D)
                        y2 = a + sqrt(D)
                        if coords[1] < abs(y1) < coords[3]:
                            if (coords[1] < abs(y2) < coords[3]):
                                pass
                            else:
                                interList.append([x, y1])
            
        # 왼쪽 위인 경우
        if (coordX == coords[0]) and (coordY == coords[3]):
            y = coords[3]
            D = - pow(y, 2) + 2*b*y - pow(b, 2) + self.radius + y
            if (D > 0):
                x1 = a - sqrt(D)
                x2 = a + sqrt(D)
                if coords[0] < abs(x2) < coords[2]:
                    if coords[0] < abs(x1) < coords[2]:
                        pass
                    else:
                        interList.append([x2, y])
                        x = coords[0]
                        D = - pow(x, 2) + 2*a*x - pow(a, 2) + self.radius + x
                        y1 = a - sqrt(D)
                        y2 = a + sqrt(D)
                        if coords[1] < abs(y2) < coords[3]:
                            if (coords[1] < abs(y1) < coords[3]):
                                pass
                            else:
                                interList.append([x, y2])
        return interList

    def collide(self, game_objects):
        coords = self.get_position() # 공의 left, top, right, bottom
        ballX = (coords[0] + coords[2]) * 0.5 # (x-self.radius + x+self.radius) / 2 → 즉 공의 중심의 x 좌표
        ballY = (coords[1] + coords[3]) * 0.5 #  공의 중심의 y 좌표
        
        interPoint = [] # 초기화
        pointLength = 0 # 초기화
        
        if len(game_objects) > 1: # object(brick, paddle) 2개 이상이 공과 동시에 충돌
            self.direction[1] *= -1
            print("여러 개 충돌")
        
        elif len(game_objects) == 1: # object(brick, paddle) 1개만 충돌
            game_object = game_objects[0]
            coords = game_object.get_position()
            print("한 개만 충돌")
            if ballX > coords[2]:
                if ballY > coords[3]: # 오른쪽 아래 모서리 (y축은 -일수록 위니까... 주의!)
                    print("오른쪽 아래 모서리")
                    interPoint = self.makeInterPoint(ballX, ballY, game_objects, coords[2], coords[3])
                elif ballY < coords[1]: # 오른쪽 위 모서리
                    print("오른쪽 위 모서리")
                    interPoint = self.makeInterPoint(ballX, ballY, game_objects, coords[2], coords[1])
            elif ballX < coords[0]:  
                if ballY > coords[3]: # 왼쪽 아래 모서리
                    print("왼쪽 아래 모서리")
                    interPoint = self.makeInterPoint(ballX, ballY, game_objects, coords[0], coords[3])
                elif ballY < coords[1]: # 왼쪽 위 모서리
                    print("왼쪽 위 모서리")
                    interPoint = self.makeInterPoint(ballX, ballY, game_objects, coords[0], coords[1])
            
            pointLength = len(interPoint)
            
            # interPointList = [[x1, y1], [x2, y2]]
            if (pointLength == 2): # 교점이 2개면
                    # 두 교점을 잇는 방향 벡터 
                    direcVector = [interPoint[0][0] - interPoint[1][0], interPoint[0][1] - interPoint[1][1]] # 반응 수정
                    # 법선 벡터 두 개
                    normalVector1 = [-direcVector[1], direcVector[0]] # 90도 회전
                    normalVector2 = [direcVector[1], -direcVector[0]] # 270도 회전
                    
                    mPoint = [(interPoint[0][0]+interPoint[1][0])/2, (interPoint[0][1]+interPoint[1][1])/2] # 방향 벡터 중점
                    objectCenter = [(coords[0]+coords[2])/2, (coords[1]+coords[3])/2] # game_object의 중심
                    linkVector = objectCenter - mPoint # 연결 벡터

                    if (np.dot(normalVector1, linkVector) < 0): # 내적이 0보다 작음 → cos쎄타 음수 → 둔각 (더 각도 큰 쪽)
                        self.direction = normalVector1
                    else: 
                        self.direction = normalVector2

            else:
                if ballX > coords[2]:
                    self.direction[0] = 1
                    print("오른쪽")
                elif ballX < coords[0]:
                    self.direction[0] = -1
                    print("왼쪽")
                else:
                    self.direction[1] *= -1
                    print("그외")

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()


class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='blue')
        super(Paddle, self).__init__(canvas, item)

    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)


class Brick(GameObject):
    COLORS = {1: '#999999', 2: '#555555', 3: '#222222'}

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        self.hits = hits
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            self.delete()
        else:
            self.canvas.itemconfig(self.item,
                                   fill=Brick.COLORS[self.hits])

#Game 클래스의 __init__함수에서 self.level 변수 선언하고 1로 초기화
class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.level = 1
        self.lives = 3
        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg='#aaaaff',
                                width=self.width,
                                height=self.height,)
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        self.items[self.paddle.item] = self.paddle

        self.hud = None
        self.setup_game()
        self.setup_level() #setup_level() 멤버 함수 호출
        self.canvas.focus_set()
        self.canvas.bind('<Left>',
                         lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>',
                         lambda _: self.paddle.move(10))

    def setup_game(self):
            self.add_ball()
            self.update_lives_text()
            self.text = self.draw_text(300, 200,
                                      'Press Space to start')
            self.canvas.bind('<space>', lambda _: self.start_game())


    def setup_level(self):
        choiceList1 = self.ChoiceList() # 1층
        choiceList2 = self.ChoiceList() # 2층
        choiceList3 = self.ChoiceList() # 3층
        
        if (self.level == 1): # level == 1이니까 한 층
            for x in choiceList1: #choiceList의 element 마다
                self.add_brick(x + 37.5, 50, 2) # 벽돌 추가
        elif (self.level == 2):
            for x1 in choiceList1:
                self.add_brick(x1 + 37.5, 50, 2)
            for x2 in choiceList2:
                self.add_brick(x2 + 37.5, 70, 1)
        elif (self.level == 3):
            for x1 in choiceList1:
                self.add_brick(x1 + 37.5, 50, 2)
            for x2 in choiceList2:
                self.add_brick(x2 + 37.5, 70, 1)
            for x3 in choiceList3:
                self.add_brick(x3 + 37.5, 90, 1)

    def ChoiceList(self):
        xList = range(5, self.width - 5, 75) # 생성 가능한 brick의 x좌표들 모두 담은 리스트
        choiceList = [] # random으로 선택된 x좌표만 담을 리스트
        for i in range(0, random.randint(1, 9)): #0 이상 9이하의 난수 반환 
            choiceList.append(random.choice(xList)) #xList에서 무작위로 선택해서 choiceList에 append → random.randint로부터 반환된 난수만큼 반복
        return choiceList

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='40'):
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text,
                                       font=font)

    def update_lives_text(self):
        text = 'Lives: %d, Level: %d' % (self.lives, self.level)
        if self.hud is None:
            self.hud = self.draw_text(80, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()


    def next_level(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)

        self.level += 1
        self.update_lives_text()
        
        self.setup_level()
        self.paddle.ball = None
        self.add_ball()
        self.game_loop()


    def game_loop(self):
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
       
        if num_bricks == 0: #벽돌 개수 0이면
            self.ball.speed = None # 볼 정지

            if self.level == 3: # 레벨이 3인 경우
                self.draw_text(300, 200, 'You win!') # 게임 클리어
            else: # 그 외
                self.text = self.draw_text(300, 200, 'Press Space to Next Level', size='30') 
                self.canvas.bind('<space>', lambda _: self.next_level()) # space를 누를 경우 next_level() 함수 실행

        elif self.ball.get_position()[3] >= self.height: 
            self.ball.speed = None 
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, 'Game Over')
            else:
                self.after(1000, self.setup_game)
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)

 

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Hello, Pong!')
    game = Game(root)
    game.mainloop()
