from re import search
from collections import deque
import pygame
import sys
import time
import math
import heapq

pygame.init()

# screenmiz
WIDTH = 1600
HEIGHT = 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
sensor_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
car_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# RENKLER
arkaplan = (139, 169, 119)
pastel_pink = (255, 182, 193)
brown = (80, 40, 10)
dark_gray = (169, 169, 169)
tree_green = (34, 139, 34)  # Ağaç yeşili
curtain_color_1 = (255, 215, 0)  # Altın sarısı perde
curtain_color_2 = (255, 239, 204)  # Krem rengi perde
cornice_color = (139, 69, 19)  # Kahverengi korniş
asphalt_color = (50, 50, 50)  # Asfalt yol için koyu gri
black = (0, 0, 0)  # Tekerlekler için siyah ofis ve ev içinde kullanılıyor
silver = (192, 192, 192)  # Jant rengi
white = (255, 255, 255)  # Farlar, screen çerçeveleri ve ön ızgara için white
yellow = (254, 254, 0)  # Sarı renk tanımlaması
red = (254, 0, 0)  # Kırmızı
green = (0, 254, 0)  # Yeşil
red_off = (100, 0, 0)
yellow_off = (100, 100, 0)
green_off = (0, 100, 0)
pink = (255, 192, 203)  # Pembe
havuz_mavisi = (0, 191, 255)  # MERKEZ DAİRE
stone_light = (169, 169, 169)  # Taşlı yol için açık gri
stone_dark = (105, 105, 105)  # Taşlı yol için koyu gri
small_building_color = (200, 200, 200)
building_color = (150, 150, 150)
sensor_yayagecidi = (175, 175, 175)
sensor_trafikisigi = (185, 185, 185)

# Yazı tipi ayarları
font = pygame.font.Font(None, 20)
garage_font = pygame.font.Font(None, 18)

# Graph için düğüm listesi
NodeList = [[[1420.0, 785.0], []], [[1420.0, 695.0], [[0, 50, 0]]], [[1460.0, 695.0], [[11, 50, 0], [7, 50, 0]]], [[1460.0, 785.0], [[2, 50, 0]]], [[1400.0, 675.0], [[1, 50, 0], [11, 50, 0]]], [[955.0, 675.0], [[4, 50, 0]]], [[955.0, 635.0], [[19, 50, 0], [15, 50, 0]]], [[1400.0, 635.0], [[6, 50, 0]]], [[1420.0, 615.0], [[1, 50, 0], [7, 50, 0], [7, 50, 0]]], [[1420.0, 305.0], [[8, 50, 0]]], [[1460.0, 305.0], [[27, 50, 0], [23, 50, 0]]], [[1460.0, 615.0], [[10, 50, 0]]], [[875.0, 675.0], [[5, 50, 0], [19, 50, 0]]], [[480.0, 675.0], [[12, 50, 0]]], [[480.0, 635.0], [[31, 50, 0], [35, 50, 0]]], [[875.0, 635.0], [[14, 50, 0]]], [[895.0, 615.0], [[15, 50, 0], [5, 50, 0]]], [[895.0, 480.0], [[16, 50, 0]]], [[935.0, 480.0], [[43, 50, 0], [39, 50, 0]]], [[935.0, 615.0], [[18, 50, 0]]], [[1400.0, 285.0], [[9, 50, 0], [27, 50, 0]]], [[955.0, 285.0], [[20, 50, 0]]], [[955.0, 245.0], [[47, 50, 0], [41, 50, 0]]], [[1400.0, 245.0], [[22, 50, 0]]], [[1420.0, 225.0], [[23, 50, 0], [9, 50, 0]]], [[1420.0, 155.0], [[24, 50, 0]]], [[1460.0, 155.0], [[51, 50, 0]]], [[1460.0, 225.0], [[26, 50, 10]]], [[400.0, 675.0], [[13, 50, 0], [35, 50, 0]]], [[230.0, 675.0], [[28, 50, 0]]], [[230.0, 635.0], [[55, 50, 0]]], [[400.0, 635.0], [[30, 50, 0]]], [[420.0, 615.0], [[31, 50, 0], [13, 50, 0]]], [[420.0, 480.0], [[32, 50, 0]]], [[460.0, 480.0], [[59, 50, 0], [37, 50, 0]]], [[460.0, 615.0], [[34, 50, 0]]], [[875.0, 460.0], [[43, 50, 0], [17, 50, 0]]], [[480.0, 460.0], [[36, 50, 0]]], [[480.0, 420.0], [[33, 50, 0], [59, 50, 0]]], [[875.0, 420.0], [[38, 50, 10]]], [[895.0, 400.0], [[39, 50, 0], [17, 50, 0]]], [[895.0, 305.0], [[40, 50, 0]]], [[935.0, 305.0], [[21, 50, 0], [47, 50, 0]]], [[935.0, 400.0], [[42, 50, 0]]], [[895.0, 225.0], [[41, 50, 0], [21, 50, 0]]], [[895.0, 155.0], [[44, 50, 0]]], [[935.0, 155.0], [[49, 50, 0], [63, 50, 0]]], [[935.0, 225.0], [[46, 50, 0]]], [[1400.0, 135.0], [[25, 50, 0]]], [[955.0, 135.0], [[48, 50, 0]]], [[955.0, 95.0], [[63, 50, 0], [45, 50, 0]]], [[1400.0, 95.0], [[50, 50, 0]]], [[170.0, 615.0], [[29, 50, 0]]], [[170.0, 155.0], [[52, 50, 0]]], [[210.0, 155.0], [[65, 50, 0], [71, 50, 0]]], [[210.0, 615.0], [[54, 50, 10]]], [[420.0, 400.0], [[33, 50, 0], [37, 50, 0]]], [[420.0, 155.0], [[56, 50, 0]]], [[460.0, 155.0], [[67, 50, 0], [61, 50, 0]]], [[460.0, 400.0], [[58, 50, 0]]], [[875.0, 135.0], [[45, 50, 0], [49, 50, 0]]], [[480.0, 135.0], [[60, 50, 0]]], [[480.0, 95.0], [[67, 50, 0], [57, 50, 0]]], [[875.0, 95.0], [[62, 50, 0]]], [[400.0, 135.0], [[61, 50, 0], [57, 50, 0]]], [[230.0, 135.0], [[64, 50, 0]]], [[230.0, 95.0], [[71, 50, 0], [53, 50, 0]]], [[400.0, 95.0], [[66, 50, 0]]], [[150.0, 135.0], [[53, 50, 0], [65, 50, 0]]], [[115.0, 135.0], [[68, 50, 0]]], [[115.0, 95.0], []], [[150.0, 95.0], [[70, 50, 0]]]]

class Node:
    def __init__(self, node_id, position):
        self.id = node_id
        self.position = position
        self.connection = []
#Düğümler arası bağlantı
    def add_connection(self, target_id, max_speed, extra_wait):
        if target_id != self.id:  # Kendine bağlantıyı engelle
            self.connection.append(Connection(target_id, max_speed, extra_wait))

    # Bağlantının bir temsilinin döndürülmesi
    def __repr__(self):
        return f"Node(id={self.id}, pos={self.position}, connections={self.connection})"

    def edit_connection(self, target_id, max_speed=None, extra_wait=None):
        for connection in self.connection:
            if connection.id == target_id:
                if max_speed is not None:
                    connection.speed = max_speed
                if extra_wait is not None:
                    connection.extra = extra_wait
#Bağlantıların düzenlenmesi
class Connection:
    def __init__(self, target_id, max_speed, extra):
        self.id = target_id
        self.speed = max_speed
        self.extra = extra

    def __repr__(self):
        return f"Connection(to={self.id}, speed={self.speed}, wait={self.extra})"

# Kullanımı kolaylaştırmak için Class'lara dönüştürme( node listi node ve connection nesnelerine dönüştürür)
Map = []
for i in range(len(NodeList)):
    new_node = Node(i, NodeList[i][0])
    for j in range(len(NodeList[i][1])):
        target_id, max_speed, extra_wait = NodeList[i][1][j]
        new_node.add_connection(target_id, max_speed, extra_wait)
    Map.append(new_node)

# EKLENEN RESİMLER
cop_kutusu = pygame.image.load("cop_kutusu.png")
agac = pygame.image.load("agac.png")
kazi_alani = pygame.image.load("kazi_alani.png")
yolengel = pygame.image.load("yolengel.png")
isci = pygame.image.load("amele.png")
vinc = pygame.image.load("vinc.png")
bizim_arac= pygame.image.load("pembearaba.png")
bankta_oturan_adam= pygame.image.load("bankta_oturan_adam.png")
Veteriner=pygame.image.load("veteriner.png")
# BAŞLANGIÇ NOKTAMIZ OLAN GARJIMIZ VE GÜZEL EVİMİZ
# Home sweet home...
# Ev çizim fonksiyonu
def draw_house(x, y):
    house_width, house_height = 75, 75  # Küçültülmüş ev boyutları
    pygame.draw.rect(screen, pastel_pink, (x, y, house_width, house_height))
    pygame.draw.polygon(screen, brown, [(x, y), (x + house_width // 2, y - house_height // 2), (x + house_width, y)])
    pygame.draw.rect(screen, dark_gray, (x + 26, y + 38, 23, 38))  # Kapı küçültüldü

    # pencereler
    window_size = 15
    left_window = pygame.draw.rect(screen, black, (x + 7, y + 15, window_size, window_size), 2)
    right_window = pygame.draw.rect(screen, black, (x + 53, y + 15, window_size, window_size), 2)

    # Perdeler
    pygame.draw.rect(screen, cornice_color, (left_window.x - 2, left_window.y - 5, window_size + 4, 5))
    pygame.draw.rect(screen, cornice_color, (right_window.x - 2, right_window.y - 5, window_size + 4, 5))
    pygame.draw.rect(screen, curtain_color_1,
                     (left_window.x + 2, left_window.y + 2, window_size - 4, window_size // 2))
    pygame.draw.rect(screen, curtain_color_2,
                     (left_window.x + 2, left_window.y + window_size // 2 + 2, window_size - 4, window_size // 2))
    pygame.draw.rect(screen, curtain_color_1,
                     (right_window.x + 2, right_window.y + 2, window_size - 4, window_size // 2))
    pygame.draw.rect(screen, curtain_color_2,
                     (right_window.x + 2, right_window.y + window_size // 2 + 2, window_size - 4, window_size // 2))

# Araba Garajı çizim fonksiyonu
def draw_garage(x, y):
    garage_width, garage_height = 60, 45  # Küçültülmüş garaj boyutları
    pygame.draw.rect(screen, black, (x, y, garage_width, garage_height))
    pygame.draw.rect(screen, dark_gray, (x + 8, y + 15, garage_width - 16, garage_height - 20))

    # "GARAGE" yazısını ekle
    text = garage_font.render("GARAGE", True, white)
    text_rect = text.get_rect(center=(x + garage_width // 2, y + 8))
    screen.blit(text, text_rect)

# Büyük işyeri binası çizim fonksiyonu
def draw_large_building(x, y):
    building_width, building_height = 90, 112  # Küçültülmüş boyutlar
    pygame.draw.rect(screen, building_color, (x, y, building_width, building_height))
    pygame.draw.rect(screen, black, (x, y - 15, building_width, 15))  # Düz çatı
    text = font.render("OFFICE", True, white)
    screen.blit(text, (x + 15, y - 15))

    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, black, (x + 11 + i * 22, y + 15 + j * 30, 11, 11), 2)

        # Küçük işyeri binası çizim fonksiyonu

#Küçük iş yeri binası çizimi
def draw_small_building(x, y):
    building_width, building_height = 60, 75  # Küçültülmüş boyutlar
    pygame.draw.rect(screen, small_building_color, (x, y, building_width, building_height))
    pygame.draw.rect(screen, black, (x, y - 7, building_width, 15))  # Düz çatı
    text = font.render("OFFICE", True, white)
    screen.blit(text, (x + 5, y - 8))

    for i in range(3):
        pygame.draw.rect(screen, black, (x + 8 + i * 18, y + 15, 11, 11), 2)  # Üst screenler
        pygame.draw.rect(screen, black, (x + 8 + i * 18, y + 45, 11, 11), 2)  # Alt screenler

# YOLLARIN VE ŞERİT ÇİZGİLERİNİN KALINLIĞI, ŞERİT ÇİZGİLERİ ARASI BOŞLUK
yol_width = 80
serit_width = 5
serit_gap = 45

# YOLLAR
# en üstte olan yatay yol
def draw_ust_yatay_road():
    pygame.draw.rect(screen, asphalt_color, (0, 75, WIDTH, yol_width))  # üst yatay yol
# en altta olan yatay yol
def draw_alt_yatay_road():
    pygame.draw.rect(screen, asphalt_color, (900, 615, WIDTH, yol_width))  # alt yatay yol
def draw_sol_alt_yatay_road():
    pygame.draw.rect(screen, asphalt_color, (0, 615,415, yol_width ))  # alt yatay yol
#taşlı yol
def draw_horizontal_gravel_road_with_pattern():
    block_size = 20  # Taş bloklarının boyutu (kareler)
    start_x = 415    # Yatay yolun başlangıç x koordinatı
    start_y = 615    # Yatay yolun başlangıç y koordinatı
    road_width = 80 # Yolun genişliği (kaç sıra taş olacağına bağlı)

    # Yol boyunca kaç blok yatay olarak çizilecek
    num_columns = (900 - start_x) // block_size  # Yolun uzunluğu (900 bitiş x)
    num_rows = road_width // block_size          # Yolun genişliği kadar sıra

    for row in range(num_rows):
        for col in range(num_columns):
            # Renk alternasyonu (sıra ve sütun toplamına göre)
            color = stone_light if (row + col) % 2 == 0 else stone_dark

            # Taş bloklarının koordinatları
            x = start_x + col * block_size
            y = start_y + row * block_size

            # Taşı biraz çapraz hale getirmek için her sırayı kaydır
            if row % 2 == 1:
                x += block_size // 2

            # Taş bloğunu çiz
            pygame.draw.rect(screen, color, (x, y, block_size, block_size))

# evden çıkan en soldaki dikey yol
def draw_sol_dikey_road():
    pygame.draw.rect(screen, asphalt_color, (150, 80, yol_width, HEIGHT))  # sol dikey yol
# köpekli kadının geçtiği yol
def draw_sag_dikey_road():
    pygame.draw.rect(screen, asphalt_color, (875, 80, yol_width, 650))  # sağ dikey yol
# alt kısmına yapılan ekleme minik yol
def draw_minikYol2():
    pygame.draw.rect(screen, asphalt_color, (875, 730, yol_width, 300))
# sola dönüşün yasak olduğu, soldan ikinci dikey yol
def draw_ortayol1_road():
    pygame.draw.rect(screen, asphalt_color, (400, 100, yol_width, 900))  # sol orta yolun dikey yolu
# alt kısmına yapılan ekleme minik yol
def draw_minikYol1():
    pygame.draw.rect(screen, asphalt_color, (400, 650, yol_width, 300))
# yol çalışmasının olduğu yol
def draw_orta_yatay1_road():
    pygame.draw.rect(screen, asphalt_color, (460, 400, 415, yol_width))  # sol orta yolun yatay yolu
# en sağdaki dikey yol
def draw_ortayol2_road():
    pygame.draw.rect(screen, asphalt_color, (1400, 100, yol_width, 900))  # sağ orta yolun dikey yolu
# yukarıdan ikinci yol
def draw_orta_yatay2_road():
    pygame.draw.rect(screen, asphalt_color, (935, 225, 525, yol_width))  # sağ orta yolun yatay yolu

# ŞERİT ÇİZGİLERİNİN ÇİZİLMESİ
def draw_serit_cizgileri():
    for y in range(170, 600, serit_gap * 2):
        pygame.draw.rect(screen, white, (187, y, serit_width, serit_gap))  # sol dikey yol
    for y in range(175, 600, serit_gap * 2):
        pygame.draw.rect(screen, white, (912, y, serit_width, serit_gap))  # sağ dikey yol
    for x in range(0, 1600, serit_gap * 2):
        pygame.draw.rect(screen, white, (x, 650, serit_gap, serit_width))  # alt yatay yol
    for x in range(0, 1600, serit_gap * 2):
        pygame.draw.rect(screen, white, (x, 110, serit_gap, serit_width))  # üst yatay yol
    for y in range(170, 600, serit_gap * 2):
        pygame.draw.rect(screen, white, (437, y, serit_width, serit_gap), )  # sağ orta yolun dikey yolu
    for y in range(160, 600, serit_gap * 2):
        pygame.draw.rect(screen, white, (1438, y, serit_width, serit_gap))  # sol orta yolun dikey yolu
    for x in range(460, 875, serit_gap * 2):
        pygame.draw.rect(screen, white, (x, 436, serit_gap, serit_width))  # sol orta yolun yatay yolu
    for x in range(970, 1415, serit_gap * 2):
        pygame.draw.rect(screen, white, (x, 262, serit_gap, serit_width))  # sağ orta yolun yatay yolu
    for y in range(700, 900, serit_gap * 2):
        pygame.draw.rect(screen, white, (437, y, serit_width, serit_gap))  # minikyol1 in şeritleri
    for y in range(700, 900, serit_gap * 2):
        pygame.draw.rect(screen, white, (912, y, serit_width, serit_gap))  # minikyol2 nin şeritleri
    for y in range(700, 900, serit_gap * 2):
        pygame.draw.rect(screen, white, (187, y, serit_width, serit_gap))  # minikyol1 in şeritleri
    for y in range(700, 900, serit_gap * 2):
        pygame.draw.rect(screen, white, (1438, y, serit_width, serit_gap))  # minikyol1 in şeritleri

# TRAFİK LEVHALARININ RESİMLERİNİN YÜKLEME ALANI
yaya_gecidi_img = pygame.image.load("yayagecidi.png")
tali_yol_img = pygame.image.load("yolver.png")
dur_img = pygame.image.load("durlevhasi.png")

# EKLENEN GÖRSELLERİN BOYUT AYARLAMASI
scale_factor = 0.1  # Görsellerin boyutunu küçültmek için bir ölçek faktörü
yaya_gecidi_img = pygame.transform.scale(yaya_gecidi_img, (
int(yaya_gecidi_img.get_width() * scale_factor), int(yaya_gecidi_img.get_height() * scale_factor)))
tali_yol_img = pygame.transform.scale(tali_yol_img, (
int(tali_yol_img.get_width() * scale_factor), int(tali_yol_img.get_height() * scale_factor)))
dur_img = pygame.transform.scale(dur_img, (int(dur_img.get_width() * 0.2), int(dur_img.get_height() * 0.2)))
kazi_alani = pygame.transform.scale(kazi_alani, (int(kazi_alani.get_width() * scale_factor), int(kazi_alani.get_height() * scale_factor)))
yolengel = pygame.transform.scale(yolengel, (int(yolengel.get_width() * 0.1), int(yolengel.get_height() * 0.1)))
vinc = pygame.transform.scale(vinc, (int(vinc.get_width() * 0.8), int(vinc.get_height() * 0.8)))
bizim_arac = pygame.transform.scale(bizim_arac, (int(bizim_arac.get_width() * 0.025), int(bizim_arac.get_height() * 0.025)))
bankta_oturan_adam = pygame.transform.scale(bankta_oturan_adam, (int(bankta_oturan_adam.get_width() * 1.2), int(bankta_oturan_adam.get_height() * 1.2)))
Veteriner = pygame.transform.scale(Veteriner, (int(Veteriner.get_width() * 0.8), int(Veteriner.get_height() * 0.8)))
# Araç Sınfı 2
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
        self.algorithm = "a_star" # a_star, dijkstra, bfs
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
                    if self.sensors[2].distance < 80 and araba_renkleri.__contains__(self.sensors[2].color):
                        car_velocity = 0
                else:
                    if self.sensors[2].distance < 120 and araba_renkleri.__contains__(self.sensors[2].color):
                        car_velocity = 0.5
                    if self.sensors[1].distance < 80 and araba_renkleri.__contains__(self.sensors[1].color):
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
        if not self.npc:
            next_node_id = self.path[self.target_counter + 1] if self.target_counter < len(self.path) - 1 else \
            self.path[self.target_counter]
            current_node_id = self.path[self.target_counter]
            sensor_angle = angle_from(self.position, Map[next_node_id].position)
            sensor_length = math.dist(self.position, Map[next_node_id].position)

            if self.sensors[13].detect(self.position, sensor_angle, sensor_length):
                Map[current_node_id].connection = [conn for conn in Map[current_node_id].connection if conn.id != next_node_id]
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

# TRAFİK IŞIĞININ ÇİZİMİ 1
isik_radius = 10

# TRAFİK IŞIĞINDA IŞIK RENGİNİN DEĞİŞİMİ
def draw_trafik_isigi(x, y, light_color):
    # Trafik ışığı çizimi
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 20, 60))
    pygame.draw.circle(screen, green_off if light_color != "yesil" else (0, 255, 0), (x + 10, y + 10), isik_radius)
    pygame.draw.circle(screen, yellow_off if light_color != "sari" else (255, 255, 0), (x + 10, y + 30), isik_radius)
    pygame.draw.circle(screen, red_off if light_color != "kirmizi" else (255, 0, 0), (x + 10, y + 50), isik_radius)

# Yaya geçidi çizgilerinin özellikleri
line_height = 7  # yaya gecidi şeridinin genişliği
cizgiler_arasi_aralik = 8
line_width = 55
# YAYA GEÇİTLERİNİN ÇİZDİRİLMESİ
def draw_yatay_yaya_gecidi():
    # Çizgi boyutları
    for i in range(5, 11):  # bir yolun genişliği 7-12 aralığında yani 5 piksel
        yaya_gecidi = pygame.Rect(550, i * (line_height + cizgiler_arasi_aralik), line_width,
                                  line_height)  # 550 x eksenindeki konumu
        pygame.draw.rect(screen, white if i % 1 == 0 else asphalt_color, yaya_gecidi)
def draw_dikey_yaya_gecidi():
    # Dikey yaya geçidi çizgilerini çiz
    for i in range(58, 64):  # bir yolun genişliği 80-85 aralığında yani 5 piksel
        yaya_gecidi = pygame.Rect(i * (line_height + cizgiler_arasi_aralik), 320, line_height,
                                  line_width)  # 300 y eksenindeki konumu
        pygame.draw.rect(screen, white if i % 1 == 0 else asphalt_color, yaya_gecidi)
    # GEÇİCİ ARABANIN ÇİZDİRİLMESİ
def draw_car(x, y, color):
    pygame.draw.rect(screen, color, (x, y, 30, 15), border_radius=60)  # Araba gövdesi
    pygame.draw.circle(screen, havuz_mavisi, (x + 6, y + 7.5), 5.5)
    pygame.draw.circle(screen, havuz_mavisi, (x + 23, y + 7.5), 6.5)
    #Aracın dönüşü
def angle_from(start_point, target_point, start_angle=pygame.math.Vector2(1, 0)):
    atarget_position = pygame.math.Vector2(target_point)
    start_position = pygame.math.Vector2(start_point)

    vector_to_target = atarget_position - start_position
    car_direction = pygame.math.Vector2(start_angle)

    # Aracın döneceği açı
    return (vector_to_target.rotate(car_direction.angle_to(pygame.math.Vector2([1, 0]))).angle_to(pygame.math.Vector2([1, 0])))
#Düğümlerden ilerleme
def get_closest_node(position):
    min_distance = float('inf')
    closest_node_id = 0
    for node_id, node in enumerate(Map):
        distance = math.dist(position, node.position)
        if distance < min_distance:
            min_distance = distance
            closest_node_id = node_id
    return closest_node_id

#----------------------------------------------- A* ALGORİTMASI EKLENMESİ
#başlangıç ve hedef düğümler
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

# Öklid mesafesini kullanıyoruz
def heuristic(node_id, goal_id):

    return math.dist(Map[node_id].position, Map[goal_id].position)

#düğüm ıd bağlantısı
def cost(current_id, neighbor_id, connection):
    distance = math.dist(Map[current_id].position, Map[neighbor_id].position)
    time = distance / ((connection.speed * 1000) / 60 / 60 * (3/16.66))  # Simülasyon piksel/saniye hızı
    return time + connection.extra
#Bu fonksiyon, came_from'u kullanarak hedef düğümden başlangıç düğümüne kadar olan yolu adım adım oluşturur.
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
END_NODE = 70
NPC = True

Map[15].edit_connection(14, 20, None)
Map[13].edit_connection(12, 20, None)

Map[39].edit_connection(38, None, 999)

#PEMBE SARI VE YEŞİL ARABALARIN FARKLI ALGORİTMALAR KULLANARAK YOL BULMASI
car1 = Car(Map[START_NODE].position, pygame.math.Vector2(0, -1), "yesilaraba.png")
car2 = Car(Map[START_NODE].position, pygame.math.Vector2(0, -1), "sariaraba.png")
car3 = Car(Map[START_NODE].position, pygame.math.Vector2(0, -1), "pembearaba.png")
car1.path = a_star(Map, START_NODE, END_NODE)
car2.path = dijkstra(Map, START_NODE, END_NODE)[0]
car3.path = bfs(Map, START_NODE, END_NODE)
car1.active = False
car2.active = False
car3.active = False
car1.algorithm = "a_star"
car2.algorithm = "dijkstra"
car3.algorithm = "bfs"

print(dijkstra(Map, 43, END_NODE)[0])

print(f"     A* : {car1.path}")
print(f"Dijkstra: {car2.path}")
print(f"    BFS : {car3.path}")
print(f"    BFS : {car3.path}")

#NPC Araçların rotaları
npc1 = Car(Map[53].position, pygame.math.Vector2(0, 1), "griaraba.png", NPC)
npc1.path = [53,52,29,28,13,12,5,4,11,10,23,22,47,46,63,62,67,66]
npc2 = Car(Map[7].position, pygame.math.Vector2(0, 1), "griaraba.png", NPC)
npc2.path = [7,6,15,14,31,30,55,54,65,64,61,60,45,44,41,40,17,16,15,14,35,34,59,58,61,60,49,48,25,24,9,8]
# Her araca sensör ekle
cars = [car1,car2,car3,npc1,npc2]

pembe = (253, 62, 127)
sari = (253, 185, 62)
yesil = (62, 253, 109)
gri = (179, 179, 179)

araba_renkleri = [pembe, sari, yesil, gri]
yaya_renkleri = [(253, 201, 166), (255, 121, 109), (99, 185, 240), (38, 29, 43)]

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
    car.add_sensor(0, 150, yaya_renkleri)
    car.add_sensor(10, 150, yaya_renkleri)
    car.add_sensor(-10, 150, yaya_renkleri)
    car.add_sensor(25, 150, yaya_renkleri)
    car.add_sensor(-25, 150, yaya_renkleri)

    # Yaya Geçidi Sensörü
    car.add_sensor(0, 180, [(175, 175, 175)])

    # Trafik Işığı Sensörleri
    car.add_sensor(0, 100, [(255, 0, 0), (255, 255, 0), (0, 255, 0)])
    car.add_sensor(8, 80, [(185, 185, 185)])

    # Yol Çalışması Sensörü
    car.add_sensor(0, 200, [(255, 188, 66), (51, 101, 138)])  # (255,140,0),(200,140,0)

    # Taşlı yolda yavaşlama (169,169,169) (105, 105, 105)
    car.add_sensor(0, 100, [(105, 105, 105)])

# Bütün Fonksiyonları Çağırdığımız ve Ana Ekranı Oluşturduğumuz MAIN Fonksiyon

def main():
    global DRAW_SENSOR
    pygame.display.update()
    # TRAFİK IŞIĞI ZAMANLAYICISI
    clock = pygame.time.Clock()
    start_time = time.time()
    light_color = "yesil"  # Trafik ışığı başlangıcı

    # NPC'ler
    kedi = pygame.image.load("kedi.png")
    kedi_x = 1200
    kedi_y = 750
    kedi_speed = 1
    npc_kopekli_abla_sol = pygame.image.load("npc_kopekli_abla_sol.png")
    npc_kopekli_abla_sag = pygame.image.load("npc_kopekli_abla_sag.png")
    npc_adam_on = pygame.image.load("npc_adam_on.png")
    npc_adam_arka = pygame.image.load("npc_adam_arka.png")
    # Karakter başlangıç pozisyonu ve hız
    npc_kopekli_abla_x = 920
    npc_kopekli_abla_y = 300
    npc_kopekli_abla_speed = 0.5
    gidis_sol = True
    npc_adam_x = 550
    npc_adam_y = 0
    npc_adam_speed = 0.6
    gidis_asagi = True
    run = True
    up_arrow = False
    down_arrow = False
    left_arrow = False
    right_arrow = False
    hiz = 0
    donme = 0

    # Ana Ekranı Çalıştırma ve Kapatma
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # ARACIN YÖNÜ VE KLAVYE TUŞLARIYLA HAREKETİ
                    if event.key == pygame.K_RIGHT:
                        right_arrow = True
                    if event.key == pygame.K_LEFT:
                        left_arrow = True
                    if event.key == pygame.K_UP:
                        up_arrow = True
                    if event.key == pygame.K_DOWN:
                        down_arrow = True
                        #Space tuşuna basınca tüm araçların aynı anda çıkmasını istiyorsan alttaki satırı aktif yapabilirsin
                    '''if event.key ==pygame.K_SPACE: 
                        car1.active = True
                        car2.active = True
                        car3.active = True'''

                    if event.key ==pygame.K_1:
                        car1.active = True
                    if event.key ==pygame.K_2:
                        car2.active = True
                    if event.key ==pygame.K_3:
                        car3.active = True
                    if event.key == pygame.K_s:
                        if DRAW_SENSOR == False:
                            DRAW_SENSOR = True
                        else:
                            DRAW_SENSOR = False

            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        up_arrow = False
                    if event.key == pygame.K_DOWN:
                        down_arrow = False
                    if event.key == pygame.K_RIGHT:
                        right_arrow = False
                    if event.key == pygame.K_LEFT:
                        left_arrow = False

        if up_arrow + down_arrow == 1:
            hiz = (up_arrow * 2 - 1) * 10
        else:
            hiz = 0

        if left_arrow + right_arrow == 1:
            donme = (right_arrow * 2 - 1) * 10
        else:
            donme = 0



        # Arkaplan rengini uygula
        screen.fill(arkaplan)

        # Kazı Alanındaki Yer Resmini Ekrana Yazdır

        # --------------------------------------------------------------------------------------------------------------
        screen.blit(kazi_alani, (700, 470))
        screen.blit(kazi_alani, (700, 480))
        screen.blit(kazi_alani, (750, 480))
        screen.blit(kazi_alani, (800, 480))
        # Trafik Işığı Renk Döngüsü
        # 20 SANİYE YEŞİL, 3 SANİYE SARI, 10 SANİYE KIRMIZI, 3 SANİYE SARI, 20 SANİYE YEŞİL... OLACAK ŞEKİLDE...
        # 6 SANİYE YEŞİL, 2 SANİYE SARI, 4 SANİYE KIRMIZI, 2 SANİYE SARI, 20 SANİYE YEŞİL... OLACAK ŞEKİLDE...
        elapsed_time = (time.time() - start_time) % 14  # TOPLAM 36 SANİYE

        if elapsed_time < 6:
            light_color = "yesil"
        elif elapsed_time < 8:
            light_color = "sari"
        elif elapsed_time < 12:
            light_color = "kirmizi"
        '''
        car_x_red -= car_speed_red
        car_x_yellow += car_speed_yellow
        '''
        kedi_x += kedi_speed

        # NPCLER
        '''
        # NPC Arabalar ve Kedi
        if car_x_yellow > 1800:  # Sarı Araba Alttaki Yoldan Geçecek
            car_x_yellow = -100

        if car_x_red < -100:  # Kırmızı Araba Yukardaki Yoldan
            car_x_red = 1800
        if car_x_red > 1800:
            car_x_red = 1800
            '''
        if kedi_x > WIDTH:
            kedi_x = 200

            # Sağdaki Dikey Yolda Yaya Geçidinden Geçen Köpekli Kadın
        if gidis_sol:
            npc_kopekli_abla = npc_kopekli_abla_sol
            npc_kopekli_abla_x -= npc_kopekli_abla_speed
            if npc_kopekli_abla_x < 700:  # Sol sınır
                gidis_sol = False
                npc_kopekli_abla = npc_kopekli_abla_sag
        else:
            npc_kopekli_abla_x += npc_kopekli_abla_speed
            if npc_kopekli_abla_x > 1000:  # Sağ sınır
                gidis_sol = True
                npc_kopekli_abla = npc_kopekli_abla_sol

                # Üst Yatay Yolda Yaya Geçidinden Geçen Yalnız Yıkık Adam
        if gidis_asagi:
            npc_adam = npc_adam_on
            npc_adam_y += npc_adam_speed
            if npc_adam_y > 200:  # Aşağı sınır
                gidis_asagi = False
                npc_adam = npc_adam_arka
        else:
            npc_adam_y -= npc_adam_speed
            if npc_adam_y < -75:  # Yukarı sınır
                gidis_asagi = True
                npc_adam = npc_adam_on

                # KÜÇÜLTÜLMÜŞ KAMYONUN DETAYLI ÇİZİMİ

        def draw_truck(x, y):
            # Kamyon gövdesi (turuncu) - boyut küçültüldü
            pygame.draw.rect(screen, (255, 140, 0), (x - 90, y, 90, 35), border_radius=6)

            # Tuğla şekilli yük (daha detaylı, küçültülmüş)
            for i in range(3):  # Satır sayısı azaltıldı
                for j in range(2):  # İki satır tuğla
                    brick_color = (210, 105, 30) if (i + j) % 2 == 0 else (180, 90, 20)
                    pygame.draw.rect(screen, brick_color, (x - 85 + i * 10, y + 6 + j * 5, 10, 4))

                    # Saydam yük örtüsü - boyut küçültüldü
            overlay_surface = pygame.Surface((70, 18), pygame.SRCALPHA)  # Boyutları küçültüldü
            overlay_surface.fill((200, 200, 200, 100))
            screen.blit(overlay_surface, (x - 85, y + 6))

            # Kabin (sürücü bölümü) - boyut küçültüldü
            pygame.draw.rect(screen, (255, 140, 0), (x, y + 6, 18, 30), border_radius=6)
            pygame.draw.polygon(screen, (255, 140, 0), [(x, y + 6), (x + 18, y), (x + 18, y + 6)])

            # Kabin detayları (kapı ve screen) - boyut küçültüldü
            pygame.draw.rect(screen, white, (x + 4, y + 14, 8, 10))
            pygame.draw.rect(screen, white, (x + 6, y + 10, 6, 8))

            # Kapı kolu
            pygame.draw.circle(screen, silver, (x + 12, y + 18), 1.5)

            # Farlar - boyut küçültüldü ve yukarı konumlandırıldı
            pygame.draw.circle(screen, yellow, (x - 8, y + 3), 2.5)

            # Tekerlekler - boyut küçültüldü
            pygame.draw.circle(screen, (0, 0, 0), (x + 9, y + 38), 5)  # Ön tekerlek
            pygame.draw.circle(screen, (0, 0, 0), (x - 60, y + 37), 5)  # Arka sol tekerlek
            pygame.draw.circle(screen, (0, 0, 0), (x - 30, y + 37), 5)  # Arka sağ tekerlek

            # Jantlar - boyut küçültüldü
            pygame.draw.circle(screen, white, (x + 9, y + 38), 2)  # Ön tekerlek jant
            pygame.draw.circle(screen, white, (x - 60, y + 37), 2)  # Arka sol tekerlek jant
            pygame.draw.circle(screen, white, (x - 30, y + 37), 2)  # Arka sağ tekerlek jant

            # Arka kısım detayları - boyut küçültüldü
            pygame.draw.rect(screen, (200, 140, 0), (x - 90, y + 30, 90, 6))

            # Arka lambalar - boyut küçültüldü
            pygame.draw.circle(screen, red, (x - 85, y + 35), 1.5)  # Sol arka lamba
            pygame.draw.circle(screen, red, (x - 70, y + 35), 1.5)  # Sağ arka lamba

        # Kamyon konumu !!!KAMYONUN YER DEĞİŞİKLİĞİ İÇİN!!!
        truck_x = 1366
        truck_y = 262

        # Fonksiyonları Ekrana Yazdırma

        draw_alt_yatay_road()
        draw_horizontal_gravel_road_with_pattern()  # Yatay taşlı yolu çiziyoruz
        draw_sol_alt_yatay_road()
        draw_sol_dikey_road()
        draw_ust_yatay_road()
        draw_sag_dikey_road()
        draw_ortayol1_road()
        draw_orta_yatay1_road()
        draw_ortayol2_road()
        draw_orta_yatay2_road()
        draw_minikYol1()
        draw_minikYol2()
        draw_serit_cizgileri()

        pygame.draw.rect(screen, sensor_yayagecidi, (610, 75, 5, 80))  # adamın geçtiği yaya geçidi
        pygame.draw.rect(screen, sensor_yayagecidi, (540, 75, 5, 80))  # adamın geçtiği yaya geçidi
        pygame.draw.rect(screen, sensor_yayagecidi, (875, 380, 80, 5))  # kadının geçtiği yaya geçidi
        pygame.draw.rect(screen, sensor_yayagecidi, (875, 310, 80, 5))  # kadının geçtiği yaya geçidi
        pygame.draw.rect(screen, sensor_trafikisigi,(1400, 220, 80, 2))  # sağ dikey yoldaki yatay trafik ışığı çizgisi
        pygame.draw.rect(screen, sensor_trafikisigi,(150, 225, 80, 2))  # sol dikey yoldaki yatay trafik ışığı çizgisi
        draw_trafik_isigi(235, 160, light_color)  # sol üst kesişen yolda trafik ışığı
        draw_trafik_isigi(1487, 160, light_color)  # sağ dikey yol sonundaki trafik ışığı

        # Yaya Geçitlerini Ekle
        draw_yatay_yaya_gecidi()
        draw_dikey_yaya_gecidi()

        # NPC'leri Ekle
        screen.blit(npc_kopekli_abla, (npc_kopekli_abla_x, npc_kopekli_abla_y))
        screen.blit(npc_adam, (npc_adam_x, npc_adam_y))
        screen.blit(kedi, (kedi_x, kedi_y))

        # Tabelaları Konumlarına Göre Yerleştir
        screen.blit(yaya_gecidi_img, (620, 100))
        screen.blit(yaya_gecidi_img, (950, 360))
        screen.blit(dur_img, (760, 420))
        screen.blit(dur_img, (420, 390))
        screen.blit(yolengel, (665, 440))
        screen.blit(isci, (750, 450))
        screen.blit(agac, (750, 200))
        screen.blit(agac, (550, 200))
        screen.blit(agac, (1000, 450))
        screen.blit(agac, (1250, 450))
        screen.blit(agac, (30, 300))
        screen.blit(agac, (30, 400))
        screen.blit(agac, (280, 500))
        screen.blit(agac, (280, 350))
        screen.blit(agac, (280, 200))
        screen.blit(cop_kutusu, (1350, 700))
        screen.blit(vinc, (620, 370))
        screen.blit(cop_kutusu, (200, 40))
        screen.blit(bankta_oturan_adam, (630, 250))
        screen.blit(Veteriner, (1100, 400))
        # kamyonun çizimi
        draw_truck(truck_x, truck_y)
        # Ev ve işyeri çizimleri
        # Küçük ev ve garajı çiz, evin sol alt köşeye yerleştir
        draw_house(1330, HEIGHT - 60)  # Küçültülmüş ev koordinatları
        draw_garage(1415, HEIGHT - 45)  # Küçültülmüş garaj konumu

        # Küçük ofis binalarını hizaladım
        draw_large_building(20, 10)  # Küçük büyük işyeri
        draw_small_building(120, 10)  # Küçük küçük işyeri

        for car in cars:
            car.draw(screen)

        for car in cars:
            c_auto = car.auto()
            car.drive(c_auto[0], c_auto[1])

        screen.blit(tali_yol_img, (800, 615))
        screen.blit(tali_yol_img, (430, 615))#Araçlartabelalarınüzerinden geçiyor gibi görünmesin diye sonradan eklendi

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