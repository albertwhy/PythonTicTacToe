import pygame
import numpy as np
import copy


class Board:
    def __init__(self, screen, screen_width, dimension):
        self.screen = screen
        self.screen_width = screen_width
        self.dimension = dimension
        self.startx = 50
        self.starty = 148
        self.rec_width = int((self.screen_width - (self.startx * 2)) / self.dimension)
        
        # form winning conditions
        winnero = ['o' for c in range(dimension)]
        winnerx = ['x' for c in range(dimension)]
        self.winnero = winnero # o winning condition for test_winner
        self.winnerx = winnerx # x winning condition for test_winner
        self.board = [['' for c in range(dimension)] for c in range(dimension)] # form empty array
        


    def draw_board(self): # draw board
        for i in range(self.dimension):
            for j in range(self.dimension):
                if (i+j) % 2 == 0: #1,1 ; 1,3; 2,2; 1,3; 3,3
                    color = (250,213,197) # pale pink
                else:
                    color = (239, 138, 94) # salmon
                topx = self.startx + self.rec_width * i
                topy = self.starty + self.rec_width * j
                sides = self.rec_width # length and width of sides
                pygame.draw.rect(self.screen, color, [topx, topy, sides, sides])

    def draw_pieces(self, player, pos): # calculate which square is pressed based on mouse position x, y
        board_coord=[]
        font_size = int(self.rec_width * 0.8) # 80% of squares, more squares = smaller font
        offset_pixel = font_size * 1/3
        midx = self.startx + offset_pixel + (int(pos[1])) * (self.rec_width) # 30 is for adjustment
        midy = self.starty + (int(pos[0])) * (self.rec_width)
        board_coord.append(midx)
        board_coord.append(midy)
        piece = pygame.font.SysFont("Times New Roman", font_size).render(player, False, (0, 0, 255))
        screen.blit(piece, board_coord)


def check_winner(board_array3): # check for winner
    result = "no winner"
    i = 0
    spaces_per_side = len(board_array3)
    board_array3_t = np.transpose(board_array3)
    board_array3_d1 = np.diagonal(board_array3)
    board_array3_d2 = np.fliplr(board_array3).diagonal()
    empty_space_list = [[i,j] for j in range(len(board_array3)) for i in range(len(board_array3)) if board_array3[i][j] == '']
    while i < spaces_per_side and result == "no winner":
        
        if board1.winnerx in (list(board_array3[i]), list(board_array3_t[i]), list(board_array3_d1), list(board_array3_d2)):
            result = "x wins"
        elif board1.winnero in (list(board_array3[i]), list(board_array3_t[i]), list(board_array3_d1), list(board_array3_d2)):
            result = "o wins"
        else:
            result = "no winner"
        i += 1

    if result == "no winner" and len(empty_space_list) == 0: 
        result = "tie game"

    return result



iter_count = 0 # to count how many iteration ran
def minimax_test(board, depth, max_or_min):
    global iter_count
    iter_count += 1
    result = check_winner(board)
    returned_value = []
    print(f'board: {board}, result: {result}, depth: {depth}')
    #print(result in ["o win", "x win", "tie game"])
    if depth == 0 or result in ["o wins", "x wins", "tie game"]: # o maximizing, x minimizing; stop condition
        if result == "o wins":
            return (10*(depth + 1), 0, 0) # higher number means win in less moves. 10 means win on last move, 10(depth+1) means win on 1st move
        elif result == "x wins":
            return (-10*(depth + 1), 0, 0) # Lower number means lose in less moves
        elif result == "tie game": # game tie
            return (0, 0, 0)

    else: # keep branching
        if max_or_min == "max": # 'o' maximizing

            # We're initially setting it to -2 as worse than the worst case:
            maxv = -2000

            px = None
            py = None

            for i in range(0, len(board)):
                for j in range(0, len(board)):
                    if board[i][j] == '':
                        # On the empty field player 'O' makes a move and calls Min
                        # That's one branch of the game tree.
                        board[i][j] = 'o'
                        (m, min_i, min_j) = minimax_test(board, depth-1, "min")
                        # Fixing the maxv value if needed
                        if m > maxv:
                            maxv = m
                            px = i
                            py = j
                        # Setting back the field to empty
                        board[i][j] = ''
            return (maxv, px, py)


        # Player 'X' is min, in this case human
        elif max_or_min == "min":

            # We're initially setting it to 2 as worse than the worst case:
            minv = 2000

            qx = None
            qy = None

            for i in range(0, len(board)):
                for j in range(0, len(board)):
                    if board[i][j] == '':
                        board[i][j] = 'x'
                        (m, max_i, max_j) = minimax_test(board, depth-1, "max")
                        if m < minv:
                            minv = m
                            qx = i
                            qy = j
                        board[i][j] = ''

            return (minv, qx, qy)

        




# initialize game
pygame.init()

# create game screen
screen_width = 400
screen_height = 540
screen = pygame.display.set_mode((screen_width, screen_height)) # width, height; starts at top-left corner ie 0,0 at top-left corner

# title and icon. Icons can be downloaded on flaticon.com
# Icons made by <a href="https://www.flaticon.com/authors/good-ware" title="Good Ware">Good Ware</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
pygame.display.set_caption("Tic-Tac-Toe") # change the title of the game window
icon = pygame.image.load('.\\src\\tic-tac-toe.png') # change the icon on the title bar. used 32px for icon
pygame.display.set_icon(icon)



# draw empty board. drawn sequence. Act like layers. background draw first, then the rest
screen.fill((0, 0, 0)) # RGB max 255 background
noSquares = 3 # array size. ie 3 = 3 x 3
board1 = Board(screen, screen_width, noSquares) # create instance
board1.draw_board() # call class method draw_board


# initialize array
print(board1.board)

# test cases for check_winner()
# board_array2 = [['o','x','-'],['-','o','o'],['x','x','o']] # o wins, diagonal1, 1 time
# board_array3 = [['-','x','-'],['o','o','o'],['x','x','-']] # o wins, 2 time
# board_array4 = [['x','x','x'],['-','o','o'],['x','x','o']] # x wins, 1 time
# board_array5 = [['-','-','x'],['-','o','o'],['x','x','x']] # x wins, 3 time
# print(check_winner(board1.board))

# reset button
reset_img = pygame.image.load('.\\src\\reset64.png')
screen.blit(reset_img, (board1.startx, 30))  # reset button 64 x 64

# vs computer buttons
vs_leftx = board1.startx + 180
vs_lefty = 30
vs_boxx = vs_leftx + 70
vs_boxy = vs_lefty + 10
vs_img = pygame.image.load('.\\src\\vs64.png')
screen.blit(vs_img, (vs_leftx, vs_lefty)) # vs icon 64 x 64
pygame.draw.rect(board1.screen, (255,255,250), [vs_boxx, vs_boxy, 30, 30])



running = True
move_counter = 1 # x first
vs_flag = False
while running:


    


    # background image
    # background = screen.blit(".\\src\\background.png", (x, y))

    for event in pygame.event.get():
        #print(event.type)
        if event.type == pygame.QUIT:
            running = False

        if event.type ==  5: # touch pad clicked
            mouse_pos = pygame.mouse.get_pos()
            #print(mouse_pos)
            if board1.startx <= mouse_pos[0] <= board1.startx + 64  \
              and 30 <= mouse_pos[1] <= 94: # reset play area and array
                board1.draw_board()
                for clear_i in range(len(board1.board)):
                    for clear_j in range(len(board1.board)):
                        board1.board[clear_i][clear_j] = ''
                move_counter = 1

            elif vs_boxx <= mouse_pos[0] <= vs_boxx + 30  \
              and vs_boxy <= mouse_pos[1] <= vs_boxy + 30: # vs box clicked
                if len([[i,j] for j in range(len(board1.board)) for i in range(len(board1.board)) if board1.board[i][j] != '']) == 0: #board is empty
                    if vs_flag == False: # currently empty, need x, start running ai, set vs_flag = True
                        vs_x = pygame.font.SysFont("Times New Roman", 28).render('x', False, (0, 0, 255)) # put an x in the box
                        screen.blit(vs_x, (vs_boxx+10, vs_boxy))
                        vs_flag = True
                    else: # currently filled, cover x, stop ai, set vs_flat = False
                        pygame.draw.rect(board1.screen, (255,255,250), [vs_boxx, vs_boxy, 30, 30])
                        vs_flag = False

            else:
                play_length = screen_width - (2 * board1.startx) # the board area length
                # calculate which square is pressed
                col = (mouse_pos[0] - board1.startx) // board1.rec_width # for array update
                row = (mouse_pos[1] - board1.starty) // board1.rec_width # for array update
                box_pos = (row, col) # for printing on screen
                if board1.startx <= mouse_pos[0] <= board1.startx + play_length  \
                and board1.starty <= mouse_pos[1] <= board1.starty + play_length \
                and board1.board[row][col] not in ("x", "o") \
                and comment == "no winner": 
                    if move_counter % 2 == 1:
                        current_move = 'o'
                    else:
                        current_move = 'x'
                    board1.board[row][col] = current_move # update board array
                    board1.draw_pieces(current_move, box_pos) # draw piece
                    move_counter += 1
                    if vs_flag == True: # human vs computer
                        if move_counter % 2 == 1:
                            xo = 'o'
                            max_or_min = "max"
                        else:
                            xo = 'x'
                            max_or_min = "min"
                        empty_depth = [[i,j] for j in range(len(board1.board)) for i in range(len(board1.board)) if board1.board[i][j] == '']
                        depth = len(empty_depth)
                        (who_wins, c_row, c_col) = minimax_test(board1.board, depth, max_or_min)
                        if board1.board[c_row][c_col] == '':
                            board1.board[c_row][c_col] = xo
                            board1.draw_pieces(xo, (c_row, c_col))
                        move_counter += 1 # o's turn again
                        
                        
                    
                    

    # winner comment
    screen.fill(pygame.Color("black"), (50, board1.starty + 310, 350, board1.starty + 320)) # cover the old blit
    comment = check_winner(board1.board)
    com_out = pygame.font.SysFont("Times New Roman", 30).render(comment, False, (255, 255, 255))
    screen.blit(com_out, (50,board1.starty + 310))

    
    


    # update board
    pygame.display.update()

# for testing purposes
#board4 = [['o','o',''],['x','',''],['','','']]
#print(f'called function: {minimax_test(board4, 6, "min")}') # max is o and min is x




