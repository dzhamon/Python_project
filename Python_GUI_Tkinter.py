# Канал Ютуб Источник знаний, Python GUI tkinter #3 - Дочерние окна
# https://www.youtube.com/watch?v=grnchooO2wU

from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar

class Window:
	def __init__(self, width, height, title="Анализ закупочных процессов", resizable=(True, True)):
		self.root = Tk()
		self.root.title(title)
		self.root.geometry(f"{width}x{height}")
		self.root.resizable(resizable[0], resizable[1])
		self.root.iconbitmap("python_104451.ico")
		
		self.pb = Progressbar(self.root, orient=HORIZONTAL, mode="determinate", length=400)
		
		self.label = Label(self.root, text='  Главное окно  ', bg='yellow', font=("Courier 12"))
		print(self.label.configure().keys())
		# если использовать bg='#RGB', то номера сочетания цветов можно выбирать на сайте
		# (google) Color Picker. А можно указывать 'yellow', 'green' и т.д.
		self.label2 = Label(self.root, text="  Конкурсные проработки  ", bg='yellow', font=('Courier 12'))
		
		# здесь пример использования insert - вставки текста в поле entry
		text_var = " Меня вставят в поле entry "
		# len_text = int(len(text_var))
		self.entry = Entry(self.root, width=len(text_var))
		
		len_text = len(text_var)
		self.entry.insert(0, text_var)
		
		self.numbers = Combobox(self.root, values=(1, 2, 3, 4, 5), state='readonly')
			
	def run(self):
		self.draw_widgets()
		self.root.mainloop()
		
		
		
	def draw_widgets(self):
		top_frame = LabelFrame(self.root, text="Top Frame")
		bottom_frame = LabelFrame(self.root, text="Bottom_Frame")
		top_frame.pack(anchor=NW, padx=10, pady=10, ipady=10, fill='x') # pad задает отступ для фрейма вне экрана (от границы окна)
		bottom_frame.pack(anchor=NW, padx=10, ipadx=10, ipady=10, fill='x') # ipad задает отступы внутри фрейма
		
		Label(top_frame, width=30, height=2, bg='red', text='First').pack(side=LEFT, padx=10)
		Label(top_frame, width=30, height=2, bg='orange', text='Second').pack(side=LEFT, padx=10)
		Label(bottom_frame, width=30, height=2, bg='yellow', text='Third').pack(side=LEFT, padx=10)
		Label(bottom_frame, width=30, height=2, bg='Green', text='Fourth').pack(side=LEFT)
		self.label.pack(anchor=NW, side=LEFT ) #padx=20, pady=20)
		self.label2.pack(anchor=NW, side=LEFT)
		# параметры label - pad - это отступы по x и y, relief - это рельеф
	
		Button(self.root, text='Info', width=10, command= lambda: mb.showinfo("Info", "Info message")).pack()
		Button(self.root, text='Warning', width=10, command=lambda: mb.showwarning("Warning", "Warning message")).pack()
		Button(self.root, text='Error', width=10, command=lambda: mb.showerror("Error", "Error message")).pack()
		
		Button(self.root, text='Quit', width=10, command=self.exit).pack()
		
		self.entry.pack()
		Button(self.root, text="Кнопка из Entry", width=int(len("Кнопка из entry")), command=self.get_text_entry).pack()
		
		self.numbers.pack(anchor=W)
		Button(self.root, text="Get", width=10, command=self.get_number).pack(anchor=W)
		family_tup = ('Иванов', 'Петров', 'Сидоров')
		c = Combobox(self.root, values=family_tup)
		c.current(0) # 0 - это элемент кортежа values, который должен быть прорисован в комбобоксе
		c.pack()
		
		self.pb.pack()
		from time import sleep
		for i in range(401):
			self.pb.configure(value=i)
			self.pb.update()
			sleep(0.05)
		self.pb.configure(value=0)
	
	# значение из комбобокс можно получить и не задействуя специальную для этого кнопку Button
	# для этого используется метод bind
		self.numbers.bind("<<ComboboxSelected>>", self.sel_changed)
		
	def get_number(self): # функция получения значения выбранного в combobox
		value = self.numbers.get() #value - это значение выбранное в комбобоксе
		index = self.numbers.current() # index - это индекс выбранного значения
		mb.showinfo("Get Info", f"Index: {index}, value: {value}")
	
		
	def exit(self):
		choice = mb.askyesno("Quit", "Do you want to quit?")
		if choice:
			self.root.destroy()
		else:
			Label(self.root, text='Мы займемся другой работой!').pack()
			
	def sel_changed(self, event):
		value = self.numbers.get()  # value - это значение выбранное в комбобоксе
		index = self.numbers.current()  # index - это индекс выбранного значения
		mb.showinfo("Get Info", index=index, value=value)
	
			
	def get_text_entry(self):
		text = self.entry.get()
		mb.showinfo("Текст из Entry", text)
		
	def repeat_text(self):
		text = self.entry.get()
		
		
		
if __name__ =="__main__":
	window = Window(1090,542, "   Анализ закупочных процессов")
	window.run()
	

C:\Users\dzhamshed.amonov\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\JetBrains\PyCharm Community Edition 2023.2.1