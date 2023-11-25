# Из youtube, "Источник знаний", Python GUI tkinter #22

from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import Notebook


class Window:
	def __init__(self, width, height, title="Анализ закупочных процессов", resizable=(True, True)):
		self.root = Tk()
		self.root.title(title)
		self.root.geometry(f"{width}x{height}")
		self.root.resizable(resizable[0], resizable[1])
		self.root.iconbitmap("python_104451.ico")
		self.tabs_control = Notebook(self.root, height=300, width=30, padding=(10,10,10,10)) # это управление вкладками (notebook)
		
	
	# можно программно определить какую вкладку и когда переключали
		self.tabs_control.bind("<<NotebookTabChanged>>", self.tab_changed)
		
	def run(self):
		self.draw_widgets()
		self.root.mainloop()
		
	def draw_widgets(self):
		self.draw_menu()
		self.tabs_control.pack(fill=BOTH, expand=1)
		self.tab_1 = Frame(self.tabs_control)  # создается первая вкладка
		self.tabs_control.add(self.tab_1, text="    First_tab    ")  # вкладка добавляется в tab_control
		
		self.tab_2 = Frame(self.tabs_control)
		self.tabs_control.add(self.tab_2, text="     Second_tab     ")
		Label(self.tab_1, text="Приветствую на вкладке №1", bg="lime").pack(fill=BOTH, expand=1)
		Text(self.tab_2).pack()
		
		self.tab_3 = Frame(self.tabs_control)
		self.tabs_control.insert(END, self.tab_3, text="     Third tab     ") # вкладку можно добавлять сразу нарисовав ее в draw_widgets
		self.tab_4 = Frame(self.tabs_control)
		self.tabs_control.insert(END, self.tab_4, text="     Fourth tab     ")
		
		self.tabs_control.select(self.tab_3)
		print(f"Selected tab: {self.tabs_control.select()}") # Это пример программного попадания в нужную вкладку
		
		#  и эдесь же пример вывода параметров необходимой вкладки
		print(f"tab_4 params: {self.tabs_control.tab(self.tab_4)}")
		
		
	def draw_menu(self):
		menu_bar = Menu(self.root)
		
		file_menu = Menu(menu_bar, tearoff=0)  # здесь привязка идет не к руту а к menu_bar
		file_menu.add_separator()
		file_menu.add_command(label="Выйти", command=self.exit)
		
		info_menu = Menu(menu_bar, tearoff=0)
		info_menu.add_command(label="About", command=self.show_info)
		
		menu_bar.add_cascade(label="File", menu=file_menu)
		menu_bar.add_cascade(label="Справка", menu=info_menu)
		self.root.configure(menu=menu_bar)
		
	def exit(self):
		choice = mb.askyesno("Quit", "Do you want to quit?")
		if choice:
			self.root.destroy()
			
	def tab_changed(self, event):
		print(f"Changed tab to: {self.tabs_control.select()}")
	
	def show_info(self):
		mb.showinfo("Информация", "Лучшее графическое приложение")
		
		
		
		
if __name__ == "__main__":
	window = Window(1090, 542, "   Анализ закупочных процессов")
	window.run()