# загружаем необходимые библиотеки

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
from tkinter import messagebox as mb
from tkinter import filedialog as fd

import pandas as pd

class Window:
	def __init__(self, width, height, title="Анализ закупочных процессов", resizable=(True, True)):
		self.root = Tk()
		self.root.title(title)
		self.root.geometry(f"{width}x{height}")
		self.root.resizable(resizable[0], resizable[1])
		# if icon is not None:
		self.root.iconbitmap("python_104451.ico")
		self.tabs_control = Notebook(self.root, height=100, width=30,
		                             padding=(5, 5, 5, 5))  # это управление вкладками (notebook)
		
		#self.text = ScrolledText(self.root, width=1080, height=540, padx=10, pady=10)
		
	
	def df_tolist(self, df):
		# Create an empty list
		Row_list = []
		
		# Iterate over each row
		for i in range((df.shape[0])):
			# Using iloc to access the values of
			# the current row denoted by "i"
			Row_list.append(list(df.iloc[i, :]))
		
		# Print the list
		return Row_list
	
	
	def run(self):
		self.draw_widgets()
		self.root.mainloop()
	
	def draw_widgets(self):
		self.draw_menu()
		
		self.draw_treeview()
		
		self.tabs_control.pack(fill=BOTH, expand=1)
		self.tab_1 = Frame(self.tabs_control)
		self.tabs_control.add(self.tab_1, text="    Общие загруженные данные    ")
		
		self.tabs_control.tab_1.draw_treeview()
		
		self.tab_2 = Frame(self.tabs_control)
		self.tabs_control.add(self.tab_2, text="    Это второе окно    ")
		
	def draw_treeview(self):
		employes = [["Tom", 38, "tom@email.com"], ["Bob", 42, "bob@email.com"], ["Sam", 28, "sam@email.com"],
		          ["Alice", 33, "alice@email.com"], ["Kate", 21, "kate@email.com"], ["Ann", 24, "ann@email.com"]]
		columns = ['name', 'age', 'email']
		tree_view = ttk.Treeview(self.tabs_control, columns=columns, show="headings")
		
		# Определяем заголовки
		for i in range(len(columns)):
			tree_view.heading(columns[i], text=columns[i], anchor=W)
		
		# добавляем данные
		for person in employes:
			tree_view.insert(self.tabs_control, END, values=person) # на этой строке выдает ошибку - не найден Notebook
		
	def draw_tree(self):
		# Данные для отображения
		people = [["Tom", 38, "tom@email.com"], ["Bob", 42, "bob@email.com"], ["Sam", 28, "sam@email.com"],
		          ["Alice", 33, "alice@email.com"], ["Kate", 21, "kate@email.com"], ["Ann", 24, "ann@email.com"],
		          ["Alim", 37, "alice@email.com"], ["Katerin", 21, "kate@email.com"], ["Anna", 24, "ann@email.com"],
		          ["Balice", 31, "alice@email.com"], ["Karine", 21, "kate@email.com"], ["Anyuta", 24, "ann@email.com"],
		          ["Mike", 34, "mike@email.com"], ["Alex", 52, "alex@email.com"], ["Jess", 28, "jess@email.com"]]

		tab_columns = ['name', 'age', 'email']
		self.tree = ttk.Treeview(self.root, columns=tab_columns, show="headings")
		self.tree.pack(fill=BOTH, expand=1)
		# Определяем заголовки
		for i in range(len(tab_columns)):
			self.tree.heading(tab_columns[i], text=tab_columns[i], anchor=W)

		# добавляем данные
		for person in people:
			self.tree.insert("", END, values=person)
		
	def draw_menu(self):
		menu_bar = Menu(self.root)
		
		file_menu = Menu(menu_bar, tearoff=0) # здесь привязка идет не к руту а к menu_bar
		file_menu.add_command(label="Открыть ...", command=self.open_file)
		file_menu.add_command(label="Сохранить как ...", command=self.save_file)
		file_menu.add_command(label="Открыть папку", command=self.open_dir)
		file_menu.add_separator()
		file_menu.add_command(label="Выйти", command=self.exit)
		
		# структура выпадающего вложенного меню
		edit_menu = Menu(menu_bar, tearoff=0)
		parameters_menu = Menu(edit_menu, tearoff=0)
		parameters_menu.add_checkbutton(label="Автосохранение", offvalue=0, onvalue=1, variable=self.auto_save)
		parameters_menu.add_checkbutton(label="Автозагрузка", offvalue=0, onvalue=1, variable=self.auto_load)
		edit_menu.add_cascade(label="Параметры", menu=parameters_menu)
		edit_menu.add_separator()
		
		values_menu = Menu(edit_menu, tearoff=0)
		values_menu.add_radiobutton(label="Один", value=1, variable=self.value)
		values_menu.add_radiobutton(label="Два", value=2, variable=self.value)
		values_menu.add_radiobutton(label="Три", value=3, variable=self.value)
		edit_menu.add_cascade(label="Значение",menu=values_menu)
		
		info_menu = Menu(menu_bar, tearoff=0)
		info_menu.add_command(label="About", command=self.show_info)
		
		menu_bar.add_cascade(label="Файл", font=("Courier", 13), menu=file_menu)
		file_menu.config(font=("Courier", 11))
		menu_bar.add_cascade(label="Настройки", menu=edit_menu)
		edit_menu.config(font=("Courier", 11))
		menu_bar.add_cascade(label="Справка", menu=info_menu)
		info_menu.config(font=("Courier", 11))
		self.root.configure(menu=menu_bar)
		menu_bar.config(font=("Courier", 11))
		
	def open_dir(self):
		path = fd.askdirectory(mustexit=True)
		self.text.insert(END, f"Папка {path}\n")
	
	
	def open_file(self):
		global tab_columns
		# здесь вариант программирования поиска названия файлов
		wanted_files = (("DATA files", "*.xlsx; *.csv"),
		                ("ALL", "*.*")) # здесь создаёь маски разыскиваемых файлов

		file_name = fd.askopenfilename(initialdir="D:/", title="FIND A FILE", filetypes=wanted_files)

		excel_data = pd.read_csv(file_name)
		
		tab_columns = excel_data.columns
		return
		
		
	def save_file(self):
		name = fd.asksaveasfilename(filetypes=(("TEXT files","*.txt"), ("Python files", "*.py")))
		if name:
			self.text.insert((END, f"Сохранить файл по пути {name}\n"))
			with open(name, "w") as f:
				f.write("123")
		# выше вариант записи названия файла
		# ниже вариант записи самого файла
		file = fd.asksaveasfile()
		file.write('123')
		file.close()
		
	def show_info(self):
		mb.showinfo("Информация", "Лучшее графическое приложение")
		
	def auto_save_changed(self):
		mb.showinfo("Auto_save", f"Value: {self.auto_save.get()}")
		
	def cmd(self): # будет выполняться при выборе Файл-Сохранить
		mb.showinfo("123", "123")
	
	def exit(self):
		choice = mb.askyesno("Quit", "Do you want to quit?")
		if choice:
			self.root.destroy()


if __name__ == "__main__":
	window = Window(1090, 542, "   Анализ закупочных процессов")
	window.run()

