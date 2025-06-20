#MARIA LOURDES T. VILLARUZ
#BSCS - 3A
#KILLER SUDOKU SOLVER USING BACKTRACKING ALGORITHM

import pygame
import sys
import random

WIDTH = 400
HEIGHT = 400
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4x4 Killer Sudoku Solver")
screen.fill(BLACK)

def draw_grid(board):
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
        pygame.draw.line(screen, WHITE, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            font = pygame.font.Font(None, 36)
            cell_value = board[i][j]
            if cell_value != 0:
                text = font.render(str(cell_value), True, WHITE)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)


def draw_sums(constraints):
    font = pygame.font.Font(None, 24)
    space = 5
    colors = [
        (0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (128, 0, 128), (255, 165, 0),
        (128, 128, 0), (0, 128, 128), (255, 192, 203), (0, 128, 0),
        (0, 0, 128), (128, 0, 0), (128, 128, 128), (255, 69, 0),
        (0, 255, 128), (160, 32, 240)
    ]

    for idx, (cells, target_sum) in enumerate(constraints):
        color = colors[idx % len(colors)]
        for cell in cells:
            row, col = cell
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            pygame.draw.line(screen, color, (x, y), (x + CELL_SIZE, y), 2)
            pygame.draw.line(screen, color, (x, y), (x, y + CELL_SIZE), 2)
            pygame.draw.line(screen, color, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
            pygame.draw.line(screen, color, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)

            sum_text = font.render(str(target_sum), True, color)
            text_rect = sum_text.get_rect(
                topleft=(col * CELL_SIZE + space, row * CELL_SIZE + space)
            )
            screen.blit(sum_text, text_rect)

def print_board(board):
    for row in board:
        print(row)

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)
    return None

def valid(bo, num, pos, constraints):
    if not (is_valid_row(bo, num, pos[0]) and
            is_valid_col(bo, num, pos[1]) and
            is_valid_box(bo, num, pos[0], pos[1])):
        return False


    for cells, target_sum in constraints:
        if pos in cells:
            if sum([bo[row][col] for row, col in cells if bo[row][col] != 0]) + num > target_sum:
                return False

    return True

def is_valid_row(bo, num, row):
    return num not in bo[row]

def is_valid_col(bo, num, col):
    return num not in [bo[row][col] for row in range(len(bo))]

def is_valid_box(bo, num, row, col):
    box_x = col // 2
    box_y = row // 2

    for i in range(box_y * 2, box_y * 2 + 2):
        for j in range(box_x * 2, box_x * 2 + 2):
            if bo[i][j] == num and (i, j) != (row, col):
                return False

    return True

def solve_sudoku(board, constraints):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 5):
        if valid(board, i, (row, col), constraints):
            board[row][col] = i

            if solve_sudoku(board, constraints):
                return True

            board[row][col] = 0

    return False

def users_constraints():
    user_constraints = []

    selected_cells = set()
    dragging = False
    sum_input = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    selected_cells.add((row, col))
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    sum_value = int(sum_input) if sum_input.isdigit() else 0
                    user_constraints.append((list(selected_cells), sum_value))
                    selected_cells.clear()
                    sum_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    sum_input = sum_input[:-1]
                elif event.key in range(pygame.K_0, pygame.K_9 + 1):
                    sum_input += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if (row, col) in selected_cells:
                    selected_cells.remove((row, col))

        screen.fill(BLACK)
        draw_grid([[0] * GRID_SIZE for _ in range(GRID_SIZE)])
        for cell in selected_cells:
            pygame.draw.rect(screen, BLUE, (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            font = pygame.font.Font(None, 24)
            sum_text = font.render(sum_input, True, WHITE)
            text_rect = sum_text.get_rect(
                topleft=(cell[1] * CELL_SIZE + 5, cell[0] * CELL_SIZE + 5)
            )
            screen.blit(sum_text, text_rect)

        draw_sums(user_constraints)

        solve_button_width = 80
        solve_button_height = 30
        solve_button_rect = pygame.Rect((WIDTH - solve_button_width) // 2, HEIGHT - solve_button_height - 10,
                                        solve_button_width, solve_button_height)
        pygame.draw.rect(screen, BLUE, solve_button_rect)
        font = pygame.font.Font(None, 24)
        solve_text = font.render("Solve", True, WHITE)
        solve_text_rect = solve_text.get_rect(center=solve_button_rect.center)
        screen.blit(solve_text, solve_text_rect)

        pygame.display.flip()

        solve_button_clicked = pygame.mouse.get_pressed()[0] and solve_button_rect.collidepoint(pygame.mouse.get_pos())
        if solve_button_clicked:
            return user_constraints, selected_cells

def welcome_screen():
    font_large = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 20)
    welcome_text = font_large.render("Welcome to Killer Sudoku!", True, WHITE)
    instruction_text1 = font_small.render("Instructions:", True, WHITE)
    instruction_text2 = font_small.render("1. Drag to select cells.", True, WHITE)
    instruction_text3 = font_small.render("2. Type numbers for the sum and Press 'Enter' to input.", True, WHITE)
    instruction_text4 = font_small.render("3. Click the selected cell to delete.", True, WHITE)
    instruction_text5 = font_small.render("4. Click on the 'Solve' button to solve the Sudoku.", True, WHITE)
    start_button_text = font_large.render("Start", True, BLACK)
    welcome_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    instruction_rect1 = instruction_text1.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 50))
    instruction_rect2 = instruction_text2.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 80))
    instruction_rect3 = instruction_text3.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 110))
    instruction_rect4 = instruction_text4.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 140))
    instruction_rect5 = instruction_text5.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 170))
    start_button_rect = start_button_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.fill(BLACK)
    screen.blit(welcome_text, welcome_rect)
    screen.blit(instruction_text1, instruction_rect1)
    screen.blit(instruction_text2, instruction_rect2)
    screen.blit(instruction_text3, instruction_rect3)
    screen.blit(instruction_text4, instruction_rect4)
    screen.blit(instruction_text5, instruction_rect5)
    pygame.draw.rect(screen, WHITE, start_button_rect, 2)
    pygame.draw.rect(screen, WHITE, start_button_rect)
    screen.blit(start_button_text, start_button_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if start_button_rect.collidepoint(x, y):
                        return

def solve_sudoku_gui(board, constraints, gui_update_function):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 5):
        if valid(board, i, (row, col), constraints):
            replaced_value = board[row][col] if board[row][col] != 0 else None
            board[row][col] = i
            gui_update_function(board, (row, col), i, True, replaced_value)

            if solve_sudoku_gui(board, constraints, gui_update_function):
                return True

            board[row][col] = 0
            gui_update_function(board, (row, col), 0, False, replaced_value)

    return False

def gui_update_function(board, position, value, is_addition, replaced_value):
    row, col = position
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    font = pygame.font.Font(None, 36)


    pygame.draw.rect(screen, BLACK, (x + 1, y + 1, CELL_SIZE - 1, CELL_SIZE - 1))

    if is_addition:

        text_color = (0, 255, 0)
    else:
        text_color = WHITE


    if replaced_value is not None:
        value = replaced_value
    else:
        value = board[row][col]


    if value != 0:
        text = font.render(str(value), True, text_color)
        text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(20)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("4x4 Sudoku")
    welcome_screen()
    user_constraints, selected_cells = users_constraints()


    sudoku_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]


    for row, col in selected_cells:
        sudoku_board[row][col] = random.randint(1, 4)


    if solve_sudoku_gui(sudoku_board, user_constraints, gui_update_function):
        print("Sudoku Solved:")
        print_board(sudoku_board)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw_grid(sudoku_board)
        draw_sums(user_constraints)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
