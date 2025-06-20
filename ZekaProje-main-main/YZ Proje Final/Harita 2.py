from collections import deque
from xml.sax.handler import property_dom_node

import pygame
import sys
import time
import math
import heapq

pygame.init()

WIDTH, HEIGHT = 1600, 850
pygame.display.set_caption("yol falan")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (63, 63, 63)
arkaplan = (139, 169, 119)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
sensor_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
car_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

NodeList = [[[95.0, 730.0], []], [[260.0, 730.0], [[0, 100, 0]]], [[260.0, 770.0], [[7, 100, 0], [29, 100, 0], [23, 100, 0]]], [[95.0, 770.0], [[2, 100, 0]]], [[400.0, 730.0], [[1, 100, 0], [29, 100, 0], [23, 100, 0]]], [[755.0, 730.0], [[4, 100, 0]]], [[755.0, 770.0], [[35, 100, 0], [11, 100, 0]]], [[400.0, 770.0], [[6, 100, 0]]], [[780.0, 705.0], [[5, 100, 0], [35, 100, 0]]], [[780.0, 595.0], [[8, 100, 0]]], [[820.0, 595.0], [[59, 100, 0], [15, 100, 0]]], [[820.0, 705.0], [[10, 100, 0]]], [[755.0, 570.0], [[9, 100, 0], [59, 100, 0]]], [[545.0, 570.0], [[12, 100, 0]]], [[545.0, 530.0], [[19, 100, 0], [31, 100, 0]]], [[755.0, 530.0], [[14, 100, 0]]], [[480.0, 505.0], [[31, 100, 0], [13, 100, 0]]], [[480.0, 395.0], [[16, 100, 0]]], [[520.0, 395.0], [[67, 100, 0], [25, 100, 0]]], [[520.0, 505.0], [[18, 100, 0]]], [[280.0, 650.0], [[1, 100, 0], [7, 100, 0], [29, 100, 0]]], [[280.0, 395.0], [[20, 100, 0]]], [[320.0, 395.0], [[71, 100, 0], [27, 100, 0]]], [[320.0, 650.0], [[22, 100, 0]]], [[345.0, 330.0], [[71, 100, 0], [21, 100, 0]]], [[455.0, 330.0], [[24, 100, 0]]], [[455.0, 370.0], [[17, 100, 0], [67, 100, 0]]], [[345.0, 370.0], [[26, 100, 0]]], [[499.14213562373095, 579.142135623731], [[13, 100, 0], [19, 100, 0]]], [[384.14213562373095, 694.142135623731], [[28, 100, 0]]], [[355.85786437626905, 665.857864376269], [[1, 100, 0], [23, 100, 0], [7, 100, 0]]], [[470.85786437626905, 550.857864376269], [[30, 100, 0]]], [[845.0, 730.0], [[11, 100, 0], [5, 100, 0]]], [[1355.0, 730.0], [[32, 100, 0]]], [[1355.0, 770.0], [[39, 100, 0]]], [[845.0, 770.0], [[34, 100, 0]]], [[1380.0, 705.0], [[33, 100, 0]]], [[1380.0, 245.0], [[36, 100, 0]]], [[1420.0, 245.0], [[77, 100, 0], [43, 100, 0]]], [[1420.0, 705.0], [[38, 100, 0]]], [[1355.0, 220.0], [[37, 100, 0], [77, 100, 0]]], [[1145.0, 220.0], [[40, 100, 0]]], [[1145.0, 180.0], [[47, 100, 0], [53, 100, 0]]], [[1355.0, 180.0], [[42, 100, 0]]], [[1055.0, 220.0], [[53, 100, 0], [41, 100, 0]]], [[845.0, 220.0], [[44, 100, 0]]], [[845.0, 180.0], [[65, 100, 0], [61, 100, 0]]], [[1055.0, 180.0], [[46, 100, 0]]], [[845.0, 380.0], [[63, 100, 0], [57, 100, 0]]], [[1055.0, 380.0], [[48, 100, 0]]], [[1055.0, 420.0], [[55, 100, 0]]], [[845.0, 420.0], [[50, 100, 0]]], [[1080.0, 355.0], [[49, 100, 0]]], [[1080.0, 245.0], [[52, 100, 0]]], [[1120.0, 245.0], [[41, 100, 0], [47, 100, 0]]], [[1120.0, 355.0], [[54, 100, 0]]], [[780.0, 505.0], [[15, 100, 0], [9, 100, 0]]], [[780.0, 445.0], [[56, 100, 0]]], [[820.0, 445.0], [[51, 100, 0], [63, 100, 0]]], [[820.0, 505.0], [[58, 100, 0]]], [[780.0, 355.0], [[57, 100, 0], [51, 100, 0]]], [[780.0, 265.0], [[60, 100, 0]]], [[820.0, 265.0], [[45, 100, 0], [65, 100, 0]]], [[820.0, 355.0], [[62, 100, 0]]], [[515.7349158131262, 322.27549112076326], [[25, 100, 0], [17, 100, 0]]], [[735.7349158131262, 207.27549112076326], [[64, 100, 0]]], [[754.2650841868738, 242.72450887923674], [[45, 100, 0], [61, 100, 0]]], [[534.2650841868738, 357.72450887923674], [[66, 100, 0]]], [[280.0, 305.0], [[21, 100, 0], [27, 100, 0]]], [[280.0, 95.0], [[68, 100, 0]]], [[320.0, 95.0], [[75, 100, 0]]], [[320.0, 305.0], [[70, 100, 0]]], [[345.0, 30.0], [[69, 100, 0]]], [[1355.0, 30.0], [[72, 100, 0]]], [[1355.0, 70.0], [[79, 100, 0], [83, 100, 0]]], [[345.0, 70.0], [[74, 100, 0]]], [[1420.0, 95.0], [[83, 100, 0], [73, 100, 0]]], [[1420.0, 155.0], [[76, 100, 0]]], [[1380.0, 155.0], [[43, 100, 0], [37, 100, 0]]], [[1380.0, 95.0], [[78, 100, 0]]], [[1445.0, 30.0], [[73, 100, 0], [79, 100, 0]]], [[1500.0, 30.0], [[80, 100, 0]]], [[1500.0, 70.0], []], [[1445.0, 70.0], [[82, 100, 0]]]]

class Node:
    def __init__(self, position):
        self.position = position
        self.connection = []

    def add_connection(self, target_id, max_speed, extra_wait):
        self.connection.append(Connection(target_id, max_speed, extra_wait))

    def __repr__(self):
        return f"Node(pos={self.position}, connections={self.connection})"

    def edit_connection(self, target_id, max_speed=None, extra_wait=None):
        for connection in self.connection:
            if connection.id == target_id:
                if max_speed is not None:
                    connection.speed = max_speed
                if extra_wait is not None:
                    connection.extra = extra_wait

class Connection:
    def __init__(self, target_id, max_speed, extra):
        self.id = target_id
        self.speed = max_speed
        self.extra = extra

    def __repr__(self):
        return f"Connection(to={self.id}, speed={self.speed}, wait={self.extra})"

Map = []

for i in range(len(NodeList)):
    new_node = Node(NodeList[i][0])
    for j in range(len(NodeList[i][1])):
        new_node.add_connection(NodeList[i][1][j][0], NodeList[i][1][j][1], NodeList[i][1][j][2])
    Map.append(new_node)

# draw_road() ile çizilecek yolların baş ve son noktaları
Roads = [
    [[100, 750], [1400, 750]],
    [[1400, 50], [1400, 750]],
    [[1400, 50], [300, 50]],
    [[300, 750], [300, 50]],
    [[300, 750], [500, 550]],
    [[800, 550], [500, 550]],
    [[800, 200], [800, 750]],
    [[500, 350], [800, 200]],
    [[1400, 200], [800, 200]],
    [[500, 350], [500, 550]],
    [[500, 350], [300, 350]],
    [[800, 400], [1100, 400]],
    [[1100, 200], [1100, 400]],
    [[1400, 50], [1500, 50]],
]

run = True

# iki nokta arasında belirli kalınlıkta çizgi çizen fonksiyon
def draw_line(start, end, width, color):
    width = width / 2
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dx, dy)

    offset = math.pi / 2

    corners = [[start[0] + width * math.sin(angle + offset), start[1] + width * math.cos(angle + offset)],
               [end[0] + width * math.sin(angle + offset)  , end[1] + width * math.cos(angle + offset)  ],
               [end[0] + width * math.sin(angle - offset)  , end[1] + width * math.cos(angle - offset)  ],
               [start[0] + width * math.sin(angle - offset), start[1] + width * math.cos(angle - offset)]]

    pygame.draw.polygon(screen, color, corners)

# yolun gri kısmını çizen fonkyison
def draw_road(start, end, road_width):
    pygame.draw.circle(screen, GREY, start, road_width/2)
    pygame.draw.circle(screen, GREY, end, road_width/2)
    draw_line(start, end, road_width, GREY)

# yolun beyaz çizgilerini çizen fonkyison
def draw_road_lines(start, end, line_width):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dx, dy)
    length = math.floor(math.dist(start, end))
    segments = math.floor(math.dist(start, end)/40)

    for i in range(segments):
        j = (i + 0.25) / segments
        k =  (i + 0.75) / segments
        line_start = [start[0] + j * length * math.sin(angle), start[1] + j * length * math.cos(angle)]
        line_end = [start[0] + k * length * math.sin(angle), start[1] + k * length * math.cos(angle)]

        draw_line(line_start, line_end, line_width, WHITE)


class Car(pygame.sprite.Sprite):
    def __init__(self, _position, _direction, _image, _npc=False):
        super().__init__()
        self.original_image = pygame.image.load(_image).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (40, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=_position)
        self.sensor_cover = pygame.image.load("siyaharaba.png").convert_alpha()
        self.sensor_cover = pygame.transform.scale(self.sensor_cover, (40, 40))

        self.position = _position
        self.velocity = 0
        self.max_velocity = 3
        self.acceleration = 0.2

        self.direction = _direction
        self.rotation = 0
        self.max_rotation = 3
        self.rotation_change = 0.5

        self.sensors = []

        self.target_position = [0, 0]
        self.target_counter = 0
        self.target_found = False
        self.front_sensor_threshold = 35
        self.turn_shift = 0
        self.turn_sensor = 0
        self.search_angle = 0

        self.path = []
        self.npc_path = []
        self.algorithm = "a_star" # a, b, d
        self.npc = _npc

        self.active = True

    def drive(self, _velocity, _rotation):
        if _velocity == 0 or _velocity is None:
            if math.fabs(self.velocity) < self.acceleration:
                self.velocity = 0
            if self.velocity != 0:
                self.velocity -= math.copysign(self.acceleration, self.velocity)
        else:
            velocity = _velocity
            if math.fabs(_velocity) > self.max_velocity:
                velocity = math.copysign(self.max_velocity, _velocity)
            if self.velocity < velocity:
                self.velocity += min(self.acceleration, velocity - self.velocity)
            elif self.velocity > velocity:
                self.velocity -= min(self.acceleration, self.velocity - velocity)

        if _rotation == 0 or _rotation is None:
            if math.fabs(self.rotation) < self.rotation_change:
                self.rotation = 0
            if self.rotation != 0:
                self.rotation -= math.copysign(self.rotation_change, self.rotation)
        else:
            rotation = _rotation
            if math.fabs(_rotation) > self.max_rotation:
                rotation = math.copysign(self.max_rotation, _rotation)
            if self.rotation < rotation:
                self.rotation += min(self.rotation_change, rotation - self.rotation)
            elif self.rotation > rotation:
                self.rotation -= min(self.rotation_change, self.rotation - rotation)

        if self.velocity != 0:
            self.direction = self.direction.rotate(
                self.rotation * math.copysign(min(1, (3 * math.fabs(self.velocity) / self.max_velocity)),
                                              self.velocity))
            self.position = (
            self.position[0] + self.velocity * self.direction.x, self.position[1] + self.velocity * self.direction.y)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, round(self.direction.angle_to(pygame.math.Vector2(0, -1))))
        self.rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, self.rect.topleft)
        pygame.draw.circle(screen, (0, 120, 255), self.target_position, 5)

    def add_sensor(self, _direction, _length, _target_color):
        self.sensors.append(Sensor(_direction, _length, _target_color))

    def auto(self, _target_position=None):
        if not self.active:
            return [0, 0]

        if self.npc and self.npc_path == []:
            self.npc_path = self.path

        rotated_image = pygame.transform.rotate(self.sensor_cover, round(self.direction.angle_to(pygame.math.Vector2(0, -1))))
        self.rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, self.rect.topleft)

        # Eğer hedef pozisyon verilmişse ve target_counter sıfır değilse
        if _target_position is not None and self.target_counter != 0:
            self.target_position = _target_position
        else:
            # Eğer path boşsa veya target_counter sınırı aştıysa, araç durmalı
            if (not self.path or self.target_counter >= len(self.path) )and not self.npc:
                # print("Geçerli bir rota yok veya hedef tamamlandi. Araç bekliyor...")
                self.velocity = 0
                return [0, 0]

            self.target_position = Map[self.path[self.target_counter]].position

            if math.dist(self.position, self.target_position) < 30:
                if self.target_counter < len(self.path) - 1:
                    self.target_counter += 1
                elif self.npc and math.dist(self.position, self.target_position) < 30 and self.target_counter == len(self.path) - 1:
                    self.path = self.npc_path
                    self.target_counter = 0

        target_distance = math.dist(self.position, self.target_position)
        target_angle = angle_from(self.position, self.target_position, self.direction)
        if target_angle > 0:
            target_angle = 0.1 * target_angle

        # Sensörleri aracın yönü ve konumunda çalıştır
        for sensor in self.sensors:
            sensor.detect(self.position, self.direction.angle_to(pygame.math.Vector2(1, 0)))

        # Sensorle yoldan çıkmama
        if target_angle > 0:  # Araç sağa dönecekse
            if self.sensors[1].distance < 60:
                if self.sensors[2].distance > 60:
                    target_angle *= 0.5
                if self.sensors[1].distance < 47:
                    target_angle = 0
                    if self.sensors[1].distance < 43:
                        target_angle = -1
                        if self.sensors[1].distance < 25:
                            target_angle = -4

            if self.sensors[3].distance < 30:
                target_angle = -0.5
                if self.sensors[3].distance < 20:
                    target_angle = -4

        if target_angle < 0:
            if self.sensors[2].distance < 60:
                if  self.sensors[1].distance > 60:
                    target_angle *= 0.5
                if self.sensors[2].distance < 47:
                    target_angle = 0
                    if self.sensors[2].distance < 43:
                        target_angle = 1
                        if self.sensors[2].distance < 25:
                            target_angle = 4

            if self.sensors[4].distance < 30:
                target_angle = 0.5
                if self.sensors[4].distance < 20:
                    target_angle = 4

        # Hedef noktaya göre hız ayarlama
        car_velocity = 10 - min(abs(target_angle), 17.2) / 2

        # Hedefe ulaşınca dur
        if math.dist(self.position, self.target_position) < 13:
            car_velocity = 0

        # Duvara gelince dönme
        if self.sensors[0].distance < 50 and car_velocity > 0:
            car_velocity = 0.1

        if self.sensors[0].distance < self.front_sensor_threshold:
            self.front_sensor_threshold = 55
            if self.sensors[2].distance < self.sensors[1].distance:
                if target_angle < 0:
                    target_angle = -10
            else:
                if target_angle > 0:
                    target_angle = 10
            car_velocity -= (10 - min(math.fabs(target_angle), 5) / 2)
            if car_velocity < 0:
                target_angle = -10 * target_angle
            if self.sensors[0].distance < 35:
                car_velocity = -2
                target_angle = 0
        else:
            self.front_sensor_threshold = 35

        # Araçlara çarpmama
        car = 0
        for sensor in range(1, 2):
            if self.sensors[sensor].distance < 65 and araba_renkleri.__contains__(self.sensors[sensor].color):
                car += 1

        if self.sensors[0].distance < 120 and araba_renkleri.__contains__(self.sensors[0].color):
            if math.fabs(target_angle) > 1:
                target_angle = 0
                car_velocity = 0.5
                if target_angle > 0:
                    if self.sensors[1].distance < 120 and araba_renkleri.__contains__(self.sensors[1].color):
                        car_velocity = 0.5
                    if self.sensors[2].distance < 60 and araba_renkleri.__contains__(self.sensors[2].color):
                        car_velocity = 0
                else:
                    if self.sensors[2].distance < 120 and araba_renkleri.__contains__(self.sensors[2].color):
                        car_velocity = 0.5
                    if self.sensors[1].distance < 60 and araba_renkleri.__contains__(self.sensors[1].color):
                        car_velocity = 0
            else:
                car_velocity = 0.3
        elif car > 0:
            car_velocity = 1
            if self.sensors[1].distance < 60 or self.sensors[2].distance < 60:
                car_velocity = 0.5

        if math.fabs(target_angle) > 0.5 and (self.sensors[3].distance < 60 and araba_renkleri.__contains__(self.sensors[3].color) and target_angle < 0 or self.sensors[4].distance < 60 and araba_renkleri.__contains__(self.sensors[4].color) and target_angle > 0 ):
            car_velocity = 0.1

        if self.sensors[0].distance < 60 and araba_renkleri.__contains__(self.sensors[0].color):
            car_velocity = -0.2
            if self.sensors[0].distance < 40:
                car_velocity = -0.6

        # Yaya görünce bekleme
        if (self.sensors[5].distance < 150 or self.sensors[6].distance < 160 or
                self.sensors[7].distance < 160 or self.sensors[8].distance < 180 or
                self.sensors[9].distance < 180):
            car_velocity *= 0.15
            if (self.sensors[5].distance < 90 or self.sensors[6].distance < 95 or
                    self.sensors[7].distance < 95 or self.sensors[8].distance < 105 or
                    self.sensors[9].distance < 105):
                car_velocity = 0
        elif self.sensors[10].distance < 180:
            car_velocity *= 0.2



        # Trafik Işığı Tespiti
        sensor_length = min(target_distance + 50, 500)

        if self.target_found:
            self.search_angle = -20
            while self.search_angle < 20:
                self.sensors[11].detect(
                    self.position,
                    self.direction.angle_to(pygame.math.Vector2(1, 0)) + target_angle + self.turn_sensor + self.search_angle,sensor_length + 20)
                self.search_angle += 2
                if self.sensors[11].distance < 500:
                    self.turn_sensor += self.search_angle
                    break
            if self.sensors[11].distance > 500:
                self.target_found = False

        self.turn_shift = (self.turn_shift + 1) % 20

        if not self.target_found:
            self.turn_sensor = -100 + self.turn_shift
            while self.turn_sensor < 80 and not self.target_found:
                self.turn_sensor += 20
                sensor_new_length = min(sensor_length, max(50,(200 + sensor_length) * (math.cos(self.turn_sensor * (math.pi / 180)) * ((1 - (math.fabs(self.turn_sensor) / 80)) ** 4) * (sensor_length / 500))))
                sensor_new_length += min(sensor_length,(sensor_length + 120) * (math.cos(self.turn_sensor * (math.pi / 180))) * (1 - (sensor_length / 500))) + 50
                self.sensors[11].detect(
                    self.position,
                    self.direction.angle_to(pygame.math.Vector2(1, 0)) + target_angle + self.turn_sensor, sensor_new_length)
                if self.sensors[11].distance < 500:
                    self.target_found = True
                    break

        if self.target_found:
            if ((self.sensors[11].color == (255, 255, 0) or self.sensors[11].color == (255, 0, 0)) and self.sensors[11].distance < 200):
                car_velocity *= 0.2
            if (self.sensors[11].color == (255, 0, 0) and self.sensors[12].distance < 60):
                car_velocity = 0

        # Vinç Algılama ve Geri Dönüş
        if not self.npc or True:
            next_node_id = self.path[self.target_counter + 1] if self.target_counter < len(self.path) - 1 else \
            self.path[self.target_counter]
            current_node_id = self.path[self.target_counter]
            sensor_angle = angle_from(self.position, Map[next_node_id].position)
            sensor_length = math.dist(self.position, Map[next_node_id].position)

            if self.sensors[13].detect(self.position, sensor_angle, sensor_length):
                Map[current_node_id].connection = [conn for conn in Map[current_node_id].connection if conn.id != next_node_id]
                if self.npc:
                    self.path = a_star(Map, self.npc_path[self.target_counter - 1], self.npc_path[0])
                    if self.path == None:
                        node_step = 0
                        while self.path == None and node_step < len(self.npc_path) - 1:
                            node_step += 1
                            self.path = a_star(Map, self.npc_path[self.target_counter - 1], self.npc_path[node_step])
                        self.npc_path = self.path
                else:
                    match self.algorithm:
                        case "a_star":
                            self.path = a_star(Map, self.path[self.target_counter - 1], END_NODE)
                        case "bfs":
                            self.path = bfs(Map, self.path[self.target_counter - 1], END_NODE)
                        case "dijkstra":
                            self.path = dijkstra(Map, self.path[self.target_counter - 1], END_NODE)[0]
                self.target_counter = 0

            if math.dist(self.position, self.target_position) < 20:
                car_velocity = 0

        max_speed = car_velocity
        if self.target_counter > 0:
            for connection in Map[self.path[self.target_counter-1]].connection:
                if connection.id == self.path[self.target_counter]:
                    max_speed = (connection.speed * 1000) / 60 / 60 * (3/16.66)

        if math.fabs(car_velocity) > max_speed:
            car_velocity = math.copysign(max_speed, car_velocity)

        self.draw(screen)
        return [car_velocity, -target_angle]

        self.original_image = pygame.transform.scale(self.original_image, (40, 40))

# Sensörlerin çizimi
DRAW_SENSOR = True

class Sensor:
    def __init__(self, _direction, _length, _target_colors):
        self.direction = _direction
        self.length = _length
        self.colors = _target_colors
        self.distance = 0
        self.color = None

    def detect(self, _position, _rotation, _length=None):
        if _length == None:
            _length = self.length

        rotation = (self.direction + _rotation) * math.pi/180
        if math.fabs(math.cos(rotation)) < math.fabs(math.sin(rotation)):
            dx = math.copysign(math.cos(rotation) / math.sin(rotation), math.cos(rotation))
            dy = -math.copysign(1, math.sin(rotation))
            loop = math.fabs(math.floor(_length * math.sin(rotation)))
        else:
            dx = math.copysign(1, math.cos(rotation))
            dy = -math.copysign(math.sin(rotation) / math.cos(rotation), math.sin(rotation))
            loop = math.fabs(math.floor(_length * math.cos(rotation)))

        step_size = 10
        precision_range = 50

        if _length < precision_range:
            loop_range = loop
        else:
            loop_range = (loop - precision_range) / step_size + precision_range

        for i in range(int(loop_range)):
            if i > precision_range:
                i = (i - precision_range) * step_size + precision_range
            pixel_position = (int(_position[0] + i * dx), int(_position[1] + i * dy))
            if pixel_position[0] > 0 and pixel_position[0] < screen.get_width() and pixel_position[1] > 0 and pixel_position[1] < screen.get_height():
                pixel_color = screen.get_at(pixel_position)
                color_check = False
                for color in self.colors:
                    if pixel_color == color:
                        color_check = True
                        self.color = color
                if color_check:
                    if DRAW_SENSOR:
                        pygame.draw.line(sensor_surface, (254, 254, 254), _position, (_position[0] + i * dx, _position[1] + i * dy), 3)
                        pygame.draw.circle(sensor_surface, (0, 254, 0), (_position[0] + i * dx, _position[1] + i * dy), 3)
                    self.distance = math.dist((0,0), (i * dx, i * dy))
                    return True

        if DRAW_SENSOR:
            pygame.draw.line(sensor_surface, (254, 254, 254, 123), _position, (_position[0] + _length * math.cos(rotation), _position[1] - _length * math.sin(rotation)), 1)
            pygame.draw.circle(sensor_surface, (254, 0, 0, 64), (_position[0] + _length * math.cos(rotation), _position[1] - _length * math.sin(rotation)), 3)
        self.distance = 999
        return False

def path_cost(Map, _path):
    cost = 0
    for i in range(len(_path)-2):
        for connection in Map[_path[i]].connection:
            if connection.id == _path[i+1]:
                cost += math.dist(Map[_path[i]].position, Map[_path[i+1]].position) / (connection.speed * 1000) / 60 / 60 * (3/16.66)
    return cost

def angle_from(start_point, target_point, start_angle=pygame.math.Vector2(1, 0)):
    atarget_position = pygame.math.Vector2(target_point)
    start_position = pygame.math.Vector2(start_point)

    vector_to_target = atarget_position - start_position
    car_direction = pygame.math.Vector2(start_angle)

    # Aracın döneceği açı
    return (vector_to_target.rotate(car_direction.angle_to(pygame.math.Vector2([1, 0]))).angle_to(pygame.math.Vector2([1, 0])))

def get_closest_node(position):
    min_distance = float('inf')
    closest_node_id = 0
    for node_id, node in enumerate(Map):
        distance = math.dist(position, node.position)
        if distance < min_distance:
            min_distance = distance
            closest_node_id = node_id
    return closest_node_id


# -------------------------------------------------------------------------------- A*
def a_star(Map, start_id, goal_id):
    open_set = {start_id}
    came_from = {}
    g_score = {node: float('inf') for node in range(len(Map))}
    g_score[start_id] = 0
    f_score = {node: float('inf') for node in range(len(Map))}
    f_score[start_id] = heuristic(start_id, goal_id)

    while open_set:
        current = min(open_set, key=lambda node: f_score[node])

        if current == goal_id:
            return reconstruct_path(came_from, current)

        open_set.remove(current)

        for connection in Map[current].connection:
            neighbor = connection.id
            tentative_g_score = g_score[current] + cost(current, neighbor, connection)

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal_id)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None  # Eğer hedefe ulaşılamazsa


def heuristic(node_id, goal_id):
    # Öklid mesafesini kullanıyoruz
    return math.dist(Map[node_id].position, Map[goal_id].position)


def cost(current_id, neighbor_id, connection):
    distance = math.dist(Map[current_id].position, Map[neighbor_id].position)
    time = distance / ((connection.speed * 1000) / 60 / 60 * (3/16.66))  # Simülasyon piksel/saniye hızı
    return time + connection.extra

def reconstruct_path(came_from, current):
    total_self = [current]
    while current in came_from:
        current = came_from[current]
        total_self.append(current)
    return total_self[::-1]  # Ters çeviriyoruz


# -------------------------------------------------------------------------------- BFS
def bfs(graph, node1, node2):
    queue = deque([(node1, [node1])])
    visited = set()

    while queue:
        current_node, path = queue.popleft()

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == node2:
            return path

        for connection in graph[current_node].connection:
            if connection.extra != 999:
                queue.append((connection.id, path + [connection.id]))
    return None


# -------------------------------------------------------------------------------- Djikstra
def dijkstra(Map, start_id, goal_id):
    distances = {i: float('inf') for i in range(len(Map))}
    distances[start_id] = 0.0
    previous_nodes = {}
    visited = set()
    pq = []
    heapq.heappush(pq, (0.0, start_id))

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node == goal_id:
            break
        if current_node in visited:
            continue
        visited.add(current_node)

        for conn in Map[current_node].connection:
            neighbor_id = conn.id
            dist_pixels = math.dist(Map[current_node].position, Map[neighbor_id].position)
            dist_meters = dist_pixels / (3/16.66)
            speed_m_per_s = ((conn.speed * 1000) / 360)
            travel_time = (dist_meters / speed_m_per_s) + conn.extra
            new_distance = current_distance + travel_time

            if new_distance < distances[neighbor_id]:
                distances[neighbor_id] = new_distance
                previous_nodes[neighbor_id] = current_node
                heapq.heappush(pq, (new_distance, neighbor_id))

    # Reconstruct path
    path = []
    node = goal_id
    while node in previous_nodes:
        path.append(node)
        node = previous_nodes[node]
    path.append(start_id)
    path.reverse()

    return path, distances[goal_id]

START_NODE = 3
END_NODE = 82
NPC = True

car1 = Car(Map[START_NODE].position, pygame.math.Vector2(1, 0), "yesilaraba.png")
car2 = Car(Map[START_NODE].position, pygame.math.Vector2(1, 0), "sariaraba.png")
car3 = Car(Map[START_NODE].position, pygame.math.Vector2(1, 0), "pembearaba.png")

car1.path = a_star(Map, START_NODE, END_NODE)
car2.path = dijkstra(Map, START_NODE, END_NODE)[0]
car3.path = bfs(Map, START_NODE, END_NODE)

car1.active = False
car2.active = False
car3.active = False

print(f"     A* : {car1.path}")
print(f"Dijkstra: {car2.path}")
print(f"    BFS : {car3.path}")

npc1 = Car(Map[21].position, pygame.math.Vector2(0, 1), "griaraba.png", NPC)
npc1.path = [21, 20, 7, 6, 11, 59, 58, 63, 62, 65, 64, 25, 24]

npc2 = Car(Map[61].position, pygame.math.Vector2(0, 1), "griaraba.png", NPC)
npc2.path = [61, 60, 57, 56, 9, 8, 35, 34, 39, 38, 43, 42, 47, 46]

npc3 = Car(Map[18].position, pygame.math.Vector2(0, -1), "griaraba.png", NPC)
npc3.path = [18, 67, 66, 61, 60, 51, 50, 55, 54, 47, 46, 61, 60, 57, 56, 15, 14, 19]

npc4 = Car(Map[49].position, pygame.math.Vector2(-1, 0), "griaraba.png", NPC)
npc4.path = [49, 48, 63, 62, 65, 64, 17, 16, 13, 12, 59, 58, 63, 62, 45, 44, 53, 52]

npc5 = Car(Map[37].position, pygame.math.Vector2(0, 1), "griaraba.png", NPC)
npc5.path = [37, 36, 33, 32, 11, 10, 59, 58, 63, 62, 45, 44, 41, 40]

npc6 = Car(Map[31].position, pygame.math.Vector2(-1, 1).normalize(), "griaraba.png", NPC)
npc6.path = [31, 30, 7, 6, 11, 10, 15, 14]

# Her araca sensör ekle
cars = [car1, car2, car3, npc1, npc2, npc3, npc4, npc5, npc6]

pembe = (253, 62, 127)
sari = (253, 185, 62)
yesil = (62, 253, 109)
gri = (179, 179, 179)

araba_renkleri = [pembe, sari, yesil, gri]

for car in cars:
    # Yol Kenarı Sensörleri
    if car.npc:
        target_colors = [arkaplan, pembe, sari, yesil, gri]
    else:
        target_colors = [arkaplan, gri]
    car.add_sensor(0, 120, target_colors)
    car.add_sensor(30, 120, target_colors)
    car.add_sensor(-30, 120, target_colors)
    car.add_sensor(50, 80, target_colors)
    car.add_sensor(-50, 80, target_colors)

    # Yaya Sensöleri
    car.add_sensor(0, 150, [(253, 201, 166), (255, 121, 109), (99, 185, 240)])
    car.add_sensor(9, 150, [(253, 201, 166), (255, 121, 109), (99, 185, 240)])
    car.add_sensor(-9, 150, [(253, 201, 166), (255, 121, 109), (99, 185, 240)])
    car.add_sensor(20, 150, [(253, 201, 166), (255, 121, 109), (99, 185, 240)])
    car.add_sensor(-20, 150, [(253, 201, 166), (255, 121, 109), (99, 185, 240)])

    # Yaya Geçidi Sensörü
    car.add_sensor(0, 180, [(175, 175, 175)])

    # Trafik Işığı Sensörleri
    car.add_sensor(0, 100, [(255, 0, 0), (255, 255, 0), (0, 255, 0)])
    car.add_sensor(8, 80, [(185, 185, 185)])

    # Yol Çalışması Sensörü
    car.add_sensor(0, 200, [(255, 188, 66), (51, 101, 138)])  # (255,140,0),(200,140,0)

    # Taşlı yolda yavaşlama (169,169,169) (105, 105, 105)
    car.add_sensor(0, 100, [(105, 105, 105)])

vinc_resmi = pygame.image.load("vinc.png")
vinc_resmi = pygame.transform.scale(vinc_resmi, (int(vinc_resmi.get_width() * 0.8), int(vinc_resmi.get_height() * 0.8)))
vincler = []

def main():
    pygame.display.update()

    # TRAFİK IŞIĞI ZAMANLAYICISI
    clock = pygame.time.Clock()
    start_time = time.time()

    global DRAW_SENSOR

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if DRAW_SENSOR == False:
                            DRAW_SENSOR = True
                        else:
                            DRAW_SENSOR = False
                    if event.key ==pygame.K_SPACE:
                        car1.active = True
                        car2.active = True
                        car3.active = True

                    if event.key ==pygame.K_1:
                        car1.active = True
                    if event.key ==pygame.K_2:
                        car2.active = True
                    if event.key ==pygame.K_3:
                        car3.active = True

            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Get the mouse position
                vincler.append((mouse_x, mouse_y))  # Add the position to the vinc list

        screen.fill(arkaplan)

        for road in Roads:
            draw_road(road[0], road[1], 80)
        for road in Roads:
            draw_road_lines(road[0], road[1], 3)
        for vinc in vincler:
            screen.blit(vinc_resmi, ((vinc[0]-45), (vinc[1])-65))
        for car in cars:
            car.draw(screen)

        for car in cars:
            c_auto = car.auto()
            car.drive(c_auto[0], c_auto[1])

        # Sensörleri Çiz
        screen.blit(sensor_surface, (0, 0))
        screen.blit(car_surface, (0, 0))
        sensor_surface.fill((0, 0, 0, 0))

        # Araba Şeyisini Temizle
        car_surface.fill((0, 0, 0, 0))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()