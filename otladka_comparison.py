import pandas as pd
from itertools import groupby
import collections
from collections import Counter
pd.options.display.float_format = '{:,.2f}'.format

# Данная функция удаляет в списках показателей nan
def del_nan(list_name):
    L1 = [item for item in list_name if not(pd.isnull(item)) == True]
    L1, list_name = list_name, L1
    return list_name

def dict_compar(dict_d, dict_c, actor):
	dict1 = dict_d
	dict2 = dict_c
	dict1_len = len(dict1)
	dict2_len = len(dict2)
	# total_dict_count = dict1_len + dict2_len
	bad_dict = {}
	new_dict = {}
	for i in dict1:
		if i in dict2:
			if dict1[i] == dict2[i]:
				continue
			else:
				for k in range(len(dict1[i])):
					if isinstance(dict1[i][k], str):
						if dict1[i][k].strip() in dict2[i]:
							continue
						else:
							bad_dict[i] = dict1[i]
							new_dict[i] = dict2[i]
					else:
						if dict1[i][k] in dict2[i]:
							continue
						else:
							bad_dict[i] = dict1[i]
							new_dict[i] = dict2[i]
						
	len_bad_dict = len(bad_dict)
	if len_bad_dict==0:
		pass
	else:
		print('Лот № ', lst_lt, ' исполнитель - ', actor, file=ff)
		print('Есть несовпадения:!', file=ff)
		print('Было', bad_dict, file=ff)
		print('Стало', new_dict, file=ff)
		print(' ', file=ff)
	return

# Загружаем данные с лотами
df_data = pd.read_csv("data_df.csv")

# удалим столбец 'Unnamed: 0'
df_data = df_data.drop(columns = ['Unnamed: 0'], axis=1)

# Загрузим файл с данными по контрактам
df_contr = pd.read_csv("contract_df.csv")

# удалим столбец 'Unnamed: 0'
df_contr = df_contr.drop(columns = ['Unnamed: 0'], axis=1)

# фильтует из таблицы все строки, в которых столбец 'contract_date' - не пустой
df_contr_filtr = df_contr[df_contr['contract_number'].notna()]

# в числовых столбцах таблицы все NaN заменим на нули
df_contr[['goods_qty','unit_price', 'amount_of_goods', 'additional_expenses', 'total_price']] = \
    df_contr[['goods_qty','unit_price', 'amount_of_goods', 'additional_expenses', 'total_price']].fillna(0)

# найдем пересечение двух множеств - множества контрактов и множества ЛОТов
set_lots = set(df_contr['lot_number']) & set(df_data['Номер_лота'])

# вытащим в отдельную переменную наименования дисциплин
discipline_names = del_nan(set(df_data['Дисциплина']))

# создадим словарь : keys - Дисциплины : values - соответствующие им номера лотов (?? это номера лотов из set_lots ??)
dict_of_discip = {}
for discipline_name in discipline_names:
    lst_tmp = []
    # отберем данные по очередной Дисциплине из списка и разместим их в df_tmp_disc
    df_tmp = df_data.loc[df_data['Дисциплина']==discipline_name]
    # отберем номера лотов из df_tmp
    nmr_lots = list(set(df_tmp['Номер_лота']))
    lst_tmp.append(nmr_lots)
    dict_of_discip[discipline_name] = lst_tmp
    
# Код алгоритма сравнения ТМЦ по Лоту и ТМЦ по договору/контракту
""" Здесь будет код по сравнению Лот-Контракт по всему словарю dict_of_discip"""

# создаем цикл по Дисциплинам

for discipline_name in discipline_names: # выбираем наименование Дисциплины
	file_name = 'compar_' + discipline_name[0:7]
	ff = open(file_name, "a", encoding='utf-8')
	print("Сравнительный анализ по дисциплине ", discipline_name, file=ff)
	print(' ', file=ff)
	print("Сравнительный анализ по дисциплине ", discipline_name)
	num_of_lots = 0
	list_lots = dict_of_discip.get(discipline_name) # для отобранной Дисциплины выбираем все ее Лоты
	for list_lot in list_lots: # выбириаем очередной Лот
		contracts = 0
		for lst_lt in list_lot: # выбирается очередной лот
			if lst_lt in set_lots: # Лот принадлежит set_lots ?
				num_of_lots += 1
				df_data_ll = df_data.loc[df_data['Номер_лота']==lst_lt]
				df_data_ll = df_data_ll[['Номер_лота','Присуждено_контрагенту','Наименование_ТМЦ','Кол-во_поставщика',
				                         'Сумма_контракта','Валюты_контракта']]
				df_contr_ll = df_contr.loc[df_contr['lot_number']==lst_lt]
				actor = set(df_contr_ll['contract_actor'].to_list())
				df_contr_ll = df_contr_ll[['lot_number','contract_owner','goods_name','goods_qty',
				                           'total_price','currency']]
				# переименуем столбцы второго датафрейма
				dict_of_columns = {}
				for i in range(len(df_data_ll.columns)):
					dict_of_columns[df_contr_ll.columns[i]] = df_data_ll.columns[i]
				df_contr_ren = df_contr_ll.rename(columns=dict_of_columns)
				# определим размеры датафреймов
				len_df_data_ll = len(df_data_ll)
				len_df_contr_ren = len(df_contr_ll)
				# из временных датафреймов построим словари
				dict_d = df_data_ll.to_dict('list')
				dict_c = df_contr_ren.to_dict('list')
				# сколько позиций в датафреймах?
				if (len_df_data_ll == 1) & (len_df_contr_ren == 1):
					# Здесь нужно сделать обращение к функции и передать параметры
					dict_compar(dict_d, dict_c, actor)
					# количество позиций ТМС в Лотах больше единицы ( два и больше)
					# определим количество контрагенов в Лотах ( в случае "шахматки")
					continue
				elif len_df_data_ll == len_df_contr_ren: # размеры равны, но больше 1
					dict_compar(dict_d, dict_c, actor)
					continue
				elif len_df_data_ll > len_df_contr_ren:
					contr_name = list(set(df_data_ll['Присуждено_контрагенту']))
					print('Лот ', lst_lt, ', исполнитель -', actor, file=ff)
					print('Для лота ', lst_lt, ' контрагента ',contr_name, ' в договоре уменьшены позиции ТМС', file=ff)
					print(' ',file=ff)
					continue
				elif len_df_data_ll < len_df_contr_ren:
					contr_name = list(set(df_data_ll['Присуждено_контрагенту']))
					print('Лот ', lst_lt, ', исполнитель -', actor, file=ff)
					print('Для лота ', lst_lt, ' контрагента ', contr_name, ' в договоре добавлены позиции ТМС', file=ff)
					print(' ',file=ff)
					continue
				else:
					dict_compar(dict_d, dict_c, actor)
			continue
		print('Просмотрено Лотов', num_of_lots, file=ff)
		continue
	ff.close()

