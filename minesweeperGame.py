from static.games.minesweeper.minesweeper import MineSweeper
import time


row = int(input("Enter the number of rows: "))
col = int(input("Enter the number of columns: "))
Minegame = MineSweeper(row,col)
Minegame.startGame()

Minegame.name = input("Enter your name: ")


while True:
    print("Current Board:", Minegame.name)
    for row_cnt in range(row):
        for col_cnt in range(col):
            res = Minegame.getSpace(row_cnt,col_cnt)
            if res == -2:
                print("F",end=" ")
            elif res == -1:
                print("O",end=" ") 
            elif res == 9:
                print("B",end=" ") 
            else:
                print(res,end=" ")
        print()
    print("Game Over:", Minegame.gameOver)
    print("Score:", Minegame.score)
    print("Time:", Minegame.time)
    if(Minegame.gameOver):
        break
    pick_row, pick_col , Flag= map(int, input("Pick rows, col and Flag separated by a space: ").split())
    if Flag == 1:
        Minegame.pickSpace(pick_row, pick_col, True);
    else:
        Minegame.pickSpace(pick_row, pick_col, False);
    
    print("After picking:")







