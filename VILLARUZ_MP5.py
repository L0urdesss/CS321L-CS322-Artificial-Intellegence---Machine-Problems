#MARIA LOURDES T. VILLARUZ
#BSCS-3A

import random
from collections import deque


def generate_random_position(size, exclude=[]):
    position = (random.randint(0, size - 1), random.randint(0, size - 1))
    while position in exclude:
        position = (random.randint(0, size - 1), random.randint(0, size - 1))
    return position


def generate_random_pit_position(size, exclude=[]):
    pit_positions = []
    used_positions = set(exclude)
    for i in range(size):
        for j in range(size):
            position = (i, j)
            if position not in used_positions and random.random() < 0.2:
                pit_positions.append(position)
                used_positions.add(position)
    return pit_positions


bullet_path = []
shot_temp = False
has_bullet = True
board_state = []
is_stench_found = False
is_wumpus_found = False
size = 4
agent_position = (size - 1, 0)
used_positions = set()
used_positions.add((3, 0))
used_positions.add((2, 0))
used_positions.add((3, 1))
wumpus_position = generate_random_position(size, exclude=used_positions)
used_positions.add(wumpus_position)
gold_position = generate_random_position(size, exclude=used_positions)
used_positions.add(gold_position)
pit_positions = generate_random_pit_position(size, exclude=used_positions)
is_bump = False
is_scream = False
face_direction = '+y'
agent_point = 0
moving = False


def initialize_board_state(size, agent_position):
    global board_state
    board_state = [[(i, j), False, False, False, False, False] for i in range(size) for j in range(size)]
    update_visited(agent_position)
    update_board_state(agent_position, size, False, False)


def print_board_state(size):
    global board_state
    temp_array = []
    for i in range(size):
        for j in range(size):
            temp = False
            for state in board_state:
                if (i, j) == state[0]:
                    if state[3]:
                        print("V", end="  ")
                        temp = True
                    elif state[1] and state[2]:
                        print("OK", end=" ")
                        temp = True
                    elif state[5] and state[4]:
                        print("WP", end=" ")
                        temp = True
                    elif state[4]:
                        print("W", end="  ")
                        temp = True
                    elif state[5]:
                        print("P", end="  ")
                        temp = True
                    if temp == True:
                        temp_array.append((i, j))
            if temp == False:
                print("-", end="  ")

        print()


def print_board(size, agent_position, wumpus_position, pit_positions, gold_position, isRevealMap):
    for i in range(size):
        for j in range(size):
            if (i, j) == agent_position:
                print("A", end=" ")
            elif (i, j) == wumpus_position and isRevealMap:
                print("W", end=" ")
            elif (i, j) in pit_positions and isRevealMap:
                print("P", end=" ")
            elif (i, j) == gold_position and isRevealMap:
                print("G", end=" ")
            else:
                print("-", end=" ")
        print()


def is_valid_position(size, position):
    x, y = position
    return 0 <= x < size and 0 <= y < size


def is_wumpus_at(position, wumpus_position):
    return position == wumpus_position


def is_agent_at_start(position):
    return position == (3, 0)


def is_pit_at(position, pit_positions):
    return position in pit_positions


def is_gold_at(position, gold_position):
    return position == gold_position


def is_agent_alive(agent_position, wumpus_position, pit_positions):
    return agent_position != wumpus_position and agent_position not in pit_positions


def is_hit(agent_position, face_direction):
    global wumpus_position
    global bullet_path

    size = 4

    if face_direction == '+x':
        for x in range(agent_position[0] - 1, -1, -1):
            bullet_path.append((x, agent_position[1]))
    elif face_direction == '-x':
        for x in range(agent_position[0] + 1, size):
            bullet_path.append((x, agent_position[1]))
    elif face_direction == '+y':
        for y in range(agent_position[1] + 1, size):
            bullet_path.append((agent_position[0], y))
    elif face_direction == '-y':
        for y in range(agent_position[1] - 1, -1, -1):
            bullet_path.append((agent_position[0], y))
    if (bullet_path):
        for path in bullet_path:
            if is_wumpus_at(path, wumpus_position):
                print("hit")
                wumpus_position = (None, None)
                return True

    return False


def ai_hit_possible_path(agent_position, face_direction):
    size = 4
    global wumpus_position
    bullet_path = []

    if face_direction == '+x':
        for x in range(agent_position[0] - 1, -1, -1):
            bullet_path.append((x, agent_position[1]))
    elif face_direction == '-x':
        for x in range(agent_position[0] + 1, size):
            bullet_path.append((x, agent_position[1]))
    elif face_direction == '+y':
        for y in range(agent_position[1] + 1, size):
            bullet_path.append((agent_position[0], y))
    elif face_direction == '-y':
        for y in range(agent_position[1] - 1, -1, -1):
            bullet_path.append((agent_position[0], y))

    global board_state
    possible_wumpus = []
    for state in board_state:
        if state[4]:
            possible_wumpus.append(state[0])
    print("wumpus: ", possible_wumpus)
    if (bullet_path):
        print("bullet: ", bullet_path)
        for path in bullet_path:
            for possiblepath in possible_wumpus:
                if is_wumpus_at(path, wumpus_position):
                    return True
                elif path == possiblepath:
                    return True

    return False


def get_adjacent_pos(agent_position):
    adjacent_pos = []

    if agent_position[0] != 3:
        adjacent_pos.append((agent_position[0] + 1, agent_position[1]))
    if agent_position[0] != 0:
        adjacent_pos.append((agent_position[0] - 1, agent_position[1]))
    if agent_position[1] != 3:
        adjacent_pos.append((agent_position[0], agent_position[1] + 1))
    if agent_position[1] != 0:
        adjacent_pos.append((agent_position[0], agent_position[1] - 1))

    return adjacent_pos


def after_shot():
    global has_bullet
    global bullet_path
    global board_state
    for path in bullet_path:
        for state in board_state:
            if path == state[0]:
                state[1] = True
    bullet_path = []
    has_bullet = False


def update_board_state(agent_position, size, stench, breeze):
    global board_state
    global is_wumpus_found
    global is_stench_found

    if not stench or not breeze:
        adjacent_pos_array = get_adjacent_pos(agent_position)
        for adjacent_pos in adjacent_pos_array:
            for state in board_state:
                if state[0] == adjacent_pos:
                    if not breeze:
                        state[2] = True
                    if not stench:
                        state[1] = True
    if stench or breeze:
        adjacent_pos_array = get_adjacent_pos(agent_position)
        for adjacent_pos in adjacent_pos_array:
            for state in board_state:
                if state[0] == adjacent_pos:
                    if stench and not is_wumpus_found:
                        state[4] = True
                    if stench and is_stench_found:
                        if not state[4]:
                            state[1] = True
                    if breeze:
                        state[5] = True

    for state in board_state:
        if state[3]:
            state[2] = True
            state[1] = True
        if state[2]:
            state[5] = False
        if state[1]:
            if state[4]:
                is_stench_found = True
                state[4] = False

    if is_stench_found:
        count = 0
        for state in board_state:
            if state[4]:
                count += 1
        if count == 1:
            is_wumpus_found = True

    if is_wumpus_found:
        for state in board_state:
            if state[4]:
                state[2] = True
                state[5] = False


def update_visited(agent_position):
    for state in board_state:
        if state[0] == agent_position:
            state[3] = True


def move_agent(agent_position, direction, size, face_direction):
    global gold_position
    global agent_point
    global has_bullet
    new_position = agent_position
    new_face_direction = face_direction

    if direction == "FORWARD":
        if face_direction[1] == 'y':
            if face_direction[0] == '+':
                new_position = (agent_position[0], agent_position[1] + 1)
            else:
                new_position = (agent_position[0], agent_position[1] - 1)
        elif face_direction[1] == 'x':
            if face_direction[0] == '+':
                new_position = (agent_position[0] - 1, agent_position[1])
            else:
                new_position = (agent_position[0] + 1, agent_position[1])

        if not is_valid_position(size, new_position):
            return agent_position, face_direction, True, False  # Bump detected

    elif direction == "TURNLEFT":
        if face_direction[1] == 'x':
            if face_direction[0] == '+':
                new_face_direction = '-y'
            else:
                new_face_direction = '+y'
        elif face_direction[1] == 'y':
            if face_direction[0] == '+':
                new_face_direction = '+x'
            else:
                new_face_direction = '-x'

    elif direction == "TURNRIGHT":
        if face_direction[1] == 'x':
            if face_direction[0] == '+':
                new_face_direction = '+y'
            else:
                new_face_direction = '-y'
        elif face_direction[1] == 'y':
            if face_direction[0] == '+':
                new_face_direction = '-x'
            else:
                new_face_direction = '+x'

    elif direction == "SHOOT":
        if has_bullet:
            agent_point += -10
            if is_hit(agent_position, face_direction):
                return agent_position, face_direction, False, True
            else:
                after_shot()
                return agent_position, face_direction, False, False
    elif direction == "GRAB":
        if is_gold_at(agent_position, gold_position):
            print("\033[93mYou got the gold! +1000\033[0m")  # Yellow text
            gold_position = (None, None)
            agent_point += 1000
        else:
            print("\033[91mThere is no gold.\033[0m")  # Red text
    elif direction == "CLIMB":
        if is_agent_at_start(agent_position):
            print("Climbing Out")
            if (gold_position == (None, None)):
                print("\033[93mYou got the gold! +1000\033[0m")  # Yellow text
                agent_point += 1000
            else:
                print("\033[91mYou didn't get the gold.\033[0m")  # Red text
            total_points()
            exit()
        else:
            print("Cannot climb here")
    elif direction == "ESC":
        exit()

    agent_point += -1
    return new_position, new_face_direction, False, False


def get_agent_direction(face_direction):
    if face_direction == '+y':
        direction = '\u2192'  # Right
    elif face_direction == '-y':
        direction = '\u2190'  # Left
    elif face_direction == '+x':
        direction = '\u2191'  # Up
    elif face_direction == '-x':
        direction = '\u2193'  # Down
    return direction


def update_print_state(stench, breeze, glitter, bump, scream):
    if stench:
        stench_state = "Stench"
    else:
        stench_state = "_"
    if breeze:
        breeze_state = "Breeze"
    else:
        breeze_state = "_"
    if glitter:
        glitter_state = "Glitter"
    else:
        glitter_state = "_"
    if bump:
        bump_state = "Bump"
    else:
        bump_state = "_"
    if scream:
        scream_state = "Scream"
    else:
        scream_state = "_"

    print("States: [", stench_state, breeze_state, glitter_state, bump_state, scream_state, "]")


def update_board_on_wumpus_death():
    global board_state
    for state in board_state:
        if state[1] == False:
            state[1] = True
        if state[4] == True:
            state[4] = False


def is_valid_location(location):
    x, y = location
    return 0 <= x < 4 and 0 <= y < 4


def rotate_left(direction):
    directions = ["+x", "-y", "-x", "+y"]
    return directions[(directions.index(direction) + 1) % 4]


def rotate_right(direction):
    directions = ["+x", "+y", "-x", "-y"]
    return directions[(directions.index(direction) + 1) % 4]


def move_forward(location, direction):
    x, y = location
    if direction == "+x":
        return (x - 1, y)
    elif direction == "-x":
        return (x + 1, y)
    elif direction == "+y":
        return (x, y + 1)
    elif direction == "-y":
        return (x, y - 1)


def find_shortest_path(current_location, target_location, safe_locations, initial_direction):
    directions = ["+x", "+y", "-x", "-y"]
    visited = set()
    queue = deque([(current_location, [], initial_direction)])

    while queue:
        current, actions, direction = queue.popleft()
        visited.add((current, direction))

        for action in ["move_forward", "rotate_left", "rotate_right"]:
            if action == "move_forward":
                next_location = move_forward(current, direction)
                if next_location in safe_locations and is_valid_location(next_location) and (
                next_location, direction) not in visited:
                    if next_location == target_location:
                        return actions + ["FORWARD"]
                    queue.append((next_location, actions + ["FORWARD"], direction))
            elif action == "rotate_left":
                next_direction = rotate_left(direction)
                if (current, next_direction) not in visited:
                    queue.append((current, actions + ["TURNLEFT"], next_direction))
            elif action == "rotate_right":
                next_direction = rotate_right(direction)
                if (current, next_direction) not in visited:
                    queue.append((current, actions + ["TURNRIGHT"], next_direction))

    return None


def total_points():
    global agent_point
    if agent_point >= 0:
        print("Total Points Earned: \033[93m{}\033[0m".format(agent_point))  # Yellow text
    else:
        print("Total Points Earned: \033[91m{}\033[0m".format(agent_point))  # Red text

def possible_wumpus():
    global board_state
    count = 0
    for state in board_state:
        if state[4]:
            count += 1
    return count


def ai_play(isRevealMap):
    global size
    global agent_position
    global wumpus_position
    global pit_positions
    global gold_position
    global face_direction
    global is_bump
    global is_scream
    global agent_point
    global has_bullet

    initialize_board_state(size, agent_position)
    direction = get_agent_direction(face_direction)
    total_points()
    print("Current agent position:", agent_position)
    print("Agent Direction: \033[33m{}\033[0m".format(direction))
    update_print_state(False, False, False, False, False)
    print("Map:")
    print_board(size, agent_position, wumpus_position, pit_positions, gold_position, isRevealMap)
    print("State:")
    print_board_state(size)
    found_gold = False
    bump_state = False
    scream_state = False
    stench_state = False
    breeze_state = False
    glitter_state = False
    ready_shoot = False
    walk_shoot = False
    while is_agent_alive(agent_position, wumpus_position, pit_positions):
        skip_walk = False

        if found_gold:
            decision_array = ai_go_home(agent_position, face_direction)
            decision_array.insert(0, "GRAB")
        elif ready_shoot:
            print("INSIDE READY SHOOT")
            decision_array = ai_shoot(agent_position, face_direction)
            ready_shoot = False

        else:
            decision_array = ai_move(agent_position, face_direction)
            if not decision_array:
                count = possible_wumpus()
                if has_bullet and count > 0:
                    decision_array = ai_kill_wumpus(agent_position, face_direction)
                    if not decision_array:
                        skip_walk = True
                    walk_shoot = True
                else:
                    decision_array = ai_go_home(agent_position, face_direction)

        bump_state = False
        scream_state = False
        stench_state = False
        breeze_state = False
        glitter_state = False

        if not ready_shoot and not skip_walk:
            for decision in decision_array:
                print("\nCurrent agent position:", agent_position)
                print("AI PICKED: ", decision)
                agent_position, face_direction, is_bump, is_scream = move_agent(agent_position, decision, size,
                                                                                face_direction)
                print("Agent moved to:", agent_position)
                update_visited(agent_position)
                direction = get_agent_direction(face_direction)
                print("Agent Direction: \033[33m{}\033[0m".format(direction))
                total_points()
                if is_scream:
                    scream_state = True
                    update_board_on_wumpus_death()

                if is_bump:
                    bump_state = True

                if (agent_position[0] - 1, agent_position[1]) == wumpus_position or \
                        (agent_position[0] + 1, agent_position[1]) == wumpus_position or \
                        (agent_position[0], agent_position[1] - 1) == wumpus_position or \
                        (agent_position[0], agent_position[1] + 1) == wumpus_position:
                    stench_state = True

                if (agent_position) == gold_position:
                    glitter_state = True
                    found_gold = True

                if (agent_position[0] - 1, agent_position[1]) in pit_positions or \
                        (agent_position[0] + 1, agent_position[1]) in pit_positions or \
                        (agent_position[0], agent_position[1] - 1) in pit_positions or \
                        (agent_position[0], agent_position[1] + 1) in pit_positions:
                    breeze_state = True
                update_print_state(stench_state, breeze_state, glitter_state, bump_state, scream_state)
                update_board_state(agent_position, size, stench_state, breeze_state)

                if is_wumpus_at(agent_position, wumpus_position):
                    print("The Wumpus got you! Game Over!")
                    agent_point += -1000
                    total_points()
                    exit()
                elif is_pit_at(agent_position, pit_positions):
                    print("Agent fell into a pit! Game Over!")
                    agent_point += -1000
                    total_points()
                    exit()

                print("Map:")
                print_board(size, agent_position, wumpus_position, pit_positions, gold_position, isRevealMap)
                print("State:")
                print_board_state(size)

                input("Press Enter to continue...")

                if (
                        bump_state or scream_state or stench_state or breeze_state or glitter_state) and not found_gold and not walk_shoot:
                    break
        if ready_shoot:
            walk_shoot = False
        if walk_shoot:
            ready_shoot = True
            walk_shoot = False


def ai_shoot(agent_position, face_direction):
    closest_path = []
    turn_decision = ai_in_range(agent_position, face_direction)
    print("turn_decision: ", turn_decision)
    print("turn: ", turn_decision)
    if turn_decision:
        for turn in turn_decision:
            closest_path.append(turn)
    closest_path.append("SHOOT")
    return closest_path


def ai_in_range(agent_position, face_direction):
    clock_wise_direction = ['+y', '-x', '-y', '+x']
    counter_clock_wise_direction = ['+x', '-y', '-x', '+y']

    def make_turn(turn_direction, direction):
        num_turns = 0
        while True:
            if ai_hit_possible_path(agent_position, direction):
                break
            else:
                direction = turn(turn_direction, direction)
            num_turns += 1
        return num_turns

    num_turns_right = make_turn('TURNRIGHT', face_direction)
    num_turns_left = make_turn('TURNLEFT', face_direction)
    if num_turns_right < num_turns_left:
        return ['TURNRIGHT'] * num_turns_right
    else:
        return ['TURNLEFT'] * num_turns_left


def turn(direction, face):
    if direction == 'TURNRIGHT':
        if face == '+y':
            face = '-x'
        elif face == '-x':
            face = '-y'
        elif face == '-y':
            face = '+x'
        elif face == '+x':
            face = '+y'
    elif direction == 'TURNLEFT':
        if face == '+x':
            face = '-y'
        elif face == '-y':
            face = '-x'
        elif face == '-x':
            face = '+y'
        elif face == '+y':
            face = '+x'
    return face


def get_horizontal_coordinates(x, y, width):
    horizontal_coordinates = [(x, j) for j in range(width) if j != y]
    return horizontal_coordinates


def get_vertical_coordinates(x, y, height):
    vertical_coordinates = [(i, y) for i in range(height) if i != x]
    return vertical_coordinates


def get_wumpus_bullet_path():
    path_array = []
    target_locations = []
    size = 4
    global board_state

    for state in board_state:
        if state[4]:
            target_locations.append(state[0])

    if target_locations:
        for location in target_locations:
            vertical_coords = get_vertical_coordinates(location[0], location[1], size)
            horizontal_coords = get_horizontal_coordinates(location[0], location[1], size)
            path_array.extend(vertical_coords)
            path_array.extend(horizontal_coords)

        path_array_copy = path_array.copy()
        for state in board_state:
            for path in path_array_copy:
                if path == state[0]:
                    if not state[1] or not state[2]:
                        path_array.remove(path)

    return path_array


def ai_kill_wumpus(agent_position, face_direction):
    closest_path = []
    global board_state
    safe_locations = []
    closest_length = float('inf')  # Initialize with infinity

    target_locations = get_wumpus_bullet_path()

    safe_locations = get_safe_locations()

    if not target_locations:
        return None
    else:
        for location in target_locations:
            shortest_path = find_shortest_path(agent_position, location, safe_locations, face_direction)
            if shortest_path is None or len(shortest_path) < closest_length:
                closest_path = shortest_path
                closest_length = len(shortest_path) if shortest_path is not None else 0
        # print("got inner")

        return closest_path


def ai_move(agent_position, face_direction):
    decision_array = ai_get_closest_ok(agent_position, face_direction)

    return decision_array


def ai_go_home(agent_position, face_direction):
    safe_locations = []
    shortest_path = []
    exit_location = (3, 0)

    safe_locations = get_safe_locations()

    shortest_path = find_shortest_path(agent_position, exit_location, safe_locations, face_direction)
    shortest_path.append("CLIMB")

    return shortest_path


def get_safe_locations():
    global board_state

    safe_locations = []

    for state in board_state:
        if state[1] and state[2]:
            safe_locations.append(state[0])

    return safe_locations


def ai_get_closest_ok(agent_position, face_direction):
    closest_path = None
    closest_length = float('inf')
    global board_state
    safe_locations = []
    target_locations = []

    safe_locations = get_safe_locations()

    for state in board_state:
        if state[1] and state[2] and not state[3]:
            target_locations.append(state[0])

    for location in target_locations:
        shortest_path = find_shortest_path(agent_position, location, safe_locations, face_direction)
        if shortest_path is not None and len(shortest_path) < closest_length:
            closest_path = shortest_path
            closest_length = len(shortest_path)

    return closest_path

def main_menu():
    print("\033[95mWELCOME TO WUMPUS WORLD!\033[0m")
    input("\033[94mPress Enter for AI to start...\033[0m")


    ai_play(True)

if __name__ == "__main__":
    main_menu()

