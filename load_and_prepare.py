# Модуль загрузки данных из файла отчета EXCEL и подготовка рабочего DataFrame

# загружаем необходимые библиотеки

import pandas as pd
import numpy as np
from PyQt5 import QtWidgets
from load_prepare_file import Ui_MainWindow
from collections import Counter
pd.options.display.float_format = '{:,.2f}'.format

# Данная функция удаляет в списках показателей nan
def del_nan(list_name):
    L1 = [item for item in list_name if not(pd.isnull(item)) == True]
    L1, list_name = list_name, L1
    return list_name

# Функция "обрезки" строки до нужного символа
def cut_list(lstt_act):
    last_act = []
    for lst_act in lstt_act:
        try:
            if lst_act != 'nan':
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
        path, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file',
            '', 'All files (*)')
        self.ui.led_1.setText(path)
        excel_data_df = pd.read_excel(path)

        # Заменяем пробелы в названиях столбцов на знаки "_" и избавляемся от (.)

        excel_data_df = excel_data_df.rename(columns=lambda x: x.replace(' ', '_'))
        excel_data_df = excel_data_df.rename(columns=lambda x: x.replace('.', '_'))
        """ Меняем  формат датa на " компьютерный"
        excel_data_df['Дата_открытия_лота'] = pd.to_datetime(excel_data_df['Дата_открытия_лота'],
            infer_datetime_format=True)
        excel_data_df['Дата_закрытия_лота'] = pd.to_datetime(excel_data_df['Дата_закрытия_лота'],
            infer_datetime_format=True)
        """
        # переименуем столбец Исполнитель_МТО_(Ф_И_О) на Исполнитель_МТО ("отрежем" хвост _(Ф_И_О))
        excel_data_df = excel_data_df.rename(columns={'Исполнитель_МТО_(Ф_И_О_)': 'Исполнитель_МТО'})
        excel_data_df[['Номер_лота']] = excel_data_df[['Номер_лота']].astype(object)  # заменим тип с целого на object
        # excel_data_df - это сырые, несгруппированные данные из таблицы Excel

        # заменим в числовых полях excel_data_df все отсутствующие данные (nan) на ноль (0)
        excel_data_df['Кол-во_поставщика'] = excel_data_df['Кол-во_поставщика'].replace(np.nan, 0)
        excel_data_df['Сумма_контракта'] = excel_data_df['Сумма_контракта'].replace(np.nan, 0)

        columns_name = excel_data_df.columns

        excel_data_df = excel_data_df.drop_duplicates()

        # создадим копию основного датафрейма и запишем его в текущую директорию
        # data_df = excel_data_df.copy()
        excel_data_df.to_csv("data_df.csv")
        self.ui.led_3.clear()
        self.ui.led_3.setText("DataFrame data_df подготовлен и готов к анализу")
        
if __name__== "__main__":
    import sys
    app = QtWidgets.QApplication([])
    application = my_win()
    application.show()
    sys.exit(app.exec_())