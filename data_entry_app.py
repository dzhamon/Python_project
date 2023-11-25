# data_entry_app.py (from Mur_Python GUI Programming with Tkinter)
from datetime import datetime
from pathlib import Path
import csv
import tkinter as tk
from tkinter import ttk


"""A widget containing a label and input together."""
class LabelInput(tk.Frame):
	def __init__(self, parent, label, var, input_class=ttk.Entry, input_args=None,
	             label_args=None, **kwargs):
		super().__init__(parent, **kwargs)
		input_args = input_args or {}
		label_args = label_args or {}
		self.variable = var
		self.variable.label_widget = self
		
		if input_class in (ttk.Checkbutton, ttk.Button):
			input_args["variable"] = self.variable
		else:
			input_args["textvariable"] = self.variable
		
		if input_class == ttk.Radiobutton:
			self.input = tk.Frame(self)
			for v in input_args.pop('values', []):
				button = ttk.Radiobutton(self.input, value=v, text=v, **input_args )
		else:
			self.input = input_class(self, **input_args)
		button.pack(side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x')
		
		self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
		self.columnconfigure(0, weight=1)
	
	"""Override grid to add default sticky values"""
	def grid(self, sticky=(tk.E + tk.W), **kwargs):
		super().grid(sticky=sticky,**kwargs)
		

# Идея заключается в создании класса для построения Ограниченного виджета Text,
# который можно было бы сохранить в переменной
class BoundText(tk.Text):
	def __init__(self, *args, textvariable=None, **kwargs):
		super().__init__(*args, **kwargs)
		self._variable = textvariable
		if self._variable:
			self.insert('1.0', self._variable.get())
		self._variable.trace_add('write', self._set_content)
		self.bind('<<Modified>>', self._set_var)
	
	def _set_content(self, *_):
		self.delete('1.0', tk.END)
		self.insert('1.0', self._variable.get())
	
	"""Set the variable to the text	contents"""
	def _set_var(self, *_):
		if self.edit_modified():
			content = self.get('1.0', 'end-1chars')
		self._variable.set(content)
		self.edit_modified(False)
		
"""The input form for our widgets"""
class DataRecordForm(ttk.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._vars = {'Date': tk.StringVar(), 'Time': tk.StringVar(),
		              'Technician': tk.StringVar(), 'Lab': tk.StringVar(), 'Plot':
			            tk.IntVar(), 'Seed Sample': tk.StringVar(), 'Humidity':
			            tk.DoubleVar(), 'Light': tk.DoubleVar(), 'Temperature':
			            tk.DoubleVar(), 'Equipment Fault': tk.BooleanVar(), 'Plants':
			            tk.IntVar(), 'Blossoms': tk.IntVar(), 'Fruit': tk.IntVar(), 'Min Height':
			            tk.DoubleVar(), 'Max Height': tk.DoubleVar(), 'Med Height': tk.DoubleVar(),
		                'Notes': tk.StringVar()}