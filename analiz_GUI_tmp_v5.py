# analiz_GUI_tmp_v5 - программа анализа КЛ на основе "Отчета о конкурсных проработках"
# Загружаем необходимые библиотеки
# from my_new_form_tmp import Ui_MainWindow
from itertools import groupby
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
from collections import Counter

from my_new_form_v2 import Ui_MainWindow

pd.options.display.float_format = '{:,.2f}'.format

disc_name = []
isp_name = []
dict_disc_act_freq = {}

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

# Функция формирования списка уникальных Лотов из их общего числа (из числа повторяющихся Лотов)

def get_unique_numbers(list_tup):
    list_of_unique_numbers = []
    unique_numbers = set(list_tup)

    for number in unique_numbers:
        list_of_unique_numbers.append(number)

    return list_of_unique_numbers

# ========================================================

def disc_isp():
    global disc_name
    global isp_name
    list_of_freq = dict_disc_act_freq[disc_name][0][isp_name][:20]
    df = pd.DataFrame(list_of_freq)
    print(isp_name)
    print(df)
    return
# ========================================================
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.setText("Выберите файл")

        # Здесь будут методы реакции на нажатие кнопок
        self.ui.pushButton.clicked.connect(self.choose_file)  # choose_file функция действия по нажатию на кнопку
        self.setStyleSheet("QLineEdit_3 { background-color: yellow }")
        
        
        # Зжесь кнопка формирования выборки по отобранным параметрам
        
        self.ui.pushButton_2.clicked.connect(disc_isp)

        #-------------------------------------------------------------------------

    def choose_file(self):
        global disc_name
        global dict_disc_act_freq
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_3.setText("Началась загрузка данных и их подготовка к анализу")
        path, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file',
            '', 'All files (*)')
        self.ui.lineEdit.setText(path)
        excel_data_df = pd.read_excel(path)
        
        # Заменяем пробелы в названиях столбцов на знаки "_" и избавляемся от (.)

        excel_data_df = excel_data_df.rename(columns=lambda x: x.replace(' ', '_'))
        excel_data_df = excel_data_df.rename(columns=lambda x: x.replace('.', '_'))
        # Меняем  формат датa на " компьютерный"
        excel_data_df['Дата_открытия_лота'] = pd.to_datetime(excel_data_df['Дата_открытия_лота'],
            infer_datetime_format=True)
        excel_data_df['Дата_закрытия_лота'] = pd.to_datetime(excel_data_df['Дата_закрытия_лота'],
            infer_datetime_format=True)

        # переименуем столбец Исполнитель_МТО_(Ф_И_О) на Исполнитель_МТО ("отрежем" хвост _(Ф_И_О))
        excel_data_df = excel_data_df.rename(columns = {'Исполнитель_МТО_(Ф_И_О_)' : 'Исполнитель_МТО'})
        excel_data_df[['Номер_лота']] = excel_data_df[['Номер_лота']].astype(object) # заменим тип с целого на object
        # excel_data_df - это сырые, несгруппированные данные из таблицы Excel

        # заменим в числовых полях excel_data_df все отсутствующие данные (nan) на ноль (0)
        excel_data_df['Количество_ТМЦ'] = excel_data_df['Количество_ТМЦ'].replace(np.nan, 0)
        excel_data_df['Сумма_контракта'] = excel_data_df['Сумма_контракта'].replace(np.nan, 0)

        columns_name = excel_data_df.columns
        
        # в основном датафрейме удалим все повторяющиеся строки в Лотах
        number_lots = del_nan(set(excel_data_df['Номер_лота']))
        for number_lot in number_lots:
            df_vrem = ''
            df_vrem = excel_data_df.loc[excel_data_df['Номер_лота']==number_lot]
            if len(df_vrem) > 1:
                list_tup = []
                for ind in range(len(df_vrem)):
                    ssl = df_vrem.iloc[[ind][0]].to_list()
                    ssl[4] = ssl[4].date()
                    ssl[5] = ssl[5].date()
                    ssl = tuple(ssl)
                    list_tup.append(ssl)
                list_unique_tup = get_unique_numbers(list_tup)
                df_vrem = pd.DataFrame(list_unique_tup, columns = columns_name)
                continue
            else:
                    # удаляем из excel_data_df строки по номеру лота (number_lot)
                    excel_data_df = excel_data_df[excel_data_df['Номер_лота']!=number_lot]
                    # добавляем df_vrem в конец excel_data_df
                    excel_data_df = excel_data_df.append(df_vrem, ignore_index=True)

        """ создадим списки - Номера Лотов, исполнителей, дисциплины, наим проектов, контрагентов, валюты """
        number_lots = del_nan(get_unique_only(excel_data_df['Номер_лота']))
        actor_names = del_nan(get_unique_only(excel_data_df['Исполнитель_МТО']))
        discipline_names = del_nan(get_unique_only(excel_data_df['Дисциплина']))
        project_names = del_nan(get_unique_only(excel_data_df['Наименование_проекта']))
        contragent_winners = del_nan(get_unique_only(excel_data_df['Присуждено_контрагенту']))
        currency_names = del_nan(get_unique_only(excel_data_df['Валюты_контракта']))
        
        global dict_names
        dict_names = {'Номер_лота': number_lots, 'Дисциплина': discipline_names,
                      'Наименование_проекта': project_names, 'Исполнитель_МТО_(Ф_И_О_)': actor_names,
                      'Присуждено_контрагенту': contragent_winners, 'Валюты_контракта': currency_names}
        
        # создадим копию основного датафрейма
        data_df = excel_data_df.copy()

        # Сгруппируем основной датафрейм
        ser_grouped = data_df.groupby(['Номер_лота', 'Дисциплина', 'Наименование_проекта', 'Дата_открытия_лота',
                                       'Дата_закрытия_лота', 'Исполнитель_МТО', 'Присуждено_контрагенту',
                                       'Валюты_контракта'])['Сумма_контракта'].sum()
                
        
        list_cols = data_df.columns # список всех наименований столбцов Таблицы
        

        # Этот dict_base очень удобный и адекватный основной источник информации для
        # построения различного рода словарей
        dict_base = ser_grouped.to_dict()

        """ Построим на основе  dict_base несколько словарей """

        # 1. Построим словарь - dict_discip_actors (Дисциплины : Исполнители)
        
        global dict_discip_actors
        global disc_name
        dict_discip_actors = {}
        for disc_name in discipline_names:
            disc_list = []
            for key in dict_base:
                if disc_name in key:
                    disc_list.append(key[5].partition(' (')[0])
                else:
                    continue
            disc_list = get_unique_only(disc_list)
            disc_list = cut_list(disc_list)
            dict_discip_actors[disc_name] = disc_list
       
        # dict_discip_actors - это словарь, где ключи - наименования Дисциплин,
        # значения - список Исполнителей (формат Фамилия Имя Отчество)

        # 2. Создаем второй словарь dict_act_contrg. Здесь придется работать с dict_base и
        # только что созданным dict_discip_actors

        dict_act_contrg = {}
        for key1, value in dict_discip_actors.items():
            for val in value:
                lst_tmp =[]
                for key in dict_base:
                    if key[5].partition(' (')[0] == val:
                        lst_tmp.append(key[6])
                    else:
                        continue
                lst_tmp = get_unique_only(lst_tmp)
                lst_tmp = cut_list(lst_tmp)
                dict_act_contrg[val] = lst_tmp

        # Пример выборки и агрегирования минимальной и максимальной сумм контрактов
        # по проектам в разрезе валют
        agg_func_selection = {'Сумма_контракта': ['first', 'last']} # создаем агрегирующую функцию
        data_df.sort_values(by=['Сумма_контракта'], ascending=False).groupby(['Наименование_проекта','Валюты_контракта']).agg(agg_func_selection)

        # Группировка data_df - суммы и средние значения сумм в разрезе валют
        # по дисциплинам Компании
        agg_sum = {'Сумма_контракта':['sum', 'mean']}
        data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_sum)

        # Суммы контрактов (проработок) по проектам Компании в разрезе валют
        agg_sum = {'Сумма_контракта':['sum', 'mean']}
        data_df.groupby(['Наименование_проекта', 'Валюты_контракта']).agg(agg_sum)

        # Количество контрактов (проработок) в разрезе Дисциплин
        agg_func_count = {'Дисциплина': ['count']}
        data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_func_count)

        # а как это количество проработок делится между Исполителями?
        agg_func_count = {'Дисциплина': ['count']}
        data_actors_count = data_df.groupby(['Дисциплина','Исполнитель_МТО', 'Валюты_контракта']).agg(agg_func_count)

        # Группировка data_df - суммы и средние значения сумм в разрезе валют
        # по дисциплинам Компании
        agg_sum = {'Сумма_контракта':['sum', 'mean']}
        data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_sum)

        # Суммы контрактов (прработок) по проектам Компании в разрезе валют
        agg_sum = {'Сумма_контракта':['sum', 'mean']}
        data_df.groupby(['Наименование_проекта', 'Валюты_контракта']).agg(agg_sum)

        # Количество контрактов (проработок) в разрезе Дисциплин
        agg_func_count = {'Дисциплина': ['count']}
        data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_func_count)

        # Полный Алгоритм выбора всех контрактов, заключенных одним отдельно взятым исполнителем
        # и сортировка его в порядке возрастания

        # 1. Формируется кросс-таблица:  Контрагенты-Исполнитель ЛОТа и записываем её в
        # переменную vib_contr_acts

        # vib_contr_acts = pd.crosstab(excel_data_df['Присуждено_контрагенту'], [excel_data_df['Исполнитель_МТО']])
        # почему excel_data_df? Посмотреть с data_df
        vib_contr_acts = pd.crosstab(data_df['Присуждено_контрагенту'], [data_df['Исполнитель_МТО']])
        # переименуем столбцы таблицы на сокращенные (без телефонов). Формат - "Фамилия Имя Отчество".

        list_acts = vib_contr_acts.columns
        list_acts = cut_list(list_acts)
        vib_actors = vib_contr_acts.rename(columns=dict(zip(vib_contr_acts.columns, list_acts)))

        """ далее код в порядке эксперимента по одному исполнителю """
        # выборка происходит из cross-таблицы
        # этот блок кода формирует словарь, где key - Исполнитель МТО, value - список кортежей
        # (контрагент, частота заключения контрактов)
        #var_tmp = 'Давришев Евгений'
        #dict_var_tmp = {}
        #tupl_list = []
        #i = 0
        #for idx in vib_actors.index:
        #    if vib_actors.loc[idx, var_tmp] != 0:
        #        tupl_tmp = (vib_actors.index[i], vib_actors.loc[idx, var_tmp])
        #        tupl_list.append(tupl_tmp)
        #        i = i + 1
        #dict_var_tmp[var_tmp] = tupl_list

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
                    if vib_actors.loc[idx, val] != 0:
                        tupl_tmp = (idx, vib_actors.loc[idx, val])
                        tupl_list.append(tupl_tmp)
                    i = i + 1
                tupl_list.sort(key=lambda x: x[1], reverse=True)
                dict_var_tmp[val] = tupl_list
            list_key.append(dict_var_tmp)
            dict_disc_act_freq[key] = list_key
        # в этом словаре - {'Дисциплина': ['Исполнитель': ('Контрагент', частота контрактов) и т.д.] ... и т.д.}
        """ словарь формируется в полном объеме, согласно алгоритма """

        self.ui.lineEdit_3.clear()
        # mywindow.setStyleSheet("QlineEdit_3 {background-color : green}")
        self.ui.lineEdit_3.setText("Данные загружены и подготовлены к работе")
        # Далее, переносим код в блок визуализации (analiz_GUI_tmp_v3.py)
        global list_columns
        list_columns = ['Дисциплина', 'Наименование_проекта']
        for i in range(len(list_columns)):
            self.ui.comboBox.addItem(list_columns[i])
            i += 1
        self.ui.comboBox.activated[str].connect(self.onActivated)

    # эта функция выполняется после выбора элемента из ComboBox (by clicking)
    def onActivated(self, text):
        def new_list(old_list):
            n_list = [item for item in old_list if not (pd.isnull(item)) == True]
            return n_list
    
        global pokaz_name
        for list_col in list_columns:
            if text == list_col:
                pokaz_name = text
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(new_list(dict_names.get(pokaz_name)))
        self.ui.listWidget.clicked.connect(self.item_clicked)
        

    def second_clicked(self, item):
        global isp_name
        choice_item = self.ui.listWidget_2.currentItem()
        isp_name = (choice_item.text())
        self.ui.lineEdit_4.clear()
        text_linEd4 = "Контрагенты и их кол-во, с которыми работал " + isp_name
        self.ui.lineEdit_4.setText(text_linEd4)
    
    def item_clicked(self, item):
        global disc_name
        item = self.ui.listWidget.currentItem()
        disc_name = (item.text())

        self.ui.listWidget_2.clear()
        self.ui.lineEdit_2.setText(disc_name)
        
        my_line = dict_discip_actors.get(disc_name)
        self.ui.listWidget_2.addItems(my_line)
        self.ui.listWidget_2.clicked.connect(self.second_clicked)
        
# -------------------------------------------------------
if __name__== "__main__":
    import sys
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec_())


"""
# Возвращаемся с новой задачей. присваиваем переменной item наименование одной из Дисциплин
# переменной item_name ФИО одного из Исполнителей МТО
item = 'Трубная продукция и МП/МК'
item_name = 'Давришев Евгений'

# выделим для выбранного Исполнителя первые 20 кортежей (контрагент, частота контрактов)
list_of_freq = dict_disc_act_freq[item][0][item_name][:20]
# создадим из списка кортежей list_of_freq DataFrame (для построения графика)
df = pd.DataFrame(list_of_freq)

print(df)
# продумать Вариант -  подготовить список для всех Исполнителей выбранной Дисциплины
# и на его основе готовить визуализацию - Наклонная черта (плоскость)??
list_all_freq = dict_disc_act_freq[item][0]
all_contrgs = []
for value in list_all_freq.values():
    for val in value[:20]:
        all_contrgs.append(val[0])
all_contrgs = get_unique_only(all_contrgs)
"""




