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
    

    # ?????? ???????????? ???????????? ?????? ???????????? ??????
    def CheckFood(self, headX, headY, snakeBody):
        foodX = random.randint(0, self.W-1)
        foodY = random.randint(0, self.H-1)

        # ?????? ????????? (HEAD??? ????????? FOOD??? ????????? ?????? ??????) 
        if self.board[headY][headX][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["FOOD"]:
            self.snake.length += 1 # snake??? ?????? +1
            # ????????? ?????? ????????? (???, EMPTY??? ????????? FOOD ?????????, ???????????? x, y ?????? ?????? ??????)
            while self.board[foodY][foodX][SnakeGame.element["SPRITE"]] != SnakeGame.sprite["EMPTY"]:
                foodX = random.randint(0, self.W-1)
                foodY = random.randint(0, self.H-1)
            self.board[foodY][foodX][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"] 
            
        else: 
            # ?????? ?????? ?????? ?????? ?????? ?????? (????????? EMPTY??? ???????????? snakeBody ?????????????????? ??????)
            self.board[snakeBody[0][1]][snakeBody[0][0]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
            snakeBody.pop(0)
    

    # ?????? ?????? ?????? ???????????? ??????
    def GameOver(self, headX, headY): 
        gameOver = False

        # HEAD??? ????????? ?????? ????????? ????????? ?????? ??????
        if (headY == self.H or headY < 0 ) or (headX == self.W or headX < 0):
            gameOver = True
            print("Game Over")
        # head??? body??? ???????????? ?????? ??????
        elif self.board[headY][headX][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["BODY"]:
            gameOver = True
            print("Game Over")

        return gameOver


    def GameLoop(self):
        self.DrawScene()

        current = SnakeGame.direction["RIGHT"]
        ret = SnakeGame.direction["RIGHT"]

        # snake??? head??? tail??? x, y ??????
        snakeHeadY = self.snake.head[0]
        snakeHeadX = self.snake.head[1]
        snakeTailY = self.snake.tail[0]
        snakeTailX = self.snake.tail[1]
        # snake??? body?????? ?????? ?????? ?????? list
        snakeBody = [(snakeTailX, snakeTailY), (snakeTailX+1, snakeTailY), (snakeTailX+2, snakeTailY)]

        while (True):
            start = time.time()

            while (time.time() - start) <= self.delay/1000:

                if msvcrt.kbhit():
                    ret = current 
                    current = SnakeGame.GetDirection() 
    
                    if (ret + current == 0): # ?????? ?????? ????????? ?????? ????????? ?????? ?????? ?????? X 
                         current = ret

            if (current == 2): # ?????????
                snakeHeadX += 1 # HEAD??? X?????? +1
                # ?????? HEAD??? ?????? ????????? snakeBody ???????????? ???????????? ????????? BODY??? ?????????
                snakeBody.append((snakeHeadX-1, snakeHeadY))
                self.board[snakeHeadY][snakeHeadX-1][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]

            elif (current == -2): # ??????
                snakeHeadX -= 1 
                snakeBody.append((snakeHeadX+1, snakeHeadY))
                self.board[snakeHeadY][snakeHeadX+1][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]

            elif (current == 1): # ???
                snakeHeadY -= 1 
                snakeBody.append((snakeHeadX, snakeHeadY+1))
                self.board[snakeHeadY+1][snakeHeadX][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]

            elif (current == -1): # ??????
                snakeHeadY += 1 
                snakeBody.append((snakeHeadX, snakeHeadY-1))
                self.board[snakeHeadY-1][snakeHeadX][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]

            gameOver =self.GameOver(snakeHeadX, snakeHeadY) 
            if (gameOver):
                return # ?????? ????????? ?????? while??? ??????
            else:
                # ?????? ?????? CheckFood ?????? ???????????? ?????? ???????????? ???????????? ?????? ??????
                self.CheckFood(snakeHeadX, snakeHeadY, snakeBody) 
                # ????????? HEAD ?????? ????????? ?????????
                self.board[snakeHeadY][snakeHeadX][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"] 

            self.DrawScene()
            print("Score: {}".format(self.snake.length - self.initLen))
        

if __name__ == '__main__' :
    game = SnakeGame(60, 24, 4, 300)
    game.GameLoop()