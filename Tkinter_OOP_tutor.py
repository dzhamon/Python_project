# Библиотека Tkinter-9-Использование ООП
from tkinter import *

class Question:
	def __init__(self, main):
		self.entry1 = Entry(main, width=3, font=15)
		self.button1 = Button(main, text="Проверить")
		self.label1 = Label(main, width=27, font=15)
		
		self.entry1.grid(roe=0, column=0)
		self.button1.grid(roe=0, column=1)
		self.label1.grid(roe=0, column=2)
		
		self.button1.bind("<Button-1>", self.answer)
		
	def answer(self, event):
		txt = self.entry1.get()
		
		try:
			if int(txt) < 18:
				self.label1['text'] = 'Пока сюда нельзя!'
			else:
				self.label1['text'] = 'Добро пожаловать!'
		except ValueError:
			self.label1['text'] = 'Введите корректный возраст!'


root = Tk()



root.mainloop()