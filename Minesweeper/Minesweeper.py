import tkinter as tk
from tkinter import messagebox 
import random


class Game(tk.Frame):
    def __init__(self, master):

        # frame & canvas
        super(Game, self).__init__(master)
        self.square = 20 # 한 칸
        self.width = 10 
        self.height = 10 
        self.canvas = tk.Canvas(self, bg='#A9A9A9', width=self.width*self.square, height=self.height*self.square)

        # 지뢰, 깃발
        self.mine = 0 
        self.pattern =  []
        self.leftSquare = 0 # 남은 칸 수
        self.rightFlag = 0 # 지뢰의 위치에 꽂은 깃발

        # 메뉴
        menubar = tk.Menu(master) # 상위메뉴 - 메뉴바
        filemenu = tk.Menu(menubar, tearoff=0) # 메뉴바의 하위 메뉴
        filemenu.add_command (label="9*9", command=self.lowLevelBegin)
        filemenu.add_command (label="16*16", command=self.middleLevelBegin)
        filemenu.add_command (label="30*16", command=self.highLevelBegin)
        filemenu.add_separator() # file 메뉴당 구분선 생성
        filemenu.add_command (label="Exit", command=master.destroy)
        menubar.add_cascade(label="File", menu=filemenu) # 상위메뉴 file과 하위 메뉴 filemenu 연결
        master.config(menu=menubar) # master에 메뉴 등록

        self.canvas.pack() # canvas 그리기
        self.pack() # frame 그리기


    def lowLevelBegin(self):
        self.canvas.destroy() # canvas 지우기
        self.width = 9
        self.height = 9
        self.mine = 10
        self.makeBoard()

    def middleLevelBegin(self):
        self.canvas.destroy()
        self.width = 16
        self.height = 16
        self.mine = 40
        self.makeBoard()
        
    def highLevelBegin(self):
        self.canvas.destroy()
        self.width = 30
        self.height = 16
        self.mine = 99
        self.makeBoard()


    def makeBoard(self):
        self.pattern =  [[[0]*4 for x in range(self.width)] for y in range(self.height)] # 3차원 배열 
        self.leftSquare = self.width * self.height - self.mine # 남은 타일의 개수 = 가로 * 세로 - 지뢰 
        self.rightFlag = 0
        
        # 보드 초기화
        for x in range(self.width): 
            for y in range(self.height):
                self.pattern[y][x][0] = 0 # (x, y)가 지뢰인지 아닌지 (0: 지뢰 X/ 1: 지뢰 O)
                self.pattern[y][x][1] = 0 # (x, y) 마우스 클릭 여부 (1: 왼쪽 클릭/ 0: 아무 클릭 X /-1: 오른쪽 클릭)
                self.pattern[y][x][2] = 0 # 주변에 지뢰 몇개인지 (0~8 가능)
                self.pattern[y][x][3] = 0 # (x, y)의 text 저장(To delete)
        
        # 캔버스에 선 그리기
        self.canvas = tk.Canvas(self, bg='#A9A9A9', width=self.width*self.square, height=self.height*self.square)
        for x in range(self.width):    
            self.canvas.create_line(x*self.square, 0, x*self.square, self.height*self.square, fill='#000000', width='1')
        for y in range(self.height):
            self.canvas.create_line(0, y*self.square, self.width*self.square, y*self.square, fill='#000000', width='1')

        # 지뢰 생성
        for i in range(self.mine): ## 지뢰의 개수만큼
            x = random.randint(0, self.width-1) # 지뢰가 위치할 x, y 좌표값 랜덤으로 생성 (index 범위 주의: random.randint는 이상 & 이하!!)
            y = random.randint(0, self.height-1)  
            while (self.pattern[y][x][0] == 1): # 중복인 경우 다시 뽑기
                x = random.randint(0,self.width-1) 
                y = random.randint(0,self.height-1)
            self.pattern[y][x][0] = 1 # 지뢰 정보 저장

        # 보드의 각 칸마다 지뢰 개수
        for y in range(self.height):
            for x in range(self.width):
                for yy in range(-1, 2):
                    for xx in range(-1, 2):
                        if x+xx < 0: # 왼쪽 가장자리면
                            continue 
                        if x+xx >= self.width: # 오른쪽 가장자리
                            continue 
                        if y+yy < 0: # 위쪽 가장자리
                            continue
                        if y+yy >= self.height: # 아래쪽 가장자리
                            continue
                        if (self.pattern[y+yy][x+xx][0] == 1): # 지뢰이면
                            self.pattern[y][x][2] += 1 # count +1
                            
        self.canvas.pack()
        self.mouseBind()


   # 주변 지뢰 개수 판단 & 오픈
    def detect_region(self, x, y):
        for yy in range(-1, 2):
            for xx in range(-1, 2):
                if x+xx < 0: # 왼쪽 가장자리
                    continue 
                if x+xx >= self.width: # 오른쪽 가장자리
                    continue 
                if y+yy < 0: # 위쪽 가장자리
                    continue
                if y+yy >= self.height: # 아래쪽 가장자리
                    continue

                if (self.pattern[y][x][2] == 0): # 현재 좌표의 지뢰의 개수가 0일 때
                    if (self.pattern[y+yy][x+xx][1] != 1): # 주변 좌표 마우스 왼쪽 클릭 안되어 있는 상태면
                        self.detect_region(x+xx, y+yy) # 재귀

            if (self.pattern[y][x][1] == -1): # 깃발 마킹 되어있는 상태면
                self.canvas.delete(self.pattern[y][x][3]) # 깃발 text 지우기
            self.draw_text(x , y, str(self.pattern[y][x][2]), '#000000') # 주변 지뢰 개수 text 그리기
            self.pattern[y][x][1] = 1 
            

    def mouseBind(self):
        self.canvas.bind('<Button-1>', self.left_button)
        self.canvas.bind('<Button-3>', self.right_button)

    def win(self):
        tk.messagebox.showinfo('Win', 'You win!')
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')

    def lose(self):
        tk.messagebox.showinfo('Lose', 'You Lose!')
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')


    def left_button(self, event):
        x = event.x // self.square # 클릭한 좌표를 self.square로 나눈 정수 몫의 값
        y = event.y // self.square

        if (self.pattern[y][x][1] == 0): # 중복 클릭 방지
            if (self.pattern[y][x][0] == 0): # 지뢰 아니면
                self.detect_region(x, y) 
                self.leftSquare -= 1 
                if (self.leftSquare == 0): 
                    self.win() # 지뢰 제외한 칸 모두 오픈(마우스 왼쪽 클릭)하면 win

            elif (self.pattern[y][x][0] == 1): # 지뢰이면
                for x in range(self.width):
                    for y in range(self.height):
                        if (self.pattern[y][x][0] == 1): # 모든 지뢰 보여주기
                            if (self.pattern[y][x][1] == -1): # 깃발 마킹 되어있으면
                                    self.canvas.delete(self.pattern[y][x][3]) # 깃발 지우고
                                    self.draw_text(x , y, '💣', '#cc0000') # 폭탄 그리기 (빨간색)
                            else:
                                self.draw_text(x , y, '💣', '#000000') # 폭탄 그리기 (검은색)

                self.lose() 


    def right_button(self, event):
        x = event.x // self.square
        y = event.y // self.square

        if (self.pattern[y][x][1] == 0): # 중복 클릭 방지
            if (self.pattern[y][x][0] == 1): # 깃발 마킹한 좌표가 지뢰이면
                self.rightFlag += 1 # rightFlag 하나 증가
            self.pattern[y][x][1] = -1 
            self.pattern[y][x][3] = self.draw_text(x , y, '🚩','#cc0000') # 깃발 그리기
            
            if (self.rightFlag == self.mine): # 모든 지뢰를 깃발로 마킹했으면
                self.win() # win

    def draw_text(self, x, y, text, fill):
        font = ('Arial', '11')
        text = self.canvas.create_text(x*self.square+10, y*self.square+10, text=text, fill=fill, font=font)
        return text

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Minesweeper')
    game = Game(root)
    game.mainloop()