import csv

kod = ()
numbers = (0,1,2,3,4,5,6,7,8,9)
tup_num1, tup_num2 = numbers, numbers
tup_lett1 = ('S', 'Q', 'W')
tup_lett2 = ('A', 'T', 'P', 'L')

list_kod = []
with open('lunokod.csv', 'a', newline='') as f:
	for i in tup_num1:
		for j in tup_lett1:
			for k in tup_num2:
				for l in tup_lett2:
					list_kod.append(str(i) + j + str(k) + l)
					writer = csv.writer(f)
					writer.writerow(list_kod)
					list_kod = []
					