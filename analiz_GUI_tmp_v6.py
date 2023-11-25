# В этом модуле всё GUI построить на Tkinter!!!

# analiz_GUI_tmp_v5 - программа анализа КЛ на основе "Отчета о конкурсных проработках"
# GUI заимствовано из https://dev-gang.ru/article/python-i-pyqt-sozdanie-menu-panelei-instrumentov-i-strok-sostojanija-l7ubf6mm7n/
# Загружаем необходимые библиотеки
from itertools import groupby
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import os
import datetime
from my_new_form_v3 import Ui_MainWindow

pd.options.display.float_format = '{:,.2f}'.format

disc_name = []
isp_name = []
dict_disc_act_freq = {}
df_data = ''
df = ''
row_count = 0
col_count = 0
list_of_freq = []

# Эта функция собирет в массив только уникальные элементы
def get_unique_only(st):
    lst1 = []
    count = 0
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
    L1 = [item for item in list_name if not(pd.isnull(item)) is True]
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
            print('Ошибка при чтении', lst_act)
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


# ========================================================
class mywindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self._createActions()
        self._createMenuBar()
        self._connectActions()
        
        self.ui.setupUi(self)
        
        # Здесь будут методы реакции на нажатие кнопок
        self.setStyleSheet("QLineEdit_3 { background-color: yellow }")

        # Вызов функции формирования QTableWidget и наполнения его данными
        self.ui.btn_2.clicked.connect(self.table_wid)
        
    def newFile(self):
        # здесь должна быть логика открытия нового файла
        # self.centralWidget.setText("<b>File > New</b> clicked")
        # просмотреть рабочий каталог на наличие файла data_df.csv.
        # Если он есть загрузить новый файл.xlsx подготовить данные и записать их в конец существующего файла csv.
        # Если его нет, то подготовить данные и сохранить их в файле data_df.csv
        filename = 'data_df.csv'
        if os.path.exists(filename):
            if os.path.isfile(filename):
                print('ФАЙЛ', ' => ', filename)
                print('Размер:', os.path.getsize(filename) // 1024, 'Кб')
                print('Дата создания:',
                      datetime.datetime.fromtimestamp(
                          int(os.path.getctime(filename))))
                print('Дата последнего открытия:',
                      datetime.datetime.fromtimestamp(
                          int(os.path.getatime(filename))))
                print('Дата последнего изменения:',
                      datetime.datetime.fromtimestamp(
                          int(os.path.getmtime(filename))))
                # все выводы от оператора print вывести в появляющееся окошко и создать запрос (Загружаем? Да/Нет)
                # сюда нужно вызвать модуль load_and_prepare. После подготовки данных загрузить их
                # в конец существующего файла data_df.csv
        else:
            print('Объект не найден')
        pass
        
    def openFile(self):
        # self.ui.lineEdit_3.setText("We are hear!")  # ("<b>File > Open...</b> clicked")
        # здесь должны быть логика открытия существующего файда
        print("We are Hear!")
        df_data = pd.read_csv("data_df.csv")

        global disc_name
        global dict_disc_act_freq

        """ создадим списки - Номера Лотов, исполнителей, дисциплины, наим проектов, контрагентов, валюты """
        number_lots = del_nan(set(df_data['Номер_лота']))
        actor_names = del_nan(set(df_data['Исполнитель_МТО']))
        discipline_names = del_nan(set(df_data['Дисциплина']))
        project_names = del_nan(set(df_data['Наименование_проекта']))
        contragent_winners = del_nan(set(df_data['Присуждено_контрагенту']))
        currency_names = del_nan(set(df_data['Валюты_контракта']))

        global dict_names
        dict_names = {'Номер_лота': number_lots, 'Дисциплина': discipline_names,
                      'Наименование_проекта': project_names, 'Исполнитель_МТО_(Ф_И_О_)': actor_names,
                      'Присуждено_контрагенту': contragent_winners, 'Валюты_контракта': currency_names}

        # Сгруппируем основной датафрейм
        ser_grouped = df_data.groupby(['Номер_лота', 'Дисциплина', 'Наименование_проекта', 'Дата_открытия_лота',
                                       'Дата_закрытия_лота', 'Исполнитель_МТО', 'Присуждено_контрагенту',
                                       'Валюты_контракта'])['Сумма_контракта'].sum()
        print('Step 1')

        list_cols = df_data.columns  # список всех наименований столбцов Таблицы

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

        print('Step 2')

        # dict_discip_actors - это словарь, где ключи - наименования Дисциплин,
        # значения - список Исполнителей (формат Фамилия Имя Отчество)

        # 2. Создаем второй словарь dict_act_contrg. Здесь придется работать с dict_base и
        # только что созданным dict_discip_actors

        dict_act_contrg = {}
        for key1, value in dict_discip_actors.items():
            for val in value:
                lst_tmp = []
                for key in dict_base:
                    if key[5].partition(' (')[0]==val:
                        lst_tmp.append(key[6])
                    else:
                        continue
                lst_tmp = get_unique_only(lst_tmp)
                lst_tmp = cut_list(lst_tmp)
                dict_act_contrg[val] = lst_tmp

        # Пример выборки и агрегирования минимальной и максимальной сумм контрактов
        # по проектам в разрезе валют
        agg_func_selection = {'Сумма_контракта': ['first', 'last']}  # создаем агрегирующую функцию
        df_data.sort_values(by=['Сумма_контракта'], ascending=False).groupby(['Наименование_проекта',
                                                                              'Валюты_контракта']).agg(agg_func_selection)

        # Группировка df_data - суммы и средние значения сумм в разрезе валют
        # по дисциплинам Компании
        agg_sum = {'Сумма_контракта': ['sum', 'mean']}
        df_data.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_sum)

        # Суммы контрактов (проработок) по проектам Компании в разрезе валют
        agg_sum = {'Сумма_контракта': ['sum', 'mean']}
        df_data.groupby(['Наименование_проекта', 'Валюты_контракта']).agg(agg_sum)

        # Количество контрактов (проработок) в разрезе Дисциплин
        agg_func_count = {'Дисциплина': ['count']}
        df_data.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_func_count)

        # а как это количество проработок делится между Исполителями?
        agg_func_count = {'Дисциплина': ['count']}
        data_actors_count = df_data.groupby(['Дисциплина', 'Исполнитель_МТО', 'Валюты_контракта']).agg(agg_func_count)

        # Группировка df_data - суммы и средние значения сумм в разрезе валют
        # по дисциплинам Компании
        agg_sum = {'Сумма_контракта': ['sum', 'mean']}
        df_data.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_sum)

        # Суммы контрактов (прработок) по проектам Компании в разрезе валют
        agg_sum = {'Сумма_контракта': ['sum', 'mean']}
        df_data.groupby(['Наименование_проекта', 'Валюты_контракта']).agg(agg_sum)

        # Количество контрактов (проработок) в разрезе Дисциплин
        agg_func_count = {'Дисциплина': ['count']}
        df_data.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_func_count)

        print('Step 3')

        # Полный Алгоритм выбора всех контрактов, заключенных одним отдельно взятым исполнителем
        # и сортировка его в порядке возрастания

        # 1. Формируется кросс-таблица:  Контрагенты-Исполнитель ЛОТа и записываем её в
        # переменную vib_contr_acts

        # vib_contr_acts = pd.crosstab(excel_df_data['Присуждено_контрагенту'], [excel_df_data['Исполнитель_МТО']])
        # почему excel_df_data? Посмотреть с df_data
        vib_contr_acts = pd.crosstab(df_data['Присуждено_контрагенту'], [df_data['Исполнитель_МТО']])
        # переименуем столбцы таблицы на сокращенные (без телефонов). Формат - "Фамилия Имя Отчество".

        list_acts = vib_contr_acts.columns
        list_acts = cut_list(list_acts)
        vib_actors = vib_contr_acts.rename(columns=dict(zip(vib_contr_acts.columns, list_acts)))

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
        # в этом словаре - {'Дисциплина': ['Исполнитель': ('Контрагент', частота контрактов) и т.д.] ... и т.д.}
        """ словарь формируется в полном объеме, согласно алгоритма """

        print('Step 4')

        self.ui.lineEdit_3.clear()
        # mywindow.setStyleSheet("QlineEdit_3 {background-color : green}")
        self.ui.lineEdit_3.setText("Данные загружены и подготовлены к работе")
        global list_columns
        list_columns = ['Дисциплина', 'Наименование_проекта']
        for i in range(len(list_columns)):
            self.ui.comboBox.addItem(list_columns[i])
            i += 1
        self.ui.comboBox.activated[str].connect(self.onActivated)

        print('Step 5')

    def saveFile(self):
        # здесь будет логика сохранения файла
        # self.centralWidget.setText("<b>File > Save</b> clicked")
        pass
    
    def copyContent(self):
        # зжесь будет логика копирования контента
        # self.centralWidget.setText("<b>Edit > Copy</b> clicked")
        pass

    def pasteContent(self):
        # Logic for pasting content goes here...
        # self.centralWidget.setText("<b>Edit > Pate</b> clicked")
        pass

    def cutContent(self):
        # Logic for cutting content goes here...
        # self.centralWidget.setText("<b>Edit > Cut</b> clicked")
        pass

    def helpContent(self):
        # Logic for launching help goes here...
        # self.centralWidget.setText("<b>Help > Help Content...</b> clicked")
        pass
        
    def about(self):
        # логика диалога about будет здесь
        pass


    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        # File menu
        fileMenu = QMenu("&File", self)
        fileMenu.setFont(QtGui.QFont("Times", 12))
        menuBar.addMenu(fileMenu)
        # Creating menus using QMenu object
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu = menuBar.addMenu("&Edit")
        editMenu.setFont(QtGui.QFont("Times", 12))
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)
        # Help menu
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.setFont(QtGui.QFont("Times", 12))
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)
        
    def _createActions(self):
        # File actions
        self.newAction = QAction(self)
        self.newAction.setText("Новый")
        self.openAction = QAction("Открыть существующий...", self)
        self.saveAction = QAction("Сохранить", self)
        self.exitAction = QAction("Выход", self)
        
        # Edit actions
        self.copyAction = QAction("Копировать", self)
        self.pasteAction = QAction("Вставить", self)
        self.cutAction = QAction("Вырезать", self)
        # Help menu
        self.helpContentAction = QAction("Help Content", self)
        self.aboutAction = QAction("About", self)
        
        
    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        # Connect Edit actions
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        self.cutAction.triggered.connect(self.cutContent)
        # Connect Help actions
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)
#-------------------------------------------------------------------------
        
    def table_wid(self):
        if pokaz_name == 'Дисциплина':
            global disc_name
            global isp_name
            global list_of_freq
            list_of_freq = dict_disc_act_freq[disc_name][0][isp_name]
            df = pd.DataFrame(list_of_freq)
            row_count = len(df.index)
            col_count = len(df.columns)
            self.ui.tableWidget_2.setRowCount(row_count)
            self.ui.tableWidget_2.setColumnCount(col_count)
            row = 0
            for tup in list_of_freq:
                col = 0
                for item in tup:
                    print(row, '', col, '', item)
                    self.ui.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row += 1
        else:
            pass
    
    def clear(self):
        self.ui.tableWidget_2.clear()
    
    def choose_file(self):
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_3.setText(" df_data.pkl, подготовленный в модуле load_and_prepare")
       
    # эта функция выполняется после выбора элемента из ComboBox (by clicking)
    def onActivated(self, text):
        def new_list(old_list):
            n_list = [item for item in old_list if not (pd.isnull(item)) == True]
            return n_list
    
        global pokaz_name
        for list_col in list_columns:
            if text == list_col:
                pokaz_name = text
                print(pokaz_name)
        if pokaz_name == 'Дисциплина':
            self.ui.listWidget.clear()
            self.ui.listWidget.addItems(new_list(dict_names.get(pokaz_name)))
            self.ui.listWidget.clicked.connect(self.item_clicked)
            self.ui.lineEdit_4.clear()
            text_linEd4 = "Будет выборка ТМС по выбранному проекту "
            self.ui.lineEdit_4.setText(text_linEd4)
            self.ui.btn_2.clicked.connect(self.table_wid)
        else:
            print('Дальнейшая работа будет здесь!')
            # Нужно будет пересмотреть форму Ui и построить новую с учетом появившегося алгоритмя анализа
            
            
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
        disc_name = (item.text()) # здесь выбирается наименование проекта (напр Аль-Бухари)
        print("Случай 2 -->",disc_name)
        
        # Далее необходимо набросать группировок и сортировок
        # с возможностью вывода в QTableWidget

        self.ui.listWidget_2.clear()
        self.ui.lineEdit_2.setText(disc_name)
    
        my_line = dict_discip_actors.get(disc_name)
        self.ui.listWidget_2.addItems(sorted(my_line))
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




