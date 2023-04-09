import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()  # создаём объект графа

# определяем список узлов (ID узлов)
nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

# определяем список рёбер
# список кортежей, каждый из которых представляет ребро
# кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром
edges = [(1, 2, 2700), (1, 5, 2000), (2, 3, 150), (5, 6, 1200), (5, 4, 25), (3, 6, 800), (3, 17, 1300), (5, 8, 1100), (7, 8, 600), (8, 11, 350), (11, 9, 350), (5, 6, 1200), (6, 9, 600), (9, 13, 60), (8, 14, 2500), (10, 14, 750), (9, 10, 250), (14, 15, 1500), (10, 12, 1500), (17, 19, 1000), (18, 19, 300), (19, 12, 100), (19, 24, 1100), (17, 20, 1800), (20, 21, 2200), (20, 22, 500), (23, 22, 200), (22, 24, 300), (24, 25, 3500), (15, 16, 3000), (1, 25, 200)]

# добавляем информацию в объект графа
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

# рисуем граф и отображаем его
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()