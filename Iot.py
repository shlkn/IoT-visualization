# import matplotlib.pyplot as plt # type: ignore
import networkx as nx
import random as rnd
import datetime as dt
import json as js
import socket
import time
import paho.mqtt.client as mqtt 
from typing import List, Dict

# возвращает (cписок вершин пути)
# TODO: пока псевдорандом, поменять на рандом
# TODO: не обрабатывает, если пути нет
def create_route(G: nx.Graph, start_index: int) -> List:
    while True:
        end_node = rnd.choices(list(G), k = 1)
        if start_index != end_node[0]:
            break
    # алгоритм Дейкстры для взвешенного графа
    return nx.dijkstra_path(G, source = start_index, target = end_node[0])

# возвращает (список из 10 грузовиков, случайно выбираемых из списка json-ов)
def create_trucks(T: List) -> List:
    trucks_json: List = []
    for i in range (1,11):
        car = js.loads(T[rnd.randrange(0, 4)])
        #TODO: число вершин убрать номером, сделать переменной
        car["current_place"] = rnd.randint(1, 25)
        #TODO: начальное время должно задаваться
        car["current_time"] = dt.datetime(2023, 5, 22, hour = 12, minute=0)
        trucks_json.append(car)
    return trucks_json

# получает граф, путь, сведения о машине (пока только скорость), время начала пути
# возвращает список словарей с информацией об отрезках пути
# TODO: сведения о машине должны приходить в виде объекта
# TODO: сменить постоянную скорость на рандомную в диапазоне доступных для машины
# TODO: добавить остановки в каждом пункте
# TODO: скорость приходит в км/ч, а расстояние в метрах

def traverse_route(G: nx.Graph, route: List,
                  vehicle_speed: float, start_time: dt.datetime) -> List[Dict]:
    #TODO: speed limit = 80
    if vehicle_speed > 80:
        vehicle_speed = 50
    route_edges: List[Dict] = []
    for i in range(len(route) - 1):
        vehicle_speed_rnd = rnd.uniform(vehicle_speed - 30, vehicle_speed + 30)
        vehicle_speed_m_min = vehicle_speed_rnd * 1000.0 # км/ч перевели в м/ч
        vehicle_speed_m_min /= 60.0 # м/ч перевели в м/мин
        
        #TODO: debug *100
        minutes = G[route[i]][route[i+1]]["weight"] * 100 / vehicle_speed_m_min
        edge = {
            "start": route[i],          # начальный пункт
            "end": route[i + 1],        # конечный пункт
            "start_time": start_time,   # время выезда
            "end_time": start_time + dt.timedelta(minutes = minutes), # время прибытия 
            "speed": vehicle_speed_rnd      # скорость машины (постоянная)
        }
        start_time += dt.timedelta(minutes = minutes)
        route_edges.append(edge)
    return route_edges

# TODO: переделать в направленный граф и/или мультиграф
G = nx.Graph()  # создаём объект графа

# определяем список узлов (ID узлов)
# TODO: почему не циклом?
# TODO: если есть остановки в узлах, указать их мин и макс длительность как свойства улзов
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

# json каждого из грузовиков
KAMAZ_4308_69 = """{ "truck_type": "KAMAZ 4308-69",
"power_output": 242, "max_speed_kmh": 100,
"racing_to_60_kmh_seconds": 65, "braking_60kmh_meters": 51.38,
"fuel_volume": 210, "fuel_usage": 14, "capacity": 5730}"""
KAMAZ_65117_48 = """{ "truck_type": "KAMAZ 65117-48",
"power_output": 292, "max_speed_kmh": 95,
"racing_to_60_kmh_seconds": 45, "braking_60kmh_meters": 36.7,
"fuel_volume": 500, "fuel_usage": 27, "capacity": 14500}"""
GAZEL_NEXT = """{ "truck_type": "GAZEL NEXT",
"power_output": 152, "max_speed_kmh": 130,
"racing_to_60_kmh_seconds": 10.4,"braking_60kmh_meters": 32.5,
"fuel_volume": 68, "fuel_usage": 8.5, "capacity": 1050}"""
MAZ_6312C9 = """{ "truck_type": "MAZ 6312C9",
"power_output": 309, "max_speed_kmh": 85,
"racing_to_60_kmh_seconds": 55, "braking_60kmh_meters": 48.45,
"fuel_volume": 500, "fuel_usage": 25.5, "capacity": 14250}"""

# создаем список, содержащий json каждого типа грузовиков
trucks_json = [KAMAZ_4308_69, KAMAZ_65117_48, GAZEL_NEXT, MAZ_6312C9]

def create_routes_dict(truck_list: List) -> Dict:
    routes_dict = {}
    index = 1
    for t in truck_list:
        car_dict = {}
        car_dict['car'] = t
        #TODO: сделать пути больше
        #TODO: убрать магический номер маршрутов
        for i in range(0, 10):
            route = create_route(G, car_dict['car']['current_place'])
            start_time_init = car_dict['car']['current_time']
            route_info = traverse_route(G, route, t["max_speed_kmh"], start_time_init)
            if 'route_info' in car_dict:
                car_dict['route_info'] = car_dict['route_info'] + route_info
            else:
                car_dict['route_info'] = route_info
            car_dict['car']['current_place'] = route[-1]
            car_dict['car']['current_time'] = route_info[-1]["end_time"]
        
        routes_dict[index] = car_dict
        index += 1
    return routes_dict

# Для красивой печати и проверки данных
def create_routes_json(routes_dict: Dict):
    routes_json = js.dumps(routes_dict, indent=4, default=str)
    return routes_json

# создаем список из 10 грузовиков, выбирая случайную комбинацию из 4 типов грузовиков
truck_list = create_trucks(trucks_json)

routes_dict = create_routes_dict(truck_list)
print(create_routes_json(routes_dict))




# mqtt
def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
    else:
        print("could not connect, return code:", return_code)

client = mqtt.Client("Client1")
client.on_connect=on_connect
broker_hostname = "localhost"
port = 1890 
car_speed_topic = "test/car_speed/"
car_places_topic = "test/car_places/"

client.connect(broker_hostname, port)
client.loop_start()


def publish_to_telegraf(routes_dict: Dict):
    for route in routes_dict:
        car_id = route
        car_route = routes_dict[route]['route_info']
        print(car_id)
        
        for edge in car_route:
            # start_place = edge['start']
            # start_time = edge['start_time']
            # start_speed = edge['speed']
            end_place = edge['end']
            end_time = edge['end_time']
            end_speed = edge['speed']
            #print(start_time, start_speed, end_time, end_speed)

            payload = js.dumps({
                    'ts': end_time.timestamp(),
                    'car_speed': end_speed,
                    #'place': start_place,
                    'metric_name': 'car_speed'}).encode()

            result = client.publish(car_speed_topic + str(car_id), payload)
            status = result[0]
            if status == 0:
                print("Message "+ str(payload) + " is published to topic " + car_speed_topic + str(car_id))
            else:
                print("Failed to send message to topic " + car_speed_topic + str(car_id))

            #TODO: учесть самую первую вершину
            payload = js.dumps({
                    'ts': end_time.timestamp(),
                    'car_places': end_place,
                    'metric_name': 'car_places'}).encode()
            result = client.publish(car_places_topic + str(car_id), payload)
            status = result[0]
            if status == 0:
                print("Message "+ str(payload) + " is published to topic " + car_places_topic + str(car_id))
            else:
                print("Failed to send message to topic " + car_places_topic + str(car_id))


publish_to_telegraf(routes_dict)
