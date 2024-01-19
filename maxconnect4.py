#!/usr/bin/env python3

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import sys
from MaxConnect4Game import *
from datetime import datetime


def oneMoveGame(currentGame):

    st = datetime.now()
    if currentGame.pieceCount == 42:    # Is the board full already?
        print('BOARD FULL\n\nGame Over!\n')
        sys.exit(0)

    currentGame.aiPlay() # Make a move (only random is implemented)

    print('Game state after move:')
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()
    et = datetime.now()

    print("Start Time:", st.time())
    print("Finish Time:", et.time())
    print("Execution Time:", et-st)


def interactiveGame(currentGame):

    while True:
        currentGame.printGameBoard()
        print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

        if currentGame.currentTurn == 1:
            print("Computer's Turn")
            currentGame.aiPlay() 

        else:
            while True:
                try:
                    col = int(input("Human's Turn (Enter Column 0-6):"))
                    if col > 6:
                        print("Invalid Column Input, Maximum Allowed value is 6.")
                        continue
                    res = currentGame.playPiece(col)
                    if res:
                        break
                    print("Invalid Column Input, Column Full")

                except KeyboardInterrupt:
                    sys.exit(0)
                except Exception as e:
                    print("Invalid Numerical Input:", e)

            currentGame.currentTurn = 1

        currentGame.checkPieceCount()
        currentGame.countScore()

        if currentGame.pieceCount == 42:
            print("Game Finished. Final Score:")
            print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
            if currentGame.player1Score > currentGame.player2Score:
                print("Player 1 WON")
            elif currentGame.player1Score < currentGame.player2Score:
                print("Player 2 WON")
            else:
                print("MATCH DRAW")
            break


    # sys.exit('Interactive mode is currently not implemented')


def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print('Four command-line arguments are needed:')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
        # Read the initial game state from the file and save in a 2D list
        file_lines = currentGame.gameFile.readlines()
        currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
        currentGame.currentTurn = int(file_lines[-1][0])
        currentGame.gameFile.close()

    except IOError:
        # sys.exit("\nError opening input file.\nCheck file name.\n")
        print("Starting from Scratch")
        currentGame.currentTurn = int(1)


    print('\nMaxConnect-4(game\n')
    print('Game state before move:')
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.maxdepth = int(argv[-1])

    if game_mode == 'interactive':
        print("Max Depth:", currentGame.maxdepth)
        interactiveGame(currentGame) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)
