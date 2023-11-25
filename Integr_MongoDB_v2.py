from pymongo import MongoClient
import pandas as pd
import numpy as np

# загружаем базу с данными конкурентных листов (ex_data_2016_2023.xlsx)
excel_data_df = pd.read_excel("KL28290923.xlsx")

# Производим некоторые преобразования и очистку данных в датафрейме
# Заменяем пробелы в названиях столбцов на знаки "_" и избавляемся от (.)

excel_data_df = excel_data_df.rename(columns=lambda x: x.replace(' ', '_'))
excel_data_df = excel_data_df.rename(columns=lambda x: x.replace('.', '_'))

# переименуем столбец Исполнитель_МТО_(Ф_И_О) на Исполнитель_МТО ("отрежем" хвост _(Ф_И_О))
excel_data_df = excel_data_df.rename(columns={'Исполнитель_МТО_(Ф_И_О_)': 'Исполнитель_МТО'})
excel_data_df[['Номер_лота']] = excel_data_df[['Номер_лота']].astype(object)  # заменим тип с целого на object

# заменим в числовых полях excel_data_df все отсутствующие данные (nan) на ноль (0)
excel_data_df['Сумма_контракта'] = excel_data_df['Сумма_контракта'].replace(np.nan, 0)

columns_name = excel_data_df.columns

# Удаляем все повторяющиеся строки
excel_data_df = excel_data_df.drop_duplicates()

# запишем датафрейм в формате CSV его в текущую директорию
excel_data_df.to_csv("data_df_2.csv")

# конвертируем фрейм в словарь данных
dict_data_df = excel_data_df.to_dict()
	
# создаем клиента
client = MongoClient("localhost", 27017)

# соединяемся с базой данных
db = client['My_datas']
my_collection = db.kl_data

# готовим dict_data_df для записи в базу данных
items = []
for key, value in dict_data_df.items():
    kitems = []
    for kley, lvalue in value.items():
        kitems.append({
                        'key': kley,
                        'value' : lvalue
                      })
    items.append({'key' : key,
                 'value': kitems})
for i in range(len(items)):
    my_collection.insert_one(items[i])
    
# далее занимаемся выборкой документов из коллекции



# помещаем словарь dict_data_bson в коллекцию базы данных
my_collection.insert_one(dict_data_bson)
client.close()

# Здесь необходимо решить вопрос о помещении в коллекцию словарей с объемом, превышающим 16 МВ

# Далее займемся написание кода для извлечения документов из коллекции
def find_document(collection, elements, multiple=False):
    """ Функция извлечения одного или нескольких документов из коллекции """
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)

# здесь извлекаем документ из коллекции
result = find_document(my_collection, {'Присуждено_контрагенту': 'WOOD PROFIT ООО'})