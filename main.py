import sys
import pygame
from constant import *
from board import GomokuBoard

def draw_board(board, preview_pos = None):
    screen.fill(BG_COLOR)
    board_pixel_size = (BOARD_SIZE - 1) * CELL_SIZE
    for i in range(BOARD_SIZE):
        pos = OFFSET + i * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR,(OFFSET, pos),(OFFSET + board_pixel_size, pos), 3)
        pygame.draw.line(screen, LINE_COLOR,(pos, OFFSET),(pos, OFFSET + board_pixel_size), 3)
    stars = [(3, 3), (3,11), (3, 7), (11, 3), (11, 11), (11, 7), (7, 7), (7, 3), (7, 11)]
    for r, c in stars:
        x = OFFSET + c * CELL_SIZE
        y = OFFSET + r * CELL_SIZE
        pygame.draw.circle(screen, LINE_COLOR, (x, y), 7)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board.board[r][c] != 0:
                x = OFFSET + c * CELL_SIZE
                y = OFFSET + r * CELL_SIZE
                color = BLACK if board.board[r][c] == 1 else WHITE
                pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 2 - 4)
                if board.board[r][c] == -1:
                    pygame.draw.circle(screen, BLACK, (x, y), CELL_SIZE // 2 - 4, 2)
    if preview_pos and not board.game_over:
        row, col = preview_pos
        if board.board[row][col] == 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            x = OFFSET + col * CELL_SIZE
            y = OFFSET + row * CELL_SIZE
            color = BLACK if board.current_player == 1 else WHITE
            radius = CELL_SIZE // 2 - 4
            s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color, 120), (radius, radius), radius)
            screen.blit(s, (x - radius, y - radius))

    if board.game_over:
        if board.winner == 1:
            msg = "🎉 BLACK WIN 🎉"
        elif board.winner == -1:
            msg = "🎉 WHITE WIN 🎉"
        else:
            msg = "🎉 DRAW 🎉"
        text_color = RED
    else:
        msg = "BLACK'S TURN" if board.current_player == 1 else "WHITE'S TURN"
        text_color = TEXT_COLOR

    text = font.render(msg, True, text_color)
    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, OFFSET + board_pixel_size + 30))
    tip = small_font.render("R: restart   U: undo", True, (0,0,0))
    screen.blit(tip, (WINDOW_WIDTH // 2 - tip.get_width() // 2, OFFSET + board_pixel_size + 75))

def main():
    global screen, font, small_font
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Gomoku")
    font = pygame.font.SysFont("Microsoft YaHei", 32)
    small_font = pygame.font.SysFont("Microsoft YaHei", 22)
    board = GomokuBoard()
    clock = pygame.time.Clock()
    preview_pos = None
    print("✅ Loaded")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                col = round((mx - OFFSET) / CELL_SIZE)
                row = round((my - OFFSET) / CELL_SIZE)
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                    preview_pos = (row, col)
                else:
                    preview_pos = None

            elif event.type == pygame.MOUSEBUTTONDOWN and not board.game_over:
                if event.button == 1:
                    mx, my = event.pos
                    col = round((mx - OFFSET) / CELL_SIZE)
                    row = round((my - OFFSET) / CELL_SIZE)
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                        board.make_move(row, col)
                        preview_pos = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board.reset()
                elif event.key == pygame.K_u:
                    board.undo_move()
                    board.game_over = False
                    board.winner = 0

        draw_board(board, preview_pos)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


