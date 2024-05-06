import csv
from math import log2

"""
Nom: Ianovici
Prénom: Abel
Matricule: 000569935

Description :

Fonctions :
	class Node:
		def is_leaf(self) -> bool:
		def add_edge(self, label:str, child:'Node') -> None:

	class Edge:

	class Mushroom:
		def is_edible(self) -> bool:
		def add_attribute(self, name:str, value:str) -> None:
		def get_attribute(self, name:str) -> str:
		def get_attribute_dict(self,) -> dict:

	def load_dataset(path:str) -> list[Mushroom]:

	def filter_mushrooms_by_value(mushrooms:list[Mushroom], attribute:str,
																						value:str) -> list[Mushroom]:
	def attribute_mapping(mushrooms:list[Mushroom]) -> dict[str,list[str]]:

	def edible_proportion(mushrooms:list[Mushroom]) -> float:
	def entropy(mushrooms:list[Mushroom]) -> float:
	def information_gain(mushrooms:list[Mushroom], attribute:str) -> float:
	def build_decision_tree(mushrooms:list[Mushroom]) -> Node:

	def print_tree(root:Node, level:int=0) -> None:
"""


class Node:
	def __init__(self, criterion:str, is_leaf:bool=False):
		self.edges_ = [] # liste des arcs du noeud
		self.criterion_ = criterion
		self.leaf = is_leaf

	def is_leaf(self) -> bool:
		return self.leaf

	def add_edge(self, label:str, child:'Node') -> None:
		self.edges_.append(Edge(self, child, label))


class Edge:
	def __init__(self, parent:Node, child:Node, label:str):
		self.parent_ = parent
		self.child_ = child
		self.label_ = label


class Mushroom:
	def __init__(self, edible:bool):
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

	def get_attribute_dict(self) -> dict:
		return self.attributes


def load_dataset(path:str) -> list[Mushroom]:
	"""
	Lis un fichier csv et separe les labels
	"""
	mushrooms = list()
	with open(path, newline='') as csvfile:
		dataset = csv.reader(csvfile)
		labels = next(dataset)
		for row in dataset:
			if row[0] == 'Yes': # si comestible
				elem = Mushroom(True)
			else:               # si non-comestible
				elem = Mushroom(False)
			for i in range(1,len(labels)):
				elem.add_attribute(labels[i], row[i])
			mushrooms.append(elem)
	return mushrooms

def filter_mushrooms_by_value(mushrooms:list[Mushroom], attribute:str,
															value:str) -> list[Mushroom]:
	filtred_mushrooms= list()
	for m in mushrooms:
		if value == m.get_attribute(attribute):
			filtred_mushrooms.append(m)
	return filtred_mushrooms

def attribute_mapping(mushrooms:list[Mushroom]) -> dict[str,list[str]]:
	attribute_map = dict()
	hash = dict()
	for m in mushrooms:
		for label, value in m.get_attribute_dict().items():
			hash.setdefault(label, set())
			if value not in hash[label]:
				attribute_map.setdefault(label, list()).append(value)
				hash.setdefault(label, set()).add(value)
	return attribute_map

def edible_proportion(mushrooms:list[Mushroom]) -> float:
	res = 0.0
	for m in mushrooms:
		if m.is_edible():
			res+=1
	if len(mushrooms)!=0:
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
	gain = 0
	base_entropy = entropy(mushrooms) # H(C)

	sublist_entropy_sum = 0						# SUM(v) Pa=v * H(Ca=v)
	for value in ATTRIBUTES[attribute]:
		sublist = filter_mushrooms_by_value(mushrooms, attribute, value) # Ca=v
		value_proportion = (len(sublist)/len(mushrooms))								 # Pa=v
		sublist_entropy = entropy(sublist)															 # H(Ca=v)
		sublist_entropy_sum += value_proportion * sublist_entropy
		#print("- ", value, ":", "\n    entropy :", sublist_entropy,
		#		"\n    proportion :", value_proportion)
	gain = base_entropy - sublist_entropy_sum # I(C|A)
	#print("\nI(C|A) = " + str(base_entropy) + " - " + str(sublist_entropy_sum))
	return gain

def build_decision_tree(mushrooms:list[Mushroom]) -> Node:
	attribute_map = attribute_mapping(mushrooms)
	best_division_attribute = None
	best_gain = 0.0
	for attribute in ATTRIBUTES:
		#print("===========================================", attribute, "\n")
		current_gain = information_gain(mushrooms, attribute)
		if current_gain > best_gain:
			best_gain = current_gain
			best_division_attribute = attribute
	#print(best_gain, best_division_attribute)
	if best_division_attribute is not None:
		root = Node(best_division_attribute)
		for value in attribute_map[best_division_attribute]:
			sublist = filter_mushrooms_by_value(mushrooms,
																			 best_division_attribute, value)
			#print("\n -- tree :")
			#print_tree( root)
			subtree = build_decision_tree(sublist)
			root.add_edge(value, subtree)
	else:
		if mushrooms[0].is_edible(): 
			root = Node("Yes", is_leaf=True)
		else:
			root = Node("No", is_leaf=True)
	return root

def print_tree(root:Node, level:int=0) -> None:
		if root.is_leaf():
			print("  " * (level+1) + root.criterion_)
			return
		print("  " * level + root.criterion_)
		for edge in root.edges_:
			print("  " * (level+1) + edge.label_)
			print_tree(edge.child_, level + 1)

MUSHROOMS = load_dataset("test.csv")
ATTRIBUTES = attribute_mapping(MUSHROOMS)

print(edible_proportion(MUSHROOMS))
print(entropy(MUSHROOMS))

tree = build_decision_tree(MUSHROOMS)
print_tree(tree, 1)







