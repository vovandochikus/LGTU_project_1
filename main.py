# Линейный конгруэнтный генератор для генерации псевдослучайных чисел
class LCG:
    def __init__(self, seed):
        self.modulus = 2**31 - 1
        self.multiplier = 48271
        self.increment = 0
        self.seed = seed

    def next(self):
        self.seed = (self.multiplier * self.seed + self.increment) % self.modulus
        return self.seed

# Определяем классы для игрока и NPC
class Character:
    def __init__(self, name, hp, mp, arm, dmg):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.arm = arm
        self.dmg = dmg

    def attack(self, target):
        damage_dealt = max(0, self.dmg - target.arm)
        target.hp -= damage_dealt
        return damage_dealt

class Player(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, mp=50, arm=5, dmg=10)

class Enemy(Character):
    def __init__(self):
        super().__init__("Enemy", hp=50, mp=0, arm=2, dmg=8)

# Функция для генерации карты
def generate_map(size):
    return [['.' for _ in range(size)] for _ in range(size)]

# Функция для отображения карты
def render_map(game_map, player_pos, enemy_pos):
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            if (x, y) == player_pos:
                print('P', end=' ')
            elif (x, y) == enemy_pos:
                print('E', end=' ')  # Отображение врага как 'E'
            else:
                print(game_map[y][x], end=' ')
        print()
    print()

# Функция для проверки коллизий
def check_collision(pos, game_map):
    x, y = pos
    if x < 0 or y < 0 or x >= len(game_map) or y >= len(game_map):
        return True
    return False

# Функция для перемещения врага к игроку
def move_enemy_towards_player(enemy_pos, player_pos):
    enemy_x, enemy_y = enemy_pos
    player_x, player_y = player_pos

    if enemy_x < player_x:
        enemy_x += 1
    elif enemy_x > player_x:
        enemy_x -= 1

    if enemy_y < player_y:
        enemy_y += 1
    elif enemy_y > player_y:
        enemy_y -= 1

    return (enemy_x, enemy_y)

# Основная игра
def main():
    print("Выберите тип карты: 1 - стандартная (5x5), 2 - генерация (введите размер)")
    choice = input("Ваш выбор: ")
    
    if choice == '1':
        game_map = generate_map(5)
    elif choice == '2':
        size = int(input("Введите размер карты (например, 5 для 5x5): "))
        if size <= 0:
            print("Размер карты должен быть положительным числом.")
            return
        game_map = generate_map(size)
    else:
        print("Неверный выбор.")
        return

    player = Player(name="Hero")
    enemy = Enemy()

    # Инициализация генератора случайных чисел с произвольным значением
    lcg = LCG(seed=12345)
    
    # Генерация позиции врага с помощью LCG
    enemy_pos = (lcg.next() % len(game_map), lcg.next() % len(game_map))

    player_pos = (0, 0)

    while player.hp > 0 and enemy.hp > 0:
        render_map(game_map, player_pos, enemy_pos)
        print(f"{player.name} HP: {player.hp}, MP: {player.mp}")
        print(f"{enemy.name} HP: {enemy.hp}")

        action = input("Выберите действие: (w/a/s/d для перемещения, f для атаки): ").lower()

        if action == 'w':
            new_pos = (player_pos[0], player_pos[1] - 1)
        elif action == 's':
            new_pos = (player_pos[0], player_pos[1] + 1)
        elif action == 'a':
            new_pos = (player_pos[0] - 1, player_pos[1])
        elif action == 'd':
            new_pos = (player_pos[0] + 1, player_pos[1])
        elif action == 'f':
            if player_pos == enemy_pos:
                damage = player.attack(enemy)
                print(f"{player.name} атакует {enemy.name} и наносит {damage} урона.")
                continue
            else:
                print("Враг рядом, но вы не можете атаковать его издалека.")
                continue
        else:
            print("Неверное действие.")
            continue
        if not check_collision(new_pos, game_map):
            player_pos = new_pos
            
            # Проверка на столкновение с врагом
            if player_pos == enemy_pos:
                damage = enemy.attack(player)
                print(f"{enemy.name} атакует {player.name} и наносит {damage} урона.")
            else:
                # Перемещение врага к игроку
                enemy_pos = move_enemy_towards_player(enemy_pos, player_pos)
                # Проверка на столкновение после движения врага
                if player_pos == enemy_pos:
                    damage = enemy.attack(player)
                    print(f"{enemy.name} атакует {player.name} и наносит {damage} урона.")
        else:
            print("Стена! Вы не можете пройти.")

    if player.hp <= 0:
        print("Вы погибли!")
    elif enemy.hp <= 0:
        print("Вы победили врага!")

if __name__ == "__main__":
    main()
