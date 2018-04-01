from tkinter import *
import random
from math import *

class SnakeGUI:
    def __init__(self):
        self.win = Tk()
        self.win.title("Snake")
        self.win.geometry("800x700")
        self.canvas = Canvas(self.win, height=600,width=600, bg = "white")
        self.canvas.pack()
        self.coordx1 = 300
        self.coordy1 = 300
        self.coordx2 = 320
        self.coordy2 = 320
        self.snakelist = []
        self.snakecoordinate1 = [self.coordx1,self.coordy1]
        self.snakecoordinate2 = [self.coordx2,self.coordy2]
        self.snakelist.append(self.snakecoordinate1)
        self.rectangle = self.canvas.create_rectangle(self.snakelist[0][0],self.snakelist[0][1],self.snakelist[0][0]+20,self.snakelist[0][1]+20, fill = 'black',outline='white', tags = "headsnake")
        self.snakecoordinate1.append(self.rectangle)
        self.delay = 200
        self.dx = 0
        self.dy = 0
        self.limit = False  # Allows you to move the snake in all four directions at the beginning of the game
        self.count = 1
        self.foodPellet()
        self.consume = False
        self.gamestate = "Pause"
        self.pausebutton = Button(self.win, text = "Start", command = self.startGame)
        self.pausebutton.pack()
        self.scorecount = Label(self.win, text = 'Score:' + str(self.count))
        self.scorecount.pack()
        self.gameinprogress = False
        self.win.bind("<Left>", self.flag)
        self.win.bind("<Right>", self.flag)
        self.win.bind("<Up>", self.flag)
        self.win.bind("<Down>", self.flag)
        self.win.bind("<a>", self.flag)
        self.win.bind("<w>", self.flag)
        self.win.bind("<d>", self.flag)
        self.win.bind("<s>", self.flag)
        self.win.bind("<space>", self.spacebar)
        self.win.mainloop()
    def youLose(self):
        self.canvas.delete('all')
        self.scorecount.pack_forget()
        self.pausebutton.pack_forget()
        self.win.unbind("<Left>")
        self.win.unbind("<Right>")
        self.win.unbind("<Up>")
        self.win.unbind("<Down>")
        self.win.unbind("<a>")
        self.win.unbind("<w>")
        self.win.unbind("<d>")
        self.win.unbind("<s>")
        self.win.unbind("<space>")
        self.win.bind("<space>",self.restartSpacebar)
        self.gamestate = "Pause"
        self.restart = Button(self.win, text = "Restart?", command = self.restartGame)
        self.restart.pack()
        self.canvas.create_text(300,300,text='Score: ' + str(self.count), font = ('Times', 25))
        self.canvas.create_text(300,250,text = 'Game over', font = ('Times',25))
    def spacebar(self,space):
        if self.gamestate == "Pause":
            self.startGame()
        elif self.gamestate == "Running":
            self.pauseGame()
    def flag(self,keys):
        if keys.keysym == "Left" or keys.keysym == "a":
            self.direction = 0
            self.dx = 20
            self.dx *= -1
            self.dy = 0
            if self.limit == True: #Makes it so you can't turn the direction opposite to your movement
                self.win.unbind("<d>")
                self.win.unbind("<Right>")
                self.win.bind("<a>",self.flag)
                self.win.bind("<s>",self.flag)
                self.win.bind("<w>",self.flag)
                self.win.bind("<Up>",self.flag)
                self.win.bind("<Left>",self.flag)
                self.win.bind("<Down>",self.flag)
        elif keys.keysym == "Right" or keys.keysym == "d":
            self.direction = 0
            self.dx = 20
            self.dx *= 1
            self.dy = 0
            if self.limit == True:
                self.win.unbind("<a>")
                self.win.unbind("<Left>")
                self.win.bind("<d>",self.flag)
                self.win.bind("<s>",self.flag)
                self.win.bind("<w>",self.flag)
                self.win.bind("<Up>",self.flag)
                self.win.bind("<Right>",self.flag)
                self.win.bind("<Down>",self.flag)
        elif keys.keysym == "Down" or keys.keysym == "s":
            self.direction = 0
            self.dy = 20
            self.dy *=1
            self.dx = 0
            if self.limit == True:
                self.win.unbind("<w>")
                self.win.unbind("<Up>")
                self.win.bind("<a>",self.flag)
                self.win.bind("<s>",self.flag)
                self.win.bind("<d>",self.flag)
                self.win.bind("<Left>",self.flag)
                self.win.bind("<Right>",self.flag)
                self.win.bind("<Down>",self.flag)
        elif keys.keysym == "Up" or keys.keysym == "w":
            self.direction = 0
            self.dy = 20
            self.dy *= -1
            self.dx = 0
            if self.limit == True:
                self.win.unbind("<s>")
                self.win.unbind("<Down>")
                self.win.bind("<a>",self.flag)
                self.win.bind("<d>",self.flag)
                self.win.bind("<w>",self.flag)
                self.win.bind("<Up>",self.flag)
                self.win.bind("<Right>",self.flag)
                self.win.bind("<Left>",self.flag)
            
    def moveSnake(self):
        if self.gamestate == "Running":
            self.consume = False
            self.coordx1 += self.dx
            self.coordx2 += self.dx
            self.coordy1 += self.dy
            self.coordy2 += self.dy
            self.distance() #checks to see how far it is from the food pellet
            self.rectangle = self.canvas.create_rectangle(self.coordx1,self.coordy1,self.coordx2,self.coordy2, fill = 'black',outline = 'white', tags = 'headsnake')
            self.snakecoordinate1 = [self.coordx1,self.coordy1,self.rectangle]
            self.snakelist.append(self.snakecoordinate1)
            self.snakelist.remove(self.snakelist[len(self.snakelist)-1]) 
            self.snakelist.append(self.snakecoordinate1)
            if self.distance() == 0: #Checks if the food pellet is eaten
                self.canvas.delete('food')
                self.limit = True #If you have more than 1 rectangle, you can't move in the direction opposite to you
                self.scorecount.pack_forget()
                self.foodPellet()
                self.consume = True
                self.delay -= 5
                self.count += 1
                self.scorecount = Label(self.win, text = 'Score:' + str(self.count))
                self.scorecount.pack()
            elif self.consume == False:
                self.canvas.delete(self.snakelist[0][2])
                del self.snakelist[0]
            for i in self.snakelist[1:]: #checks to see if the snake runs into itself
                if self.snakelist[0][0] == i[0] and self.snakelist[0][1] == i[1]:
                    self.youLose()
            if self.coordx2 >600:
                self.youLose()
            elif self.coordy1 < 0:
                self.youLose()
            elif self.coordy2 >600:
                self.youLose()
            elif self.coordy1 <0:
                self.youLose()
            elif self.coordx1 <0:
                self.youLose()
            self.canvas.after(self.delay, self.moveSnake)
    def distance(self):
        self.distance1 = (self.circlecoordinate1[0] - self.snakecoordinate1[0])**2
        self.distance2 = (self.circlecoordinate1[1] - self.snakecoordinate1[1])**2
        self.distance3 = sqrt(self.distance1+self.distance2)
        return self.distance3
    def startGame(self):
        if self.gameinprogress == False: #This makes it randomly go one direction at the beginning of the game
            self.direction = random.randint(1,4)
            if self.direction == 1: #Goes left
                self.dx = 20
                self.dx *= -1
                self.dy = 0
            elif self.direction == 2: #Goes right
                self.dx = 20
                self.dx *= 1
                self.dy = 0
            elif self.direction == 3: #Goes down
                self.dy = 20
                self.dy *=1
                self.dx = 0
            elif self.direction == 4: #Goes up
                self.dy = 20
                self.dy *= -1
                self.dx = 0
            self.gameinprogress = True
        self.gamestate = "Running"
        self.pausebutton['command'] = self.pauseGame
        self.pausebutton['text'] = "Pause"
        self.win.bind("<Left>", self.flag)
        self.win.bind("<Right>", self.flag)
        self.win.bind("<Up>", self.flag)
        self.win.bind("<Down>", self.flag)
        self.win.bind("<a>", self.flag)
        self.win.bind("<w>", self.flag)
        self.win.bind("<d>", self.flag)
        self.win.bind("<s>", self.flag)
        self.moveSnake()
    def pauseGame(self):
        self.gamestate = "Pause"
        self.pausebutton['text'] = "Start"
        self.pausebutton['command'] = self.startGame
        self.win.unbind("<Left>")
        self.win.unbind("<Right>")
        self.win.unbind("<Up>")
        self.win.unbind("<Down>")
        self.win.unbind("<a>")
        self.win.unbind("<w>")
        self.win.unbind("<d>")
        self.win.unbind("<s>")
    def foodPellet(self):
        self.circlecoordx1 = random.randint(0,600)//20 * 20
        self.circlecoordy1 = random.randint(0,600)//20 * 20
        self.circlecoordx2 = self.circlecoordx1 + 20
        self.circlecoordy2 = self.circlecoordy1 + 20
        self.circlecoordinate1 = [self.circlecoordx1,self.circlecoordy1]
        for x in self.snakelist: #This tells the food pellet not to spawn inside of the snake
            if self.circlecoordx1 == x[0] and self.circlecoordy1 == x[1]:
                self.canvas.delete('food')
                self.circlecoordx1 = random.randint(0,600)//20 * 20
                self.circlecoordy1 = random.randint(0,600) //20 * 20
                self.circlecoordx2 = self.circlecoordx1 + 20
                self.circlecoordy2 = self.circlecoordy1 + 20
                self.circlecoordinate1 = [self.circlecoordx1,self.circlecoordy1]
                self.canvas.create_oval(self.circlecoordx1,self.circlecoordy1,self.circlecoordx2,self.circlecoordy2, fill = 'black', tags = 'food')
        self.canvas.create_oval(self.circlecoordx1,self.circlecoordy1,self.circlecoordx2,self.circlecoordy2, fill = 'black', tags = 'food')
    def restartGame(self):
        self.canvas.delete('all')
        self.restart.pack_forget()
        self.pauseGame()
        self.pausebutton = Button(self.win, text = "start", command = self.startGame)
        self.pausebutton.pack()
        self.coordx1 = 300
        self.coordy1 = 300
        self.coordx2 = 320
        self.coordy2 = 320
        self.snakelist = []
        self.snakecoordinate1 = [self.coordx1,self.coordy1]
        self.snakecoordinate2 = [self.coordx2,self.coordy2]
        self.snakelist.append(self.snakecoordinate1)
        self.rectangle = self.canvas.create_rectangle(self.snakelist[0][0],self.snakelist[0][1],self.snakelist[0][0]+20,self.snakelist[0][1]+20, fill = 'black',outline='white', tags = "headsnake")
        self.snakecoordinate1.append(self.rectangle)
        self.delay = 200
        self.dx = 0
        self.dy = 0
        self.count = 1
        self.foodPellet()
        self.consume = False
        self.gamestate = "Pause"
        self.scorecount = Label(self.win, text = 'Score:' + str(self.count))
        self.scorecount.pack()
        self.gameinprogress = False
        self.win.bind("<Left>", self.flag)
        self.win.bind("<Right>", self.flag)
        self.win.bind("<Up>", self.flag)
        self.win.bind("<Down>", self.flag)
        self.win.bind("<a>", self.flag)
        self.win.bind("<w>", self.flag)
        self.win.bind("<d>", self.flag)
        self.win.bind("<s>", self.flag)
        self.win.bind("<space>", self.spacebar)
    def restartSpacebar(self,spacebar):
        self.restartGame()
       
a = SnakeGUI()
