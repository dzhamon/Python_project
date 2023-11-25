# Загружаем необходимые библиотеки
from datetime import datetime
from itertools import groupby

import numpy as np
import pandas as pd
from PyQt5 import QtWidgets

from my_new_form_v2 import Ui_MainWindow

pd.options.display.float_format = '{:,.2f}'.format

# Эта функция собирет в массив только уникальные элементы
def get_unique_only(st):
    #Empty list
    lst1 = []
    count = 0
    # traverse the array
    for i in st:
        if i != 0:
            if i not in lst1:
                count += 1
                lst1.append(i)
    return lst1

# Функция построения группировок Лотов по показателям
# здесь: grouping_names - список с выделенными показателями, inn_group - список словарей dict_group
def group_build(grouping_names, inn_group):
    out_group = []
    for m in range(len(grouping_names)):
        out_group.append('')
    i = 0
    for grouping_name in grouping_names:
        out_group[i] = []
        for sp_num in range(len(inn_group)):
            for value in inn_group[sp_num].values():
                if grouping_name != value:
                    continue
                else:
                    out_group[i].append(inn_group[sp_num])
        i = i + 1
    return out_group


""" Задача этой функции - принять параметры группировки информации
    и передать в основной код сгруппированный список словарей """
def sort_func(group_dict, pokazat_name, var_tmp):
    def key_func(k):
        return k[pokazat_name]

    # sort dict_group data by 'company' key.
    group_dict = sorted(group_dict, key=key_func)

    group_tmp = groupby(group_dict, key=key_func)
    dd_tmp = []
    for key, value in group_tmp:
        if key==var_tmp:
            dd_tmp.append(list(value))
    return dd_tmp

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

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.setText("Выберите файл")

        # Здесь будут методы реакции на нажатие кнопок
        self.ui.pushButton.clicked.connect(self.choose_file)  # choose_file функция действия по нажатию на кнопку
        
        # -----------------------------------------------------------------------
    def choose_file(self):
        path, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file',
            '', 'All files (*)')
        self.ui.lineEdit.setText(path)
        print(path)
        start_time = datetime.now()
        excel_data_df = pd.read_excel(path)
        # Заменяем пробелы в названиях столбцов на знаки "_" и избавляемся от (.)
        excel_data_df = excel_data_df.rename(columns=lambda x: x.replace(' ', '_'))
        excel_data_df = excel_data_df.rename(columns=lambda x: x.replace('.', '_'))
        # Меняем  формат датa на " компьютерный"
        excel_data_df['Дата_открытия_лота'] = pd.to_datetime(excel_data_df['Дата_открытия_лота'],
            infer_datetime_format=True)
        excel_data_df['Дата_закрытия_лота'] = pd.to_datetime(excel_data_df['Дата_закрытия_лота'],
            infer_datetime_format=True)

        # переименуем столбец Исполнитель_МТО_(Ф_И_О) на Исполнитель_МТО
        excel_data_df = excel_data_df.rename(columns={'Исполнитель_МТО_(Ф_И_О_)': 'Исполнитель_МТО'})
        
        excel_data_df[['Номер_лота']] = excel_data_df[['Номер_лота']].astype(object)
        # excel_data_df - это сырые, несгруппированные данные из таблицы Excel

        # заменим в числовых полях excel_data_df все отсутствующие данные (nan) на ноль (0)
        excel_data_df['Количество_ТМЦ'] = excel_data_df['Количество_ТМЦ'].replace(np.nan, 0)
        excel_data_df['Сумма_контракта'] = excel_data_df['Сумма_контракта'].replace(np.nan, 0)
        print('Подготовка данных занимает -->', (datetime.now()-start_time))

        print('Step 1')
        start_time = datetime.now()
        """ создадим списки - Номера Лотов, исполнителей, дисциплины, наим проектов, контрагентов, валюты """
        number_lots = get_unique_only(excel_data_df['Номер_лота'])
        actor_names = get_unique_only(excel_data_df['Исполнитель_МТО'])
        discipline_names = get_unique_only(excel_data_df['Дисциплина'])
        project_names = get_unique_only(excel_data_df['Наименование_проекта'])
        contragent_winners = get_unique_only(excel_data_df['Присуждено_контрагенту'])
        currency_names = get_unique_only(excel_data_df['Валюты_контракта'])
        print('Step 2')
        # Оставляем в созданных массивах только уникальные элементы
        number_lots = get_unique_only(del_nan(number_lots))
        actor_names = get_unique_only(del_nan(actor_names))
        discipline_names = get_unique_only(del_nan(discipline_names))
        project_names = get_unique_only(del_nan(project_names))
        contragent_winners = get_unique_only(del_nan(contragent_winners))
        currency_names = get_unique_only(del_nan(currency_names))

        # Создаем рабочий DataFrame
        data_df = excel_data_df.copy()
        print('Step 4')

        # Сгруппируем основной датафрейм
        ser_grpd_df = data_df.groupby(['Номер_лота', 'Дисциплина', 'Наименование_проекта', 'Дата_открытия_лота',
                                       'Дата_закрытия_лота', 'Исполнитель_МТО', 'Присуждено_контрагенту',
                                       'Валюты_контракта']).sum()
        df_ser_grpd = ser_grpd_df.reset_index()

        """ Подготовим список наименований колонок, с которыми мы будем работать  """
        global list_cols
        global dict_names

        list_cols = ['Номер_лота', 'Дисциплина', 'Наименование_проекта',
                     'Дата_открытия_лота', 'Дата_закрытия_лота', 'Исполнитель_МТО_(Ф_И_О_)',
                     'Присуждено_контрагенту', 'Валюты_контракта', 'Сумма_контракта']

        dict_names = {'Номер_лота': number_lots, 'Дисциплина': discipline_names,
                      'Наименование_проекта': project_names, 'Исполнитель_МТО_(Ф_И_О_)': actor_names,
                      'Присуждено_контрагенту': contragent_winners, 'Валюты_контракта': currency_names}
        # приведенные выше list_cols и dict_names необходимо записать в виде кода
        
        # Группировка data_df - суммы и средние значения сумм в разрезе валют
        # по дисциплинам Компании
        agg_sum = {'Сумма_контракта': ['sum', 'mean']}
        data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_sum)

        # Суммы контрактов (прработок) по проектам Компании в разрезе валют
        agg_sum = {'Сумма_контракта': ['sum', 'mean']}
        data_df.groupby(['Наименование_проекта', 'Валюты_контракта']).agg(agg_sum)

        # Количество контрактов (проработок) в разрезе Дисциплин

        agg_func_count = {'Дисциплина': ['count']}
        data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_func_count)

        # а как это количество проработок делится между Исполителями?

        agg_func_count = {'Дисциплина': ['count']}
        data_actors_count = data_df.groupby(['Дисциплина', 'Исполнитель_МТО', 'Валюты_контракта']).agg(agg_func_count)

        # Группировка data_df - суммы и средние значения сумм в разрезе валют
        # по дисциплинам Компании
        agg_sum = {'Сумма_контракта': ['sum', 'mean']}
        data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_sum)

        # Суммы контрактов (прработок) по проектам Компании в разрезе валют
        agg_sum = {'Сумма_контракта': ['sum', 'mean']}
        data_df.groupby(['Наименование_проекта', 'Валюты_контракта']).agg(agg_sum)

        # Количество контрактов (проработок) в разрезе Дисциплин

        agg_func_count = {'Дисциплина': ['count']}
        data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_func_count)

        # а как это количество проработок делится между Исполителями?

        agg_func_count = {'Дисциплина': ['count']}
        data_actors_count = data_df.groupby(['Дисциплина', 'Исполнитель_МТО', 'Валюты_контракта']).agg(agg_func_count)

        # Полный Алгоритм выбора всех контрактов, заключенных одним отдельно взятым исполнителем
        # и сортировка его в порядке возрастания

        # 1. Формируется кросс-таблица:  Контрагенты-Исполнитель ЛОТа и записываем её в
        # переменную vib_contr_acts

        vib_contr_acts = pd.crosstab(excel_data_df['Присуждено_контрагенту'], [excel_data_df['Исполнитель_МТО']])

        # переименуем столбцы таблицы на сокращенные (без телефонов). Формат - "Фамилия Имя Отчество".

        list_acts = vib_contr_acts.columns
        list_acts = cut_list(list_acts)
        vib_actors = vib_contr_acts.rename(columns=dict(zip(vib_contr_acts.columns, list_acts)))

        """ далее код в порядке эксперимента по одному исполнителю """

        """ Попробуем переделать код, чтобы он работал не на одного пользователя, а на всех
            из ранее созданного словаря
        """
        dict_disc_act_freq = {}
        for key, value in dict_discip_actors.items():
            list_key = []
            dict_var_tmp = {}
            for val in value:
                tupl_list = []
                i = 0
                for idx in vib_actors.index:
                    if vib_actors.loc[idx, val]!=0:
                        tupl_tmp = (idx, vib_actors.loc[idx, val])
                        tupl_list.append(tupl_tmp)
                    i = i + 1
                tupl_list.sort(key=lambda x: x[1], reverse=True)
                dict_var_tmp[val] = tupl_list
            list_key.append(dict_var_tmp)
            dict_disc_act_freq[key] = list_key
        """ словарь формируется в полном объеме, согласно заложенной логике """
        
        print('группировка данных и создание словарей --> ', (datetime.now()-start_time))

        global list_columns
        list_columns = data_df.columns
        for i in range(len(list_columns)):
            self.ui.comboBox.addItem(list_columns[i])
            i += 1
        self.ui.comboBox.activated[str].connect(self.onActivated)

    # эта функция выполняется после выбора элемента из ComboBox (by clicking)
    def onActivated(self, text):
        def new_list(old_list):
            n_list = [item for item in old_list if not(pd.isnull(item))==True]
            return n_list
        global pokaz_name
        for list_col in list_columns:
            if text == list_col:
                pokaz_name = text
                print(pokaz_name)
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(new_list(dict_names.get(pokaz_name)))
        self.ui.listWidget.clicked.connect(self.item_clicked)
        

    def item_clicked(self, item):
        item = self.ui.listWidget.currentItem()
        print(item, '->', 'выбор из первого окошка')
        disc_name = (item.text())
        print(disc_name, '->', 'Это здесь')

        # Далее. По переменной disc_name из словаря dict_disc_act_freq необходимо выделить Исполнителей
        # этой дисциплины и вывести в новый listWidget_2

# -------------------------------------------------------
if __name__== "__main__":
    import sys
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec_())