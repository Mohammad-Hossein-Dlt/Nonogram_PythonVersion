import random
import tkinter as tk
from config.gameCore import Nonogram
from constants.themeData import ThemeData
from constants.lang import Language
#-------------------------------------------------------------------------------
class GamePad(tk.Frame, Nonogram):
    chance = []
    allowedMistake = 0
    def __init__(self, parent, gameScale = 10, gamehardship = 0.3 , showsomenonepoints = False):
        tk.Frame.__init__(self, master= parent)
        Nonogram.__init__(self, scale=gameScale, hardship= gamehardship)
        self.gameScale= gameScale
        self.gamehardship= gamehardship
        self.columnlabels, self.rowlabels, self.btns  = dict(), dict(), dict()
        # ------------------------------ Game Frame ------------------------------
        self.gameFrame = tk.Frame(self, background= "#E6E6FA")
        self.gameFrame.pack(fill= tk.BOTH, expand= tk.YES)
        # Game Control Frame
        self.controlframe = tk.Frame(self.gameFrame)
        self.controlframe.grid(column=0, row=0)
        # Game Control
        self.controls = tk.Frame(self.controlframe, background= ThemeData.controls)
        # Column Guide Main Frame
        self.columnsGuideFrame = tk.Frame(self.gameFrame, background= "blue")
        self.columnsGuideFrame.grid(column=1,row=0,sticky='nswe')
        # Column Guide Labels Frame
        self.guideColumnsLabels = tk.Frame(self.columnsGuideFrame, background= ThemeData.columnGuideColor)
        # Row Guide Main Frame
        self.rowGuideFrame = tk.Frame(self.gameFrame, background= "blue")
        self.rowGuideFrame.grid(column=0,row=1,sticky="nswe")
        # Row Guide Labels Frame
        self.guideRowsLabels = tk.Frame(self.rowGuideFrame, background= ThemeData.rowGuideColor)
        # Buttons Frame
        self.btnsFrame = tk.Frame(self.gameFrame, background= "green")
        self.btnsFrame.grid(column=1,row=1)
        # ------------------------------ Game Info ------------------------------
        self.gameinfo = tk.Frame(self, background= "#E97451")
        # Chance Label
        self.gameChance = tk.Label(self.gameinfo, background= ThemeData.gameChanceColor , text= f"{Language.chanceText} {' '.join(GamePad.chance)}", font= ("sans-serif",14))
        self.gameChance.pack(fill=tk.X, side=tk.LEFT,expand=tk.YES)
        # Programmer Name / Game Result Label
        self.providedBy = tk.Label(self.gameinfo, background= ThemeData.providedByColor , text= "Programmed By: Mh_Dlt ", font= ("sans-serif",14))
        self.providedBy.pack(fill=tk.X, side= tk.RIGHT, expand= tk.NO)
        # Gameinfo Pack
        self.gameinfo.pack(fill=tk.X, expand= tk.YES)
        # ------------------------------ Generate Controls Button ------------------------------
        # EXIT Button
        self.menubtn = tk.Button(self.controls, text= Language.menuText, width= 6)
        self.menubtn.pack(padx= 4, pady= 4)
        # Restart Button
        self.restartbtn = tk.Button(self.controls, text= Language.restartText, width= 6)
        self.restartbtn.pack(padx= 4, pady= 4)
        # Controls Frame Pack
        self.controls.pack()
        # ------------------------------  Generate Column Guide Label ------------------------------
        for c in self.helpcolumns: self.columnlabels[c] = Labels(parent= self.guideColumnsLabels, value= self.helpcolumns[c], gameframe=self )
        self.guideColumnsLabels.pack(fill=tk.BOTH, expand=1)
        # ------------------------------  Generate Row Guide Label ------------------------------
        for r in self.helprows: self.rowlabels[r] = Labels(parent= self.guideRowsLabels, value= self.helprows[r], gameframe=self)
        self.guideRowsLabels.pack(fill=tk.BOTH, expand=1)
        # ------------------------------  Generate Buttons ------------------------------
        for p in self.allpointslist: self.btns[p] = Button(parent= self.btnsFrame, point=p, gameframe= self)
        # ------------------------------  Show Some False Buttons If User Wants To ------------------------------
        if showsomenonepoints == True:
            number = int(len(self.Nonepoints)*(0.4))
            somenonepoints = []
            while len(somenonepoints) != number:
                n = random.choice(self.Nonepoints)
                if n not in somenonepoints : somenonepoints.append(n)
            print(len(somenonepoints))
            for falsebtn in somenonepoints : self.btns[falsebtn].configure(background= ThemeData.falsebuttonColor , state= "disabled", text= 'X')
#-------------------------------------------------------------------------------
class Labels(tk.Label):
    def __init__(self, parent, value, gameframe):
        tk.Label.__init__(self, parent)
        self.gameFrame = gameframe
        if parent == self.gameFrame.guideColumnsLabels:
            self.config(background = ThemeData.guidesLabels , width= 4, text= "\n".join(value))
            self.pack(fill=tk.BOTH , expand=tk.YES, side=tk.LEFT,padx=2)
        if parent == self.gameFrame.guideRowsLabels:
            self.config(background = ThemeData.guidesLabels,height=2, text=" - ".join(value))
            self.pack(fill=tk.BOTH, expand=tk.YES, side=tk.TOP, pady= 2)
#-------------------------------------------------------------------------------
class Button(tk.Button):
    mistaketimes = 0 
    def __init__(self,parent, point, gameframe):
        tk.Button.__init__(self, parent)
        self.point = point
        self.gameFrame = gameframe
        self.config(height= 2, width = 4, command= lambda:Button.check(self) , background= ThemeData.buttonColor)
        self.grid(column= point[0], row=point[1])
    def check(self):
        if self.point in self.gameFrame.Nonepoints: 
            Button.mistaketimes +=1
            self.configure(background= ThemeData.falsebuttonColor, state= "disabled", text= 'X')
            if len(GamePad.chance) != 0 :
                GamePad.chance.pop()
                self.gameFrame.gameChance.configure(text= f"{Language.chanceText} {' '.join(self.gameFrame.chance)}")
            if len(GamePad.chance) == 0 : self.gameFrame.gameChance.configure(text= Language.noMoreChanceText)
            if Button.mistaketimes == GamePad.allowedMistake :
                for i in self.gameFrame.btns: self.gameFrame.btns[i].configure(state= "disabled", text= 'X')
                self.gameFrame.providedBy.configure(text= Language.loseText )
                Button.mistaketimes = 0
        else: 
            # If all true points in a culomn or row are selected disable other points which are none
            self.configure(background= ThemeData.truebuttonColor , state= "disabled")
            self.gameFrame.truePoints.remove(self.point)
            c, r = 0, 0
            for i in self.gameFrame.truePoints:
                if i[0] == self.point[0] : c+=1
                if i[1] == self.point[1] : r+=1
            if c==0: 
                for i in self.gameFrame.Nonepoints:
                    if i[0] == self.point[0] : self.gameFrame.btns[i].configure(background= ThemeData.falsebuttonColor , state= "disabled", text= 'X')
            if r==0: 
                for i in self.gameFrame.Nonepoints:
                    if i[1] == self.point[1] : self.gameFrame.btns[i].configure(background= ThemeData.falsebuttonColor , text= 'X')
            if len(self.gameFrame.truePoints) == 0: 
                self.gameFrame.providedBy.configure(text= Language.winText )
                Button.mistaketimes = 0
