class Person:
	def __init__(self, name, age, pay=0, job=None):
		self.name = name
		self.age = age
		self.pay = pay
		self.job = job
		
	def lastName(self):
		return self.name.split()[-1]
	
	def giveRaise(self, percent):
		self.pay *= (1.0 + percent)
		
	def __str__(self):
		return ('<%s => %s: %s, %s>' %
			   (self.__class__.__name__, self.name, self.job, self.pay))
	
class Manager(Person):
	"""	класс со специализированным	методом	giveRaise,
		наследующий	обобщенные методы lastName	и 	__str__
	"""
	def __init__(self, name, age, pay):
		Person.__init__(self, name, age, pay, 'manager')
	def giveRaise(self, percent, bonus=0.1):
		Person.giveRaise(self, percent + bonus)
		
if __name__=='__main__':
	bob = Person('Bob Smith', 44)
	sue = Person('Sue Jones', 47, 4000, 'hardware')
	tom = Manager(name='Tom Doc', age=50, pay=50000)
	print(sue, sue.pay, sue.lastName())
	
	for obj in (bob, sue, tom):
		obj.giveRaise(.10)
		print(obj)