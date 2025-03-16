from flask import Flask, request
import random
import time
class MineSweeper:
    '''
    2D list
    0-8: uncovered number of mines around space
    9: uncovered mine
     negative: covered equivalent
    -10: covered zero
    -10: flagged equivalent of negative
    '''
    
    
    
    __COVERED_ZERO = -10
    __FLAG_MOD = 10

    __OPEN = -1
    #  @return {int} value representing a selectable space
    @property
    def OPEN(self):
        return MineSweeper.__OPEN
    __FLAG = -2
    # @return {int} value representing a flag placemnt
    @property
    def FLAG(self):
        return MineSweeper.__FLAG
    __MINE = 9
    # @return {int} value representing a mine
    @property
    def MINE(self):
        return MineSweeper.__MINE
    
    '''
        Create a populating MineSweeper board
        @param rows number of rows in the game
        @param cols number of columns in the game
    '''

    def __init__(self,rows: int,cols: int):
        self.__numMines = 0
        self.__startTime = 0
        self.__board = []

        self.__score = 0
        self.__name = ''
        self.__gameOver = 0 #1 = win, -1 = lose, 0 = keep going

        self.__PERCENT_CHANCE_MINE = 20
        for row in range(rows):
            r = []
            for col in range(cols):
                r.append(0)
            self.__board.append(r)
        
        self.startGame()
        self.__resetBoard()
    
    
    def __resetBoard(self):
        self.__score = self.rows * self.cols

        #Reset the board to zeros
        for row in range(self.rows):
            for col in range(self.cols):
                self.__board[row][col] = 0
        
        #Place mines and calculate board spaces
        for row in range(self.rows):
            for col in range(self.cols):
                isMine = random.randint(0,99) < self.__PERCENT_CHANCE_MINE
                if(isMine):
                    self.__board[row][col] = -self.MINE
                    self.__numMines += 1
                    #Deduct one from adjacent spaces
                    for r in range(row-1,row+2):
                        for c in range(col -1, col + 2):
                            if r >= 0 and r < self.rows and c >= 0 and c < self.cols:
                                if(not (self.__board[r][c] == -self.MINE)):
                                    self.__board[r][c] -= 1
        #Set zeros to their covered values
        for row in range(self.rows):
            for col in range(self.cols):
                if(self.__board[row][col] == 0):
                    self.__board[row][col] = MineSweeper.__COVERED_ZERO
    
    '''
         * Picks a space and enforces rules of MineSweeper
         *
         * @param {int} row row to select (start at zero)
         * @param {int} col column to select (start at zero)
         * @param {bool} toogleFlag true to toggle a flag placement
         * @return {boolean} true if the move was valid, false otherwise
         */
    '''

    def pickSpace(self, row: int, col: int, toggleFlag = False):
        if(self.__gameOver):
            return False
        
        if (row < 0 or row >= self.rows or col < 0 or col >= self.cols):
            return False
        
        #Already picked
        if (self.__board[row][col] >= 0):
            return False
          
            
        #Toggle the Flag
        if(toggleFlag):
            mod = -MineSweeper.__FLAG_MOD
            if(self.__board[row][col] < mod):
                mod  = mod * -1
            self.__board[row][col] += mod
            return True
        
        #Flagged spaces cannot be picked
        if (self.__board[row][col] < -MineSweeper.__FLAG_MOD):
            return False
        
        self.__uncoverSpace(row,col)
        self.__score -= 1
        if (self.__board[row][col]==0):
            #Hit a zero, uncover the spaces around this one
            for r in range(row -1, row + 2):
                for c in range(col -1, col + 2):
                    self.pickSpace(r,c)
        elif self.__board[row][col] == self.MINE:
            #Losing Free the score and time taken
            self.__gameOver = -1
            self.__startTime = -1 * self.time
        
        #Winning!
        if(self.__score== self.__numMines):
            self._gameOver = 1
            self.__startTime = -1 *self.time
    
    def __uncoverSpace(self,row: int,col: int):
        if(self.__board[row][col] >= 0):
            return self.__board[row][col]
        
        #Remove the flag
        if self.__board[row][col]< -MineSweeper.__FLAG_MOD:
            self.__board[row][col] += MineSweeper.__FLAG_MOD
        
        #Uncover the space
        if self.__board[row][col] < 0:
            self.__board[row][col] = self.__board[row][col] * -1
        
        #Set the zero properly
        if self.__board[row][col] == -MineSweeper.__COVERED_ZERO:
            self.__board[row][col] = 0
        #print(self.__board[row][col])
        return self.__board[row][col]
    
    '''
    Get the status of a space
    @param {int} row the row to query (starting at zero)
    @param {int} col the column to query (starting at zero)
    @return {int} value at (row,col) if uncovered, OPEN if covered or invalid
    '''

    def getSpace(self,row: int,col: int):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return self.OPEN
        
        #Game's Over... uncover the space!
        if self.__gameOver:
            self.__uncoverSpace(row,col)
            return self.__board[row][col]
        
        if self.__board[row][col] < -MineSweeper.__FLAG_MOD:
            return self.FLAG
        
        if self.__board[row][col] < 0:
            return self.OPEN
        
        return self.__board[row][col]
    
    '''
    Begins the game
    '''

    def startGame(self):
        self.__startTime = time.time() * 1000            
    
    #return number of columns in the game
    @property
    def cols(self):
        return len(self.__board[0])
    
    #return number of rows in the game
    @property
    def rows(self):
        return len(self.__board)
    
    #The game over status of the game
    #@return {int} negative if loss, positive if win, zero otherwise
         
    @property
    def gameOver(self):
        #print(self.__gameOver)
        return self.__gameOver
    
    #return calculated score of the game
    @property
    def score(self):
        return self.__score
    
    #@return seconds which have passed in the game
    @property
    def time(self):
        if self.__startTime <= 0:
            return abs(self.__startTime)
        return (time.time()*1000)-self.__startTime
    
    #@return {string} name of the player

    @property
    def name(self):
        return self.name
    
    #@return new name of the player

    @name.setter
    def name(self, val: str):
        self.name = val

    


        
    


    


        


        
        


    
    

    

    

