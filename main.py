import random


class Part:

    # Initialize the attributes
    def __init__(self, name: str, attack_level=0, defense_level=0, energy_consumption=0):
        self.name = name
        self.attack_level = attack_level
        self.defense_level = defense_level
        self.energy_consumption = energy_consumption
        self.critical = False

    # Return a dic with the values formatted
    def get_status_dict(self):
        formatted_name = self.name.replace(" ", "_").lower()
        return {
            "{}_name".format(formatted_name): self.name.upper(),
            "{}_status".format(formatted_name): self.is_available(),
            "{}_attack".format(formatted_name): self.attack_level,
            "{}_defense".format(formatted_name): self.defense_level,
            "{}_energy_consume".format(formatted_name): self.energy_consumption,
        }

    # Calculate the defense after the attack
    def reduce_defense(self, attack_level):
        self.defense_level = self.defense_level - attack_level
        if self.defense_level < 0:
            self.defense_level = 0

    # Return True if the defense is > 0
    def is_available(self):
        return not self.defense_level <= 0

    def is_critical(self, part_to_use):
        chance = self.critical_chance(part_to_use)
        if chance == 3:
            self.critical = True
            self.attack_level *= 2
        else:
            self.critical = False

    @staticmethod
    def critical_chance(part_to_use):
        if part_to_use == 1:
            b = 5
        else:
            b = 10
        return random.randint(1, b)

    def return_to_normal(self):
        if self.critical:
            self.attack_level /= 2


class Robot:
    # Send value to the Part class
    def __init__(self, name, color_code):
        self.name = name
        self.color_code = color_code
        self.energy = 100
        self.parts = [
            Part("Head", attack_level=5, defense_level=10, energy_consumption=5),
            Part("Weapon", attack_level=15, defense_level=0, energy_consumption=10),
            Part("Left Arm", attack_level=3, defense_level=20, energy_consumption=10),
            Part("Right Arm", attack_level=6, defense_level=20, energy_consumption=10),
            Part("Left Leg", attack_level=4, defense_level=20, energy_consumption=15),
            Part("Right Leg", attack_level=8, defense_level=20, energy_consumption=15),
        ]

    # Receive status from dic
    def print_status(self):
        print(self.color_code)
        str_robot = robot_art.format(**self.get_part_status())
        self.greet()
        self.print_energy()
        print(str_robot)
        print(colors["White"])

    # Greetings
    def greet(self):
        print("Hello, my name is", self.name)

    # Energy
    def print_energy(self):
        print("We have", self.energy, " percent energy left")

    # Add property to the parts
    def get_part_status(self):
        part_status = {}
        for part in self.parts:
            status_dict = part.get_status_dict()
            part_status.update(status_dict)
        return part_status

    # Calculate the attack and energy consumption
    def attack(self, current_robot, enemy_robot, part_to_use, part_to_attack):
        current_robot.parts[part_to_use].is_critical(part_to_use)
        enemy_robot.parts[part_to_attack].reduce_defense(self.parts[part_to_use].attack_level)
        self.energy -= self.parts[part_to_use].energy_consumption
        current_robot.parts[part_to_use].return_to_normal()

    # Verify the energy
    def is_on(self):
        return self.energy > 0

    # Verify if there is available parts
    def is_there_available_part(self):
        for part in self.parts:
            if part.is_available():
                return True
        return False

    # Verify if the part is available to attack
    @staticmethod
    def is_part_available_to_attack(current_robot, part_to_use):
        part = current_robot.parts[part_to_use].is_available()
        return part

    # Verify if the part is available to be attacked
    @staticmethod
    def is_part_available_to_be_attacked(enemy_robot, part_to_attack):
        part = enemy_robot.parts[part_to_attack].is_available()
        return part


robot_art = r"""
      0: {head_name}
      Is available: {head_status}
      Attack: {head_attack}                              
      Defense: {head_defense}
      Energy consumption: {head_energy_consume}
              ^
              |                  |1: {weapon_name}
              |                  |Is available: {weapon_status}
     ____     |    ____          |Attack: {weapon_attack}
    |oooo|  ____  |oooo| ------> |Defense: {weapon_defense}
    |oooo| '    ' |oooo|         |Energy consumption: {weapon_energy_consume}
    |oooo|/\_||_/\|oooo|          
    `----' / __ \  `----'           |2: {left_arm_name}
   '/  |#|/\/__\/\|#|  \'           |Is available: {left_arm_status}
   /  \|#|| |/\| ||#|/  \           |Attack: {left_arm_attack}
  / \_/|_|| |/\| ||_|\_/ \          |Defense: {left_arm_defense}
 |_\/    O\=----=/O    \/_|         |Energy consumption: {left_arm_energy_consume}
 <_>      |=\__/=|      <_> ------> |
 <_>      |------|      <_>         |3: {right_arm_name}
 | |   ___|======|___   | |         |Is available: {right_arm_status}
// \\ / |O|======|O| \  //\\        |Attack: {right_arm_attack}
|  |  | |O+------+O| |  |  |        |Defense: {right_arm_defense}
|\/|  \_+/        \+_/  |\/|        |Energy consumption: {right_arm_energy_consume}
\__/  _|||        |||_  \__/        
      | ||        || |          |4: {left_leg_name} 
     [==|]        [|==]         |Is available: {left_leg_status}
     [===]        [===]         |Attack: {left_leg_attack}
      >_<          >_<          |Defense: {left_leg_defense}
     || ||        || ||         |Energy consumption: {left_leg_energy_consume}
     || ||        || || ------> |
     || ||        || ||         |5: {right_leg_name}
   __|\_/|__    __|\_/|__       |Is available: {right_leg_status}
  /___n_n___\  /___n_n___\      |Attack: {right_leg_attack}
                                |Defense: {right_leg_defense}
                                |Energy consumption: {right_leg_energy_consume}

"""

colors = {
    "Black": '\x1b[90m',
    "Blue": '\x1b[94m',
    "Cyan": '\x1b[96m',
    "Green": '\x1b[92m',
    "Magenta": '\x1b[95m',
    "Red": '\x1b[91m',
    "White": '\x1b[97m',
    "Yellow": '\x1b[93m',
}


def build_robot():
    robot_name = input("Robot name: ")
    color_code = choose_color()
    robot = Robot(robot_name, color_code)
    robot.print_status()
    return robot


def choose_color():
    available_colors = colors
    print("Available colors:")
    for key, value in available_colors.items():
        print(value, key)
    print(colors["White"])
    while True:
        chosen_color = input("Choose a color: ").capitalize()
        if chosen_color in available_colors:
            color_code = available_colors[chosen_color]
            return color_code
        print('This color does not exists')


def play():
    playing = True
    print("Welcome to the game!")
    print("Datas for player 1:")
    robot_one = build_robot()
    print("Datas for player 2:")
    robot_two = build_robot()

    round_count = 0
    available = False
    available_attack = False

    while playing:
        if round_count % 2 == 0:
            current_robot = robot_one
            enemy_robot = robot_two
        else:
            current_robot = robot_two
            enemy_robot = robot_one
        current_robot.print_status()
        if available:
            print("This part is not available because it's broken, try another one")

        if available_attack:
            print("This part can't be attacked. -1 turn")
        available_attack = False
        part_to_use = ''
        in_range = True
        while in_range:
            print("What part should I use to attack?:")
            part_to_use = input("Choose a number part: ")
            part_to_use = int(part_to_use)
            if part_to_use in range(0, 5):
                in_range = False
            else:
                print('This part does not exists')

        is_available = current_robot.is_part_available_to_attack(current_robot, part_to_use)

        if is_available or part_to_use == 1:
            enemy_robot.print_status()
            part_to_attack = ''
            in_range = True
            while in_range:
                print("Which part of the enemy should we attack?")
                part_to_attack = input("Choose a enemy number part to attack: ")
                part_to_attack = int(part_to_attack)
                if part_to_attack in range(0, 5):
                    in_range = False
                else:
                    print('This part does not exists')

            is_available_to_attack = current_robot.is_part_available_to_be_attacked(enemy_robot, part_to_attack)

            if is_available_to_attack:
                current_robot.attack(current_robot, enemy_robot, part_to_use, part_to_attack)
                round_count += 1
            else:
                available_attack = True
                current_robot.attack(current_robot, enemy_robot, part_to_use, part_to_attack)
                round_count += 1
        else:
            available = True

        if not enemy_robot.is_on() or enemy_robot.is_there_available_part() is False:
            playing = False
            if not enemy_robot.is_on():
                print(f"Congratulations, {current_robot} won because the enemy turned off")
            else:
                print(f"Congratulations, {current_robot} won because the enemy has been destroyed")


play()
