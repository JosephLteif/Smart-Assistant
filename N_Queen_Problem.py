import cv2
import operator
from PIL import Image
# Python3 program to solve N Queen  
# Problem using backtracking 
global N 
N = 8
 
def printSolution(board):
    coord = dict()
    for i in range(N): 
        for j in range(N):
            point = board[i][j]
            print (point, end = " ")
            if point == 1:
                coord[i] = j 
        print()
    return coord
  
# A utility function to check if a queen can 
# be placed on board[row][col]. Note that this 
# function is called when "col" queens are 
# already placed in columns from 0 to col -1. 
# So we need to check only left side for 
# attacking queens 
def isSafe(board, row, col): 
  
    # Check this row on left side 
    for i in range(col): 
        if board[row][i] == 1: 
            return False
  
    # Check upper diagonal on left side 
    for i, j in zip(range(row, -1, -1),  
                    range(col, -1, -1)): 
        if board[i][j] == 1: 
            return False
  
    # Check lower diagonal on left side 
    for i, j in zip(range(row, N, 1),  
                    range(col, -1, -1)): 
        if board[i][j] == 1: 
            return False
  
    return True
  
def solveNQUtil(board, col): 
      
    # base case: If all queens are placed 
    # then return true 
    if col >= N: 
        return True
  
    # Consider this column and try placing 
    # this queen in all rows one by one 
    for i in range(N): 
  
        if isSafe(board, i, col): 
              
            # Place this queen in board[i][col] 
            board[i][col] = 1
  
            # recur to place rest of the queens 
            if solveNQUtil(board, col + 1) == True: 
                return True
  
            # If placing queen in board[i][col] 
            # doesn't lead to a solution, then 
            # queen from board[i][col] 
            board[i][col] = 0
  
    # if the queen can not be placed in any row in 
    # this colum col then return false 
    return False

#This function is used to place the Queen images on the ChessBoard image
def Place_Queens(Board, Queen, index_x, index_y):

    # suppose img1 and img2 are your two images
    img1 = Board
    img2 = Queen

    # suppose img2 is to be shifted by `shift` amount 
    shift = (8+(index_x*27)+(index_x%2)*1, 3+(index_y*27)+(index_y%2)*1)

    # compute the size of the panorama
    x = map(operator.add, img2.size, shift)
    nw, nh = map(max, x, img1.size)
    print(nw)
    print(nh)

    # paste img1 on top of img2
    newimg1 = Image.new('RGBA', size=(nw, nh), color=(0, 0, 0, 0))
    newimg1.paste(img2, shift)
    newimg1.paste(img1, (0, 0))

    # paste img2 on top of img1
    newimg2 = Image.new('RGBA', size=(nw, nh), color=(0, 0, 0, 0))
    newimg2.paste(img1, (0, 0))
    newimg2.paste(img2, shift)

    # blend with alpha=0.5
    result = Image.blend(newimg1, newimg2, alpha=0.5)
    
    return result
  
# This function solves the N Queen problem using 
# Backtracking. It mainly uses solveNQUtil() to 
# solve the problem. It returns false if queens 
# cannot be placed, otherwise return true and 
# placement of queens in the form of 1s. 
# note that there may be more than one 
# solutions, this function prints one of the 
# feasible solutions. 
def solveNQ(): 
    board = [ [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]

    if solveNQUtil(board, 0) == False: 
        print ("Solution does not exist") 
        return False

    coord = printSolution(board)
    ChessBoardimg = Image.open("Data\\N_Queen_Puzzle_Data\\Assets\\ChessBoard.png")
    Queenimg = Image.open("Data\\N_Queen_Puzzle_Data\\Assets\\Queen.png")
    for i in coord:
        ChessBoardimg = Place_Queens(ChessBoardimg, Queenimg, coord[i], i)
    ChessBoardimg.show()
    cv2.waitKey(0)
    return True
  
# Driver Code 
solveNQ() 
  