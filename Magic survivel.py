from tkinter import *
import random
import math
import time


def but_e(event=None):
    def exit_but_e(event=None):
        root1.destroy()
        root.deiconify()

    root.withdraw()
    root1 = Toplevel()
    root1.geometry('1540x920+-10+0')
    canvas = Canvas(root1, height=920, width=1540)
    canvas.pack()
    canvas.create_rectangle(50, 100, 1500, 700, width=4)
    t = Button(root1, text='Выход в главное меню', font="Arial 32", command=exit_but_e)
    t.place(x=550, y=800)
    y = Label(root1, text='Правила игры', font="Arial 32")
    y.place(x=600, y=10)


def but_h(event=None):
    def exit_but_h(event=None):
        root1.destroy()
        root.deiconify()

    root.withdraw()
    root1 = Toplevel()
    root1.geometry('1540x920+-10+0')
    canvas = Canvas(root1, height=920, width=1540)
    canvas.pack()
    canvas.create_rectangle(5, 5, 1530, 75, width=3)
    t = Button(root1, text='Выход в главное меню', font="Arial 32", command=exit_but_h)
    t.place(x=550, y=800)
    y = Label(root1, text='№ Рекорда', font="Arial 20")
    y.place(x=10, y=20)
    canvas.create_rectangle(170, 5, 1530, 75, width=3)
    y = Label(root1, text='Имя игрока', font="Arial 20")
    y.place(x=400, y=20)
    canvas.create_rectangle(800, 5, 1530, 75, width=3)
    y = Label(root1, text='Рекорд', font="Arial 20")
    y.place(x=1100, y=20)
    p = 1
    for p in range(7):
        y1 = 100 + p * (50 + 50)
        canvas.create_rectangle(15, y1, 1510, y1 + 50, width=3)
        y = Label(root1, text=p + 1, font="Arial 20")
        y.place(x=75, y=y1 + 10)
        canvas.create_rectangle(170, y1, 1510, y1 + 50, width=3)
        canvas.create_rectangle(800, y1, 1510, y1 + 50, width=3)


class AutoShooter:
    def __init__(self, canvas, player_coords):
        self.canvas = canvas
        self.player_coords = player_coords
        self.damage = 10
        self.last_shot_time = 0
        self.shot_cooldown = 1
        self.bullets = []

    def find_nearest_enemy(self, enemies):
        if not enemies:
            return None

        player_x = (self.player_coords[0] + self.player_coords[2]) / 2
        player_y = (self.player_coords[1] + self.player_coords[3]) / 2

        nearest = None
        min_distance = float('inf')

        for enemy in enemies:
            enemy_coords = self.canvas.coords(enemy.id)
            if not enemy_coords:
                continue

            enemy_x = (enemy_coords[0] + enemy_coords[2]) / 2
            enemy_y = (enemy_coords[1] + enemy_coords[3]) / 2

            distance = math.sqrt((player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest = enemy

        return nearest

    def shoot_at_enemy(self, enemies, current_time):
        if current_time - self.last_shot_time < self.shot_cooldown:
            return

        enemy = self.find_nearest_enemy(enemies)
        if not enemy:
            return

        self.last_shot_time = current_time

        player_x = (self.player_coords[0] + self.player_coords[2]) / 2
        player_y = (self.player_coords[1] + self.player_coords[3]) / 2

        enemy_coords = self.canvas.coords(enemy.id)
        enemy_x = (enemy_coords[0] + enemy_coords[2]) / 2
        enemy_y = (enemy_coords[1] + enemy_coords[3]) / 2

        dx = enemy_x - player_x
        dy = enemy_y - player_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            return

        dx, dy = dx / distance, dy / distance

        bullet_size = 10
        bullet = self.canvas.create_oval(
            player_x - bullet_size / 2, player_y - bullet_size / 2,
            player_x + bullet_size / 2, player_y + bullet_size / 2,
            fill='blue', outline='black'
        )

        speed = 25
        self.bullets.append({
            'id': bullet,
            'dx': dx * speed,
            'dy': dy * speed,
            'damage': self.damage
        })

    def move_bullets(self, enemies):
        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in self.bullets[:]:
            self.canvas.move(bullet['id'], bullet['dx'], bullet['dy'])
            bullet_coords = self.canvas.coords(bullet['id'])

            if not bullet_coords or (bullet_coords[0] < 0 or bullet_coords[2] > self.canvas.winfo_width() or
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
                        enemies_to_remove.append(enemy)
                    bullets_to_remove.append(bullet)
                    break

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.canvas.delete(bullet['id'])
                self.bullets.remove(bullet)

        for enemy in enemies_to_remove:
            if enemy in enemies:
                self.canvas.delete(enemy.id)
                enemies.remove(enemy)


class Enemy:
    def __init__(self, canvas, screen_width, screen_height, size, player_coords):
        self.canvas = canvas
        self.size = size
        self.speed = 10
        self.player_coords = player_coords
        self.color = 'red'
        self.last_damage_time = 0
        self.damage_cooldown = 1
        self.hp = 10

        self.x, self.y = self.generate_position(screen_width, screen_height)
        self.id = canvas.create_rectangle(
            self.x, self.y,
            self.x + self.size, self.y + self.size,
            fill=self.color, outline=self.color
        )

    def take_damage(self, amount):
        self.hp -= amount
        return self.hp <= 0

    def generate_position(self, screen_width, screen_height):
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

    def move_towards_player(self, enemies, player_coords):
        self.repel_from_other_enemies(enemies)

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

        current_time = time.time()
        if (abs(player_x - current_x) < self.size and
                abs(player_y - current_y) < self.size and
                current_time - self.last_damage_time >= self.damage_cooldown):
            self.last_damage_time = current_time
            return 10

        return 0


def game(event=None):
    hp = 100
    root.withdraw()
    root2 = Toplevel()
    root2.attributes('-fullscreen', True)
    root2.configure(bg='white')
    root2.focus_force()

    screen_width = root2.winfo_screenwidth()
    screen_height = root2.winfo_screenheight()

    canvas = Canvas(root2, bg='white', highlightthickness=0)
    canvas.pack(fill='both', expand=True)


    size = 50
    player = canvas.create_rectangle(
        (screen_width - size) // 2,
        (screen_height - size) // 2,
        (screen_width + size) // 2,
        (screen_height + size) // 2,
        fill='blue', outline='blue'
    )

    enemies = []
    move_speed = 25
    last_spawn_time = time.time()
    spawn_interval = 0.5

    shooter = AutoShooter(canvas, canvas.coords(player))

    # UI elements
    time_rect = canvas.create_rectangle(screen_width // 2 - 100, 10, screen_width // 2 + 100, 50,
                                        outline="black", fill="white")
    hp_rect = canvas.create_rectangle(30, screen_height - 70, 330, screen_height - 30,
                                      outline="black", fill="white")
    game_start_time = time.time()
    time_text = canvas.create_text(screen_width // 2, 30, text="Время: 0:00", font="Arial 24", fill="black")
    hp_text = canvas.create_text(180, screen_height - 50, text=f"Здоровье: {hp}", font="Arial 24", fill="black")

    # Pause variables
    is_paused = False
    pause_menu_items = []
    game_loop_id = None

    def create_pause_menu():
        nonlocal pause_menu_items

        current_time = time.time() - game_start_time
        minutes = int(current_time) // 60
        seconds = int(current_time) % 60
        overlay = canvas.create_rectangle(
            0, 0, screen_width, screen_height,
            fill="black", stipple="gray25"
        )
        menu_frame = canvas.create_rectangle(
            screen_width // 2 - 210, screen_height // 2 - 300,
            screen_width // 2 + 210, screen_height // 2 + 300,
            fill="white", outline="black", width=3
        )
        pause_text = canvas.create_text(
            screen_width // 2, screen_height // 2 - 250,
            text="Игра на паузе", font="Arial 28", fill="black"
        )
        # Resume button
        resume_btn = Button(root2, text="Продолжить", font="Arial 26", width=15,command=resume_game)
        resume_btn.place(x=screen_width // 2 - 150, y=screen_height // 2 - 200)

        time_pause_rect=canvas.create_rectangle(
            screen_width // 2 -150, screen_height // 2 - 100,
            screen_width // 2 +155, screen_height // 2 -30,
            fill="white", outline="black", width=1)

        time_pause_text = canvas.create_text(
            screen_width // 2 , screen_height // 2 - 65,
            text=f"Время: {minutes}:{seconds:02d}", font="Arial 26", fill="black")

        score_pause_rect = canvas.create_rectangle(
            screen_width // 2 - 150, screen_height // 2 + 10 ,
            screen_width // 2 + 155, screen_height // 2 + 75,
            fill="white", outline="black", width=1)

        volume_btn = Button(root2, text="Выключить звук", font="Arial 26", width=15,)
        volume_btn.place(x=screen_width // 2 - 150, y=screen_height // 2 + 100)

        exit_btn = Button(
            root2, text="Выход в меню", font="Arial 26",width=15,
            command=lambda: [root2.destroy(), root.deiconify()]
        )
        exit_btn.place(x=screen_width // 2 - 150, y=screen_height // 2 + 200)

        # Save all pause menu items for later removal
        pause_menu_items = [overlay, menu_frame, pause_text,time_pause_text,time_pause_rect,score_pause_rect, resume_btn,volume_btn, exit_btn]

    def remove_pause_menu():
        nonlocal pause_menu_items
        for item in pause_menu_items:
            if isinstance(item, int):
                canvas.delete(item)
            else:
                item.place_forget()
        pause_menu_items = []

    def toggle_pause(event=None):
        nonlocal is_paused, game_loop_id
        if not is_paused:
            is_paused = True
            if game_loop_id:
                root2.after_cancel(game_loop_id)
            create_pause_menu()
        else:
            resume_game()

    def resume_game():
        nonlocal is_paused, game_loop_id
        if is_paused:
            is_paused = False
            remove_pause_menu()
            game_loop()

    def move_canvas(event):
        if is_paused:
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

        shooter.player_coords = canvas.coords(player)

        canvas.coords(time_text, screen_width // 2, 30)
        canvas.coords(time_rect, screen_width // 2 - 100, 10, screen_width // 2 + 100, 50)
        canvas.coords(hp_text, 180, screen_height - 50)
        canvas.coords(hp_rect, 30, screen_height - 70, 330, screen_height - 30)
        canvas.coords(screen_width - 180, screen_height - 50)

    for key in ['Down', 'Up', 'Left', 'Right']:
        root2.bind(f'<KeyPress-{key}>', move_canvas)

    root2.bind('<Escape>', toggle_pause)

    def spawn_enemy():
        nonlocal last_spawn_time
        current_time = time.time()
        if current_time - last_spawn_time >= spawn_interval and len(enemies) < 20:
            enemies.append(Enemy(
                canvas, screen_width, screen_height,
                size, canvas.coords(player)
            ))
            last_spawn_time = current_time

    def game_loop():
        nonlocal hp, game_loop_id

        if is_paused:
            return

        current_time = time.time() - game_start_time
        minutes = int(current_time) // 60
        seconds = int(current_time) % 60
        canvas.itemconfig(time_text, text=f"Время: {minutes}:{seconds:02d}")

        spawn_enemy()
        shooter.shoot_at_enemy(enemies, time.time())
        shooter.move_bullets(enemies)

        damage_taken = 0
        player_coords = canvas.coords(player)
        for enemy in enemies[:]:
            damage = enemy.move_towards_player(enemies, player_coords)
            damage_taken += damage

        if damage_taken > 0:
            hp = max(0, hp - damage_taken)
            canvas.itemconfig(hp_text, text=f"Здоровье: {hp}")

            if hp <= 0:
                canvas.create_text(screen_width // 2, screen_height // 2,
                                   text="Игра окончена!", font="Arial 36", fill="red")

                Button(root2, text="В главное меню", font="Arial 24",
                       command=lambda: [root2.destroy(), root.deiconify()]).place(
                    x=screen_width // 2 - 100, y=screen_height // 2 + 100)
                return

        game_loop_id = root2.after(30, game_loop)

    game_loop()


def g_menu():
    global root
    root = Tk()
    root.attributes('-fullscreen', True)

    Label(text='Magic Survival', font="Arial 36").place(x=630, y=150)
    Button(text='Начать игру ', font="Arial 36", width=15, command=game).place(x=570, y=250)
    Button(text='Правила игры', font="Arial 36", width=15, command=but_e).place(x=570, y=350)
    Button(text='Рекорды', font="Arial 36", width=15, command=but_h).place(x=570, y=450)
    Button(text='Выход из игры', font="Arial 36", width=15, command=root.destroy).place(x=570, y=550)

    root.mainloop()


g_menu()