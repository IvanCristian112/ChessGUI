import pygame
import chess
import chess.variant
import os

class Dropdown:
    def __init__(self, options, pos, size, font_size=30):
        self.options = options
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.Font(None, font_size)
        self.selected_option = options[0]
        self.active = False
        self.option_rects = [pygame.Rect(pos[0], pos[1] + size[1] * (i + 1), size[0], size[1]) for i in range(len(options))]
    
    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        text_surface = self.font.render(self.selected_option, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        
        if self.active:
            for i, option in enumerate(self.options):
                pygame.draw.rect(screen, (200, 200, 200), self.option_rects[i])
                pygame.draw.rect(screen, (0, 0, 0), self.option_rects[i], 2)
                text_surface = self.font.render(option, True, (0, 0, 0))
                screen.blit(text_surface, (self.option_rects[i].x + 5, self.option_rects[i].y + 5))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            elif self.active:
                for i, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = self.options[i]
                        self.active = False
                        break
                self.active = False
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_ESCAPE:
                self.active = False
    
    def get_selected_option(self):
        return self.selected_option

class Button:
    def __init__(self, text, pos, size, font_size=30):
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.Font(None, font_size)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event, callback):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                callback()

class ScrollableMoveList:
    def __init__(self, pos, size, font_size=24):
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.Font(None, font_size)
        self.moves = []
        self.scroll_offset = 0
        self.line_height = font_size + 5

    def add_move(self, move):
        move_number = (len(self.moves) // 2) + 1
        if len(self.moves) % 2 == 0:
            self.moves.append(f"{move_number}. {move}")
        else:
            self.moves.append(f"{move}")

        max_scroll = max(0, len(self.moves) * self.line_height - self.rect.height)
        self.scroll_offset = min(self.scroll_offset, max_scroll)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_offset = max(self.scroll_offset - self.line_height, 0)
            elif event.button == 5:  # Scroll down
                max_scroll = max(0, len(self.moves) * self.line_height - self.rect.height)
                self.scroll_offset = min(self.scroll_offset + self.line_height, max_scroll)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        for i, move in enumerate(self.moves):
            text_surface = self.font.render(move, True, (0, 0, 0))
            y_position = self.rect.y + 5 + (i // 2) * self.line_height - self.scroll_offset
            if i % 2 == 0:
                screen.blit(text_surface, (self.rect.x + 5, y_position))
            else:
                screen.blit(text_surface, (self.rect.x + 75, y_position))

class ChessBoardGUI:
    def __init__(self, ruleset):
        pygame.init()
        self.ruleset = ruleset
        self.reset_board()
        self.square_size = 64
        self.board_size = self.square_size * 8
        self.window_width = self.board_size + 200  # Extra space for future elements
        self.window_height = self.board_size + 40  # Dropdown menu height
        self.selected_piece = None  # Track the selected piece's square
        self.possible_moves = []  # Legal moves for the selected piece
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Chess Board')
        self.clock = pygame.time.Clock()
        self.images = {}
        self.load_images()
        self.dropdown = Dropdown(["Standard", "Antichess", "KingOfTheHill", "ThreeCheck"], 
                                 (self.board_size + 10, 10), (180, 30))
        self.move_list = ScrollableMoveList((self.board_size + 10, 50), (180, self.board_size - 60))
        self.export_button = Button("Export Moves", (self.board_size + 10, self.window_height - 30), (180, 30))
    
    def reset_board(self):
        if self.ruleset == 'Antichess':
            self.board = chess.variant.AntichessBoard()
        elif self.ruleset == 'KingOfTheHill':
            self.board = chess.variant.KingOfTheHillBoard()
        elif self.ruleset == 'ThreeCheck':
            self.board = chess.variant.ThreeCheckBoard()
        else:
            self.board = chess.Board()

    def load_images(self):
        piece_types = ['p', 'n', 'b', 'r', 'q', 'k']
        colors = ['w', 'b']
        for color in colors:
            for piece_type in piece_types:
                filename = f'{color}_{piece_type}.png'
                path = os.path.join('Images', filename)
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (self.square_size, self.square_size))
                self.images[f'{color}{piece_type}'] = image

    def draw_board(self):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color, pygame.Rect(col*self.square_size, row*self.square_size, self.square_size, self.square_size))

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                column = chess.square_file(square)
                row = 7 - chess.square_rank(square) # Pygame's y-axis starts at the top
                color = 'w' if piece.color else 'b'
                piece_image = self.images[f'{color}{piece.symbol().lower()}']
                self.screen.blit(piece_image, pygame.Rect(column*self.square_size, row*self.square_size, self.square_size, self.square_size))

    def select_piece(self, square):
        # Select a piece and highlight its legal moves
        piece = self.board.piece_at(square)
        if piece and piece.color == self.board.turn:
            self.selected_piece = square
            self.possible_moves = [move for move in self.board.legal_moves if move.from_square == square]
        else:
            self.selected_piece = None
            self.possible_moves = []

    def draw_highlight(self):
        # Highlight the selected square and possible moves
        if self.selected_piece is not None:
            s = pygame.Surface((self.square_size, self.square_size))  # the size of your rect
            s.set_alpha(128)  # alpha level
            s.fill((255, 255, 0))  # this fills the entire surface
            rect = pygame.Rect(chess.square_file(self.selected_piece) * self.square_size, 
                               (7 - chess.square_rank(self.selected_piece)) * self.square_size, 
                               self.square_size, self.square_size)
            self.screen.blit(s, rect)  # (0,0) are the top-left coordinates

            # Highlight legal moves
            for move in self.possible_moves:
                s.fill((0, 255, 0))  # Green for possible moves
                rect = pygame.Rect(chess.square_file(move.to_square) * self.square_size, 
                                   (7 - chess.square_rank(move.to_square)) * self.square_size, 
                                   self.square_size, self.square_size)
                self.screen.blit(s, rect)

    def draw_dragging_piece(self, drag_pos):
        # Draw the piece that is being dragged
        if self.selected_piece is not None:
            piece = self.board.piece_at(self.selected_piece)
            if piece:
                color = 'w' if piece.color else 'b'
                piece_image = self.images[f'{color}{piece.symbol().lower()}']
                piece_rect = piece_image.get_rect(center=drag_pos)
                self.screen.blit(piece_image, piece_rect)

    def export_moves(self):
        with open('moves.txt', 'w') as f:
            for move in self.move_list.moves:
                f.write(move + '\n')

    def run(self):
        running = True
        dragging = False
        drag_pos = None

        while running:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < self.board_size and mouse_pos[1] < self.board_size:
                col = mouse_pos[0] // self.square_size
                row = mouse_pos[1] // self.square_size
                current_square = chess.square(col, 7 - row)
            else:
                current_square = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if current_square is not None:
                        # Check if the clicked square has a piece of the current player's color
                        piece = self.board.piece_at(current_square)
                        if piece and piece.color == self.board.turn:
                            self.selected_piece = current_square
                            dragging = True
                            drag_pos = mouse_pos
                elif event.type == pygame.MOUSEBUTTONUP and dragging:
                    if current_square is not None:
                        # Attempt to make a move
                        move = chess.Move(self.selected_piece, current_square)
                        if move in self.board.legal_moves:
                            san_move = self.board.san(move)
                            self.board.push(move)
                            self.move_list.add_move(san_move)
                    self.selected_piece = None
                    dragging = False
                elif event.type == pygame.MOUSEMOTION and dragging:
                    drag_pos = mouse_pos

                self.dropdown.handle_event(event)
                self.move_list.handle_event(event)
                self.export_button.handle_event(event, self.export_moves)

            self.screen.fill((169, 169, 169))  # Fill the screen with grey background
            self.draw_board()
            self.draw_pieces()
            if dragging:
                self.draw_dragging_piece(drag_pos)
            self.draw_highlight()
            self.move_list.draw(self.screen)
            self.export_button.draw(self.screen)
            self.dropdown.draw(self.screen)  # Draw the dropdown last to make sure it is on top
            pygame.display.flip()
            self.clock.tick(60)
            self.check_ruleset()

        pygame.quit()

    def check_ruleset(self):
        selected_ruleset = self.dropdown.get_selected_option()
        if selected_ruleset != self.ruleset:
            self.ruleset = selected_ruleset
            self.reset_board()
            self.move_list = ScrollableMoveList((self.board_size + 10, 50), (180, self.board_size - 60))  # Reset the move list when ruleset changes

def main():
    gui = ChessBoardGUI("Standard")
    gui.run()

if __name__ == "__main__":
    main()
