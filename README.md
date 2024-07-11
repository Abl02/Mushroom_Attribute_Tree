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
