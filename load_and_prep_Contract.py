# Модуль загрузки данных из файла отчета EXCEL и подготовка рабочего DataFrame

# загружаем необходимые библиотеки

import pandas as pd
import numpy as np
from PyQt5 import QtWidgets
from load_prep_ontract import Ui_MainWindow
from collections import Counter

pd.options.display.float_format = '{:,.2f}'.format


# Данная функция удаляет в списках показателей nan
def del_nan(list_name):
	L1 = [item for item in list_name if not (pd.isnull(item))==True]
	L1, list_name = list_name, L1
	return list_name


# Функция "обрезки" строки до нужного символа
def cut_list(lstt_act):
	last_act = []
	for lst_act in lstt_act:
		try:
			if lst_act!='nan':
				last_act.append(lst_act.partition(' (')[0])
		except AttributeError:
			continue
	return last_act


# Функция формирования списка уникальных Лотов из их общего числа (из числа повторяющихся Лотов)

def get_unique_numbers(list_tup):
	list_of_unique_numbers = []
	unique_numbers = set(list_tup)
	
	for number in unique_numbers:
		list_of_unique_numbers.append(number)
	
	return list_of_unique_numbers


# ===============================================
class my_win(QtWidgets.QMainWindow):
	def __init__(self):
		super(my_win, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.btn_1.clicked.connect(self.choose_file)
	
	def choose_file(self):
		self.ui.led_2.clear()
		self.ui.led_2.setText("Началась загрузка данных и их подготовка к анализу")
		path, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file', '', 'All files (*)')
		self.ui.led_1.setText(path)
		contract_df = pd.read_excel(path)
		contract_df = contract_df.drop_duplicates()
		
		# Переименуем все столбцы нашего датафрейма contract_df
		contract_df.columns = ['lot_number', 'lot_end_date', 'contract_number', 'contract_date', 'contract_actor',
		                        'contract_owner', 'goods_name', 'vendor_unit', 'goods_qty', 'unit', 'unit_price',
		                       'amount_of_goods', 'additional_expenses', 'total_price', 'currency']
		
		
		# Меняем  формат датa на " компьютерный"
		
		contract_df['lot_end_date'] = pd.to_datetime(contract_df['lot_end_date'], infer_datetime_format=True)
		
		# все отсутствующие Даты заключения контракта заменяем на '01.01.1900'.
		contract_df['contract_date'] = contract_df['contract_date'].fillna('01.01.1900')
		# contract_df['contract_date'] = pd.to_datetime(contract_df['contract_date'], infer_datetime_format=True)
		
		# contract_df - это сырые, несгруппированные данные из таблицы Excel
		
		# заменим в числовых полях contract_df все отсутствующие данные (nan) на ноль (0)
		contract_df['goods_qty'] = contract_df['goods_qty'].replace(np.nan, 0)
		contract_df['total_price'] = contract_df['total_price'].replace(np.nan, 0)
		contract_df['unit_price'] = contract_df['unit_price'].replace(np.nan, 0)
		contract_df['additional_expenses'] = contract_df['additional_expenses'].replace(np.nan, 0)
		
		columns_name = contract_df.columns
		
		# запишем подготовленный contract_df в contr_df.csv
		contract_df.to_csv("contract_df.csv")
		self.ui.led_3.clear()
		self.ui.led_3.setText("DataFrame contr_df подготовлен и готов к анализу")


if __name__=="__main__":
	import sys
	app = QtWidgets.QApplication([])
	application = my_win()
	application.show()
	sys.exit(app.exec_())