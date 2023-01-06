import random
import os
import time
import msvcrt

class Snake:
    def __init__(self, n):
        self.length = n
        self.head = []
        self.tail = []

class SnakeGame:
    direction = {"LEFT":-2, "DOWN":-1, "NON_DIR":0, "UP":1, "RIGHT":2}
    sprite = {"EMPTY":0, "BODY":1, "HEAD":2, "FOOD":3}
    element = {"SPRITE":0, "DIRECTION":1}
    
    def __init__(self, w, h, length, delay):
        self.W = w
        self.H = h
        self.initLen = length
        self.snake = Snake(length)
        self.delay = delay  
        self.board = [[[0]*2 for x in range(self.W)] for y in range(self.H)]
        #self.board[a][b][c]

        self.snake.head = [self.H//2, self.snake.length-1]
        self.snake.tail = [self.H//2, 0]

        for i in range(0, self.snake.length):
            self.board[self.H//2][i][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]
            self.board[self.H//2][i][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]

        self.board[self.H//2][self.snake.length-1][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
        self.board[self.H//2][self.snake.length-1][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]

        
        x = random.randint(0, self.W-1)
        y = random.randint(0, self.H-1)
        while self.board[y][x][SnakeGame.element["SPRITE"]]\
              != SnakeGame.sprite["EMPTY"]:
            x = random.randint(0, self.W-1)
            y = random.randint(0, self.H-1)

        self.board[y][x][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"]

    def DrawScene(self):
        os.system('cls||clear')
        for x in range(0, self.W+2):
            print("=", end="")
        print("")
        for y in range(0, self.H):
            print("|", end="")
            for x in range(0, self.W):
                if self.board[y][x][SnakeGame.element["SPRITE"]]\
                   == SnakeGame.sprite["BODY"]:
                    print("+", end="")
                elif  self.board[y][x][SnakeGame.element["SPRITE"]]\
                     == SnakeGame.sprite["HEAD"]: 
                    print("@", end="")
                elif  self.board[y][x][SnakeGame.element["SPRITE"]]\
                     == SnakeGame.sprite["FOOD"]:
                    print("*", end="")
                else:
                    print(" ", end="")
            print("|")

        for x in range(0, self.W+2):
            print("=", end="")
        print("")
                

    @staticmethod
    def GetDirection():
        rtn = SnakeGame.direction["NON_DIR"]
        msvcrt.getch()
        ch = msvcrt.getch().decode()
        
        if ch == chr(72):
            print("UP")
            rtn = SnakeGame.direction["UP"]
        elif ch == chr(75):
            print("LEFT")
            rtn = SnakeGame.direction["LEFT"]
        elif ch == chr(77):
            print("RIGHT")
            rtn = SnakeGame.direction["RIGHT"]
        elif ch == chr(80):
            print("DOWN")
            rtn = SnakeGame.direction["DOWN"]

        return rtn
    

    # 먹이 먹었는지 확인하고 꼬리 제거하는 함수
    def CheckFood(self, headX, headY, snakeBody):
        foodX = random.randint(0, self.W-1)
        foodY = random.randint(0, self.H-1)

        # 먹이 먹으면 (HEAD의 좌표가 FOOD의 좌표와 같은 경우) 
        if self.board[headY][headX][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["FOOD"]:
            self.snake.length += 1 # snake의 길이 +1
            # 새로운 먹이 그리기 (단, EMPTY인 경우만 FOOD 그리고, 아니라면 x, y 좌표 다시 받음)
            while self.board[foodY][foodX][SnakeGame.element["SPRITE"]] != SnakeGame.sprite["EMPTY"]:
                foodX = random.randint(0, self.W-1)
                foodY = random.randint(0, self.H-1)
            self.board[foodY][foodX][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"] 
            
        else: 
            # 먹이 먹지 않은 경우 꼬리 제거 (화면에 EMPTY로 그려주고 snakeBody 리스트에서도 제거)
            self.board[snakeBody[0][1]][snakeBody[0][0]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
            snakeBody.pop(0)
    

    # 게임 오버 조건 확인하는 함수
    def GameOver(self, headX, headY): 
        gameOver = False

        # HEAD의 좌표가 화면 밖으로 나가면 게임 오버
        if (headY == self.H or headY < 0 ) or (headX == self.W or headX < 0):
            gameOver = True
            print("Game Over")
        # head와 body가 충돌하면 게임 오버
        elif self.board[headY][headX][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["BODY"]:
            gameOver = True
            print("Game Over")

        return gameOver


    def GameLoop(self):
        self.DrawScene()

        current = SnakeGame.direction["RIGHT"]
        ret = SnakeGame.direction["RIGHT"]

        # snake의 head과 tail의 x, y 좌표
        snakeHeadY = self.snake.head[0]
        snakeHeadX = self.snake.head[1]
        snakeTailY = self.snake.tail[0]
        snakeTailX = self.snake.tail[1]
        # snake의 body들의 좌표 정보 담은 list
        snakeBody = [(snakeTailX, snakeTailY), (snakeTailX+1, snakeTailY), (snakeTailX+2, snakeTailY)]

        while (True):
            start = time.time()

            while (time.time() - start) <= self.delay/1000:

                if msvcrt.kbhit():
                    ret = current 
                    current = SnakeGame.GetDirection() 
    
                    if (ret + current == 0): # 뱀의 이동 방향과 반대 방향키 누른 경우 반영 X 
                         current = ret

            if (current == 2): # 오른쪽
                snakeHeadX += 1 # HEAD의 X좌표 +1
                # 본래 HEAD가 있던 좌표를 snakeBody 리스트에 추가하고 화면에 BODY로 그리기
                snakeBody.append((snakeHeadX-1, snakeHeadY))
                self.board[snakeHeadY][snakeHeadX-1][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]

            elif (current == -2): # 왼쪽
                snakeHeadX -= 1 
                snakeBody.append((snakeHeadX+1, snakeHeadY))
                self.board[snakeHeadY][snakeHeadX+1][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]

            elif (current == 1): # 위
                snakeHeadY -= 1 
                snakeBody.append((snakeHeadX, snakeHeadY+1))
                self.board[snakeHeadY+1][snakeHeadX][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]

            elif (current == -1): # 아래
                snakeHeadY += 1 
                snakeBody.append((snakeHeadX, snakeHeadY-1))
                self.board[snakeHeadY-1][snakeHeadX][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]

            gameOver =self.GameOver(snakeHeadX, snakeHeadY) 
            if (gameOver):
                return # 게임 오버인 경우 while문 종료
            else:
                # 아닌 경우 CheckFood 함수 호출해서 먹이 먹었는지 확인하고 꼬리 제거
                self.CheckFood(snakeHeadX, snakeHeadY, snakeBody) 
                # 새로운 HEAD 좌표 화면에 그리기
                self.board[snakeHeadY][snakeHeadX][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"] 

            self.DrawScene()
            print("Score: {}".format(self.snake.length - self.initLen))
        

if __name__ == '__main__' :
    game = SnakeGame(60, 24, 4, 300)
    game.GameLoop()