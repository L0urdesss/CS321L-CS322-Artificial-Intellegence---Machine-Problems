# MARIA LOURDES T. VILLARUZ
# BSCS-3A

import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
BG = (255, 255, 255)
FG = (0, 0, 0)
WHITE = (0, 255, 0)
BLACK = (255, 0, 0)
LINE_WIDTH = 5
NODE_RADIUS = 15

NODES = {
    'A': (100, 100),
    'B': (300, 100),
    'C': (500, 100),
    'D': (200, 200),
    'E': (300, 200),
    'F': (400, 200),
    'G': (100, 300),
    'H': (200, 300),
    'I': (400, 300),
    'J': (500, 300),
    'K': (200, 400),
    'L': (300, 400),
    'M': (400, 400),
    'N': (100, 500),
    'O': (300, 500),
    'P': (500, 500),
}

COMBINATIONS = [
    ('A', 'B', 'C'),
    ('D', 'E', 'F'),
    ('K', 'L', 'M'),
    ('N', 'O', 'P'),
    ('A', 'G', 'N'),
    ('D', 'H', 'K'),
    ('F', 'I', 'M'),
    ('C', 'J', 'P')
]

ADJACENT_NODES = {
    'A': ['B', 'G'],
    'B': ['A', 'C', 'E'],
    'C': ['B', 'J'],
    'D': ['E', 'H'],
    'E': ['B', 'D', 'F'],
    'F': ['E', 'I'],
    'G': ['A', 'H', 'N'],
    'H': ['D', 'G', 'K'],
    'I': ['F', 'J', 'M'],
    'J': ['C', 'I', 'P'],
    'K': ['H', 'L'],
    'L': ['K', 'M', 'O'],
    'M': ['I', 'L'],
    'N': ['G', 'O'],
    'O': ['L', 'N', 'P'],
    'P': ['J', 'O']
}

PLAYER_1 = 1
PLAYER_2 = 2

MAX_PIECES_PER_PLAYER = {PLAYER_1: 6, PLAYER_2: 6}

PHASE_PLACING = 0
PHASE_MOVING = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Six Men\'s Morris')

current_player = PLAYER_1
placed_pieces = {node: None for node in NODES.keys()}
pieces_count = {PLAYER_1: 0, PLAYER_2: 0}
player_combinations = {PLAYER_1: [], PLAYER_2: []}
game_phase = PHASE_PLACING


def draw_nodes():
    for node, pos in NODES.items():
        if placed_pieces[node] == PLAYER_1:
            pygame.draw.circle(screen, WHITE, pos, NODE_RADIUS)
        elif placed_pieces[node] == PLAYER_2:
            pygame.draw.circle(screen, BLACK, pos, NODE_RADIUS)
        else:
            pygame.draw.circle(screen, FG, pos, NODE_RADIUS)


def draw_board():
    pygame.draw.rect(screen, FG, (NODES['A'], NODES['M']), LINE_WIDTH)
    pygame.draw.rect(screen, FG, (NODES['D'], NODES['D']), LINE_WIDTH)
    pygame.draw.line(screen, FG, NODES['G'], NODES['H'], LINE_WIDTH)
    pygame.draw.line(screen, FG, NODES['B'], NODES['E'], LINE_WIDTH)
    pygame.draw.line(screen, FG, NODES['O'], NODES['L'], LINE_WIDTH)
    pygame.draw.line(screen, FG, NODES['J'], NODES['I'], LINE_WIDTH)
    draw_nodes()
    pygame.display.flip()


def place_piece(mouse_pos):
    global current_player
    for node, pos in NODES.items():
        if pygame.Rect(pos[0] - NODE_RADIUS, pos[1] - NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2).collidepoint(
                mouse_pos):
            if pieces_count[current_player] < MAX_PIECES_PER_PLAYER[current_player]:
                if placed_pieces[node] is None:
                    placed_pieces[node] = current_player
                    pieces_count[current_player] += 1
                    print(f"Player {current_player} placed a piece at node {node}")
                    player_pieces = [node for node, player in placed_pieces.items() if player == current_player]
                    print(f"Player {current_player} has placed the following pieces: {', '.join(player_pieces)}")
                    draw_board()
                    combos = check_combinations(current_player, placed_pieces)
                    for combo in combos:
                        if combo not in player_combinations[current_player]:
                            player_combinations[current_player].append(combo)
                            print(f"Combination made. Player {current_player} can remove a piece")
                            remove_piece()
                    if player_combinations[current_player]:
                        combos = [f"({' '.join(combo)})" for combo in player_combinations[current_player]]
                        print(f"Player {current_player} Combinations: {' '.join(combos)}")
                    current_player = get_opposite_player(current_player)
                    if pieces_count[PLAYER_1] == MAX_PIECES_PER_PLAYER[PLAYER_1] and pieces_count[PLAYER_2] == \
                            MAX_PIECES_PER_PLAYER[PLAYER_2]:
                        global game_phase
                        game_phase = PHASE_MOVING
                        print("All pieces are placed. Switching to moving phase.")
                    if check_game_over(current_player):
                        declare_winner(current_player)


def move_piece(mouse_pos):
    global current_player
    selected_node = None


    for node, pos in NODES.items():
        if pygame.Rect(pos[0] - NODE_RADIUS, pos[1] - NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2).collidepoint(
                mouse_pos) and placed_pieces[node] == current_player:
            print(f"Player {current_player} selected piece at node {node} to move.")
            selected_node = node
            break

    if selected_node is not None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dest_mouse_pos = pygame.mouse.get_pos()

                    for node, pos in NODES.items():
                        if pygame.Rect(pos[0] - NODE_RADIUS, pos[1] - NODE_RADIUS, NODE_RADIUS * 2,
                                       NODE_RADIUS * 2).collidepoint(dest_mouse_pos) and placed_pieces[
                            node] == current_player:
                            print(
                                f"Player {current_player} changed selected piece to node {node}.")
                            selected_node = node
                            break
                    else:

                        for dest_node, dest_pos in NODES.items():
                            if pygame.Rect(dest_pos[0] - NODE_RADIUS, dest_pos[1] - NODE_RADIUS, NODE_RADIUS * 2,
                                           NODE_RADIUS * 2).collidepoint(dest_mouse_pos):
                                if pieces_count[current_player] == 3 or dest_node in ADJACENT_NODES[
                                    selected_node] and placed_pieces[dest_node] is None:
                                    if all(dest_node != node for node, player in placed_pieces.items() if
                                           player is not None):
                                        placed_pieces[dest_node], placed_pieces[selected_node] = placed_pieces[
                                                                                                     selected_node], None
                                        print(
                                            f"Player {current_player} moved piece from {selected_node} to {dest_node}")
                                        draw_board()
                                        if any(combo for combo in player_combinations[current_player] if
                                               selected_node in combo):
                                            player_combinations[current_player] = [combo for combo in
                                                                                   player_combinations[
                                                                                       current_player] if
                                                                                   selected_node not in combo]
                                            print(
                                                f"Removed combination containing node {selected_node} from Player {current_player} combinations.")
                                        combos = check_combinations(current_player, placed_pieces)
                                        for combo in combos:
                                            if combo not in player_combinations[current_player]:
                                                player_combinations[current_player].append(combo)
                                                print(
                                                    f"Combination made. Player {current_player} can remove a piece")
                                                remove_piece()
                                        current_player = get_opposite_player(current_player)
                                        if check_game_over(current_player):
                                            declare_winner(current_player)
                                        return
                                    else:
                                        print("Cannot move to a node occupied by any piece.")
                                        return
                        else:
                            print("Invalid destination node.")
                            return


def remove_piece():
    global current_player
    running_remove = True
    opponent_player = get_opposite_player(current_player)

    player_pieces = [node for node, p in placed_pieces.items() if p == opponent_player]
    pieces_not_in_combinations = any(
        all(piece not in combo for combo in player_combinations[opponent_player]) for piece in player_pieces)
    all_pieces_in_combinations = all(
        any(piece in combo for combo in player_combinations[opponent_player]) for piece in player_pieces)

    if all_pieces_in_combinations and pieces_count[opponent_player] > 3:
        if pieces_not_in_combinations:
            print("All pieces are part of a combination, but there are pieces not in a combination. Removal not allowed.")
            declare_winner(0)
            return
        else:
            print("Combination made. Player 1 can remove a piece")

    while running_remove:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for node, pos in NODES.items():
                    if placed_pieces[node] == opponent_player and pygame.Rect(pos[0] - NODE_RADIUS,
                                                                              pos[1] - NODE_RADIUS, NODE_RADIUS * 2,
                                                                              NODE_RADIUS * 2).collidepoint(mouse_pos):
                        is_part_of_combo = False
                        for combo in player_combinations[opponent_player]:
                            if node in combo:
                                is_part_of_combo = True
                                break

                        if not is_part_of_combo or (all_pieces_in_combinations and pieces_count[opponent_player] <= 3):
                            placed_pieces[node] = None
                            pieces_count[opponent_player] -= 1
                            MAX_PIECES_PER_PLAYER[opponent_player] -= 1
                            print(
                                f"Player {current_player} removed a piece from node {node} of Player {opponent_player}")
                            running_remove = False
                            break



def ai_place_piece():
    global current_player

    best_value, best_move = minimax(placed_pieces, pieces_count, player_combinations, current_player, depth=2,
                                    maximizing_player=True)

    if best_move is not None:
        placed_pieces[best_move] = current_player
        pieces_count[current_player] += 1

        print(f"AI (Player {current_player}) placed a piece at node {best_move} with value {best_value}")
        draw_board()

        combos = check_combinations(current_player, placed_pieces)
        for combo in combos:
            if combo not in player_combinations[current_player]:
                player_combinations[current_player].append(combo)
                print(f"Combination made. Player {current_player} can remove a piece")
                ai_remove_piece()

        if player_combinations[current_player]:
            combos = [f"({' '.join(combo)})" for combo in player_combinations[current_player]]
            print(f"Player {current_player} Combinations: {' '.join(combos)}")

        current_player = get_opposite_player(current_player)

        print(f"Player 1 pieces: {pieces_count[PLAYER_1]}, Player 2 pieces: {pieces_count[PLAYER_2]}")
        if pieces_count[PLAYER_1] == MAX_PIECES_PER_PLAYER[PLAYER_1] and pieces_count[PLAYER_2] == \
                MAX_PIECES_PER_PLAYER[PLAYER_2]:
            global game_phase
            game_phase = PHASE_MOVING
            print("All pieces are placed. Switching to moving phase.")
        if check_game_over(current_player):
            declare_winner(current_player)

    else:
        print("No valid move found for AI to place a piece.")


def ai_move_piece():
    global current_player

    best_value, best_move = minimax(placed_pieces, pieces_count, player_combinations, current_player, depth=2,
                                    maximizing_player=True)

    if best_move is not None:
        source_node, dest_node = best_move
        placed_pieces[dest_node], placed_pieces[source_node] = placed_pieces[source_node], None

        print(f"AI (Player {current_player}) moved piece from {source_node} to {dest_node} with value {best_value}")
        draw_board()

        if any(combo for combo in player_combinations[current_player] if source_node in combo):
            player_combinations[current_player] = [combo for combo in player_combinations[current_player] if
                                                   source_node not in combo]
            print(f"Removed combination containing node {source_node} from Player {current_player} combinations.")

        combos = check_combinations(current_player, placed_pieces)
        for combo in combos:
            if combo not in player_combinations[current_player]:
                player_combinations[current_player].append(combo)
                print(f"Combination made. Player {current_player} can remove a piece")
                ai_remove_piece()

        if player_combinations[current_player]:
            combos = [f"({' '.join(combo)})" for combo in player_combinations[current_player]]
            print(f"Player {current_player} Combinations: {' '.join(combos)}")

        current_player = get_opposite_player(current_player)

        if check_game_over(current_player):
            declare_winner(current_player)

    else:
        print("No valid move found for AI to move a piece.")


def ai_remove_piece():
    global current_player
    opponent_player = PLAYER_2 if current_player == PLAYER_1 else PLAYER_1

    opponent_pieces = [node for node, player in placed_pieces.items() if player == opponent_player]

    non_combination_pieces = []
    combination_pieces = []

    for piece in opponent_pieces:
        in_combination = False
        for combo in player_combinations[opponent_player]:
            if piece in combo:
                in_combination = True
                break
        if in_combination:
            combination_pieces.append(piece)
        else:
            non_combination_pieces.append(piece)

    if non_combination_pieces:

        piece_to_remove = random.choice(non_combination_pieces)
    elif combination_pieces:

        piece_to_remove = random.choice(combination_pieces)
    else:
        print("No valid move found. AI cannot remove any piece.")
        return

    placed_pieces[piece_to_remove] = None
    pieces_count[opponent_player] -= 1
    MAX_PIECES_PER_PLAYER[opponent_player] -= 1

    print(f"AI (Player {current_player}) removed a piece from node {piece_to_remove} of Player {opponent_player}")
    draw_board()

    if check_game_over(current_player):
        declare_winner(current_player)

def minimax(placed_pieces, pieces_count, player_combinations, current_player, depth, maximizing_player):
    temp_pieces = placed_pieces.copy()
    temp_count = pieces_count.copy()
    temp_combinations = player_combinations.copy()

    if depth == 0 or check_game_over(current_player):
        return evaluate_board(temp_pieces, current_player), None

    possible_moves = get_possible_moves(temp_pieces, current_player)

    if maximizing_player:
        best_value = float('-inf')
        best_move = None
        for move in possible_moves:
            temp_pieces, temp_count, temp_combinations = make_move(move, temp_pieces, temp_count, temp_combinations)
            value, _ = minimax(temp_pieces, temp_count, temp_combinations, get_opposite_player(current_player),
                               depth - 1, False)
            undo_move(move, temp_pieces, temp_count, temp_combinations)
            if value > best_value:
                best_value = value
                best_move = move
        return best_value, best_move
    else:
        best_value = float('inf')
        best_move = None
        for move in possible_moves:
            temp_pieces, temp_count, temp_combinations = make_move(move, temp_pieces, temp_count, temp_combinations)
            value, _ = minimax(temp_pieces, temp_count, temp_combinations, get_opposite_player(current_player),
                               depth - 1, True)
            undo_move(move, temp_pieces, temp_count, temp_combinations)
            if value < best_value:
                best_value = value
                best_move = move
        return best_value, best_move


def evaluate_board(temp_pieces, current_player):
    player_score = 0
    opponent_score = 0

    for node, piece in temp_pieces.items():
        if piece == current_player:
            player_score += 1
        elif piece is not None and piece != current_player:
            opponent_score += 1

    piece_count_diff = player_score - opponent_score

    player_combos = check_combinations(current_player, temp_pieces)
    opponent_combos = check_combinations(get_opposite_player(current_player), temp_pieces)
    combo_score = 10 * len(player_combos) - 4 * len(opponent_combos)

    opponent_potential_combos = check_potential_combos(get_opposite_player(current_player), temp_pieces)
    opponent_potential_combo_count = len(opponent_potential_combos)
    combo_penalty = -4 * opponent_potential_combo_count

    ai_potential_combos = check_potential_combos(current_player, temp_pieces)
    ai_potential_combo_count = len(ai_potential_combos)
    combo_reward = 2 * ai_potential_combo_count

    player_mobility = sum(1 for node, piece in temp_pieces.items() if
                          piece == current_player and None in [temp_pieces[adj_node] for adj_node in
                                                               ADJACENT_NODES[node]])
    opponent_mobility = sum(1 for node, piece in temp_pieces.items() if
                            piece != current_player and piece is not None and None in [temp_pieces[adj_node] for
                                                                                       adj_node in
                                                                                       ADJACENT_NODES[node]])
    mobility_score = player_mobility - opponent_mobility

    new_combo_score = 0
    for combo in player_combos:
        if combo not in player_combinations[current_player]:
            new_combo_score += 10

    total_score = piece_count_diff + combo_score + mobility_score + combo_penalty + combo_reward + new_combo_score

    return total_score


def check_combinations(player, temp_pieces):
    combos = []
    for combo in COMBINATIONS:
        if all(temp_pieces[node] == player for node in combo):
            combos.append(combo)
    return combos


def check_potential_combos(player, temp_pieces):
    potential_combos = []
    for combo in COMBINATIONS:
        combo_nodes = set(combo)
        player_nodes = {node for node, piece in temp_pieces.items() if piece == player}
        enemy_nodes = {node for node, piece in temp_pieces.items() if piece != player and piece is not None}
        missing_nodes = combo_nodes - player_nodes
        if len(missing_nodes) == 1:
            missing_node = missing_nodes.pop()
            if temp_pieces.get(missing_node) is None and missing_node not in enemy_nodes:
                potential_combos.append(missing_node)
    return potential_combos


def get_possible_moves(temp_pieces, current_player):
    possible_moves = []

    if game_phase == PHASE_PLACING:
        for node, piece in temp_pieces.items():
            if piece is None:
                possible_moves.append(node)
    elif game_phase == PHASE_MOVING:
        for node, piece in temp_pieces.items():
            if piece == current_player:
                if pieces_count[current_player] == 3:
                    for empty_node, empty_piece in temp_pieces.items():
                        if empty_piece is None:
                            possible_moves.append((node, empty_node))
                else:
                    for adj_node in ADJACENT_NODES[node]:
                        if temp_pieces[adj_node] is None:
                            possible_moves.append((node, adj_node))
    return possible_moves


def make_move(move, temp_pieces, temp_count, temp_combinations):
    if len(move) == 1:
        node = move[0]
        temp_pieces[node] = current_player

    elif len(move) == 2:
        source_node, dest_node = move
        temp_pieces[dest_node] = current_player
        temp_pieces[source_node] = None

    return temp_pieces, temp_count, temp_combinations


def undo_move(move, temp_pieces, temp_count, temp_combinations):
    if len(move) == 1:
        node = move[0]
        temp_pieces[node] = None
        temp_count[current_player] -= 1

    elif len(move) == 2:
        source_node, dest_node = move
        temp_pieces[source_node] = current_player
        temp_pieces[dest_node] = None

    return temp_pieces, temp_count, temp_combinations


def get_opposite_player(current_player):
    return PLAYER_2 if current_player == PLAYER_1 else PLAYER_1


def check_game_over(player):
    if game_phase == PHASE_PLACING:
        empty_nodes = [node for node, piece in placed_pieces.items() if piece is None]
        if not empty_nodes:
            print("No valid moves left for placing pieces. Game over.")
            return True

        return False
    elif game_phase == PHASE_MOVING:
        if pieces_count[player] <= 2:
            print(f"Player {player} has only 2 pieces left. Game over.")
            return True
        else:
            for node, pos in NODES.items():
                if placed_pieces[node] == player:
                    adjacent_nodes = ADJACENT_NODES[node]
                    for adj_node in adjacent_nodes:
                        if placed_pieces[adj_node] is None:
                            return False
            print(f"Player {player} has no valid moves left. Game over.")
            return True
    else:
        return False


def declare_winner(losing_player):
    global game_phase

    if losing_player != 0:
        winner = PLAYER_2 if losing_player == PLAYER_1 else PLAYER_1
        print(f"Player {winner} wins the game!")
        display_winner_screen(winner)

    game_phase = None


def display_welcome_screen():
    screen.fill(BG)
    font = pygame.font.Font(None, 36)
    text = font.render("Welcome to Six Men's Morris Game", True, FG)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)


    play_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 20, 100, 50)
    pygame.draw.rect(screen, FG, play_button)
    font = pygame.font.Font(None, 30)
    text = font.render("Play", True, BG)
    text_rect = text.get_rect(center=play_button.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

    return play_button


def main():
    global current_player

    play_button = display_welcome_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    start_game()
                    running = False

    pygame.quit()
    sys.exit()


def start_game():
    global current_player

    coin_toss = random.choice([PLAYER_1, PLAYER_2])
    current_player = coin_toss

    print(f"Coin toss result: Player {coin_toss} goes first.")
    running = True

    while running:
        screen.fill(BG)
        draw_board()

        if current_player == PLAYER_1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if game_phase == PHASE_PLACING:
                        place_piece(mouse_pos)
                    elif game_phase == PHASE_MOVING:
                        move_piece(mouse_pos)

        elif current_player == PLAYER_2:
            if game_phase == PHASE_PLACING:
                ai_place_piece()
            elif game_phase == PHASE_MOVING:
                ai_move_piece()

    pygame.quit()
    sys.exit()



def display_winner_screen(winner):
    screen.fill(BG)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player {winner} wins!", True, FG)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, FG, exit_button)
    font = pygame.font.Font(None, 30)
    exit_text = font.render("Exit", True, BG)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    main()

