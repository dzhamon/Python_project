# маленькая програ - записать словарь в базу mongo в коллекцию proba_ins
from pymongo import MongoClient
from enum import unique
import pandas as pd
import numpy as np
from bson.json_util import dumps
from bson.objectid import ObjectId

# создаем клиента
client = MongoClient("localhost", 27017)

# соединяемся с базой данных
db = client['My_datas']
my_collection = db.proba_ins

# создаем словарь
names = ["John", "Marie", "Costa", "Boota"]
ages = [27, 22, 23, 16]
sexes = ["Male", "Female", "Male", "Female"]
autos = ["Chev", "Opel", "Jig", "Velik"]
my_dict = {}

# создадим словарь my_dict
for k, v in zip(list_one, list_two):
	my_dict[k] = v + 1
	
# запишем наш словарь в коллекцию proba_ins по одному документу за раз
my_collection.create_index({"one": 1}, {unique: True})
for i in range(len(list_one)):
	my_collection.insert_one({'key': list_one[i], 'value': list_two[i]})

"""
# запишем наш словарь в коллекцию за один раз - все документы
documents = []
doc_one = {}
i = 0
for key, value in my_dict.items():
    doc_one[i] = {'key': key, 'value': value}
    documents.append(doc_one[i])
    i += 1
my_collection.insert_many(documents)
"""
