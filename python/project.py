#https://github.com/ssode/connectfour/blob/master/connect4.py 
# credit goes out to ssode as some of my code has been altered from his
# The code from this link was used as a basis for connect 4 and the mcts algorithm although,
# the code from the link has been altered quite heavily from the original as his code didnt function correctly.

import math
import random
import copy
import pygame
import sys
from pygame.locals import *
import os


#variables and colours that will be used throughout the project

ROWS = 0
COLUMNS = 0
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
width = 800
height = 450
Matte_GREEN = (93, 148, 81)
txt_col = (232, 214, 91)
BACK = (13, 80, 91)
Matte_RED = 247, 42, 42

# contains information about a move
class Move:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return "({}, {})".format(self.row, self.col)

# State Super class with methods that 3 of the board games are based off, these states represent the game boards
class State:
    def __init__(self, player=1, board=None, last_move=None,game=None):
        pass

    def next_state(self, move):
        pass

    def valid_moves(self):
        pass

    def check_win(self):
        pass

    def draw_board(self):
        pass

####################################################################################################################################################################
#                                                                                                                                                                  #
#                                                                                                                                                                  #
#                                                                      CONNECT 4                                                                                   #
#                                                                     BOARD STATE                                                                                  #
#                                                                                                                                                                  #
#                                                                                                                                                                  #
####################################################################################################################################################################


class Con4State(State):

    # initalises the board and assigns values to vars
    def __init__(self, player=1, board=None, last_move=None, game="con4"):
        if board is None:
            self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        else:
            self.board = board
        self.cur_player = player
        self.last_move = last_move
        self.win_status = self.check_win()
        self.game = game
        if self.win_status != 0:
            self.is_terminal = True
        else:
            self.is_terminal = False

    # takes a copy of the board and returns the next state with a move applied as a new state
    def next_state(self, move):
        new_board = copy.deepcopy(self.board)
        assert isinstance(move, Move)
        new_board[move.row][move.col] = self.cur_player
        return Con4State(3-self.cur_player, new_board, move)

    # finds all possible moves that can be made in the game
    def valid_moves(self):
        moves = []
        for col in range(COLUMNS):
            for row in range(ROWS-1, -1, -1):
                if self.board[row][col] == 0:
                    moves.append(Move(row, col))
                    break
        return moves

    #checks for a winning player or if the game can continue by comparing all 4 of the possible win conditions
    #assigns a win status depending on the outcome of the game based on wether it is a win or tie
    def check_win(self):
        empty_found = False

        #check horizontal spaces
        for i in range(len(self.board)):
            for j in range(len(self.board[i])-3):
                tile = self.board[i][j]
                if self.board[i][j] == tile and self.board[i][j+1] == tile and self.board[i][j+2] == tile and self.board[i][j+3] == tile and tile != 0:
                    self.win_status = tile
                    self.is_terminal = True
                    
                    return tile

        for i in range(len(self.board)-3):
            for j in range(len(self.board[i])):
                tile = self.board[i][j]
                if self.board[i][j] == tile and self.board[i+1][j] == tile and self.board[i+2][j] == tile and self.board[i+3][j] == tile and tile != 0:
                    self.win_status = tile
                    self.is_terminal = True
                    

                    return tile

        for i in range(len(self.board)-3):
            for j in range(len(self.board[i])-3):
                tile = self.board[i][j]
                if self.board[i][j] == tile and self.board[i+1][j+1] == tile and self.board[i+2][j+2] == tile and self.board[i+3][j+3] == tile and tile != 0:
                    self.win_status = tile
                    self.is_terminal = True
                    

                    return tile

        for i in range(3,len(self.board)):
            for j in range(len(self.board[i])-3):

                tile = self.board[i][j]
                if self.board[i][j] == tile and self.board[i-1][j+1] == tile and self.board[i-2][j+2] == tile and self.board[i-3][j+3] == tile and tile != 0:
                    
                    self.win_status = tile
                    self.is_terminal = True

                    return tile

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                tile = self.board[i][j]
                if tile == 0:
                    
                    empty_found = True

        if empty_found:
            return 0
        else:
            self.win_status = -1
            self.is_terminal = True
            return -1

    # draws the board using pygames in built functions 
    def draw_board(self):
       
        for c in range(COLUMNS):
            for r in range(ROWS):
                pygame.draw.rect(screen,BACK, (220+ c*box_size,r*box_size+box_size+box_size, box_size,box_size))
                pygame.draw.circle(screen, WHITE,(int(220+ c*box_size+box_size/2),int(r*box_size+box_size+box_size+box_size/2)),RADIUS)
        
        for c in range(COLUMNS):
            for r in range(ROWS):
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen, RED,(int(220+c*box_size+box_size/2),int(r*box_size+box_size+box_size+box_size/2)),RADIUS)
                elif self.board[r][c] == 2:
                   pygame.draw.circle(screen, YELLOW,(int( 220+c*box_size+box_size/2),int(r*box_size+box_size+box_size+box_size/2)),RADIUS)

        pygame.display.update()


####################################################################################################################################################################
#                                                                                                                                                                  #
#                                                                                                                                                                  #
#                                                                     TIC TAC TOE                                                                                  #
#                                                                     BOARD STATE                                                                                  #
#                                                                                                                                                                  #
#                                                                                                                                                                  #
####################################################################################################################################################################


class TTTState(State):

    # initalises the board and assigns values to vars
    def __init__(self, player=1, board=None, last_move=None, game="ttt"):
        if board is None:
            self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        else:
            self.board = board
        self.cur_player = player
        self.last_move = last_move
        self.win_status = self.check_win()
        self.game = game
        if self.win_status != 0:
            self.is_terminal = True
        else:
            self.is_terminal = False

    # takes a copy of the board and returns the next state with a move applied as a new state
    def next_state(self, move):
        new_board = copy.deepcopy(self.board)
        assert isinstance(move, Move)
        new_board[move.row][move.col] = self.cur_player
        return TTTState(3-self.cur_player, new_board, move)

    # finds all possible moves that can be made in the game
    def valid_moves(self):
        moves = []
        for col in range(COLUMNS):
            for row in range(ROWS):
                if self.board[row][col] == 0:
                    
                    moves.append(Move(row, col))
                    
        return moves

    #checks for a winning player or if the game can continue by comparing all 8 of the possible win conditions
    #assigns a win status depending on the outcome of the game based on wether it is a win or tie
    def check_win(self):
        empty_found = False
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                tile = self.board[i][j]
                if tile == 0:
                    if not empty_found:
                        empty_found = True
                    continue
                try:
                    #col 0 vertical win
                    if self.board[i][j] == tile and self.board[i+1][j] == tile and self.board[i+2][j] == tile:
                        self.win_status = tile
                        self.is_terminal = True
                        return tile
                except IndexError:
                    pass
                try:
                    #row 0 horizontal win
                    if self.board[i][j] == tile and self.board[i][j+1] == tile and self.board[i][j+2] == tile:
                        self.win_status = tile
                        self.is_terminal = True
                        return tile
                except IndexError:
                    pass
                #row 1 horizontal win
                try:
                    if self.board[i+1][j] == tile and self.board[i+1][j+1] == tile and self.board[i+1][j+2] == tile:
                        self.win_status = tile
                        self.is_terminal = True
                        return tile
                except IndexError:
                    pass
                try:
                    # right upper diagonally win
                    if self.board[0][2] == tile and self.board[2][0] == tile and self.board[1][1] == tile:
                        self.win_status = tile
                        self.is_terminal = True
                        return tile
                except IndexError:
                    pass
                try:
                    # row 2 horizontal win
                    if self.board[i+2][j] == tile and self.board[i+2][j+1] == tile and self.board[i+2][j+2] == tile:
                        self.win_status = tile
                        self.is_terminal = True
                        return tile
                except IndexError:
                    pass
                try:
                    # col 1 vertical win
                    if self.board[i][j+1] == tile and self.board[i+1][j+1] == tile and self.board[i+2][j+1] == tile:
                        self.win_status = tile
                        self.is_terminal = True
                        return tile
                except IndexError:
                    pass
                try:
                    # col 2 vertical win
                    if self.board[i][j+2] == tile and self.board[i+1][j+2] == tile and self.board[i+2][j+2] == tile:
                        self.win_status = tile
                        self.is_terminal = True
                        return tile
                except IndexError:
                    pass
                try:
                    # left upper diagonally win
                    if self.board[i][j] == tile and self.board[i+1][j+1] == tile and self.board[i+2][j+2] == tile:
                        self.win_status = tile
                        self.is_terminal = True
                        return tile
                except IndexError:
                    pass
        if empty_found:
            return 0
        else:
            self.win_status = -1
            self.is_terminal = True
            return -1

    #draws the board and puts images where the appropiate move was made
    def draw_board(self):
        
        for c in range(COLUMNS):
            for r in range(ROWS):
                pygame.draw.rect(screen,BACK, (width/2-175,100, 350,400))
                pygame.draw.line(screen, WHITE,(185+165,30+100),(185+165,30+390),6)
                pygame.draw.line(screen, WHITE,(185+265,30+100),(185+265,30+390),6)
                pygame.draw.line(screen, WHITE,(185+65,30+200),(185+365,30+200),6)
                pygame.draw.line(screen, WHITE,(185+65,30+300),(185+365,30+300),6)

        for c in range(COLUMNS):
            for r in range(ROWS):
                if self.board[r][c] == 1:
                    X_img = pygame.image.load('images/White-X.png')
                    screen.blit(X_img, (250+c*box_size,30+r*box_size+100))
                    
                elif self.board[r][c] == 2:
                    O_img = pygame.image.load('images/White-O.png')
                    screen.blit(O_img, (250+c*box_size,30+r*box_size+100))
                   

        pygame.display.update()



####################################################################################################################################################################
#                                                                                                                                                                  #
#                                                                                                                                                                  #
#                                                                       OTHELLO                                                                                    #
#                                                                     BOARD STATE                                                                                  #
#                                                                                                                                                                  #
#                                                                                                                                                                  #
####################################################################################################################################################################

class OthelloState(State):

    # initalises the board and assigns values to vars
    def __init__(self,player=1,board=None,last_move=None, game="Oth"):
        if board is None:
            self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
            self.board[3][3] = 1
            self.board[3][4] = 2
            self.board[4][3] = 2
            self.board[4][4] = 1
        else:
            self.board = board
        self.cur_player = player
        self.last_move = last_move
        self.win_status = self.check_win()
        self.game = game
        if self.win_status != 0:
            self.is_terminal = True
        else:
            self.is_terminal = False

    # takes a copy of the board, flips the appropiate pieces and returns the next state with the new move and pieces flipped as a new state
    def next_state(self,move):
        new_board = copy.deepcopy(self.board)
        assert isinstance(move, Move)
        new_board[move.row][move.col] = self.cur_player
        
        self.flip_pieces(new_board,move.row,move.col,self.cur_player)
        return OthelloState(3-self.cur_player, new_board, move)

    # finds all possible moves that can be made in the game by searching for a move in each direction
    def valid_moves(self):
        moves=[]
        for row in range(ROWS):
            for col in range(COLUMNS):
                if(self.board[row][col] == 0 ):
                    
                    N = self.legal_move(row,col,-1,0)
                    S = self.legal_move(row,col,1,0)
                    E = self.legal_move(row,col,0,1)
                    W = self.legal_move(row,col,0,-1)
                    NE = self.legal_move(row,col,-1,1)
                    NW = self.legal_move(row,col,-1,-1)
                    SE = self.legal_move(row,col,1,1)
                    SW = self.legal_move(row,col,1,-1)

                    if((N or S or E or W or NE or NW or SE or SW) == True):
                    
                        
                        moves.append(Move(row,col))
                        
        return moves

    #  finds the starting move and checks if next move turns it into an illegal move
    def legal_move(self,row,col,x,y):
        
        if row+x <0  or row+x>7:
            return False
        if col+y<0 or col+y>7:
            return False
        if self.board[row+x][col+y]!=3-self.cur_player:
            return False
        if row+x+x <0 or row+x+x>7:
            return False
        if col+y+y<0 or col+y+y>7:
            return False
        else:
            return self.find_end(row+x+x,col+y+y,x,y)

    #finds if there is an end position to a possible legal move. if there is the move is allowed
    def find_end(self,row,col,x,y):
        if row + x<0 or row+x>7:
            return False
        if col+y<0 or col+y>7:
            return False
        if(self.board[row][col] == 0):
            return False
        if(self.board[row][col] == self.cur_player):
            return True
        return self.find_end(row+x,col+y,x,y)

    #checks if any pieces in each direction can be flipped.
    def flip_pieces(self,board,row,col,player):
        self.flip(board,row,col,-1,0,player)
        self.flip(board,row,col,1,0,player)
        self.flip(board,row,col,0,1,player)
        self.flip(board,row,col,0,-1,player)
        self.flip(board,row,col,-1,1,player)
        self.flip(board,row,col,-1,-1,player)
        self.flip(board,row,col,1,1,player)
        self.flip(board,row,col,1,-1,player)

    #flips any of the pieces that need flipping
    def flip(self,board,row,col,x,y,player):
        if row + x<0 or row+x>7 or col+y<0 or col+y>7:
            return False
        if board[row][col] == 0:
            return False
        if board[row+x][col+y] == player:

            return True
        else:
            if self.flip(board,row+x,col+y,x,y,player):
                
                board[row+x][col+y]=player
                return True
            else:
                return

    #checks if there are any valid moves left in the game and if not counts up pieces per player and
    #assigns a win status depending on the outcome of the game based on wether it is a win or tie
    def check_win(self):
        empty_found = False
        winner = 0
        player1 = 0
        ai =0

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    empty_found = True
                if self.board[i][j] == 1:
                    player1 += 1
                elif self.board[i][j] == 2:
                    ai +=1
        if(len(self.valid_moves())>0):
            return 0
        else:

            if(player1>ai):
                winner = 1
                self.win_status = 1
                self.is_terminal = True

            elif(ai>player1):
                winner = 2
                self.win_status = 2
                self.is_terminal = True
            elif(ai==player1):
                winner = -1
                self.win_status = -1
                self.is_terminal = True
            
        return winner

    # draws the board using pygames in built functions 
    def draw_board(self):
        for c in range(COLUMNS):
            for r in range(ROWS):
                pygame.draw.rect(screen,BACK, (200+r*box_size,c*box_size+box_size+box_size, box_size,box_size))
                pygame.draw.circle(screen, Matte_GREEN,(int(200+r*box_size+box_size/2),int(c*box_size +box_size+box_size/2)),RADIUS)

        for c in range(COLUMNS):
            for r in range(ROWS):

                if self.board[r][c] == 1:
                    
                    pygame.draw.circle(screen, WHITE,(int(200+c*box_size+box_size/2),int(r*box_size+box_size+box_size/2)),RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen, BLACK,(int(200+c*box_size+box_size/2),int(r*box_size+box_size+box_size/2)),RADIUS)



####################################################################################################################################################################
#                                                                                                                                                                  #
#                                                                                                                                                                  #
#                                                                      INVASION                                                                                    #
#                                                                     GAME STATE                                                                                   #
#                                                                                                                                                                  #
#                                                                                                                                                                  #
####################################################################################################################################################################

class Invasion():
    invader = pygame.image.load('images/enemy.png')
    ship = pygame.image.load('images/ship.png')
    mcts_enemy = pygame.image.load('images/mcts-enemy.png')

    #initalises each var and assigns values to them, sets up arrays for bullets and positions of ship, enemies and mcts enemy and arrays to check if each one is alive.
    #sets starting positions of the enemies to be random across the top of screen.
    def __init__(self,shipX = width/2-10,shipY=height-68,move_left=False,move_right=False,shot=[],shot_ready=[], inv_alive =[], invaderX = [], invaderY = [], mcts_enemyX = [] ,mcts_alive = True, mcts_enemyY = [] ,bulletX = [],bulletY =[], is_terminal = False,game = "invasion",last_move = None,bullets_left=4):
        global total_invaders, bullets
        
        self.shipX = shipX
        self.shipY = shipY
        
        self.shot = shot
        self.shot_ready = shot_ready
        self.move_left = move_left
        self.move_right = move_right
        self.is_terminal = is_terminal
        self.game =game
        self.last_move = last_move
        
        self.invaderX = invaderX
        self.invaderY = invaderY
        self.inv_alive = inv_alive
        self.bullets_left = bullets_left

        #each time state gets called this empties array so it can be repopulated with increased number of enemies
        if len(invaderX) >0 and len(invaderY) >0 and len(inv_alive)>0:
            
            invaderX[:] = []
            invaderY[:] = []
            inv_alive[:] = []

        for x in range(total_invaders):

            self.invaderX.append(random.randint(width/4-20,width-(width/4)-10))
            self.invaderY.append(10)
            self.inv_alive.append(True)


        #resets the mcts enemy on each initalization
        self.mcts_enemyX = mcts_enemyX
        self.mcts_enemyY = mcts_enemyY
        if len(mcts_enemyX) > 0 and len(mcts_enemyY) > 0:
            mcts_enemyX[:] = []
            mcts_enemyY[:] = []

        if len(mcts_enemyX) < 1 and len(mcts_enemyY) < 1:
            self.mcts_enemyX.append(random.randint(width/4-20,width-(width/4)-10))
            self.mcts_enemyY.append(10)
        self.mcts_alive = mcts_alive
        

        #resets the bullets on each initalization
        self.bulletY = bulletY
        self.bulletX = bulletX
        if len(bulletX) >0 and len(bulletY) >0 and len(shot)>0:
            
            bulletX[:] = []
            bulletY[:] = []
            shot[:] = []
            shot_ready[:] = []
        for y in range(bullets):
            self.bulletY.append(375)
            self.bulletX.append(self.shipX)
            self.shot.append(False)
            self.shot_ready.append(True)


    #moves the character left 
    def MoveLeft(self):

        while self.move_left:
            if(self.shipX - 1 < width/4-20):
                break
            self.shipX = self.shipX - 1
            
            self.draw_board()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                        state.move_left = False




    #moves character right
    def MoveRight(self):
       while self.move_right:
            if(self.shipX + 1  >width-(width/4)-10):
                break
            self.shipX = self.shipX + 1
            
            self.draw_board()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    state.move_right = False

    #assigns the valid moves for random enemies and the mcts enemy and how fast they will move
    def valid_moves(self,current,enemy):
        moves = []
        if enemy == "invader":
            down = [self.invaderX[current],self.invaderY[current] +5 ]
            left_down =[self.invaderX[current] - 10, self.invaderY[current] + 5 ]
            right_down = [self.invaderX[current] + 10,self.invaderY[current] + 5 ]
            moves = [down,left_down,right_down]
        else:
            left = [self.mcts_enemyX[0] -  10,self.mcts_enemyY[0]]
            right = [self.mcts_enemyX[0] + 10,self.mcts_enemyY[0]]
            down = [self.mcts_enemyX[0],self.mcts_enemyY[0] + 7.5 ]
            left_down =[self.mcts_enemyX[0] - 10 ,self.mcts_enemyY[0] + 7.5]
            right_down = [self.mcts_enemyX[0] +10 ,self.mcts_enemyY[0] + 7.5]
            moves = [left,right,down,left_down,right_down]
        return moves

    #applies the move to each enemy if inside of the game window
    def next_invader_state(self,move,current):
        
        if 590 > move[0] > 180:
            self.invaderX[current] = move[0]
        if 380 > move[1] > 0:
            self.invaderY[current] = move[1]

    #applies the move to each enemy if inside of the game window
    def next_state(self,move):

        if 590 > move[0] > 180:
            self.mcts_enemyX[0] = move[0]
        if 380 > move[1] > 0:
            self.mcts_enemyY[0] = move[1]

        # if self.invaderY > 360:
        #     self.lives = self.lives - 1

        

    #draws the board for invasion, draws each enemy,player and bullet to the screen
    #also draws the score your currently on and the amount of lives you have.
    def draw_board(self):
        global lives, score
        life =pygame.image.load('images/lives.png')
        bullet = pygame.image.load('images/bullet.png')

        screen.fill(BACK,(705,0,90,80))

        score_text = font2.render("{}".format(score),True,WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (745,41)
        screen.blit(score_text,score_text_rect)

        for i in range(self.bullets_left):
            screen.blit(bullet,((705+(i*20)),57))
        for i in range(lives):

            screen.blit(life,((710+(i*25)),7))
        screen.fill(BLACK,(180,0,440,450))
        
        pygame.draw.line(screen,WHITE,(width/4-20,height-70),(width-width/4+20,height-70),3)
        pygame.draw.line(screen,WHITE,(width/4-20,0),(width/4-20,height),3)
        pygame.draw.line(screen,WHITE,(width-width/4+20,0),(width-width/4+20,height),3)
        screen.blit(self.ship,(self.shipX,self.shipY))
        for x in range(total_invaders):
            if self.inv_alive[x]:
                screen.blit(self.invader,(self.invaderX[x],self.invaderY[x]))
        if self.mcts_alive:
            screen.blit(self.mcts_enemy,(self.mcts_enemyX[0],self.mcts_enemyY[0]))
        for y in range(bullets):

                if self.shot[y]:

                    pygame.draw.rect(screen,WHITE,(self.bulletX[y]+16,self.bulletY[y],4,8))

    #moves the bullet if one has been shot
    def bullet_move(self,cur):
        
        if self.shot[cur]:

            self.bulletY[cur] = self.bulletY[cur] - 5

            if self.bulletY[cur] <1:
                self.bullets_left += 1
                self.shot_ready[cur] = True
                self.shot[cur] = False
                self.bulletY[cur] = 375


    #checks if the bullet has hit an enemy based of the distance formula
    def check_hit(self,current,cur):
        global enemy
        if enemy == "invader":
            distance = math.sqrt((math.pow(self.invaderX[current]-self.bulletX[cur],2)) + (math.pow(self.invaderY[current] - self.bulletY[cur],2)))
        else:
            distance = math.sqrt((math.pow(self.mcts_enemyX[current]-self.bulletX[cur],2)) + (math.pow(self.mcts_enemyY[current] - self.bulletY[cur],2)))
        if distance < 27:
            return True
        else:
            return False




####################################################################################################################################################################
#                                                                                                                                                                  #
#                                                                                                                                                                  #
#                                                                     MONTE CARLO TREE SIMULATION                                                                  #
#                                                                           and NODE CLASSES                                                                       #
#                                                                                                                                                                  #
#                                                                                                                                                                  #
####################################################################################################################################################################

# a tree node for MCTS, contains scoring valuespla
class Node:
    #intialises the node and assigns it values
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.score = 0
        self.visits = 0
        self.expanded = False

    # returns the UCB1 of a node, or infinity of the node's visit count is 0
    # Set to 1.41 as it satisfies the hoffdeinger inequality
    def get_ucb1(self):
        if self.visits == 0:
            return float('inf')
        else:
            return self.score/self.visits + math.sqrt(1.41*math.log(self.parent.visits)/self.visits)

#class for the monte carlo tree simulation
class MCTS:

    # intialises the root state 
    def __init__(self, root):
        self.root = root

    # sets the current node to root and runs simulations of the four main stages of mcts, each with its own method and returns the best move.
    # This method from ssode was broken, i have fixed it and it runs excellently now.
    def run(self, iterations):
        
        for _ in range(iterations):
            
            node = self.root
            while(node.expanded):
                node = self.select(node)

            if(node.state.is_terminal):
                self.backpropagate(node, node.state.win_status)
            else:
                self.expand(node)
                node = random.choice(node.children)
                winner = self.playout(node)
                self.backpropagate(node, winner)


        best_move = max(self.root.children, key=lambda n: n.visits)
        return best_move.state.last_move

    # returns the first of the node's children when sorted by highest to lowest UCB1
    def select(self, node):

        if not len(node.children) == 0:
            return sorted(node.children, key=lambda n: n.get_ucb1(), reverse=True)[0]
        else:
            raise RuntimeError(f"choose called on terminal node {node}")


    # expands a node, creating all of its possible children
    # since a deep copy is not taken in valid moves for invasion one is taken here instead, it still behaves exactly the same as zero sum
    def expand(self, node):
        if node.state.game == "invasion":
            global enemy 
            if not node.expanded:
                for move in node.state.valid_moves(0,enemy):
                    temp_state = copy.deepcopy(node.state)
                    temp_state.next_state(move)
                    temp_state.last_move = move
                    node.children.append(Node(temp_state, node))
                    node.expanded = True   
        else:
            if not node.expanded:
                for move in node.state.valid_moves():
                    node.children.append(Node(node.state.next_state(move), node))
                    node.expanded = True


                   


    # plays out a random game starting from the given node
    # slight varients needed for different games just one or two extra steps
    # in Othello pieces need to be flipped
    # in invasion the random moves of the player need to happen, it chooses by repeatedly chosing random values between the ship and the mcts enemy. 
    def playout(self, node):
        
        
        temp_state = copy.deepcopy(node.state)
        
        if temp_state.game == "oth":
            our_player = self.root.state.cur_player
            while not temp_state.is_terminal:
                move = random.choice(temp_state.valid_moves())
                temp_state.board[move.row][move.col] = temp_state.cur_player
                temp_state.flip_pieces(temp_state.board,move.row,move.col,temp_state.cur_player)
                temp_state.cur_player = 3 - temp_state.cur_player
                temp_state.check_win()
            return temp_state.win_status
        elif temp_state.game == "invasion":
            while not temp_state.is_terminal:
                global enemy, bullets
                if enemy == "mcts":
                    move = random.choice(temp_state.valid_moves(0,enemy))
                    temp_state.next_state(move)
                    for cur in range(bullets):
                        temp_state.bullet_move(cur)
                        if temp_state.check_hit(0,cur):
                            return temp_state.mcts_enemyY[0] - 5

                            
                    if temp_state.shipX > temp_state.mcts_enemyX[0]:
                        temp_state.shipX = random.randint(width/4-20,int(temp_state.shipX))
                        for x in range(bullets):
                            if (not temp_state.shot[x]) and temp_state.shot_ready[x] == True:
                                
                                temp_state.shot_ready[x] = False
                                temp_state.shot[x] = True
                                temp_state.bulletX[x] = temp_state.shipX
                                break
                    elif temp_state.shipX < temp_state.mcts_enemyX[0]:
                        temp_state.shipX = random.randint(int(temp_state.shipX),width-(width/4)-10)
                        for x in range(bullets):
                            if (not temp_state.shot[x]) and temp_state.shot_ready[x] == True:
                                
                                temp_state.shot_ready[x] = False
                                temp_state.shot[x] = True
                                temp_state.bulletX[x] = temp_state.shipX
                                break
                    if temp_state.mcts_enemyY[0] > 350:
                        temp_state.win_status = temp_state.mcts_enemyY[0]
                        temp_state.is_terminal = True
                    temp_state.win_status = temp_state.mcts_enemyY[0]
            return temp_state.win_status
        else:
            our_player = self.root.state.cur_player
            while not temp_state.is_terminal:
                move = random.choice(temp_state.valid_moves())
                temp_state.board[move.row][move.col] = temp_state.cur_player
                temp_state.cur_player = 3 - temp_state.cur_player
                temp_state.check_win()
            return temp_state.win_status


    # propagates the information from the playout back up the tree
    # slightly differnt values assigned as ivasion is non finite seperate reward values need to be in place
    # as its not as simple as 1 or 0 or -1 for win loss and draw
    def backpropagate(self, node, winner):
        if node.state.game == "invasion":
            while node is not None:
                node.visits +=1
                node.score +=winner
                node = node.parent
        else:
            while node is not None:
                if node.state.cur_player == 3-winner:
                    node.score += 2
                elif winner == -1:
                    node.score +=1
                node.visits += 2
                node = node.parent



####################################################################################################################################################################
#                                                                                                                                                                  #
#                                                                                                                                                                  #
#                                                                     GAME INTRO AND                                                                               #
#                                                                     TESTING METHODS                                                                              #
#                                                                                                                                                                  #
#                                                                                                                                                                  #
####################################################################################################################################################################


# runs the introduction screen of the game and allows you to choose which game you want to play.
def game_intro():
    game_intro = True
    screen.fill(BACK)
    while game_intro:


        TTTimg = pygame.image.load('images/TTT.jpg')
        Othimg =  pygame.image.load('images/othello.jpg')
        Con4img = pygame.image.load('images/Con4.jpg')
        spaceimg =  pygame.image.load('images/invasion.jpg')

        screen.blit(TTTimg, (width/2 - 200, height/2+55))
        screen.blit(Con4img, (width/2 + 75, height/2+55))
        screen.blit(Othimg, (width/2 + 75 , height/2-110))
        screen.blit(spaceimg, (width/2 - 200, height/2-110))

        font = pygame.font.Font('freesansbold.ttf', 48)
        text = font.render("Pick Your Game",True,txt_col)
        textRect = text.get_rect()
        textRect.center = (int(width/2), height/2 - 150)
        screen.blit(text,textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_x = event.pos[0]
                click_y = event.pos[1]

                if  (width/2 - 200+150) > click_x > (width/2 - 200)  and (height/2+55+150) > click_y > (height/2+55):
                    game = "ttt"
                    game_intro = False
                    screen.fill((BACK))

                elif (width/2 +75+150) > click_x > (width/2 +75)  and (height/2+55+150) > click_y > (height/2+55):
                    game = "con4"
                    game_intro = False
                    screen.fill((BACK))

                elif (width/2 - 200 +150) > click_x > (width/2 -200)  and (height/2-110+150) > click_y > (height/2-110):
                    game = "invasion"
                    game_intro = False
                    screen.fill((BACK))

                elif (width/2 +75+150) > click_x > (width/2 +75)  and (height/2+150-110) > click_y > (height/2-110) :
                    game = "oth"
                    game_intro = False
                    screen.fill((BACK))#


        pygame.display.update()
    return game

# This allows you to choose if you want to go first or second on any of the board games available.
def choose_start():
    screen.fill((BACK))
    pygame.display.update()
    
    font = pygame.font.Font("freesansbold.ttf", 40)
    font2 = pygame.font.Font("freesansbold.ttf", 20)

    while True:
        textnum = font.render("Choose who goes first! ",True,txt_col)
        
        textnum_rect = textnum.get_rect()
        textnum_rect.center = (int(width/2), height/2 - 150)
        screen.blit(textnum,textnum_rect)
        mouse = pygame.mouse.get_pos()

        if 260+100>mouse[0]>260 and 200+30>mouse[1]>200:
            pygame.draw.rect(screen,(61,118,61),(260,200,100,30))
        else:
            pygame.draw.rect(screen,Matte_GREEN,(260,200,100,30))

        if 450+100>mouse[0]>450 and 200+30>mouse[1]>200:
            pygame.draw.rect(screen,(182,32,32),(450,200,100,30))
        else:
            pygame.draw.rect(screen,Matte_RED,(450,200,100,30))

        chosen1 = font2.render("PLAYER",True,BLACK)
        chosen2 = font2.render("AI",True,BLACK)
        chosen1_rect = chosen1.get_rect()
        chosen2_rect = chosen2.get_rect()
        chosen1_rect.center = (310,217)
        chosen2_rect.center = (500,217)

        screen.blit(chosen1,chosen1_rect)
        screen.blit(chosen2,chosen2_rect)

        pygame.display.update()


        for evt in pygame.event.get():
  
            if evt.type == pygame.QUIT:
                return
            elif evt.type == pygame.MOUSEBUTTONDOWN:
                click_x = evt.pos[0]
                click_y = evt.pos[1]

                if 260+100>click_x>260 and 200+30>click_y>200:
                    screen.fill((BACK))
                    return False,True

                if 450+100>click_x>450 and 200+30>click_y>200:
                    screen.fill((BACK))
                    return True,False

# this method allows your to pick your difficulty or the amout of simulations you want to run for the mcts.
# easy has been set to 50 as testers were not beating it and getting frustrated, 
# hard has been set to 2000,1000,500 respectively and will pretty much never lose, ive yet to see a tester or myself beat the hard bots

def mcts_sims(game):
    mcts_sims = ""
    accepted = False
    font = pygame.font.Font("freesansbold.ttf", 40)
    font2 = pygame.font.Font("freesansbold.ttf", 20)
    screen.fill((BACK))
    coun = 0

    for y in range(4):
        for x in range(3):
            
            if y == 3:
                if x == 0:
                    coun ="C"
                elif x ==1:
                    coun = 0
                elif x ==2:
                    coun = "del"
            else:
                coun +=1
            
            num = littlefont.render("{}".format(coun),True,BLACK)
            num_rect = num.get_rect()
            varX =60*x + 35
            varY =57*y+250
            num_rect.center = (varX,varY)
            pygame.draw.circle(screen,WHITE,(varX,varY),25)
            screen.blit(num,num_rect)

    pygame.display.update()
    while True:
        textnum = font.render("enter mcts sims ",True,txt_col)
        textnum2 =  font.render("or choose difficulty:",True,txt_col)
        textnum_rect = textnum.get_rect()
        textnum_rect.center = (int(width/2), height/2 - 150)
        textnum_rect2 = textnum2.get_rect()
        textnum_rect2.center = (int(width/2), height/2 - 110)
        screen.blit(textnum,textnum_rect)
        screen.blit(textnum2,textnum_rect2)
        mouse = pygame.mouse.get_pos()

        if 260+100>mouse[0]>260 and 200+30>mouse[1]>200:
            pygame.draw.rect(screen,(61,118,61),(260,200,100,30))
        else:
            pygame.draw.rect(screen,Matte_GREEN,(260,200,100,30))

        if 450+100>mouse[0]>450 and 200+30>mouse[1]>200:
            pygame.draw.rect(screen,(182,32,32),(450,200,100,30))
        else:
            pygame.draw.rect(screen,Matte_RED,(450,200,100,30))

        easy_diff = font2.render("EASY",True,BLACK)
        hard_diff = font2.render("HARD",True,BLACK)
        easy_diff_rect = easy_diff.get_rect()
        hard_diff_rect = hard_diff.get_rect()
        easy_diff_rect.center = (310,217)
        hard_diff_rect.center = (500,217)

        screen.blit(easy_diff,easy_diff_rect)
        screen.blit(hard_diff,hard_diff_rect)








        for evt in pygame.event.get():
   
            if evt.type == pygame.QUIT:
                    return
            elif evt.type == pygame.MOUSEBUTTONDOWN:
                click_x = evt.pos[0]
                click_y = evt.pos[1]

                if 260+100>click_x>260 and 200+30>click_y>200:
                    screen.fill((BACK))
                    if game == 'ttt':
                        mcts_sims = "50"
                    elif game == 'con4':
                        mcts_sims = "50"
                    elif game == 'oth':
                        mcts_sims ="50"
                    return mcts_sims

                if 450+100>click_x>450 and 200+30>click_y>200:
                    screen.fill((BACK))
                    if game == 'ttt':
                        mcts_sims = "2000"
                    elif game == 'con4':
                        mcts_sims = "1000"
                    elif game == 'oth':
                         mcts_sims = "500"
                    return mcts_sims

                if 35+25>click_x>10 and 250+25 >click_y >225:
                    if len(mcts_sims) <8:
                        screen.fill(BACK,(260,250,290,80))
                        mcts_sims += "1"
                        accepted = True
                if 95+25>click_x>70 and 250+25 >click_y >225:
                    if len(mcts_sims) <8:
                        screen.fill(BACK,(260,250,290,80))
                        mcts_sims += "2"
                        accepted = True
                if 155+25>click_x>130 and 250+25 >click_y >225:
                    if len(mcts_sims) <8:
                        screen.fill(BACK,(260,250,290,80))
                        mcts_sims += "3"
                        accepted = True
                if 35+25>click_x>10 and 307+25 >click_y >282:
                    if len(mcts_sims) <8:
                        screen.fill(BACK,(260,250,290,80))
                        mcts_sims += "4"
                        accepted = True
                if 95+25>click_x>70 and 307+25 >click_y >282:
                    if len(mcts_sims) <8:
                        screen.fill(BACK,(260,250,290,80))
                        mcts_sims += "5"
                        accepted = True
                if 155+25>click_x>130 and 307+25 >click_y >282:
                    if len(mcts_sims) <8:
                        screen.fill(BACK,(260,250,290,80))
                        mcts_sims += "6"
                        accepted = True
                if 35+25>click_x>10 and 364+25 >click_y >339:
                    if len(mcts_sims) <8:
                        screen.fill(BACK,(260,250,290,80))
                        mcts_sims += "7"
                        accepted = True
                if 95+25>click_x>70 and 364+25 >click_y >339:
                    if len(mcts_sims) <8:
                        screen.fill(BACK,(260,250,290,80))
                        mcts_sims += "8"
                        accepted = True
                if 155+25>click_x>130 and 364+25 >click_y >339:
                    if len(mcts_sims) <8:
                        screen.fill(BACK,(260,250,290,80))
                        mcts_sims += "9"
                        accepted = True
                if 35+25>click_x>10 and 421+25 >click_y >396:
                    mcts_sims = "" 
                    screen.fill(BACK,(260,250,290,80))
                    accepted = False
                if 95+25>click_x>70 and 421+25 >click_y >396:
                    if len(mcts_sims) <8:
                        screen.fill(BACK,(260,250,290,80))
                        mcts_sims += "0"
                        accepted = True
                if 155+25>click_x>130 and 421+25 >click_y >396:
                    mcts_sims = mcts_sims[:-1]
                    if mcts_sims == "":
                        accepted = False
                    screen.fill(BACK,(260,250,290,80))




                if  (width/2) - 65+135 > click_x > (width/2) - 65 and height/2 + 150 +30 > click_y > height/2 + 150:
                    if accepted == True:
                        screen.fill((BACK))
                        return mcts_sims
                    else:
                        in_error = font2.render("Please enter a number: ",True,RED)
                        in_error_rect = textnum.get_rect()
                        in_error_rect.center = (450,275)
                        screen.blit(in_error,in_error_rect)




                        

        block = font.render(mcts_sims, True, (169,169,169))
        rect = block.get_rect()
        rect.center = (400,300)
        screen.blit(block, rect)
        pygame.display.flip()
        pygame.draw.rect(screen,WHITE, ((width/2) - 65, height/2 + 150,135,30))

        if (width/2) - 65+135>mouse[0]>(width/2) - 65 and height/2 + 150 +30>mouse[1]>height/2 + 150:
            pygame.draw.rect(screen,(169,169,169), ((width/2) - 65, height/2 + 150,135,30))
        else:
            pygame.draw.rect(screen,WHITE, ((width/2) - 65, height/2 + 150,135,30))
        enter_text = font2.render("Enter",True,BLACK)
        enter_text_rect = enter_text.get_rect()
        enter_text_rect.center = (int(width/2), height/2 + 165)
        screen.blit(enter_text,enter_text_rect)


    return mcts_sims

# this method tests all the different variations of the games and how the mcts performs and outputs it to file
def testing(self):
    if game == 'ttt':

        state = TTTState()

        player1=0
        player2=0
        draw = 0
        count = 0
        ## mcts vs random
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(itr)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = random.choice(state.valid_moves())
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = TTTState()
            
        file = open("results.txt.txt","w+")
        file.write("                    Tic Tac Toe                                 \n")
        file.write("############################################################### \n")
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went first \n \n".format(player1,itr))
        file.write("Random bot won: {} times! The bot had random moves and went second \n \n".format(player2))
        file.write("It was a Draw: {} times! Mcts Easy bot had {} Sims and the random bot had random moves \n \n".format(draw,itr))
        file.close()

        player1=0
        player2=0
        draw = 0
        count = 0
        ## random vs mcts
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = random.choice(state.valid_moves())
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(itr)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = TTTState()

        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Random bot won: {} times! The bot had random moves and went first \n \n".format(player1))
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went second \n \n".format(player2,itr))
        file.write("It was a Draw: {} times! The random bot had random moves and Mcts Easy bot had {} Sims \n \n".format(draw,itr))

        player1=0
        player2=0
        draw = 0
        count =0
        ## mcts easy vs mcts hard
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(itr)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(2000)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = TTTState()
            
        file = open("results.txt","a+")
        file.write(" \n")
        file.write("############################################################### \n \n")
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went first \n \n".format(player1,itr))
        file.write("Mcts Hard bot won: {} times! The bot had 2000 Simulations and went second \n \n".format(player2))
        file.write("It was a Draw: {} times! Mcts Easy bot had {} Sims and Mcts Hard bot had 2500 Sims \n \n".format(draw,itr))

        player1=0
        player2=0
        draw = 0
        count =0
        ## mcts hard vs mcts easy
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(2000)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(itr)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = TTTState()
            
        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Mcts Hard bot won: {} times! The bot had 2000 Simulations and went First\n \n".format(player1))
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went Second \n \n".format(player2,itr))
        file.write("It was a Draw: {} times! Mcts Hard bot had 2000 Sims and Mcts Easy bot had {} Sims  \n".format(draw,itr))
        file.write("############################################################### \n \n")

        player1=0
        player2=0
        draw = 0
        state = TTTState()
        ## mcts hard vs mcts easy
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(itr)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(itr)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = TTTState()
            
        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Mcts bot 1 won: {} times! The bot had {} Simulations and went First\n \n".format(player1,itr))
        file.write("Mcts bot 2 won: {} times! The bot had {} Simulations and went Second \n \n".format(player2,itr))
        file.write("It was a Draw: {} times! Mcts botd had the same number of Sims at {}!  \n".format(draw,itr))
        file.write("############################################################### \n")

    elif game == 'con4':
        state = Con4State()

        player1=0
        player2=0
        draw = 0
        count = 0
        ## mcts vs random
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(itr)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = random.choice(state.valid_moves())
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = Con4State()
            
        file = open("results.txt","a+")
        file.write("\n\n\n\n                         Connect 4                              \n")
        file.write("############################################################### \n")
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went first \n \n".format(player1,itr))
        file.write("Random bot won: {} times! The bot had random moves and went second \n \n".format(player2))
        file.write("It was a Draw: {} times! Mcts Easy bot had {} Sims and the random bot had random moves \n \n".format(draw,itr))
        file.close()

        player1=0
        player2=0
        draw = 0
        state = Con4State()
        ## random vs mcts
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = random.choice(state.valid_moves())
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(itr)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = Con4State()

        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Random bot won: {} times! The bot had random moves and went first \n \n".format(player1))
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went second \n \n".format(player2,itr))
        file.write("It was a Draw: {} times! The random bot had random moves and Mcts Easy bot had {} Sims \n \n".format(draw,itr))

        player1=0
        player2=0
        draw = 0
        state = Con4State()
        ## mcts easy vs mcts hard
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(itr)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(1000)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = Con4State()
            
        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went first \n \n".format(player1,itr))
        file.write("Mcts Hard bot won: {} times! The bot had 1000 Simulations and went second \n \n".format(player2))
        file.write("It was a Draw: {} times! Mcts Easy bot had {} Sims and Mcts Hard bot had 1500 Sims \n \n".format(draw,itr))

        player1=0
        player2=0
        draw = 0
        state = Con4State()
        ## mcts hard vs mcts easy
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(1000)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(itr)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = Con4State()
            
        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Mcts Hard bot won: {} times! The bot had 1000 Simulations and went First\n \n".format(player1))
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went Second \n \n".format(player2,itr))
        file.write("It was a Draw: {} times! Mcts Hard bot had 1000 Sims and Mcts Easy bot had {} Sims  \n".format(draw,itr))
        file.write("############################################################### \n")

        player1=0
        player2=0
        draw = 0
        state = Con4State()
        ## mcts hard vs mcts easy
        for i in range(10):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(itr)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(itr)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = Con4State()
            
        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Mcts bot 1 won: {} times! The bot had {} Simulations and went First\n \n".format(player1,itr))
        file.write("Mcts bot 2 won: {} times! The bot had {} Simulations and went Second \n \n".format(player2,itr))
        file.write("It was a Draw: {} times! Mcts botd had the same number of Sims at {}!  \n".format(draw,itr))
        file.write("############################################################### \n")

    elif game == 'oth':
        state = OthelloState()

        player1=0
        player2=0
        draw = 0
        count = 0
        ## mcts vs random
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(itr)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = random.choice(state.valid_moves())
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = OthelloState()
            
        file = open("results.txt","a+")
        file.write("\n\n\n\n                         Othello                              \n")
        file.write("############################################################### \n")
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went first \n \n".format(player1,itr))
        file.write("Random bot won: {} times! The bot had random moves and went second \n \n".format(player2))
        file.write("It was a Draw: {} times! Mcts Easy bot had {} Sims and the random bot had random moves \n \n".format(draw,itr))
        file.close()

        player1=0
        player2=0
        draw = 0
        state = OthelloState()
        ## random vs mcts
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = random.choice(state.valid_moves())
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(itr)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = OthelloState()

        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Random bot won: {} times! The bot had random moves and went first \n \n".format(player1))
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went second \n \n".format(player2,itr))
        file.write("It was a Draw: {} times! The random bot had random moves and Mcts Easy bot had {} Sims \n \n".format(draw,itr))

        player1=0
        player2=0
        draw = 0
        state = OthelloState()
        ## mcts easy vs mcts hard
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(itr)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(500)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = OthelloState()
            
        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went first \n \n".format(player1,itr))
        file.write("Mcts Hard bot won: {} times! The bot had 500 Simulations and went second \n \n".format(player2))
        file.write("It was a Draw: {} times! Mcts Easy bot had {} Sims and Mcts Hard bot had 1000 Sims \n \n".format(draw,itr))

        player1=0
        player2=0
        draw = 0
        state = OthelloState()
        ## mcts hard vs mcts easy
        for i in range(100):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(500)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(itr)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = OthelloState()
            
        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Mcts Hard bot won: {} times! The bot had 500 Simulations and went First\n \n".format(player1))
        file.write("Mcts Easy bot won: {} times! The bot had {} Simulations and went Second \n \n".format(player2,itr))
        file.write("It was a Draw: {} times! Mcts Hard bot had 500 Sims and Mcts Easy bot had {} Sims  \n".format(draw,itr))
        file.write("############################################################### \n")

        player1=0
        player2=0
        draw = 0
        state = OthelloState()
        ## mcts hard vs mcts easy
        for i in range(10):
            count += 1
            print(game,count)
            while not state.is_terminal:
                move = MCTS(Node(state)).run(itr)
                state = state.next_state(move)
                state.check_win()
                if state.is_terminal:
                    break
                move2 = MCTS(Node(state)).run(itr)
                state = state.next_state(move2)
                state.check_win()

            if(state.win_status==1):
                player1 += 1
            elif(state.win_status==2):
                player2 += 1
            else:
                draw += 1

            state = OthelloState()
            
        file = open("results.txt","a+")
        file.write("############################################################### \n \n")
        file.write("Mcts bot 1 won: {} times! The bot had {} Simulations and went First\n \n".format(player1,itr))
        file.write("Mcts bot 2 won: {} times! The bot had {} Simulations and went Second \n \n".format(player2,itr))
        file.write("It was a Draw: {} times! Mcts botd had the same number of Sims at {}!  \n".format(draw,itr))
        file.write("############################################################### \n")



####################################################################################################################################################################
#                                                                                                                                                                  #
#                                                                                                                                                                  #
#                                                                     MAIN SECTION WHERE                                                                           #
#                                                                      EVERYTHING RUNS                                                                             #
#                                                                                                                                                                  #
#                                                                                                                                                                  #
####################################################################################################################################################################


#initalises the screen and sets up fonts to be used    
pygame.init()
size = (width,height)
screen = pygame.display.set_mode(size)
font2 = pygame.font.Font("freesansbold.ttf", 20)
bigfont = pygame.font.Font('freesansbold.ttf', 32)
littlefont = pygame.font.Font('freesansbold.ttf', 22)
tinyfont = pygame.font.Font('freesansbold.ttf', 21)

#this is the main area where the project starts off

if __name__ == "__main__":

    quit_game = False
    
    while not quit_game:
        quit = False
        while not quit:
            game = game_intro()

            ####################################################################################################################################################################
            #                                                                                                                                                                  #
            #                                                                                                                                                                  #
            #                                                                      CONNECT 4                                                                                   #
            #                                                                        GAME                                                                                      #
            #                                                                                                                                                                  #
            #                                                                                                                                                                  #
            ####################################################################################################################################################################
 
            #plays the connect 4 game
            if game == "con4":
                box_size = 50
                RADIUS = int(box_size/2 -4)
                ROWS = 6
                COLUMNS = 7
                

                itr = mcts_sims(game)
                itr = int(itr)

                ai_turn , player_turn =choose_start()

                state = Con4State()
                state.draw_board()

                text_game = bigfont.render("Connect4",True,txt_col)
                text_mcts = littlefont.render("mcts:{} iterations".format(itr),True,txt_col)
                text_game_Rect = text_game.get_rect()
                text_mcts_Rect = text_mcts.get_rect()
                text_game_Rect.center = (int(width/2), height/2-205)
                text_mcts_Rect.center = (int(width/2), height/2-175)
                screen.blit(text_game,text_game_Rect)
                screen.blit(text_mcts,text_mcts_Rect)
                pygame.display.update()
                
                #uncomment code below if you want to run testing on this game, it may take a while probably about 30 mins for this game.
                #testing(state)
                
                # while game not over run game
                while not state.is_terminal:
                    mouse = pygame.mouse.get_pos()
                    if (10+60) > mouse[0] > 10 and 10+30 > mouse[1] > 10:
                        pygame.draw.rect(screen,(168,168,168), (10, 10,60,30))
                    else:
                        pygame.draw.rect(screen,WHITE, (10, 10,60,30))

                    quit_text = font2.render("Quit",True,BLACK)
                    quit_text_rect = quit_text.get_rect()
                    quit_text_rect.center = (40,25)
                    screen.blit(quit_text,quit_text_rect)

                    #runs while there is something happening in game whether mouse move or button press
                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            sys.exit()
                        pygame.time.wait(100)
                        screen.fill(BACK, (0, 60, 800,30 ))
                        text_turn = littlefont.render("Your Turn",True,BLACK)
                        text_turn_Rect = text_turn.get_rect()
                        text_turn_Rect.center = (int(width/2), height/2-145)
                        screen.blit(text_turn,text_turn_Rect)
                        
                        # if quit is clicked exit to choose game menu
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            click_x = event.pos[0]
                            click_y = event.pos[1]
                            if  (10+60) > click_x > 10 and 10+30 > click_y > 10:

                                quit = True
                                break
                            # if button press and your move try make move where button was pressed
                            if player_turn:

                                posx =event.pos[0] - 220
                                col = int(math.floor(posx/box_size))

                                #if move chosen is allowed make the move and allow ai turn to play
                                for move in state.valid_moves():
                                    if move.col == col:
                                        state = state.next_state(move)
                                        state.draw_board()
                                        state.check_win()
                                        
                                        ai_turn = True
                                        player_turn = False

                                       
                                        break
                        #make ai move 
                        if(ai_turn and state.check_win() ==0):
                            screen.fill(BACK, (0, 60, 800,30 ))
                            
                            text_turn = littlefont.render("AI's Turn",True,WHITE)
                            text_turn_Rect = text_turn.get_rect()
                            text_turn_Rect.center = (int(width/2), height/2 - 145)
                            screen.blit(text_turn,text_turn_Rect)
                            
                            #runs the mcts and picks move
                            move = MCTS(Node(state)).run(itr)
                            state = state.next_state(move)
                            
                            state.draw_board()
                            state.check_win()
                            
                            ai_turn =False
                            player_turn = True


                    pygame.display.update()
                    if quit:
                        break
                if quit:
                    break
                pygame.draw.rect(screen,(BACK),text_game_Rect)
                pygame.draw.rect(screen,(BACK),text_mcts_Rect)
                pygame.display.update()
                screen.fill(BACK, (0, 60, 800,30 ))

               #displays end result to the screen and brings you back to choose game menu
                if(state.win_status == 1):
                    if ai_turn == False:
                        text = bigfont.render("AI Wins!".format(state.win_status),True,RED)
                    else:
                        text = bigfont.render("Player {} wins!".format(state.win_status),True,RED)
                elif(state.win_status == -1):
                    text = bigfont.render("Draw Game",True,txt_col)
                else:
                    if ai_turn == False:
                        text = bigfont.render("AI Wins!".format(state.win_status),True,YELLOW)
                    else:
                        text = bigfont.render("Player {} wins!".format(state.win_status),True,YELLOW)   
                textRect = text.get_rect()
                textRect.center = (int(width/2), height/2 - 165)
                screen.blit(text,textRect)

                pygame.display.update()
                pygame.time.wait(3000)


            ####################################################################################################################################################################
            #                                                                                                                                                                  #
            #                                                                                                                                                                  #
            #                                                                     TIC TAC TOE                                                                                  #
            #                                                                         GAME                                                                                     #
            #                                                                                                                                                                  #
            #                                                                                                                                                                  #
            ####################################################################################################################################################################

            #sets tictactoe game up
            elif game == "ttt":
                
                box_size = 100

                itr = mcts_sims(game)
                itr = int(itr)

                ai_turn , player_turn =choose_start()

                
                ROWS = 3
                COLUMNS = 3
                
                state = TTTState()
                state.draw_board()

                text_game = bigfont.render("TicTacToe",True,txt_col)
                text_mcts = littlefont.render("mcts:{} iterations".format(itr),True,txt_col)
                text_game_Rect = text_game.get_rect()
                text_mcts_Rect = text_mcts.get_rect()
                text_game_Rect.center = (int(width/2), height/2-205)
                text_mcts_Rect.center = (int(width/2), height/2-175)
                screen.blit(text_game,text_game_Rect)
                screen.blit(text_mcts,text_mcts_Rect)
                pygame.display.update()

                #uncomment code below if you want to run testing on this game, it may take a while probably about 5 mins for this game.
                #testing(state)
                
                #run while game is not over
                while not state.is_terminal:
                    mouse = pygame.mouse.get_pos()
                    if (10+60) > mouse[0] > 10 and 10+30 > mouse[1] > 10:
                        pygame.draw.rect(screen,(168,168,168), (10, 10,60,30))
                    else:
                        pygame.draw.rect(screen,WHITE, (10, 10,60,30))

                    quit_text = font2.render("Quit",True,BLACK)
                    quit_text_rect = quit_text.get_rect()
                    quit_text_rect.center = (40,25)
                    screen.blit(quit_text,quit_text_rect)
                    pygame.display.update()
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            sys.exit()
                        
                        pygame.time.wait(100)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            click_x = event.pos[0]
                            click_y = event.pos[1]
                             # if quit is clicked exit to choose game menu
                            if  (10+60) > click_x > 10 and 10+30 > click_y > 10:
                                quit = True
                                break
                            
                            if player_turn:
                                posx = event.pos[0]
                                posy = event.pos[1]

                                #checks if on screen click was in any of the boxes on the board, checks if it was allowed and makes the move. sets it to be ai's turn
                                for move in state.valid_moves():
                                    if 185+165 > posx >185+ 65 and 30+200 > posy > 30+100 and state.board[0][0] == 0 :
                                        move.row = 0
                                        move.col = 0
                                        state = state.next_state(move)
                                        state.draw_board()
                                        ai_turn = True
                                        player_turn = False
                                        screen.fill(BACK, (0, 60, 800,30 ))
                                        text_turn = littlefont.render("AI's Turn",True,BLACK)
                                        text_turn_Rect = text_turn.get_rect()
                                        text_turn_Rect.center = (int(width/2), height/2-145)
                                        screen.blit(text_turn,text_turn_Rect)
                                        pygame.display.update()

                                        break
                                    elif 185+165 > posx > 185+65 and 30+300 > posy > 30+200 and state.board[1][0] == 0:
                                        move.row = 1
                                        move.col = 0
                                        state = state.next_state(move)
                                        state.draw_board()
                                        ai_turn = True
                                        player_turn = False
                                        screen.fill(BACK, (0, 60, 800,30 ))
                                        text_turn = littlefont.render("AI's Turn",True,BLACK)
                                        text_turn_Rect = text_turn.get_rect()
                                        text_turn_Rect.center = (int(width/2), height/2-145)
                                        screen.blit(text_turn,text_turn_Rect)
                                        pygame.display.update()

                                        break
                                    elif 185+165 > posx > 185+65 and 30+390 > posy > 30+300 and state.board[2][0] == 0:
                                        move.row = 2
                                        move.col = 0
                                        state = state.next_state(move)
                                        state.draw_board()
                                        ai_turn = True
                                        player_turn = False
                                        screen.fill(BACK, (0, 60, 800,30 ))
                                        text_turn = littlefont.render("AI's Turn",True,BLACK)
                                        text_turn_Rect = text_turn.get_rect()
                                        text_turn_Rect.center = (int(width/2), height/2-145)
                                        screen.blit(text_turn,text_turn_Rect)
                                        pygame.display.update()

                                        break
                                    elif 185+265 > posx > 185+165 and 30+200 > posy > 30+100 and state.board[0][1] == 0:
                                        move.row = 0
                                        move.col = 1
                                        state = state.next_state(move)
                                        state.draw_board()
                                        ai_turn = True
                                        player_turn = False
                                        screen.fill(BACK, (0, 60, 800,30 ))
                                        text_turn = littlefont.render("AI's Turn",True,BLACK)
                                        text_turn_Rect = text_turn.get_rect()
                                        text_turn_Rect.center = (int(width/2), height/2-145)
                                        screen.blit(text_turn,text_turn_Rect)
                                        pygame.display.update()

                                        break
                                    elif 185+265 > posx > 185+165 and 30+300 > posy > 30+200 and state.board[1][1] == 0:
                                        move.row = 1
                                        move.col = 1
                                        state = state.next_state(move)
                                        state.draw_board()
                                        ai_turn = True
                                        player_turn = False
                                        screen.fill(BACK, (0, 60, 800,30 ))
                                        text_turn = littlefont.render("AI's Turn",True,BLACK)
                                        text_turn_Rect = text_turn.get_rect()
                                        text_turn_Rect.center = (int(width/2), height/2-145)
                                        screen.blit(text_turn,text_turn_Rect)
                                        pygame.display.update()

                                        break
                                    elif 185+265 > posx > 185+165 and 30+390 > posy > 30+300 and state.board[2][1] == 0:
                                        move.row = 2
                                        move.col = 1
                                        state = state.next_state(move)
                                        state.draw_board()
                                        ai_turn = True
                                        player_turn = False
                                        screen.fill(BACK, (0, 60, 800,30 ))
                                        text_turn = littlefont.render("AI's Turn",True,BLACK)
                                        text_turn_Rect = text_turn.get_rect()
                                        text_turn_Rect.center = (int(width/2), height/2-145)
                                        screen.blit(text_turn,text_turn_Rect)
                                        pygame.display.update()

                                        break
                                    elif 185+365 > posx > 185+265 and 30+200 > posy > 30+100 and state.board[0][2] == 0:
                                        move.row = 0
                                        move.col = 2
                                        state = state.next_state(move)
                                        state.draw_board()
                                        ai_turn = True
                                        player_turn = False
                                        screen.fill(BACK, (0, 60, 800,30 ))
                                        text_turn = littlefont.render("AI's Turn",True,BLACK)
                                        text_turn_Rect = text_turn.get_rect()
                                        text_turn_Rect.center = (int(width/2), height/2-145)
                                        screen.blit(text_turn,text_turn_Rect)
                                        pygame.display.update()

                                        break
                                    elif 185+365 > posx > 185+265 and 30+300 > posy > 30+200 and state.board[1][2] == 0:
                                        move.row = 1
                                        move.col = 2
                                        state = state.next_state(move)
                                        state.draw_board()
                                        ai_turn = True
                                        player_turn = False
                                        screen.fill(BACK, (0, 60, 800,30 ))
                                        text_turn = littlefont.render("AI's Turn",True,BLACK)
                                        text_turn_Rect = text_turn.get_rect()
                                        text_turn_Rect.center = (int(width/2), height/2-145)
                                        screen.blit(text_turn,text_turn_Rect)
                                        pygame.display.update()

                                        break
                                    elif 185+365 > posx > 185+265 and 30+390 > posy > 30+300 and state.board[2][2] == 0:
                                        move.row = 2
                                        move.col = 2
                                        state = state.next_state(move)
                                        state.draw_board()
                                        ai_turn = True
                                        player_turn = False
                                        screen.fill(BACK, (0, 60, 800,30 ))
                                        text_turn = littlefont.render("AI's Turn",True,BLACK)
                                        text_turn_Rect = text_turn.get_rect()
                                        text_turn_Rect.center = (int(width/2), height/2-145)
                                        screen.blit(text_turn,text_turn_Rect)
                                        pygame.display.update()

                                        break
                                if (state.check_win()):
                                    break

                        #makes ai move
                        if(ai_turn and state.check_win() != 1):

                            #runs the mcts and picks move
                            move = MCTS(Node(state)).run(itr)
                            state = state.next_state(move)
                            
                            state.draw_board()
                            ai_turn =False
                            player_turn =True
                            screen.fill(BACK, (0, 60, 800,30 ))
                            text_turn = littlefont.render("Your Turn",True,WHITE)
                            text_turn_Rect = text_turn.get_rect()
                            text_turn_Rect.center = (int(width/2), height/2-145)
                            screen.blit(text_turn,text_turn_Rect)
                            pygame.display.update()

                    if quit:
                        break
                if quit:
                    break
                pygame.draw.rect(screen,BACK,text_game_Rect)
                pygame.draw.rect(screen,BACK,text_mcts_Rect)
                screen.fill(BACK, (0, 60, 800,30 ))
                pygame.display.update()

                #displays end result to the screen and brings you back to choose game menu
                if(state.win_status == 1):
                    if ai_turn == False:
                        text = bigfont.render("AI Wins!".format(state.win_status),True,WHITE)
                    else:
                        text = bigfont.render("Player {} wins!".format(state.win_status),True,WHITE)
                elif(state.win_status == -1):
                    text = bigfont.render("Draw Game",True,txt_col)
                else:
                    if ai_turn == False:
                        text = bigfont.render("AI Wins!".format(state.win_status),True,BLACK)
                    else:
                        text = bigfont.render("Player {} wins!".format(state.win_status),True,BLACK)    
                textRect = text.get_rect()
                textRect.center = (int(width/2), height/2-180)
                screen.blit(text,textRect)
                pygame.display.update()
                pygame.time.wait(3000)

            ####################################################################################################################################################################
            #                                                                                                                                                                  #
            #                                                                                                                                                                  #
            #                                                                      OTHELLO                                                                                     #
            #                                                                       GAME                                                                                       #
            #                                                                                                                                                                  #
            #                                                                                                                                                                  #
            ####################################################################################################################################################################

            #plays the othello game
            elif game == "oth":
                box_size = 50
                RADIUS = int(box_size/2-2)
                ROWS = 8
                COLUMNS = 8
                

                itr = mcts_sims(game)
                itr = int(itr)

                ai_turn , player_turn =choose_start()

                state = OthelloState()
                state.draw_board()
                
                text_game = bigfont.render("Othello",True,txt_col)
                text_mcts = littlefont.render("mcts:{} iterations".format(itr),True,txt_col)
                text_game_Rect = text_game.get_rect()
                text_mcts_Rect = text_mcts.get_rect()
                text_game_Rect.center = (int(width/2), height/2 - 205)
                text_mcts_Rect.center = (int(width/2), height/2 - 185)
                screen.blit(text_game,text_game_Rect)
                screen.blit(text_mcts,text_mcts_Rect)
                pygame.display.update()

                #uncomment code below if you want to run testing on this game, i dont recommend it as it is a complex game and will take about 8 hours to run the tests.
                #testing(state)

                #run the game while its not over
                while not state.is_terminal:

                    mouse = pygame.mouse.get_pos()
                    if (10+60) > mouse[0] > 10 and 10+30 > mouse[1] > 10:
                        pygame.draw.rect(screen,(168,168,168), (10, 10,60,30))
                    else:
                        pygame.draw.rect(screen,WHITE, (10, 10,60,30))

                    quit_text = font2.render("Quit",True,BLACK)
                    quit_text_rect = quit_text.get_rect()
                    quit_text_rect.center = (40,25)
                    screen.blit(quit_text,quit_text_rect)

                    #prints avaiable moves to the screen so player can choose which one he wants to make
                    for move in state.valid_moves():
                        pygame.draw.circle(screen, (192,192,192),(200+(move.col*box_size)+int(box_size/2),(move.row*box_size)+box_size+int(box_size/2)),int(4))
                        
                        


                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        
                        if event.type == pygame.MOUSEBUTTONDOWN:

                            click_x = event.pos[0]
                            click_y = event.pos[1]

                            #quit if button was clicked and bring you to main choose menu
                            if  (10+60) > click_x > 10 and 10+30 > click_y > 10:

                                quit = True
                                break

                            if player_turn:

                                posx = event.pos[0] -200
                                posy = event.pos[1] + box_size

                                col = int(math.floor(posx/box_size))
                                row = int(math.floor(posy/box_size))-2

                                #makes your move if it was allowed and sets it to be ai's turn
                                for move in state.valid_moves():                             
                                    if move.col == col and move.row == row:
                                        
                                        state = state.next_state(move)
                                        
                                        state.draw_board()
                                        pygame.display.update()
                                        
                                        pygame.time.wait(500)
                                        ai_turn = True
                                        player_turn = False
                                        screen.fill(BACK, (100, 10, 175,30 ))
                                        text_turn = littlefont.render("AI's Turn",True,BLACK)

                                        text_turn_Rect = text_turn.get_rect()
                                        text_turn_Rect.center = (int(width/8)+100, height/2-200)
                                        screen.blit(text_turn,text_turn_Rect) 
                                        pygame.display.update()         
                                        break

                                       
                        #makes ai move     
                        if(ai_turn and state.check_win() != 1):
                            

                            

                            #runs the mcts and picks move
                            move = MCTS(Node(state)).run(itr)
                            state = state.next_state(move)
                            
                            state.draw_board()
                                
                            ai_turn =False
                            player_turn = True
                            screen.fill(BACK, (100, 10, 175,30 ))
                            text_turn = littlefont.render("Players Turn",True,WHITE)

                            text_turn_Rect = text_turn.get_rect()
                            text_turn_Rect.center = (int(width/8)+100, height/2-200)
                            screen.blit(text_turn,text_turn_Rect) 
                            pygame.display.update()   
                            
                        pygame.display.update()

                    
                    pygame.display.update()
                    if quit:
                        break
                if quit:
                    break
                pygame.draw.rect(screen,BACK,text_game_Rect)
                pygame.draw.rect(screen,BACK,text_mcts_Rect)
                pygame.display.update()
                screen.fill(BACK, (100, 10, 175,30 ))

                #displays end result to the screen and brings you back to choose game menu
                if(state.win_status == 1):
                    if ai_turn == False:
                        text = bigfont.render("AI Wins!".format(state.win_status),True,WHITE)
                    else:
                        text = bigfont.render("Player {} wins!".format(state.win_status),True,WHITE)
                elif(state.win_status == -1):
                    text = bigfont.render("Draw Game",True,txt_col)
                else:
                    if ai_turn == False:
                        text = bigfont.render("AI Wins!".format(state.win_status),True,BLACK)
                    else:
                        text = bigfont.render("Player {} wins!".format(state.win_status),True,BLACK) 
                textRect = text.get_rect()
                textRect.center = (int(width/2), height/2-195)
                screen.blit(text,textRect)

                pygame.display.update()
                pygame.time.wait(3000)


            ####################################################################################################################################################################
            #                                                                                                                                                                  #
            #                                                                                                                                                                  #
            #                                                                      INVASION                                                                                    #
            #                                                                        GAME                                                                                      #
            #                                                                                                                                                                  #
            #                                                                                                                                                                  #
            ####################################################################################################################################################################

            #plays the invasion game
            elif game == "invasion":
                
                #starts with 3 lives and 1 invader
                lives = 3
                score = 0
                total_invaders = 1
                bullets = 4


                left_arrow = pygame.image.load('images/left_arrow.png')
                right_arrow = pygame.image.load('images/right_arrow.png')
                
                screen.blit(left_arrow,(20,240))
                screen.blit(right_arrow,(680,240))

                pygame.draw.circle(screen,BLACK,(120,400),45)
                pygame.draw.circle(screen,BLACK,(680,400),45)


                text_shoot = littlefont.render("SHOOT",True,WHITE)              
                text_shoot_Rect = text_shoot.get_rect()
                text_shoot_Rect2 = text_shoot.get_rect()
                text_shoot_Rect.center = (120,400)
                text_shoot_Rect2.center = (680,400)
                screen.blit(text_shoot,text_shoot_Rect)
                screen.blit(text_shoot,text_shoot_Rect2)

                lives_txt = littlefont.render("lives : ",True,WHITE)
                lives_txt_rect = lives_txt.get_rect()
                lives_txt_rect.center = (660,15)

                score_txt = tinyfont.render("score: ",True,WHITE)
                score_txt_rect = score_txt.get_rect()
                score_txt_rect.center = (660,40)

                bullets_txt = tinyfont.render("bullets: ",True,WHITE)
                bullets_txt_rect = score_txt.get_rect()
                bullets_txt_rect.center = (660,65)

                screen.blit(lives_txt,lives_txt_rect)
                screen.blit(score_txt,score_txt_rect)
                screen.blit(bullets_txt,bullets_txt_rect)

                state = Invasion()
                state.draw_board()
                kill_count = 0 
                mouseclicked = False

           
                
              
                pygame.display.update()

                game_running = True
                while game_running:
                    mouse = pygame.mouse.get_pos()
                    if (10+60) > mouse[0] > 10 and 10+30 > mouse[1] > 10:
                        pygame.draw.rect(screen,(168,168,168), (10, 10,60,30))
                    else:
                        pygame.draw.rect(screen,WHITE, (10, 10,60,30))

                    quit_text = font2.render("Quit",True,BLACK)
                    quit_text_rect = quit_text.get_rect()
                    quit_text_rect.center = (40,25)
                    screen.blit(quit_text,quit_text_rect)
                    pygame.display.update()

                    pygame.time.wait(100)
                    
                    
                    enemy = "invader"
                    for event in pygame.event.get():
                        
                        
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            posx = event.pos[0]
                            posy = event.pos[1]

                            #if button pressed was quit button, quit game and brought to choose menu
                            if  (10+60) > posx > 10 and 10+30 > posy > 10:

                                quit = True
                                break

                            # moves the random invader if a button is pressed
                            for i in range(total_invaders): 
                                if state.inv_alive[i]:
                                    invader_move = random.choice(state.valid_moves(i,enemy))
                                    state.next_invader_state(invader_move,i)

                            #move left
                            if 40+100>posx>40 and 250+100>posy>250:
                                state.move_left = True
                                state.MoveLeft()
                            
                            #move right
                            if 660+100>posx>660 and 250+100>posy>250:
   
                                state.move_right = True
                                state.MoveRight()

                            #check if bullet is ready if shoot button is pressed
                            if 120+45>posx>75 and 400+45>posy> 355:
                                for x in range(bullets):
                                    if (not state.shot[x]) and state.shot_ready[x]:
                                        state.bullets_left -= 1
                                        state.shot_ready[x] = False
                                        state.shot[x] = True
                                        state.bulletX[x] = state.shipX
                                        break

                            #check if bullet is ready if shoot button is pressed
                            if 680+45>posx>635 and 400+45>posy> 355:
                                for x in range(bullets):
                                    if (not state.shot[x]) and state.shot_ready[x]:
                                        state.bullets_left -= 1
                                        state.shot_ready[x] = False
                                        state.shot[x] = True
                                        state.bulletX[x] = state.shipX
                                        break

                            pygame.display.update()

                    #moves  all invaders alive and bullets and checks if invaders got to end or if bullets killed invaders.
                    for current in range(total_invaders):
                        
                        if state.inv_alive[current]:

                            invader_move = random.choice(state.valid_moves(current,enemy))
                            state.next_invader_state(invader_move,current)

                            if state.invaderY[current] > 350:
                                lives = lives - 1
                                
                                state.invaderX[current] = random.randint(width/4-20,width-(width/4)-10)
                                state.invaderY[current] = 10
                                
                            
                            pygame.display.update()
                            for cur in range(bullets):
                                state.bullet_move(cur)
                                if state.check_hit(current,cur):
                                    state.bullets_left += 1
                                    state.inv_alive[current] = False
                                    state.shot_ready[cur]= True
                                    state.shot[cur] = False
                                    state.bulletY[cur]= 375
                                    state.invaderX[current] = -400
                                    state.invaderY[current] = -400
                                    kill_count+=1
                                    score += 25
                            state.draw_board()
                            pygame.display.update()


                    #moves the mcts enemy based on simulations and bullets and checks if it reached end or if bullets killed the mcts enemy
                    enemy = "mcts"
                    if state.mcts_alive:
                        move = MCTS(Node(state)).run(100)
                        state.next_state(move)

                        if state.mcts_enemyY[0] > 350:
                            lives = lives - 1
                            
                            state.mcts_enemyX[0] = random.randint(width/4-20,width-(width/4)-10)
                            state.mcts_enemyY[0] = 10


                        for cur in range(bullets):
                            state.bullet_move(cur)
                            if state.check_hit(0,cur):
                                state.bullets_left += 1
                                state.mcts_alive = False
                                state.shot_ready[cur]= True
                                state.shot[cur] = False
                                state.bulletY[cur]= 375
                                state.mcts_enemyY[0] = -400
                                state.mcts_enemyX[0] = -400
                                
                                kill_count +=1
                                score+=75

                    #moves bullets as others only occer on conditions and checks if they hit anything
                    for cur in range(bullets):
                        state.bullet_move(cur)
                        if state.check_hit(0,cur):
                            state.bullets_left += 1
                            state.mcts_alive = False
                            state.shot_ready[cur]= True
                            state.shot[cur] = False
                            state.bulletY[cur]= 375
                            state.mcts_enemyY[0] = -400
                            state.mcts_enemyX[0] = -400
                            
                            kill_count +=1
                            score+=75
                         
                    state.draw_board()
                    pygame.display.update()

                    #if all lives lost game over    
                    if lives < 1:
                        break

                    #if killed everyone on board reset board and incerease number of random enemies
                    if kill_count == total_invaders+1:
                        
                        total_invaders = total_invaders +1
                        
                        state = Invasion()
                        pygame.time.wait(1000)
                        kill_count =0
                        score += 100

                    if quit:
                        break

                #displays your score and the level you got to and brings you back to choose game menu

                game_over_txt = bigfont.render("Game Over",True,WHITE)
                game_over_txt_rect = game_over_txt.get_rect()
                game_over_txt_rect.center = (400,205)

                game_over_lvl = bigfont.render("Level : {}".format(total_invaders),True,WHITE)
                game_over_score = bigfont.render("Score : {}".format(score),True,WHITE)

                game_over_lvl_rect = game_over_lvl.get_rect()
                game_over_lvl_rect.center = (400,235)

                game_over_score_rect = game_over_score.get_rect()
                game_over_score_rect.center = (400,265)
                screen.blit(game_over_txt,game_over_txt_rect)
                screen.blit(game_over_lvl,game_over_lvl_rect)
                screen.blit(game_over_score,game_over_score_rect)
                pygame.display .update()
                pygame.time.wait(5000)












        


