# Построение GUI на Tkinter

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Анализ закупочных процессов")
root.iconbitmap(default="icons8-питон-48.png")
# root.iconphoto(False, icon)
root.geometry("1090x542+0+0") # ширина Х высота Y
# root.resizable(False, False) # запрет изменения размеров главного окна

# Создаем набор вкладок
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill=BOTH)

# Создаем пару фреймов
frame1 = ttk.LabelFrame(notebook)
frame2 = ttk.LabelFrame(notebook)

frame1.pack(fill=BOTH, expand=True)
frame2.pack(fill=BOTH, expand=True)

# Добавляем фреймы в качестве вкладок
notebook.add(frame1, text='Главное')
notebook.add(frame2, text='Конкурсные проработки')

lbl = Label(frame1, text='Привет!', background='red', foreground='yellow', font=('Courier'))
lbl.grid(column=0, row=0)

btn = Button(frame1, text='Click_me')
btn.grid(column=1, row=0)

lbl_1 = Label(frame2,text='это текст второй вкладки')
lbl_1.grid(column=0, row=0)
root.mainloop()