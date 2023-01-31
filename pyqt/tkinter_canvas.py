from tkinter import *
from PIL import Image, ImageTk
# from tkinter import PhotoImage

class App():
    def __init__(self, title, width, height):
        self.window = Tk()
        self.width = width
        self.height = height
        self.window.title(title)
        self.window.pimage = ImageTk.PhotoImage(Image.open("pmos.png"))
        self.lastState = {"x": 0, "y": 0}
        self.window.geometry(f'{width}x{height}')
        self.pmos_list = []
        self.nmos_list = []

    def canvas(self):
        global lbl
        global canva
        canva = Canvas(self.window, bd=0)
        canva.pack(expand=YES, fill=BOTH)
        lbl = Label(canva, image=self.window.pimage)
        lbl.place(x=0, y=0)
        self.window.pimage = ImageTk.PhotoImage(Image.open("pmos.png"))
        pLbl = Label(canva, image=self.window.pimage)
        nmosImage = ImageTk.PhotoImage(Image.open("nmos.png"))
        self.window.nimage = nmosImage
        nLbl = Label(canva, image=self.window.nimage)
        canva.create_window(30, 10, window=pLbl, anchor=NW)
        canva.create_window(130, 10, window=nLbl, anchor=NW)
        vScroll = Scrollbar(canva, orient=VERTICAL, )
        vScroll.pack(side=RIGHT, fill=Y)
        hscroll = Scrollbar(canva, orient=VERTICAL, )
        hscroll.pack(side=BOTTOM, fill=X)
        pLbl.bind('<B1-Motion>', lambda e, img=self.window.pimage: self.moveMos(e, img))
        pLbl.bind('<ButtonRelease-1>', lambda e, img=self.window.pimage: self.attachMos(e, img))
        nLbl.bind('<B1-Motion>', lambda e, img=self.window.nimage: self.moveMos(e, img))
        nLbl.bind('<ButtonRelease-1>', lambda e, img=self.window.nimage: self.attachMos(e, img))
        # nmosIn=canva.create_image((200, 50),image=nmosImage)
        # # nmosIn.bind('<Button>',self.show)

    def attachMos(self, e, img):
        # newLbl = Label(canva, image=img)
        # newLbl.place(x=self.lastState["x"], y=self.lastState['y'])
        # lbl.configure(image=None)
        # newLbl.bind('<B1-Motion>', lambda e: moveFet(e))
        #
        # def moveFet(e):
        #     newLbl.place_configure(x=e.x, y=e.y)

        global canva
        canvasName = canva
        x_pos = e.x
        y_pos = e.y
        img = img
        lbl.configure(image=None)
        lbl.place_configure(x=-100, y=-100)
        lbl.pack_forget()
        placement(canvasName, x_pos, y_pos, img)
        print('==>', img)

    def moveMos(self, e, img):
        lbl.configure(image=img)
        lbl.place(x=e.x, y=e.y)
        self.lastState['x'] = e.x
        self.lastState['y'] = e.y
        self.show(e)
        # canva.create_window((e.x, e.y),window=newLbl)

    def show(self, e):
        print(e.x, e.y)

    def end(self):
        # self.attachLabel("hh")
        # self.window.bind('<Button>',self.show)
        self.canvas()
        self.window.mainloop()


class placement():
    def __init__(self, canvasName, x_pos, y_pos, img):
        print('**************************', img)
        self.canvasName = canvasName
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.img = img
        self.newLbl = None
        self.attachMos1()

    def attachMos1(self):
        self.newLbl = Label(self.canvasName, image=self.img)
        # self.newLbl.place(x=self.x_pos, y=self.y_pos)
        self.canvasName.create_window(self.x_pos, self.y_pos, window=self.newLbl)
        self.newLbl.bind('<B1-Motion>', lambda e: self.drag_motion(e))
        print("atached")

    def moveFet(self, e):
        self.newLbl.place_configure(x=e.x, y=e.y)

    def drag_motion(self, event):
        print(event.x, event.y)
        # x = self.newLbl.winfo_x() - self.x_pos + event.x
        # y = self.newLbl.winfo_y() - self.x_pos + event.y
        # self.newLbl.place(x=x, y=y)
        self.canvasName.move(self.newLbl, event.x, event.y)
        self.x_pos = event.x
        self.y_pos = event.y


title = "My circuit simulator"
width = 600
height = 900
app = App(title, width, height)
app.end()