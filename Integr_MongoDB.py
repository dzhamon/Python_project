from pymongo import MongoClient
import pandas as pd
import numpy as np
from bson.json_util import dumps
from bson.objectid import ObjectId

def dict_to_bson(dictionary):
    items = []
    for key, value in dictionary.items():
        if isinstance(value, dict):
            items.append({
                'key': key,
                'value': dict_to_bson(value)
            })
        else:
            items.append({
                'key': key,
                'value': value,
            })
    return {'$set': items}

# создаем клиента
client = MongoClient("localhost", 27017)

# соединяемся с базой данных
db = client['My_datas']
my_collection = db.kl_data

# загружаем базу с данными конкурентных листов (ex_data_2016_2023.xlsx)
excel_data_df = pd.read_excel("KP_21_22_full_v1.xlsx")

# Производим некоторые преобразования и очистку данных в датафрейме
# Заменяем пробелы в названиях столбцов на знаки "_" и избавляемся от (.)

excel_data_df = excel_data_df.rename(columns=lambda x: x.replace(' ', '_'))
excel_data_df = excel_data_df.rename(columns=lambda x: x.replace('.', '_'))
# Меняем  формат датa на " компьютерный"
#excel_data_df['Дата_открытия_лота'] = pd.to_datetime(excel_data_df['Дата_открытия_лота'],
 #           infer_datetime_format=True)
#excel_data_df['Дата_закрытия_лота'] = pd.to_datetime(excel_data_df['Дата_закрытия_лота'],
  #          infer_datetime_format=True)

# переименуем столбец Исполнитель_МТО_(Ф_И_О) на Исполнитель_МТО ("отрежем" хвост _(Ф_И_О))
excel_data_df = excel_data_df.rename(columns={'Исполнитель_МТО_(Ф_И_О_)': 'Исполнитель_МТО'})
excel_data_df[['Номер_лота']] = excel_data_df[['Номер_лота']].astype(object)  # заменим тип с целого на object
# excel_data_df - это сырые, несгруппированные данные из таблицы Excel

# заменим в числовых полях excel_data_df все отсутствующие данные (nan) на ноль (0)
#excel_data_df['Кол-во_поставщика'] = excel_data_df['Кол-во_поставщика'].replace(np.nan, 0)
excel_data_df['Сумма_контракта'] = excel_data_df['Сумма_контракта'].replace(np.nan, 0)

columns_name = excel_data_df.columns

excel_data_df = excel_data_df.drop_duplicates()

# создадим копию основного датафрейма и запишем его в текущую директорию
        # data_df = excel_data_df.copy()
excel_data_df.to_csv("data_df.csv")

# конвертируем фрейм в словарь данных
dict_data_df = excel_data_df.to_dict()

data = []
values = []
for key, value in dict_data_df.items():
    data.append(key)
    values.append(value)
    
my_collection.insert_one(dict_to_bson(dict_data_df))
client.close()

# Здесь происходит непонятная ситуация - программа
# по неизвестным (пока!) причинам оценивает размер входного файла
# словаря и не пропускает, ссылаясь, что под дкумент базы MongoDB
# отводится maxSize = 17 MB


