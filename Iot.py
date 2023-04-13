import matplotlib.pyplot as plt
import networkx as nx
import random as rnd

from typing import Tuple, List

# возвращает (длина_пути, [cписок вершин пути])
# TODO: пока псевдорандом, поменять на рандом
# TODO: не обрабатывает, если пути нет
def createRoute(G: nx.Graph) -> Tuple[int, List]:
    route_nodes = rnd.choices(list(G), k = 2)
    # алгоритм Дейкстры для взвешенного графа
    return nx.single_source_dijkstra(G, source= route_nodes[0], target = route_nodes[1])


# получает граф, путь, сведения о машине (пока только скорость), время начала пути
# TODO: возможно общая длина пути не нужна
# TODO: сведения о машине должны приходить в виде объекта
# TODO: сменить постоянную скорость на рандомную в диапазоне доступных для машины
# TODO: сейчас время приходит строкой, изменить это
# TODO: ФУНКЦИЯ ЕЩЁ НЕ ДОДЕЛАНА, ПОКА НЕ РАБОТАЕТ
def modulateRoute(G: nx.Graph, route_tuple: Tuple[int, List],
                  vehicle_speed: int, start_time: str):
    (complete_length, route) = route_tuple
    print(route)

G = nx.Graph()  # создаём объект графа

# определяем список узлов (ID узлов)
nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

# определяем список рёбер
# список кортежей, каждый из которых представляет ребро
# кортеж (id_1, id_2) означает, что узлы id_1 и id_2 соединены ребром
# TODO: это ненаправленный граф, для направленного нужно использовать nx.DiGraph() и изменить задание рёбер
# TODO: ребро 1-25 спорное, где тогда вход/выход на карту?
edges = [(1, 2, 2700), (1, 5, 2000), (2, 3, 150), (5, 6, 1200), (5, 4, 25),
        (3, 6, 800), (3, 17, 1300), (5, 8, 1100), (7, 8, 600), (8, 11, 350),
        (11, 9, 350), (5, 6, 1200), (6, 9, 600), (9, 13, 60), (8, 14, 2500),
        (10, 14, 750), (9, 10, 250), (14, 15, 1500), (10, 12, 1500), (17, 19, 1000),
        (18, 19, 300), (19, 12, 100), (19, 24, 1100), (17, 20, 1800), (20, 21, 2200),
        (20, 22, 500), (23, 22, 200), (22, 24, 300), (24, 25, 3500), (15, 16, 3000),
        (1, 25, 200)]

# добавляем информацию в объект графа
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

# рисуем граф и отображаем его
# nx.draw(G, with_labels=True, font_weight='bold')
# plt.show()

route = createRoute(G)
modulateRoute(G, route, 60, "10:00")