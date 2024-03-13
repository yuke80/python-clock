import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import datetime, os

#root = tk.Tk()
#root.title("TkClock")

#id_ = None
#image_data = None
 
# 時計の画像を表示する300x300のキャンバス
# 最初に作るrectangleはダミー
#cv = tk.Canvas(width = 300, height = 300)
#id_ = cv.create_rectangle(0,0,300,300)
#cv.pack()

class AClock(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill='both')
        self.create_widgets()
        
    def create_widgets(self):

        self.image_data = None
        self.cv = tk.Canvas(width = 300, height = 300)
        #self.id_ = self.cv.create_rectangle(0,0,self.w,self.h)
        self.id_ = None
        self.cv.pack(expand=True, fill='both')
        
        # hand_img = Image.open("data/mky_hand.png")
        fname = os.path.dirname(__file__)+ '/data/mky_hand.png'
        hand_img = Image.open(fname)
        self.hand_img = hand_img.resize(size=(40, 40))
        
        # mickey_img = Image.open("data/mickey_mouse_black.png").convert('RGB')
        fname = os.path.dirname(__file__)+ '/data/mickey_mouse_black.png'
        mickey_img = Image.open(fname).convert('RGB')
        self.mickey_img = mickey_img.resize(size=(300,300))

        self.show_time()

    def clock_image(self):
        tm = datetime.datetime.now()
        tmhour = tm.hour
        tmminute = tm.minute
        tmsecond = tm.second
        
        # 時計の文字盤描画
        canvas = Image.new('RGBA', (300, 300), (255,255,255,0))
        draw = ImageDraw.Draw(canvas)
        for i in range(1,13):
            draw.line((280, 150, 300, 150), fill='red', width=2)
            canvas = canvas.rotate(30)
            draw = ImageDraw.Draw(canvas)
        
        # 時針の描画
        imhour = Image.new('RGBA', (300, 300), (255,255,255,0))
        drawhour = ImageDraw.Draw(imhour)
        #drawhour.polygon((150,150)+(175,140)+(250,150)+(175,160),fill='black')
        drawhour.line((150,150)+(200,150), fill='blue', width=16)
        #imhour.paste(self.hand_img,(200,130))
        imhour = imhour.rotate(-(tmhour*30+tmminute//2-90))
        canvas.paste(imhour,(0,0),imhour)
        
        # 分針の描画
        imminute = Image.new('RGBA', (300, 300), (255,255,255,0))
        drawminute = ImageDraw.Draw(imminute)
        #drawminute.polygon((150,150)+(180,145)+(270,150)+(180,155),fill='black')
        drawminute.line((150,150)+(230,150), fill='#02FF02', width=8)
        #imminute.paste(self.hand_img,(230,130))
        imminute = imminute.rotate(-(tmminute*6-90))
        canvas.paste(imminute,(0,0),imminute)
        
        # 秒針の描画
        imsecond = Image.new('RGBA', (300, 300), (255,255,255,0))
        drawsecond = ImageDraw.Draw(imsecond)
        drawsecond.line((150,150)+(270,150), fill='gray', width=2)
        #drawsecond.line((150,150)+(230,150), fill='red', width=2)
        imsecond.paste(self.hand_img,(230,130))
        imsecond = imsecond.rotate(-(tmsecond*6-90))
        canvas.paste(imsecond, (0,0), imsecond)
        
        #return canvas
        
        bg = self.mickey_img.copy()
        bg.paste(canvas,(0,0),canvas)
        return bg

    def show_time(self):

        self.cv.delete(self.id_)
        w = self.cv.winfo_width()
        h = self.cv.winfo_height()
        # 縦横小さい方をsizeにする
        size = w if w < h else h
    
        image = self.clock_image()
        # 縦横の小さい方でリサイズ
        image = image.resize((size, size))
        self.image_data = ImageTk.PhotoImage(image)
        self.id_ = self.cv.create_image(w//2, h//2, image=self.image_data)
    
        self.after(1000, self.show_time)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MKlock")
    aclock = AClock(master=root)
    aclock.mainloop()
    
