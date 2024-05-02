import csv
from math import log2
from re import sub

"""
Nom: Ianovici
Prénom: Abel
Matricule: 000569935

Description :

Fonctions :
"""

class Node:
	def __init__(self, criterion:str, is_leaf:bool=False):
		self.edges_ = [] # liste des arcs du noeud

	def is_leaf(self) -> bool:
		return True

	def add_edge(self, label:str, child:'Node') -> None:
		pass


class Edge:
	def __init__(self, parent:Node, child:Node, label:str):
		self.parent_ = parent
		self.child_ = child
		self.label_ = label


class Mushroom:
	def __init__(self, edible:bool):
		# fonction permettant de determiner
		# si un champignon est comestible
		print("created a Mushroom object")
		self.edible = edible
		self.attributes = dict()

	def __str__(self) -> str:
		return str(self.attributes)

	def is_edible(self) -> bool:
		return self.edible

	def add_attribute(self, name:str, value:str) -> None:
		self.attributes[name] = value

	def get_attribute(self, name:str) -> str:
		return self.attributes[name]

	def get_attribute_dict(self,) -> dict:
		return self.attributes


def load_dataset(path:str) -> list[Mushroom]:
	mushrooms = list()
	with open(path, newline='') as csvfile:
		dataset = csv.reader(csvfile)
		labels = next(dataset)
		print(labels)
		for row in dataset:
			if row[0] == 'Yes': # if edible
				elem = Mushroom(True)
			else:               # if not edible
				elem = Mushroom(False)
			for i in range(1,len(labels)):
				elem.add_attribute(labels[i], row[i])
			mushrooms.append(elem)
	return mushrooms

def edible_proportion(mushrooms:list[Mushroom]) -> float:
	res = 0
	for m in mushrooms:
		if m.is_edible():
			res+=1
	res = res/len(mushrooms)
	return res

def entropy(mushrooms:list[Mushroom]) -> float:
	py = edible_proportion(mushrooms)
	if py == 0 or py == 1:
		res = 0
	else:
		res = (py*log2((1-py)/py)-log2(1-py))
	return res

def information_gain(mushrooms:list[Mushroom], attribute:str) -> float:
	res = 0
	base_entropy = entropy(mushrooms)
	attribute_map = dict()
	sublist_entropy_sum = 0
	for m in mushrooms:
		attribute_map.setdefault(m.get_attribute(attribute), []).append(m)
	for key, sublist in attribute_map.items():
		sublist_entropy = entropy(sublist)
		value_proportion = (len(sublist)/len(mushrooms))
		sublist_entropy_sum += (value_proportion*sublist_entropy)
		print(key, '=========================================================')
		print('list :', sublist)
		print('entropy :', sublist_entropy)
		print('proportion :', value_proportion)
		print('sum :', sublist_entropy_sum)
	res = (base_entropy-sublist_entropy_sum)
	print()
	print('base entopy :', base_entropy)
	print('sublist entropy sum :', sublist_entropy_sum)
	return res

def build_decision_tree(mushrooms:list[Mushroom]) -> Node:
	for attribute in mushrooms[0].get_attribute_dict().keys():
		print('\n=================================\n' + attribute + '\n=================================\n')
		print(information_gain(mushrooms, attribute))

mushrooms = load_dataset('test.csv')

print(edible_proportion(mushrooms))
print(entropy(mushrooms))
build_decision_tree(mushrooms)














