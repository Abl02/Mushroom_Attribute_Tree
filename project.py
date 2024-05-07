import csv
from math import log2

"""
Nom: Ianovici
Prénom: Abel
Matricule: 000569935

Description :
	Construction d'arbre de decion avec un fichier csv

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

	def display(root:Node, level:int=0) -> None:
	def is_edible(root:Node, mushroom:Mushroom) -> bool:
	def to_boolean_expression(root:Node, expression) -> list[tuple]:

	def main(mushrooms) -> None:

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
		if isinstance(value,str) and isinstance(name,str):
			self.attributes[name] = value
		else:
			raise TypeError("Both value and name must be strings")

	def get_attribute(self, name:str) -> str:
		return self.attributes[name]

	def get_attribute_dict(self) -> dict:
		return self.attributes


def load_dataset(path:str) -> list[Mushroom]:
	"""
	Lis un fichier csv, separe les labels des autres caractéristiques
		et crée un objet Mushroom pour chaque ligne du fichier.
	:param path: Chemin du fichier csv
	:return: list des champignons
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
	"""
	Filtre les champignons par valeur
	:param mushrooms: liste des champignons
	:param attribute: attribut associe a la valeur
	:param value: valeur recherchee
	:return: list des champignons filtres
	"""
	filtred_mushrooms= list()
	for m in mushrooms:
		if value == m.get_attribute(attribute):
			filtred_mushrooms.append(m)
	return filtred_mushrooms

def attribute_mapping(mushrooms:list[Mushroom]) -> dict[str,list[str]]:
	"""
	Cree un dictionnaire qui a comme cle tous les attributs des champignons
		et comme valeur toutes les valeur possible pour cet attribut
	:param mushrooms: liste des champignons
	:return: dictionnaire des valeur possible par attribut
	"""
	attribute_map = {label: list()
									for label in mushrooms[0].get_attribute_dict().keys()}
	# Optimisation en utilisant set a la place de list pour faire des recherches en O(1)
	unique_values = {label: set()
									for label in mushrooms[0].get_attribute_dict().keys()} 
	for m in mushrooms:
		for label, value in m.get_attribute_dict().items():
			if value not in unique_values[label]: # verifie si l'element n'a pas deja ete insere
				attribute_map[label].append(value)
				unique_values[label].add(value)
	return attribute_map

def edible_proportion(mushrooms:list[Mushroom]) -> float:
	"""
	Calcule la proportion de champignons comestible dans mushrooms
	:param mushrooms: liste des champignons
	:return: la proportion de champignons comestible
	"""
	res = 0.0
	for m in mushrooms:
		if m.is_edible():
			res+=1
	if len(mushrooms)!=0:
		res = res/len(mushrooms)
	return res

def entropy(mushrooms:list[Mushroom]) -> float:
	"""
	Calcule l'entropie de mushrooms
	:param mushrooms: liste des champignons
	:return: l'entropie de mushrooms
	"""
	py = edible_proportion(mushrooms)
	if py == 0 or py == 1:
		res = 0
	else:
		res = (py*log2((1-py)/py)-log2(1-py))
	return res

def information_gain(mushrooms:list[Mushroom], attribute:str) -> float:
	"""
	Calcule le gain d'information d'un attribut par rapport aux champignons 
	:param mushrooms: liste des champignons
	:param attribute: l'attribut
	:return: le gain d'information
	"""
	gain = 0
	base_entropy = entropy(mushrooms) # H(C)
	sublist_entropy_sum = 0						# SUM(v) Pa=v * H(Ca=v)
	for value in ATTRIBUTES[attribute]:
		sublist = filter_mushrooms_by_value(mushrooms, attribute, value) # Ca=v Determiner le sous-ensemble
		value_proportion = (len(sublist)/len(mushrooms))								 # Pa=v Calcule la proportion de champignon du sous-ensemble
		sublist_entropy = entropy(sublist)															 # H(Ca=v) Calcule l'entropie du sous-ensemble
		sublist_entropy_sum += value_proportion * sublist_entropy
	gain = base_entropy - sublist_entropy_sum # I(C|A)
	return gain

def build_decision_tree(mushrooms:list[Mushroom]) -> Node:
	"""
	Construis l'arbre de decision:
		- choisis l'attribut qui a le plus grand gain d'information
		- cree le noeud associe a cet attribut
		- pour chaque valeur de cet attribut construire le sous-arbre de cette valeur
	:param mushrooms: liste des champignons
	:return: la racine de l'arbre
	"""
	attribute_map = attribute_mapping(mushrooms)
	best_division_attribute = None
	best_gain = 0.0
	if entropy(mushrooms) != 0.0: # Si l'entropie de mushrooms est nul il n'est pas necessaire de le diviser
		for attribute in ATTRIBUTES:
			current_gain = information_gain(mushrooms, attribute)
			if current_gain > best_gain:
				best_gain = current_gain
				best_division_attribute = attribute
	if best_division_attribute is not None: # si un attribut a un gain d'information non nul
		root = Node(best_division_attribute)
		for value in attribute_map[best_division_attribute]:
			sublist = filter_mushrooms_by_value(mushrooms,
																			 best_division_attribute, value)
			subtree = build_decision_tree(sublist)
			root.add_edge(value, subtree)
	else:
		if mushrooms[0].is_edible(): 
			root = Node("Yes", is_leaf=True)
		else:
			root = Node("No", is_leaf=True)
	return root

def display(root:Node, level:int=0) -> None:
	"""
	Affiche l'arbre dans le terminale
	:param root: racine de l'arbre a aficher
	:param level: niveau indentation de l'affichage
	"""
	if root.is_leaf():
		print("  " * (level-1) + "|       " + root.criterion_)
	else:
		for edge in root.edges_:
			print("  " * (level) + "|  " + root.criterion_ + " = " + edge.label_)
			display(edge.child_, level + 1)


def is_edible(root:Node, mushroom:Mushroom) -> bool:
	"""
	Cherche si le champignon donnee est comestible ou non
	:param root: racine de l'arbre
	:param mushroom: le champignon 
	:return: si le champignon est comestible
	"""
	if root.is_leaf():
		if root.criterion_ == "Yes":
			return True
		else:
			return False
	else:
		value = mushroom.get_attribute(root.criterion_)
		for edge in root.edges_:
			if value == edge.label_:
				return is_edible(edge.child_, mushroom)

def to_boolean_expression(root:Node, expression:list) -> list[tuple]:
	"""
	Convertie un arbre de decision en expression booleennes
	:param root: racine de l'arbre
	:param expression: l'ensemble qui represente les expression booleennes
	:return: expression booleennes
	"""
	for edge in root.edges_:
		if not edge.child_.is_leaf():
			expression.append((root.criterion_, edge.label_))
			expression.append(to_boolean_expression(edge.child_, []))
		elif edge.child_.criterion_ == "Yes":
			expression.append((root.criterion_, edge.label_))
	return expression

def main(mushrooms) -> None:
	global ATTRIBUTES
	ATTRIBUTES = attribute_mapping(mushrooms)
	if not ATTRIBUTES:
		raise ValueError("No data has been found in the csv file")
	tree = build_decision_tree(mushrooms)
	display(tree)

MUSHROOMS = load_dataset("mushrooms.csv")
main(MUSHROOMS)








