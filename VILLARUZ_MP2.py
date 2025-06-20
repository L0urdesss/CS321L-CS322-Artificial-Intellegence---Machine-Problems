#MARIA LOURDES T. VILLARUZ
#BSCS -3A
#KILLER SUDOKU SOLVER USING SIMULATED ANNEALING
import pygame
import sys
import random
import numpy as np

def random_board():
    board = [[0 for _ in range(4)] for _ in range(4)]
    values = random.sample(range(1, 5), 4)
    cells = [(i, j) for i in range(4) for j in range(4)]
    random.shuffle(cells)
    for i in range(4):
        for j in range(4):
            board[cells[i * 4 + j][0]][cells[i * 4 + j][1]] = values[i]
    return board

def valid(board, row, col, num, constraints):
    for c in range(4):
        if board[row][c] == num and c != col:
            return False
    for r in range(4):
        if board[r][col] == num and r != row:
            return False
    start_row = (row // 2) * 2
    start_col = (col // 2) * 2
    for i in range(start_row, start_row + 2):
        for j in range(start_col, start_col + 2):
            if board[i][j] == num and (i, j) != (row, col):
                return False
    region_sum = 0
    for cells, target_sum in constraints:
        if (row, col) in cells:
            for r, c in cells:
                if board[r][c] == num:
                    return False
                region_sum += board[r][c]
            if region_sum + num > target_sum:
                return False
            break
    return True

def fitness(board, constraints):
    score = 0
    for i in range(4):
        row_values = set()
        col_values = set()
        for j in range(4):
            row_value = board[i][j]
            col_value = board[j][i]
            if row_value not in range(1, 5) or col_value not in range(1, 5):
                score += 1
            if row_value in row_values or col_value in col_values:
                score += 1
            row_values.add(row_value)
            col_values.add(col_value)
    for cells, target_sum in constraints:
        cell_sum = sum(board[row][col] for row, col in cells)
        if cell_sum != target_sum:
            score += 1
    return score

def swap_random_cells(board):
    i1, j1 = random.randint(0, 3), random.randint(0, 3)
    i2, j2 = random.randint(0, 3), random.randint(0, 3)
    board[i1][j1], board[i2][j2] = board[i2][j2], board[i1][j1]
    return board, (i1, j1), (i2, j2)

def the_algorithm(board, constraints, temperature, cooling_rate, iterations):
    global solution_found

    if fitness(board, constraints) == 0:
        solution_found = True
        return board

    best_board = board.copy()
    best_score = fitness(board, constraints)
    while temperature > 0.0 and iterations > 0:
        for _ in range(iterations):
            new_board, (i1, j1), (i2, j2) = swap_random_cells(board)
            new_score = fitness(new_board, constraints)
            delta_e = new_score - best_score

            if delta_e < 0 or random.random() < np.exp(-delta_e / temperature):
                best_score = new_score
                best_board = new_board.copy()
                if best_score == 0:
                    print("Correct solution found.")
                    solution_found = True
                    return best_board
            else:
                best_board[i1][j1], best_board[i2][j2] = best_board[i2][j2], best_board[i1][j1]

        print("Current board:")
        for row in best_board:
            print([max(1, min(4, num)) for num in row])

        print("Iterations left:", iterations)
        print("Temperature:", temperature)

        temperature *= cooling_rate
        iterations -= 1

        if temperature <= 0.0:
            print("Temperature reached zero.")
            break

    solution_found = False
    return best_board

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
            text = font.render(str(board[i][j]), True, WHITE)
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
            return user_constraints

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

def main():
    global solution_found
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("4x4 Sudoku")
    welcome_screen()
    user_constraints = users_constraints()
    board = random_board()
    solution = the_algorithm(board, user_constraints, temperature=1.0, cooling_rate=0.95, iterations=150)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        if not solution_found:
            font = pygame.font.Font(None, 20)
            no_solution_text = font.render("No solution found. Please Click to Try again.", True, WHITE)
            text_rect = no_solution_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(no_solution_text, text_rect)
        else:
            draw_grid(solution)
            draw_sums(user_constraints)

        pygame.display.flip()

        if not solution_found and pygame.mouse.get_pressed()[0]:
            solution_found = False
            board = random_board()
            solution = the_algorithm(board, user_constraints, temperature=1.0, cooling_rate=0.95, iterations=150)

if __name__ == "__main__":
    main()
