#---------------------------
import utils_xml
#---------------------------
import os
import networkx as nx
#from sagemath import *
#from sage.all import *
import matplotlib.pyplot as plt



def get_links(lip6_members_path):
	"""
	Retourne un dictionnaire ou chaque cle est un membre premanent du lip6 et la valeur associée a la clée est la liste des coauteurs qui sont aussi membres permanents du lip6
	
	@param
	lip6_members_path : string, chemin d'acces du fihcer xml des membres permanents du lip6
	"""
	echec = 0
	links = {}
	try:
		lip6 = utils_xml.liste_lip6(lip6_members_path)
	except:
		return -2
	if(len(lip6) == 0):
		return -1
	list_file = os.listdir("Graphe/")
	for member in lip6:
		if(member+".xml" not in list_file):
			#print("telechargement du fichier de :", member)
			ret = utils_xml.download_file(member, "Graphe/", "table_html.txt")
			if(ret == 404):
				echec += 1
				continue
		coauteurs = utils_xml.get_coauteurs("Graphe/"+member+".xml")
		ltmp = []
		for aut in coauteurs:
			if(aut in lip6):
				ltmp.append(aut)
		links[member] = ltmp
	return links


def draw_graph_2membres(author_name1, author_name2):
	"""
	Retourne un graphe reseau des publications entre membres permanents du lip6

	@param
	lip6_members_path : string, chemin d'acces du ficher xml des membres permanents du lip6 
	links_dico : dictionnaire des lien entre chaque membre permanent du lip6
	author_name1 : string nom de l'auteur1 ex : "Prénom Nom"
	author_name2 : string nom de l'auteur2 ex : "Prénom Nom"
	"""
	lip6 = utils_xml.liste_lip6("Auteurs/lip6.xml")
	links_dico = get_links("Auteurs/lip6.xml")
	if(links_dico == -1):
		return -1
	elif(links_dico == -2):
		return -2
	else:
		if(author_name1 in lip6 and author_name2 in lip6):
			G = nx.Graph()
			color = []
			node_labels = {}
			nodes_size = []
			edges = []
			list_coaut1 = links_dico[author_name1]
			list_coaut2 = links_dico[author_name2]
			for key in links_dico.keys():
				if(key == author_name1):
					node_labels[author_name1] = author_name1.replace(' ', '\n')
					nodes_size.append(400)
					color.append("red")
				elif(key == author_name2):
					node_labels[author_name2] = author_name2.replace(' ', '\n')
					color.append("orange")
					nodes_size.append(400)
				elif(key in list_coaut1):
					color.append("red")
					node_labels[key] = key.replace(' ', '\n')
					nodes_size.append(100)
				elif(key in list_coaut2):
					color.append("orange")
					node_labels[key] = key.replace(' ', '\n')
					nodes_size.append(100)
				else:
					color.append("grey")
					nodes_size.append(15)
				G.add_node(key)

			for elem in list_coaut1:
				edges.append((author_name1, elem))

			for elem in list_coaut2:
				edges.append((author_name2, elem))

			G.add_edges_from(edges)
			plt.figure(figsize=(15,8))
			nx.draw_random(G, node_size=nodes_size, with_labels=True, labels=node_labels, node_color=color, font_size=8, font_weight='bold')
			plt.savefig("graphe2.png", dpi=200)
			return 0
			#plt.show()
		else:
			return -3


def draw_graph_all():
	"""
	Retourne une string de status mais enregistre une image du schéma des publication entre tous les membres permanents du lip6
	
	@param
	links_dico : dictionnaire des lien entre chaque membre permanent du lip6
	"""
	links_dico = get_links("Auteurs/lip6.xml")
	if(links_dico == -1):
		return -1
	elif(links_dico == -2):
		return -2
	else:
		G = nx.Graph()
		edges = []
		for key in links_dico.keys():
			liste = links_dico[key]
			if(len(liste) != 0):
				for element in liste:
					edges.append((key,element))
			else:
				continue
		G.add_edges_from(edges)
		plt.figure(figsize=(15,15))
		poslay = nx.spring_layout(G, k=1)
		nx.draw(G, pos=poslay, with_labels=True, node_size=10, node_color="grey", edge_color="grey", width=0.5, font_size=8, font_weight='normal')
		plt.savefig("grapheAll.png", dpi=90)
		return 0


if __name__ == '__main__':

	print(get_links("Auteurs/lip6.xml"))
	#draw_graph_2membres("Vincent Guigue", "Swan Dubois")
	#draw_graph_all(get_links("Auteurs/lip6.xml"))
	#print(liste_lip6("Auteurs/lip6.xml"))
	#http://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph.html#graph-format
