import wx
from src.interface import MyFrame

def main():
    app = wx.App(False)
    frame = MyFrame(None, title="Sistema de Doação de Sangue", size=(600, 400))
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
