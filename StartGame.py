import tkinter as tk
import json
from gui.gameMenu import GameMenu
from gui.gamePad import GamePad
from constants.themeData import ThemeData
from constants.lang import Language
#-------------------------------------------------------------------------------
class StartGame(GameMenu, GamePad):
    chance = []
    location = "Menu"
    def __init__(self):
    # Config settings start
        config = {"charactor": "💣", "numberOfChances": 3, "theme" : "Light" , "language": "en"}
        try:
            with open("config.json") as sc: config = json.load(sc)
        except IOError : 
            with open("config.json", "w") as newSC : newSC.writelines(json.dumps(config))
        StartGame.chance = [config["charactor"] for i in range(config["numberOfChances"])]
        ThemeData.__init__(config["theme"])
        Language.__init__(config["language"])
    # Config settings end
    # Recognition curent frame to config and render/show it
        if StartGame.location == "Menu":
            GameMenu.__init__(self, parent= root)
            self.startbutton.configure(command= lambda: self.startbtn())
            self.pack()
            root.title("Nonogram")
        elif StartGame.location == "GamePad":
            GamePad.chance = StartGame.chance
            GamePad.allowedMistake = len(StartGame.chance) + 1
            GamePad.__init__(self, parent= root, gameScale= self.selectedscale, gamehardship= self.sethardship, showsomenonepoints= self.showfalsebtns)
            self.menubtn.configure(command= lambda: self.menu())
            self.restartbtn.configure(command= lambda: self.restart())
            self.pack()
            root.title("Nonogram ----> By Mh_Dlt")
    ''' 
    Because of gameMenu and gamePad are render in one root and this 3 buttons(start , menu, restart) 
    destroy their parent to render their frame again or other frame
    we must configure their command after rendering their parents
    when buttons command run the function of the command will not destroy and give it to buttons command again
    '''
    def menu(self):
        self.destroy()
        StartGame.location = "Menu"
        self.__init__()
    def startbtn(self):
        self.destroy()
        StartGame.location = "GamePad"
        self.__init__()
    def restart(self):
        self.destroy()
        self.__init__()
        

if __name__ == "__main__":   
    root = tk.Tk()
    root.resizable(0, 0)
    start = StartGame()
    start.pack()
    root.mainloop() 
