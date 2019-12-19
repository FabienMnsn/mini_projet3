import math
import networkx as nx
import matplotlib.pyplot as plt
import random

def draw_graphe(auteur_name1, auteur_name2):
	"""
	Dessine un graphe ou chaque point est un memebre du lip6 et les deux point de couleur differente sont les deux meembres choisis

	@param
	auteur_name1 : string, nom et prenom de l'auteur1 séparés par un espace
	auteur_name2 : string, nom et prenom de l'auteur2 séparés par un espace
	"""
	graph = nx.Graph()

	nb_added = 0
	centre = 100
	pad = 40
	random_max = 200
	#membres permanents du lip6 = 193 - les deux auteurs sélectionnés = 191
	while(nb_added < 191):
		x = random.uniform(1,random_max)
		y = random.uniform(1,random_max)
		if(y < centre-pad or y > centre+pad):
			graph.add_node("N"+str(nb_added), pos=(x,y))
			nb_added +=1
		elif(x < centre-pad or x > centre+pad):
			graph.add_node(nb_added, pos=(x,y))
			nb_added +=1
	graph.add_node(192, pos=(centre-pad/4, centre))
	graph.add_node(193, pos=(centre+pad/4, centre))
	graph.add_edge(192,192)

	pos = nx.get_node_attributes(graph, 'pos')
	nx.draw(graph, pos, with_labels=True)

	#plt.savefig("path.png")
	plt.show()


def circular():
	rayon = 4
	marge = 1
	for x in range(-10, 10):
		for y in range(-10, 10):
			x2 = math.pow(x, 2)
			r2 = math.pow(rayon, 2)
			y2 = x2 - r2
			if((x2+y2) > (r2-marge) and (x2+y2) < (r2+marge)):
				print("eq res :")


if __name__ == '__main__':

	draw_graphe("hsfkjsfhe", "hsfjksh")