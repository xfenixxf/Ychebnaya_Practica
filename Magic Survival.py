from tkinter import *
from PIL import Image, ImageTk
from playsound import playsound
from threading import Thread
import sounddevice as sd
import soundfile as sf
import numpy as np
import random
import math
import time
import json
import sys
import os

def resource_path(relative_path):
    """ Получает абсолютный путь для ресурсов в EXE и при разработке """
    try:
        base_path = sys._MEIPASS  # Для собранного EXE
    except AttributeError:
        base_path = os.path.abspath(".")  # Для запуска из исходного кода

    path = os.path.join(base_path, relative_path)

    return path

def load_audiofile(file_path):
    global audio_data, sample_rate
    data, fs = sf.read(file_path, dtype='float32')
    if len(data.shape) == 1:
        data = np.column_stack((data, data))
    audio_data = data
    sample_rate = fs
    return data, fs

# Функция для воспроизведения в отдельном потоке
def _play_loop():
    global sound_fl
    sd.play(audio_data, sample_rate, loop=True)
    while sound_fl:
        sd.sleep(100)

# Воспроизведение фоновой музыки
def play_audio(file_path=None):
    global sound_fl
    if file_path:
        load_audiofile(file_path)

    if audio_data is not None:
        sound_fl = True
        Thread(target=_play_loop, daemon=True).start()

# Остановка воспроизведения фоновой музыки
def stop_audio():
    global sound_fl
    sound_fl = False
    sd.stop()

# Переключение состояния воспроизведения
def toggle_music():
    if sound_fl:
        stop_audio()
    else:
        play_audio()

# Инициализация плеера
music_path = resource_path(os.path.join("Sound", "music.mp3"))

def klik_sound():
    if sound_fl == True:
        klikk = resource_path(os.path.join("Sound", "klik.mp3"))
        Thread(target=lambda: playsound(klikk), daemon=True).start()


def but_e(event=None):  # окно правил игры
    def exit_but_e(event=None):
        root1.destroy()
        root.deiconify()

    root.withdraw()
    root1 = Toplevel()
    root1.attributes('-fullscreen', True)
    canvas = Canvas(root1, height=920, width=1540)
    canvas.pack()
    canvas.create_rectangle(50, 100, 1500, 780, width=4)
    t = Button(root1, text='Выход в главное меню', font="Arial 32", command=lambda: (klik_sound(), exit_but_e()))
    t.place(x=550, y=800)
    y = Label(root1, text='Правила игры', font="Arial 32")
    y.place(x=600, y=10)
    rules_text = """Игрок начинает с 100 единицами здоровья и должен продержаться 5 минут. Поражение наступает при достижении 0 HP. Игрок может перемещаться при помощи стрелок на клавиатуре.

    С первой секунды появляются обычные противники (10 HP, 5 урона), а с 2:30 добавляются элитные (30 HP, 10 урона). Игрок автоматически отбивается при помощи различных способностей.

    На старте доступна только основная атака: уровень 1 - 5 урона (перезарядка 1 сек), уровень 2 - 10 урона (0.75 сек), уровень 3 - 15 урона (0.75 сек). При повышении уровня можно получить новые способности: молния: уровень 1 - 15 урона по 2 противникам (перезарядка 3 сек), уровень 2 - 15 урона по 4 противникам (3 сек), уровень 3 - 30 урона по 4 противникам (3 сек) или взрывной снаряд: уровень 1 - 15 урона в области 125 пикселей (перезарядка 3 сек), уровень 2 - 15 урона в области 175 пикселей (3 сек), уровень 3 - 30 урона в области 175 пикселей (3 сек).

    За обычных противников даётся 1 опыт, за элитных - 3. Максимальный уровень - 7, для каждого нового уровня требуется на 50 опыта больше. При повышении уровня можно выбрать улучшение существующей способности или новую способность (если их меньше двух) в окне выбора способностей при помощи цифр "1" и "2" на клавиатуре.

    В игре игрок может вызвать окно паузы нажав на кнопку "esc" на клавиатуре и в этом окне можно включить или выключить музыку."""

    canvas.create_text(130, 130, text=rules_text, font=('Arial', 20), anchor='nw', width=1300)


def but_h(event=None):  # окно рекордов
    def exit_but_h(event=None):
        root1.destroy()
        root.deiconify()

    def load_records():
        # Загружает и возвращает массив рекордов
        default_records = [
            {"name": " ", "score": " "},
            {"name": " ", "score": " "},
            {"name": " ", "score": " "},
            {"name": " ", "score": " "},
            {"name": " ", "score": " "},
            {"name": " ", "score": " "},
            {"name": " ", "score": " "}
        ]
        record_file = resource_path(os.path.join("records.json"))
        with open(record_file, 'r') as f:  # Открываем файл
            records = json.load(f)

            records.sort(key=lambda x: x.get('score', 0), reverse=True)  # Сортируем по убыванию рекорда

            for i in range(7):
                if i < len(records):
                    default_records[i] = records[i]

            return default_records[:7]  # Всегда возвращаем 7 записей

    root.withdraw()
    root1 = Toplevel()
    root1.attributes('-fullscreen', True)
    canvas = Canvas(root1, height=920, width=1540)
    canvas.pack()

    canvas.create_rectangle(5, 5, 1530, 75, width=3)
    Label(root1, text='№ Рекорда', font="Arial 20").place(x=10, y=20)
    canvas.create_rectangle(170, 5, 1530, 75, width=3)
    Label(root1, text='Имя игрока', font="Arial 20").place(x=400, y=20)
    canvas.create_rectangle(800, 5, 1530, 75, width=3)
    Label(root1, text='Рекорд', font="Arial 20").place(x=1100, y=20)

    records = load_records()  # Загружаем массив рекордов

    for i, record in enumerate(records):
        y_pos = 100 + i * 100

        canvas.create_rectangle(15, y_pos, 1510, y_pos + 50, width=3)
        Label(root1, text=str(i + 1), font="Arial 20").place(x=75, y=y_pos + 10)
        canvas.create_rectangle(170, y_pos, 1510, y_pos + 50, width=3)
        canvas.create_rectangle(800, y_pos, 1510, y_pos + 50, width=3)

        name = record.get('name', '---')
        score = record.get('score', 0)
        Label(root1, text=name, font="Arial 20").place(x=200, y=y_pos + 10)
        Label(root1, text=str(score), font="Arial 20").place(x=1100, y=y_pos + 10)
    Button(root1, text='Выход в главное меню', font="Arial 32", command=lambda: (klik_sound(), exit_but_h())).place(x=550, y=800)


class Ability:
    def __init__(self, canvas, cooldown, damage, level=0, have=False):
        self.canvas = canvas
        self.cooldown = cooldown
        self.last_use_time = 0
        self.damage = damage
        self.level = level
        self.have = have
        self.active_effects = []

    def update(self, enemies, current_time):
        """Основной метод обновления способности"""
        if not self.have or current_time - self.last_use_time < self.cooldown:
            return 0, 0

        self.cleanup_effects(current_time)
        return self.activate(enemies, current_time)

    def activate(self, enemies, current_time):
        """Активация способности """
        return 0, 0

    def cleanup_effects(self, current_time):
        """Очистка устаревших эффектов """
        pass

    def upgrade(self):
        """Улучшение способности"""
        self.level += 1

    def can_activate(self, current_time):
        """Проверка, можно ли активировать способность"""
        return self.have and current_time - self.last_use_time >= self.cooldown

    def find_closest_enemy(self, enemies, reference_coords):
        """Поиск ближайшего врага"""
        if not enemies or not reference_coords:
            return None

        px, py = (reference_coords[0] + reference_coords[2]) / 2, (reference_coords[1] + reference_coords[3]) / 2
        closest = None
        min_dist = float('inf')

        for enemy in enemies:
            enemy_coords = self.canvas.coords(enemy.id)
            if enemy_coords:
                ex, ey = (enemy_coords[0] + enemy_coords[2]) / 2, (enemy_coords[1] + enemy_coords[3]) / 2
                dist = math.sqrt((px - ex) ** 2 + (py - ey) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    closest = enemy
        return closest

    @staticmethod
    def check_collision(obj1_coords, obj2_coords):
        """Проверка столкновения двух объектов"""
        return (obj1_coords[2] > obj2_coords[0] and
                obj1_coords[0] < obj2_coords[2] and
                obj1_coords[3] > obj2_coords[1] and
                obj1_coords[1] < obj2_coords[3])


class LightningAbility(Ability):
    def __init__(self, canvas):
        super().__init__(canvas, cooldown=2.5, damage=15)
        self.max_targets = 2
        self.start_height = 200
        self.bolt_duration = 0.3
        self.damage_delay = 0.15
        self.segment_count = 3
        self.have = False

    def activate(self, enemies, current_time):
        xp_gained, enemies_killed = 0, 0
        if enemies:
            targets = random.sample(enemies, min(self.max_targets, len(enemies)))
            for target in targets:
                if target in enemies:
                    bolt_id = self.create_bolt(target)
                    if bolt_id:
                        damage_dealt = target.take_damage(self.damage)
                        if damage_dealt or target.hp <= 0:
                            enemies_killed += 1
                            xp_gained += target.xp_value
                            self.canvas.delete(target.id)
                            enemies.remove(target)

                        self.active_effects.append({
                            'id': bolt_id,
                            'time': current_time,
                            'target': target
                        })
            self.last_use_time = current_time
        return xp_gained, enemies_killed

    def cleanup_effects(self, current_time):
        for bolt in self.active_effects[:]:
            if current_time - bolt['time'] > self.bolt_duration:
                self.canvas.delete(bolt['id'])
                self.active_effects.remove(bolt)

    def create_bolt(self, target):
        enemy_coords = self.canvas.coords(target.id)
        if not enemy_coords:
            return None

        enemy_x = (enemy_coords[0] + enemy_coords[2]) / 2
        enemy_y = enemy_coords[1]

        points = [
            enemy_x, enemy_y - self.start_height,
                     enemy_x + random.randint(-25, 25), enemy_y - self.start_height / 2,
                     enemy_x + random.randint(-15, 15), enemy_y - self.start_height / 4,
            enemy_x, enemy_y
        ]

        if sound_fl == True:
            slighting = resource_path(os.path.join("Sound", "lighting.mp3"))
            Thread(target=lambda: playsound(slighting), daemon=True).start()
        return self.canvas.create_line(points, fill='#00BFFF', width=2)
        pass

    def upgrade(self):

        if self.level == 0:
            self.have = True
            self.damage = 15
            self.max_targets = 2
        elif self.level == 1:
            self.damage += 15
            self.max_targets = 4
        elif self.level == 2:
            self.damage += 30

        super().upgrade()


class ExplosiveShotAbility(Ability):
    def __init__(self, canvas):
        super().__init__(canvas, cooldown=3, damage=0, have=False)
        self.explosion_radius = 0
        self.bullet_speed = 12
        self.bullets = []
        self.explosions = []

    def activate(self, enemies, current_time):
        player_coords = self.canvas.coords("player")
        if not player_coords:
            return 0, 0

        target = self.find_closest_enemy(enemies, player_coords)
        if not target:
            return 0, 0

        self.create_bullet(player_coords, target, current_time)
        self.last_use_time = current_time
        return 0, 0

    def create_bullet(self, player_coords, target, current_time):
        px, py = (player_coords[0] + player_coords[2]) / 2, (player_coords[1] + player_coords[3]) / 2
        enemy_coords = self.canvas.coords(target.id)
        ex, ey = (enemy_coords[0] + enemy_coords[2]) / 2, (enemy_coords[1] + enemy_coords[3]) / 2

        dx, dy = ex - px, ey - py
        dist = math.sqrt(dx ** 2 + dy ** 2)
        dx, dy = dx / dist * self.bullet_speed, dy / dist * self.bullet_speed

        bullet = self.canvas.create_oval(px - 8, py - 8, px + 8, py + 8, fill='orange', outline='darkorange', width=2)
        if sound_fl:
            shhot2 = resource_path(os.path.join("Sound", "shoot2.mp3"))
            Thread(target=lambda: playsound(shhot2), daemon=True).start()
        self.bullets.append({
            'id': bullet,
            'x': px,
            'y': py,
            'dx': dx,
            'dy': dy,
            'time': current_time
        })

    def move_bullets(self, enemies):
        xp_gained = 0
        enemies_killed = 0
        bullets_to_remove = []

        for bullet in self.bullets[:]:
            self.canvas.move(bullet['id'], bullet['dx'], bullet['dy'])
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']

            bullet_coords = self.canvas.coords(bullet['id'])
            hit_occurred = False

            for enemy in enemies[:]:
                enemy_coords = self.canvas.coords(enemy.id)
                if not enemy_coords:
                    continue

                if self.check_collision(bullet_coords, enemy_coords):
                    hit_occurred = True
                    break

            if hit_occurred:
                exp_x, exp_y = (enemy_coords[0] + enemy_coords[2]) / 2, (enemy_coords[1] + enemy_coords[3]) / 2
                explosion_id = self.canvas.create_oval(
                    exp_x - self.explosion_radius, exp_y - self.explosion_radius,
                    exp_x + self.explosion_radius, exp_y + self.explosion_radius,
                    fill='', outline='yellow', width=3
                )
                self.explosions.append({
                    'id': explosion_id,
                    'x': exp_x,
                    'y': exp_y,
                    'time': time.time()
                })

                for enemy in enemies[:]:
                    enemy_coords = self.canvas.coords(enemy.id)
                    if enemy_coords:
                        ex, ey = (enemy_coords[0] + enemy_coords[2]) / 2, (enemy_coords[1] + enemy_coords[3]) / 2
                        dist = math.sqrt((exp_x - ex) ** 2 + (exp_y - ey) ** 2)

                        if dist < self.explosion_radius:
                            if enemy.take_damage(self.damage):
                                xp_gained += enemy.xp_value
                                enemies_killed += 1
                                self.canvas.delete(enemy.id)
                                enemies.remove(enemy)

                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            self.canvas.delete(bullet['id'])
            self.bullets.remove(bullet)

        return xp_gained, enemies_killed

    def cleanup_effects(self, current_time):
        for explosion in self.explosions[:]:
            if current_time - explosion['time'] > 0.3:
                self.canvas.delete(explosion['id'])
                self.explosions.remove(explosion)

    def upgrade(self):
        super().upgrade()
        if self.level == 1:
            self.damage = 15
            self.explosion_radius = 125
            self.have = True
        elif self.level == 2:
            self.damage += 15
            self.explosion_radius += 50
        elif self.level == 3:
            self.damage += 30


class AutoShooter(Ability):
    def __init__(self, canvas):
        super().__init__(canvas, cooldown=1, damage=5, level=1, have=True)
        self.bullets = []

    def activate(self, enemies, current_time):
        player_coords = self.canvas.coords("player")
        if not player_coords:
            return 0, 0

        closest = self.find_closest_enemy(enemies, player_coords)
        if not closest:
            return 0, 0

        enemy_coords = self.canvas.coords(closest.id)
        px, py = (player_coords[0] + player_coords[2]) / 2, (player_coords[1] + player_coords[3]) / 2
        ex, ey = (enemy_coords[0] + enemy_coords[2]) / 2, (enemy_coords[1] + enemy_coords[3]) / 2
        dx, dy = ex - px, ey - py
        dist = math.sqrt(dx ** 2 + dy ** 2)
        dx, dy = dx / dist * 15, dy / dist * 15

        bullet = self.canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill='blue')
        if sound_fl:
            shhot = resource_path(os.path.join("Sound", "shoot.mp3"))
            Thread(target=lambda: playsound(shhot), daemon=True).start()
        self.bullets.append({
            'id': bullet,
            'dx': dx,
            'dy': dy,
            'damage': self.damage
        })

        self.last_use_time = current_time
        return 0, 0

    def move_bullets(self, enemies):
        xp_gained = 0
        enemies_killed = 0
        bullets_to_remove = []

        for bullet in self.bullets[:]:
            self.canvas.move(bullet['id'], bullet['dx'], bullet['dy'])
            bullet_coords = self.canvas.coords(bullet['id'])

            if (not bullet_coords or bullet_coords[0] < 0 or bullet_coords[2] > self.canvas.winfo_width() or
                    bullet_coords[1] < 0 or bullet_coords[3] > self.canvas.winfo_height()):
                bullets_to_remove.append(bullet)
                continue

            for enemy in enemies[:]:
                enemy_coords = self.canvas.coords(enemy.id)
                if not enemy_coords:
                    continue

                if (bullet_coords[2] > enemy_coords[0] and bullet_coords[0] < enemy_coords[2] and
                        bullet_coords[3] > enemy_coords[1] and bullet_coords[1] < enemy_coords[3]):
                    if enemy.take_damage(bullet['damage']):
                        xp_gained += enemy.xp_value
                        enemies_killed += 1
                        self.canvas.delete(enemy.id)
                        enemies.remove(enemy)
                    bullets_to_remove.append(bullet)
                    break

        for bullet in bullets_to_remove:
            self.canvas.delete(bullet['id'])
            if bullet in self.bullets:
                self.bullets.remove(bullet)

        return xp_gained, enemies_killed

    def upgrade(self):
        super().upgrade()
        if self.level == 2:
            self.damage = 10
            self.cooldown = 0.75
        elif self.level == 3:
            self.damage += 15


class Enemy:
    def __init__(self, canvas, screen_width, screen_height, size, player_coords):
        self.canvas = canvas
        self.size = size
        self.have = True
        self.player_coords = player_coords
        self.last_damage_time = 0
        self.damage_cooldown = 1

        self.init_enemy_characteristics()

        self.texture = Image.open(self.texture_enemy)
        self.texture = self.texture.resize((50, 50), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(self.texture)

        self.x, self.y = self.generate_position(screen_width, screen_height)
        self.id = canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size)
        self.image_obj = canvas.create_image(self.x + self.size // 2, self.y + self.size // 2, image=self.img)

    def init_enemy_characteristics(self):
        raise

    @staticmethod
    def create_enemy(enemy_type, canvas, screen_width, screen_height, size, player_coords):
        if enemy_type == "elite":
            return EliteEnemy(canvas, screen_width, screen_height, size, player_coords)
        else:
            return NormalEnemy(canvas, screen_width, screen_height, size, player_coords)

    def take_damage(self, amount):
        """Обработка получения урона"""
        self.hp -= amount
        return self.hp <= 0

    def generate_position(self, screen_width, screen_height):
        """Генерация начальной позиции врага"""
        while True:
            center_x = screen_width // 2
            center_y = screen_height // 2
            exclusion_radius = 300

            x = random.randint(0, screen_width - self.size)
            y = random.randint(0, screen_height - self.size)

            if not (center_x - exclusion_radius < x < center_x + exclusion_radius - self.size and
                    center_y - exclusion_radius < y < center_y + exclusion_radius - self.size):
                return x, y

    def repel_from_other_enemies(self, enemies):
        """Отталкивание от других врагов"""
        coords = self.canvas.coords(self.id)
        if not coords:
            return

        my_x = (coords[0] + coords[2]) / 2
        my_y = (coords[1] + coords[3]) / 2

        min_distance = self.size * 1.5
        correction_factor = 0.2

        player_coords = self.player_coords
        if not player_coords:
            return

        player_x = (player_coords[0] + player_coords[2]) / 2
        player_y = (player_coords[1] + player_coords[3]) / 2

        distance_to_player = math.sqrt((player_x - my_x) ** 2 + (player_y - my_y) ** 2)
        max_distance_from_player = 1500

        if distance_to_player > max_distance_from_player:
            self.canvas.delete(self.id)
            self.canvas.delete(self.image_obj)
            if self in enemies:
                enemies.remove(self)
            return

        for enemy in enemies[:]:
            if enemy.id == self.id:
                continue

            other_coords = self.canvas.coords(enemy.id)
            if not other_coords:
                continue

            other_x = (other_coords[0] + other_coords[2]) / 2
            other_y = (other_coords[1] + other_coords[3]) / 2

            dx = other_x - my_x
            dy = other_y - my_y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance < min_distance and distance > 0:
                overlap = min_distance - distance
                correction_x = (dx / distance) * overlap * correction_factor
                correction_y = (dy / distance) * overlap * correction_factor

                self.canvas.move(self.id, -correction_x, -correction_y)
                self.canvas.move(self.image_obj, -correction_x, -correction_y)

    def move_towards_player(self, enemies, player_coords):
        """Движение к игроку"""
        self.repel_from_other_enemies(enemies)
        self.player_coords = player_coords

        coords = self.canvas.coords(self.id)
        if not coords:
            return 0

        current_x = (coords[0] + coords[2]) / 2
        current_y = (coords[1] + coords[3]) / 2

        player_x = (player_coords[0] + player_coords[2]) / 2
        player_y = (player_coords[1] + player_coords[3]) / 2

        dx = player_x - current_x
        dy = player_y - current_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            dx, dy = dx / distance * self.speed, dy / distance * self.speed
            self.canvas.move(self.id, dx, dy)
            self.canvas.move(self.image_obj, dx, dy)

        current_time = time.time()
        if (abs(player_x - current_x) < self.size and
                abs(player_y - current_y) < self.size and
                current_time - self.last_damage_time >= self.damage_cooldown):
            self.last_damage_time = current_time
            return self.damage

        return 0


class NormalEnemy(Enemy):
    def init_enemy_characteristics(self):
        self.speed = 10
        self.hp = 10
        self.xp_value = 1
        self.damage = 5
        self.type = "normal"
        self.texture_enemy =resource_path(os.path.join("Textures", "Enemy1.jpg"))


class EliteEnemy(Enemy):
    def init_enemy_characteristics(self):
        self.speed = 15
        self.hp = 30
        self.xp_value = 3
        self.damage = 10
        self.texture_enemy = resource_path(os.path.join("Textures", "Enemy2.jpg"))


def restart_game():
    root2.destroy()
    game()


def record_menu(enemies_killed, restart_callback=None, exit_callback=None):  # окно записи рекорда
    def validate_name(new_text):
        return len(new_text) <= 15

    def save_record():
        player_name = name_entry.get().strip()
        record_file = resource_path(os.path.join("records.json"))
        if player_name:
            with open(record_file, 'r') as f:
                records = json.load(f)

            records.append({
                'name': player_name[:15],
                'score': enemies_killed
            })

            with open(record_file, 'w') as f:
                json.dump(records, f, indent=4)

            root77.destroy()
            if restart_callback:
                restart_callback()
            elif exit_callback:
                exit_callback()

    root77 = Toplevel(root2)
    root77.overrideredirect(True)
    root77.protocol("WM_DELETE_WINDOW", lambda: None)
    klik_sound()
    root2.update_idletasks()
    parent_x = root2.winfo_x()
    parent_y = root2.winfo_y()
    parent_width = root2.winfo_width()
    parent_height = root2.winfo_height()
    x = parent_x + (parent_width - 500) // 2
    y = parent_y + (parent_height - 300) // 2
    root77.geometry(f"500x300+{x}+{y}")

    main_frame = Frame(root77, bg='white', bd=2, relief='solid')
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    Label(main_frame, text="Введите имя для записи рекорда", font=("Arial", 20), bg='white').pack(pady=(20, 5))

    vcmd = (root77.register(validate_name), '%P')
    name_entry = Entry(main_frame, font=("Arial", 20), width=20, validate="key", validatecommand=vcmd)
    name_entry.pack(pady=20, ipady=5)

    btn_frame = Frame(main_frame, bg='white')
    btn_frame.pack(pady=10)

    Button(btn_frame, text="Подтвердить", font=("Arial", 18), command=lambda: (klik_sound(), save_record())).pack(
        side='left', padx=20)

    root77.grab_set()
    root77.focus_set()
    name_entry.focus()


def game(event=None):
    hp = 100
    enemies_killed = 0
    xp = 0
    xp_to_level = 50
    level = 1
    pause_start_time = 0
    total_paused_time = 0
    upgrade_time = 0
    game_over = False
    root.withdraw()
    global root2
    root2 = Toplevel()
    root2.attributes('-fullscreen', True)
    root2.configure(bg='white')
    root2.protocol("WM_DELETE_WINDOW", lambda: None)
    root2.focus_force()
    enemies = []
    move_speed = 25
    last_spawn_time = time.time()
    spawn_interval = 1
    screen_width = root2.winfo_screenwidth()
    screen_height = root2.winfo_screenheight()
    elite_spawn_time = 180
    elite_spawn_chance = 0.4
    max_enemes = 20
    playyr=resource_path(os.path.join("Textures", "player.jpg"))
    playerq = Image.open(playyr)
    playerq = playerq.resize((50, 50), Image.LANCZOS)
    player_img = ImageTk.PhotoImage(playerq)

    global canvas
    canvas = Canvas(root2, bg='white', highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    size = 50

    player = canvas.create_rectangle(
        (screen_width - size) // 2,
        (screen_height - size) // 2,
        (screen_width + size) // 2,
        (screen_height + size) // 2,
        fill='', outline='black', tags="player")

    player_sprite = canvas.create_image(
        screen_width // 2,
        screen_height // 2,
        image=player_img,
        tags="player_sprite")

    canvas.player_img = player_img
    canvas.player = player

    shooter = AutoShooter(canvas)
    lightning = LightningAbility(canvas)
    explosive_shot = ExplosiveShotAbility(canvas)

    # Элементы игры здоровье,рамки и тд
    level_rect = canvas.create_rectangle(screen_width // 2, 10, screen_width // 2 + 400, 50, outline="black",
                                         fill="white")
    level_text = canvas.create_text(screen_width // 2 + 200, 30, text=f"Уровень: {level} ({xp}/{xp_to_level} XP)",
                                    font="Arial 24", fill="black")
    time_rect = canvas.create_rectangle(screen_width // 2 - 300, 10, screen_width // 2 - 100, 50, outline="black",
                                        fill="white")
    hp_rect = canvas.create_rectangle(30, screen_height - 70, 330, screen_height - 30, outline="black", fill="white")

    time_text = canvas.create_text(screen_width // 2 - 200, 30, text="Время: 0:00", font="Arial 24", fill="black")
    hp_text = canvas.create_text(180, screen_height - 50, text=f"Здоровье: {hp}", font="Arial 24", fill="black")

    game_start_time = time.time()
    is_paused = False
    pause_menu_items = []
    game_loop_id = None

    def show_upgrade_choices():
        nonlocal is_paused, pause_menu_items, upgrade_time, pause_start_time
        pause_start_time = time.time()
        upgrade_time += time.time() - pause_start_time
        is_paused = True
        root2.unbind('<Escape>')

        overlay = canvas.create_rectangle(
            0, 0, screen_width, screen_height,
            fill="black", stipple="gray12"
        )

        menu_frame = canvas.create_rectangle(
            screen_width // 2 - 300, screen_height // 2 - 200,
            screen_width // 2 + 300, screen_height // 2 + 200,
            fill="white", outline="black", width=3
        )

        title = canvas.create_text(
            screen_width // 2, screen_height // 2 - 175,
            text="Выберите улучшение:",
            font="Arial 26", fill="black"
        )

        # Доступные улучшения
        upgrades = []

        shooter_upgrade = None
        if shooter.level < 3:
            if shooter.level == 1:
                line1 = "Выстрел: Скорострельность: 1 -> 0.5"
                line2 = "Урон: 5 -> 10 (Ур. 2/3)"
                shooter_upgrade = (line1, line2, lambda: shooter.upgrade())
            else:
                shooter_upgrade = ("Выстрел: Урон 10 -> 15 (Ур. 3/3)", lambda: shooter.upgrade())

        if not lightning.have and not explosive_shot.have:  # Первый выбор - случайная способность
            if random.randint(1, 2) == 1:
                if shooter_upgrade:
                    upgrades.append(shooter_upgrade)
                upgrades.append(("Разблокировать Молнию", lambda: lightning.upgrade()) if random.choice([True, False])
                                else ("Разблокировать Взрывной выстрел", lambda: explosive_shot.upgrade()))
            else:
                upgrades.append(("Разблокировать Молнию", lambda: lightning.upgrade()) if random.choice([True, False])
                                else ("Разблокировать Взрывной выстрел", lambda: explosive_shot.upgrade()))
                if shooter_upgrade:
                    upgrades.append(shooter_upgrade)
        else:  # Улучшения для уже разблокированной способности
            special_upgrades = []
            if lightning.have and lightning.level < 3:
                special_upgrades.append((
                    f"Молния: {'число целей 2 -> 4' if lightning.level == 1 else 'урон 15 -> 30'} (Ур. {lightning.level + 1}/3)",
                    lambda: lightning.upgrade()))

            if explosive_shot.have and explosive_shot.level < 3:
                special_upgrades.append((
                    f"Взрыв: {'радиус 125 -> 175' if explosive_shot.level == 1 else 'урон 15 -> 30'} (Ур. {explosive_shot.level + 1}/3)",
                    lambda: explosive_shot.upgrade()))

            if random.randint(1, 2) == 1:
                if shooter_upgrade:
                    upgrades.append(shooter_upgrade)
                if special_upgrades:
                    upgrades.append(random.choice(special_upgrades))
            else:
                if special_upgrades:
                    upgrades.append(random.choice(special_upgrades))
                if shooter_upgrade:
                    upgrades.append(shooter_upgrade)

        if len(upgrades) > 2:
            upgrades = random.sample(upgrades, 2)

        option_rects = []
        option_texts = []
        for i, upgrade in enumerate(upgrades):
            y_pos = screen_height // 2 - 125 + i * 125
            rect = canvas.create_rectangle(
                screen_width // 2 - 250, y_pos,
                screen_width // 2 + 250, y_pos + 100,
                outline="black", width=1
            )
            option_rects.append(rect)

            txt_num = canvas.create_text(
                screen_width // 2 - 225, y_pos + 50,
                text=f"{i + 1}", font="Arial 16", fill="black"
            )
            option_texts.append(txt_num)

            if shooter.level == 1 and len(upgrade) == 3 and upgrade[0].startswith("Выстрел:"):
                line1, line2, _ = upgrade
                txt1 = canvas.create_text(
                    screen_width // 2, y_pos + 30,
                    text=line1, font="Arial 16", fill="black"
                )
                txt2 = canvas.create_text(
                    screen_width // 2, y_pos + 70,
                    text=line2, font="Arial 16", fill="black"
                )
                option_texts.extend([txt1, txt2])
            else:
                text, action = upgrade[:2]
                txt = canvas.create_text(
                    screen_width // 2, y_pos + 50,
                    text=text, font="Arial 16", fill="black"
                )
                option_texts.append(txt)

        hint_text = "Нажмите "
        hint_text += "1" if len(upgrades) >= 1 else ""
        hint_text += " или 2" if len(upgrades) >= 2 else ""
        hint_text += " для выбора"

        hint = canvas.create_text(
            screen_width // 2, screen_height // 2 + 170,
            text=hint_text,
            font="Arial 26", fill="black"
        )

        pause_menu_items = [overlay, menu_frame, title, hint] + option_rects + option_texts

        def handle_choice(event):
            nonlocal is_paused, upgrade_time
            if event.char == '1' and len(upgrades) >= 1:
                if len(upgrades[0]) == 3:
                    upgrades[0][2]()
                else:
                    upgrades[0][1]()
            elif event.char == '2' and len(upgrades) >= 2:
                if len(upgrades[1]) == 3:
                    upgrades[1][2]()
                else:
                    upgrades[1][1]()
            else:
                return

            remove_pause_menu()
            root2.unbind('<Key>')
            root2.bind('<Escape>', toggle_pause)
            resume_game()

        root2.bind('<Key>', handle_choice)

    def create_game_over_menu():  # меню окончания игры
        nonlocal game_over

        root2.unbind('<Escape>')
        game_over = True

        game_time = time.time() - game_start_time - total_paused_time
        minutes = int(game_time) // 60
        seconds = int(game_time) % 60

        overlay = canvas.create_rectangle(0, 0, screen_width, screen_height, fill="black", stipple="gray12")
        menu_frame = canvas.create_rectangle(screen_width // 2 - 250, screen_height // 2 - 300, screen_width // 2 + 250,
                                             screen_height // 2 + 275, fill="white", outline="black", width=3)
        if game_time < 300:
            game_over_text = canvas.create_text(screen_width // 2, screen_height // 2 - 225, text="Поражение",
                                                font="Arial 40", fill="red")
        else:
            game_over_text = canvas.create_text(screen_width // 2, screen_height // 2 - 225, text="Победа",
                                                font="Arial 40", fill="green")
        time_game_over_rect = canvas.create_rectangle(
            screen_width // 2 - 200, screen_height // 2 - 150, screen_width // 2 + 200, screen_height // 2 - 70,
            fill="white", outline="black", width=1)
        time_game_over_text = canvas.create_text(screen_width // 2, screen_height // 2 - 110,
                                                 text=f"Время: {minutes}:{seconds:02d}", font="Arial 26", fill="black")

        score_game_over_rect = canvas.create_rectangle(screen_width // 2 - 200, screen_height // 2 - 50,
                                                       screen_width // 2 + 200, screen_height // 2 + 30, fill="white",
                                                       outline="black", width=1)
        score_game_over_text = canvas.create_text(screen_width // 2, screen_height // 2 - 10,
                                                  text=f"Убито врагов: {enemies_killed}", font="Arial 26", fill="black")

        exit_btn = Button(root2, text="Выход в меню", font="Arial 26", width=20,
                          command=lambda: [
                              record_menu(enemies_killed, exit_callback=lambda: [root2.destroy(), root.deiconify()])])
        exit_btn.place(x=screen_width // 2 - 205, y=screen_height // 2 + 160)

        restart_btn = Button(root2, text="Начать заново", font="Arial 26", width=20,
                             command=lambda: record_menu(enemies_killed, restart_callback=restart_game))
        restart_btn.place(x=screen_width // 2 - 205, y=screen_height // 2 + 60)


    def check_game_over():
        nonlocal game_over

        game_time = time.time() - game_start_time - total_paused_time + upgrade_time
        if game_time >= 300 :
            create_game_over_menu()
            return True

        if hp <= 0 :
            create_game_over_menu()
            return True

        return False

    def create_pause_menu():  # меню паузы
        nonlocal pause_menu_items, enemies_killed, total_paused_time
        global sound_fl

        def volume():
            nonlocal volume_btn, pause_menu_items
            global sound_fl
            volume_btn.destroy()
            toggle_music()
            if sound_fl == True:
                volume_btn = Button(root2, text="Выключить звук", font="Arial 26", width=15,
                                    command=lambda: (klik_sound(), volume()))
            else:
                volume_btn = Button(root2, text="Включить звук", font="Arial 26", width=15,
                                    command=lambda: (klik_sound(), volume()))
            volume_btn.place(x=screen_width // 2 - 150, y=screen_height // 2 + 100)
            pause_menu_items = [overlay, menu_frame, pause_text, time_pause_text, time_pause_rect, score_pause_rect,
                                resume_btn, volume_btn, exit_btn, score_pause_text]

        game_time = time.time() - game_start_time - total_paused_time
        minutes = int(game_time) // 60
        seconds = int(game_time) % 60
        overlay = canvas.create_rectangle(0, 0, screen_width, screen_height, fill="black", stipple="gray25")
        menu_frame = canvas.create_rectangle(screen_width // 2 - 210, screen_height // 2 - 300, screen_width // 2 + 210,
                                             screen_height // 2 + 300, fill="white", outline="black", width=3)
        pause_text = canvas.create_text(screen_width // 2, screen_height // 2 - 250, text="Игра на паузе",
                                        font="Arial 28", fill="black")
        resume_btn = Button(root2, text="Продолжить", font="Arial 26", width=15,
                            command=lambda: (klik_sound(), resume_game()))
        resume_btn.place(x=screen_width // 2 - 150, y=screen_height // 2 - 200)
        time_pause_rect = canvas.create_rectangle(screen_width // 2 - 150, screen_height // 2 - 100,
                                                  screen_width // 2 + 155, screen_height // 2 - 30, fill="white",
                                                  outline="black", width=1)
        time_pause_text = canvas.create_text(screen_width // 2, screen_height // 2 - 65,
                                             text=f"Время: {minutes}:{seconds:02d}", font="Arial 26", fill="black")
        score_pause_rect = canvas.create_rectangle(screen_width // 2 - 150, screen_height // 2, screen_width // 2 + 155,
                                                   screen_height // 2 + 75, fill="white", outline="black", width=1)
        score_pause_text = canvas.create_text(screen_width // 2, screen_height // 2 + 40,
                                              text=f"Убито врагов: {enemies_killed}", font="Arial 26", fill="black")
        if sound_fl == True:
            volume_btn = Button(root2, text="Выключить звук", font="Arial 26", width=15,
                                command=lambda: (klik_sound(), volume()))
        else:
            volume_btn = Button(root2, text="Включить звук", font="Arial 26", width=15,
                                command=lambda: (klik_sound(), volume()))
        volume_btn.place(x=screen_width // 2 - 150, y=screen_height // 2 + 100)
        exit_btn = Button(root2, text="Выход в меню", font="Arial 26", width=15,
                          command=lambda: [klik_sound(), root2.destroy(), root.deiconify()])
        exit_btn.place(x=screen_width // 2 - 150, y=screen_height // 2 + 200)

        pause_menu_items = [overlay, menu_frame, pause_text, time_pause_text, time_pause_rect, score_pause_rect,
                            resume_btn, volume_btn, exit_btn, score_pause_text]

    def remove_pause_menu():  # удаление меню паузы
        nonlocal pause_menu_items
        for item in pause_menu_items:
            if isinstance(item, int):
                canvas.delete(item)
            else:
                item.place_forget()
        pause_menu_items = []

    def toggle_pause(event=None):  # проверка состояния игры
        nonlocal is_paused, game_loop_id, game_over, pause_start_time

        if game_over:
            return

        if not is_paused:
            is_paused = True
            pause_start_time = time.time()
            if game_loop_id:
                root2.after_cancel(game_loop_id)
            create_pause_menu()
        else:
            resume_game()

    def resume_game():  # Возобновление игры
        nonlocal is_paused, game_loop_id, pause_start_time, total_paused_time
        is_paused = False
        total_paused_time += time.time() - pause_start_time
        remove_pause_menu()
        game_loop()

    def move_canvas(event):  # функция движения холста
        if is_paused or game_over:
            return

        offset = {
            'Down': (0, -move_speed),
            'Up': (0, move_speed),
            'Right': (-move_speed, 0),
            'Left': (move_speed, 0)
        }.get(event.keysym, (0, 0))

        for item in canvas.find_all():
            if item != player:
                canvas.move(item, *offset)
        # статичные показатели
        canvas.coords(player_sprite, screen_width // 2, screen_height // 2)
        canvas.coords(time_text, screen_width // 2 - 200, 30)
        canvas.coords(time_rect, screen_width // 2 - 300, 10, screen_width // 2 - 100, 50)
        canvas.coords(hp_text, 180, screen_height - 50)
        canvas.coords(hp_rect, 30, screen_height - 70, 330, screen_height - 30)
        canvas.coords(screen_width - 180, screen_height - 50)
        canvas.coords(level_text, screen_width // 2 + 200, 30)
        canvas.coords(level_rect, screen_width // 2, 10, screen_width // 2 + 400, 50)

    for key in ['Down', 'Up', 'Left', 'Right']:
        root2.bind(f'<KeyPress-{key}>', move_canvas)

    root2.bind('<Escape>', toggle_pause)

    def spawn_enemy():
        nonlocal last_spawn_time, elite_spawn_chance
        current_time = time.time()
        if current_time - last_spawn_time >= spawn_interval and len(enemies) < max_enemes:
            game_time = current_time - game_start_time - total_paused_time + upgrade_time

            if game_time > elite_spawn_time and random.random() < elite_spawn_chance:
                enemies.append(
                    Enemy.create_enemy(
                        "elite",
                        canvas,
                        screen_width,
                        screen_height,
                        size,
                        canvas.coords(player)
                    )
                )
            else:
                enemies.append(
                    Enemy.create_enemy(
                        "normal",
                        canvas,
                        screen_width,
                        screen_height,
                        size,
                        canvas.coords(player)
                    )
                )
            last_spawn_time = current_time

    def game_loop():
        nonlocal hp, game_loop_id, enemies_killed, xp, xp_to_level, level, elite_spawn_chance, game_over, spawn_interval, total_paused_time, upgrade_time
        current_time = time.time()
        if total_paused_time > 0:
            game_time = current_time - game_start_time - total_paused_time + upgrade_time
        else:
            game_time = current_time - game_start_time
        minutes = int(game_time) // 60
        seconds = int(game_time) % 60
        canvas.itemconfig(time_text, text=f"Время: {minutes}:{seconds:02d}")

        if check_game_over():
            return

        if is_paused:
            return

        if game_time > 60:
            spawn_interval = 0.75
        elif game_time > 120:
            spawn_interval = 0.5
        elif game_time > 180:
            spawn_interval = 0.3
        elif game_time > 240:
            elite_spawn_chance = 0.5
        elif game_time > 240:
            elite_spawn_chance = 0.7

        spawn_enemy()

        shooter.update(enemies, current_time)
        bullet_xp, bullet_kills = shooter.move_bullets(enemies)

        lightning_xp, lightning_kills = lightning.update(enemies, current_time)
        explosive_shot.update(enemies, current_time)
        explosive_xp, explosive_kills = explosive_shot.move_bullets(enemies)

        enemies_killed += lightning_kills + explosive_kills + bullet_kills
        xp += lightning_xp + explosive_xp + bullet_xp
        if xp >= xp_to_level:
            level += 1
            xp_to_level += 50
            if level < 7:
                if game_loop_id:
                    root2.after_cancel(game_loop_id)
                    show_upgrade_choices()

        if level < 6:
            canvas.itemconfig(level_text, text=f"Уровень: {level} ({xp}/{xp_to_level} XP)")
        else:
            canvas.itemconfig(level_text, text=f"Уровень: MAX")

        damage_taken = 0
        player_coords = canvas.coords(player)
        for enemy in enemies[:]:
            damage = enemy.move_towards_player(enemies, player_coords)
            damage_taken += damage
        if damage_taken > 0:
            hp =  hp - damage_taken
            if sound_fl == True:
                damages = resource_path(os.path.join("Sound", "damage.mp3"))
                Thread(target=lambda: playsound(damages), daemon=True).start()
            canvas.itemconfig(hp_text, text=f"Здоровье: {hp}")
            if hp <= 0:
                check_game_over()
                return
        game_loop_id = root2.after(30, game_loop)

    game_loop()


def g_menu():
    global root
    root = Tk()
    root.attributes('-fullscreen', True)
    root.title("Magic Survival")
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    Label(text='Magic Survival', font="Arial 36").place(x=630, y=150)
    Button(text='Начать игру ', font="Arial 36", width=15, command=lambda: (klik_sound(), game())).place(x=570, y=250)
    Button(text='Правила игры', font="Arial 36", width=15, command=lambda: (klik_sound(), but_e())).place(x=570, y=350)
    Button(text='Рекорды', font="Arial 36", width=15, command=lambda: (klik_sound(), but_h())).place(x=570, y=450)
    Button(text='Выход из игры', font="Arial 36", width=15, command=lambda: (klik_sound(), root.destroy())).place(x=570,y=550)
    root.mainloop()

sound_fl = False
audio_data = None
sample_rate = None
play_audio(music_path)
g_menu()