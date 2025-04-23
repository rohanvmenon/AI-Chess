import pygame
import sys
import random
import time
from const import *
from game import Game
from square import Square
from move import Move
from azero_ai import MCTS, StockfishNet, MCTSBoardWrapper



class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

        self.vs_ai = self.ask_mode()
        self.ai_color = 'black'
        self.mcts = MCTS(StockfishNet(r"C:\Users\Rohan\Documents\machine-learning-projects\python-chess-ai-Rohan\src\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"))

    def ask_mode(self):
        print("Choose game mode:")
        print("1. Play vs Human")
        print("2. Play vs AI")
        mode = input("Enter 1 or 2: ")
        return mode.strip() == '2'

    def ai_move(self):
        print("AI is thinking...")
        time.sleep(0.5)  # optional delay for realism
        wrapped_board = MCTSBoardWrapper(self.game.board, self.ai_color)
        best_move = self.mcts.run(wrapped_board, n_simulations=100)
        if best_move is None:
            print("AI has no legal moves. Game over or stalemate.")
            return
        print(f"AI plays: {best_move}")
        self.game.board.move(best_move.piece, best_move)
        self.game.play_sound(captured=best_move.final.piece is not None)
        self.game.next_turn()

    def mainloop(self):

            screen = self.screen
            game = self.game
            board = self.game.board
            dragger = self.game.dragger

            clock = pygame.time.Clock()  # Add a clock to control the frame rate

            while True:
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)

                    elif event.type == pygame.MOUSEMOTION:
                        dragger.update_mouse(event.pos)
                        if dragger.dragging:
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            dragger.update_blit(screen)

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final, dragger.piece)

                            if board.valid_move(dragger.piece, move):
                                captured = board.squares[released_row][released_col].has_piece()
                                board.move(dragger.piece, move)
                                board.set_true_en_passant(dragger.piece)
                                game.play_sound(captured)
                                game.next_turn()

                                if self.vs_ai and game.next_player == self.ai_color:
                                    self.ai_move()

                        dragger.undrag_piece()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_t:
                            game.change_theme()
                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
                clock.tick(60)  # Limit the frame rate to 60 FPS


if __name__ == '__main__':
    main = Main()
    main.mainloop()