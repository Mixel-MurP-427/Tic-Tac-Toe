#This is an AI designed to LEARN how to always win at Tic-tac-toe

#TODO Does this program  accept a grid in both list and string formats?
#program will use lists, but user can use str. program will convert list to str when storing in bank for efficiency.
#Possible glitch: inconsistent list/str grid format.

#setup and initialization:

assert True, "FOOL!"

print('Tic-tac-toe AI is booting up...')

import random, time, copy, pprint
from TTT_AI_Memory_Bank import games_played as bank
#open('Misc_projects/Tic-Tac-Toe/TTT_AI_Memory_Bank.py', 'rt')

ppFile = pprint.PrettyPrinter(compact=True, indent=4)

letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')


#accepts either string or list of 9 characters
def print_board(pbInput):
    if type(pbInput) == range:
        pbInput = tuple(pbInput)
        print('pbInput == ' + str(pbInput))
    if valid_board(pbInput, vbType=(list, tuple, str)):
        print("%s|%s|%s\n-+-+-\n%s|%s|%s\n-+-+-\n%s|%s|%s" % tuple(pbInput[pb] for pb in range(9)))
    else:
        print(" | | \n-+-+-\n | | \n-+-+-\n | | ")

def wait():
    time.sleep(random.randint(1, 2) / 10)

#checks if argument is a board
def valid_board(vbBoard, vbType=(list, tuple)):
    if not type(vbBoard) in vbType:
        #print('vbTypeError', vbType, type(vbBoard))
        return False
    if len(vbBoard) != 9:
        #print('vbLenError')
        return False
    for vbCell in vbBoard: 
        if not vbCell  in (' ', 'X', 'O'):
            #print('vbCellError', vbCell)
            return False
    return True

#accepts board (as a list), then directions to mirror board in, one at a time.
# '-|' and '/\\' == 180 rotation, '/-', '-\\', '|/', and '\\|' == 90 rotation; reverse any of these for -90 degree rotation.
def mirror_board(mbBoard, mbDirections):
    assert valid_board(mbBoard), 'mirror_board() mbBoard passed invalid argument: %s' % mbBoard
    mbOutput = mbBoard
    for mbLetter in range(len(mbDirections)):
        if mbDirections[mbLetter] == '-':
            mbSwitch = (6, 7, 8, 3, 4, 5, 0, 1, 2)
        elif mbDirections[mbLetter] == '/':
            mbSwitch = (8, 5, 2, 7, 4, 1, 6, 3, 0)
        elif mbDirections[mbLetter] == '|':
            mbSwitch = (2, 1, 0, 5, 4, 3, 8, 7, 6)
        elif mbDirections[mbLetter] == '\\':
            mbSwitch = (0, 3, 6, 1, 4, 7, 2, 5, 8)
        else:
            raise Exception('mirror_board() mbDirection passed invalid argument: %s' % mbDirection)

        mbOutput = list(mbOutput[mb] for mb in mbSwitch)
    return mbOutput

mirror_moves(mmMoves, mmDirections):


#Checks if board A can be mirrored to match board B. If True returns the reflection angles, if False returns None
def do_boards_match(dbmBoardA, dbmBoardB):
    #                      4 Reflections, Rotations 90, -90, 180
    assert valid_board(dbmBoardA) and valid_board(dbmBoardB), 'do_boards_match() passed invalid argument(s): %s and/or %s' % (dbmBoardA, dbmBoardB)
    for dbmReflections in ('-', '/', '|', '\\', '/-', '-/', '-|'):
        if mirror_board(dbmBoardA, dbmReflections) == dbmBoardB:
            return dbmReflections
    return False

#checks if player has given valid answer
def check_answer():
    global move
    while True:
        try:
            move = int(move)
        except ValueError:
            move = input('Invalid answer.\nYou must specify a number between 0 and 8 that is not occupied: ')
        else: #I removed a continue line in previous block
            try:
                if the_board[move] == ' ':
                    return
            except IndexError:
                move = input('Invalid answer.\nYou must specify a number between 0 and 8 that is not occupied: ')

#accepts board and returns list of possible moves, clustering those that have the same effect
def find_possible_moves(fpmBoard):
    assert valid_board(fpmBoard), 'find_possible_moves() passed invalid argument: %s' % fpmBoard
    fpmOutput = []
    for fpmCell in range(9):
        if fpmBoard[fpmCell] == ' ':
            if fpmCell == 4: #minor optimization: 4 (center) is always unique and doesn't need to be scanned
                fpmOutput.append([4])
                continue
            fpmModdedBoard = copy.deepcopy(fpmBoard)
            fpmModdedBoard[fpmCell] = 'X'
            fpmBreak = False

            for fpmGroup in fpmOutput:
                for fpmOutCell in fpmGroup:
                    fpmOutBoard = copy.deepcopy(fpmBoard)
                    fpmOutBoard[fpmOutCell] = 'X'
                    #Checks if a variant of this case is already in fpmOutput
                    if do_boards_match(fpmModdedBoard, fpmOutBoard) != False:
                        fpmGroup.append(fpmCell) #this line takes advantage of list referencing
                        fpmBreak = True
                        break
                if fpmBreak:
                    break

            if not fpmBreak:
                fpmOutput.append([fpmCell])

    return fpmOutput

#accepts a list or string of oerdered moves and the first player to move, returns a board list for it. 
def moves_to_board(mtbMoves, mtb1stPlayer):
    mtbMoves = list(mtbMoves)
    mtbOutput = [' '] * 9
    mtbCurrentPlayer = mtb1stPlayer
    for mtbMove in mtbMoves:
        mtbOutput[int(mtbMove)] = mtbCurrentPlayer
        if mtbCurrentPlayer == 'O':
            mtbCurrentPlayer = 'X'
        else:
            mtbCurrentPlayer = 'O'
    return mtbOutput

# Accepts a list of moves (in order) and the player that made the first move. Returns all (mirrored) instances found in bank that are equal.
def search_bank(sbMoves, sb1stPlayer): #I am 75% confident this function works
    global bank
    sbOutput = []
    sbBoard = moves_to_board(sbMoves, sb1stPlayer)
    for sbGame in bank:
        if sbGame['F'] == sb1stPlayer:
            sbSpecificBoard = moves_to_board(sbGame['M'][:len(sbMoves)], sbGame['F'])
            sbMatch = do_boards_match(sbSpecificBoard, sbBoard)
            #if any variation of the corresponding moves in sbGame match sbMoves:
            if sbMatch != False:
                sbOutput.append(mirror_board(sbSpecificBoard, sbMatch)) #TODO needs to output entire dict, not just a board
    return sbOutput




#player setup
wait()
print('ready')
wait()
player_name = input('\nPlease enter your name: ')
wait()
print("You will be O's and the AI will be X's.")
wait()
print("The board layout is")
wait()
print_board('blank')
wait()
first_player = input('\nWho would you like to play first? (type either "O" for yourself or "X" for the AI): ').upper()
assert first_player == 'X' or first_player == 'O', 'Player gave invalid answer: %s' % first_player






#Start running game


the_board = list(' ' * 9)
boardInOrder = []
current_player = first_player

for turn in range(1, 10):
    print('\nturn: ' + str(turn))

    if current_player == 'O': #O is for player
        #player's turn. asks player to make move.
        move = input("It's your turn\nWhere would you like to play? (0-8): ")
        check_answer() #checks if player has given valid answer

        current_player = 'X'





    else: #AI's turn
        print('The AI is thinking...')
        #find possible moves and cluster similar ones together
        options = find_possible_moves(the_board)
        #iterate over all games in bank and find relevant games
        print('options == '+str(options))
        relevant_games = []
        for group in options: #does bot need to iterate over EVERY move in each group, or only one?
            try:
                relevant_games.append(search_bank(boardInOrder + [group[0]], first_player))#will likely raise index error if group is empty
            except KeyError:
                assert group == [], 'Hubba whaaaa????'
                relevant_games.append([])
        print('relevant_games == '+str(relevant_games))

        #TODO analyze data:
            #detect immediate loses/wins if exact match is found, including loses/wins that are far future but definite
            #calculate odds of each case: Win, Unknown, Tie, Loss
            #pick random from most favorable group
        odds = [[]] * len(options)
        for group, counter in zip(relevant_games, range(len(options))):
            for game in group:
                if len(game['M']) == turn and game['W'] == 'W': #if immediate win:
                    odds[counter].append('W0')
                elif len(game['M']) == turn+1 and game['W'] == 'L': #if immediate loss:
                    odds[counter].append('L0')

        print('odds == '+str(odds))




        current_player = 'O'

    #register move to board and print
    the_board[move] = 'X' if current_player == 'O' else 'O' #must invert answer since current_player was flipped prematurely
    boardInOrder.append(move)
    print_board(the_board)




bank_file = open("Misc_projects/Tic-Tac-Toe/TTT_AI_Memory_Bank.py", 'w')
bank_file.write('#Memory bank for Tic-Tac-Toe_Bot.py\n#U == username\n#F == first_player (X for robot or O for human)\n#W == win_status\n#M == moves (in the order they happened)\ngames_played = '
+ ppFile.pformat(bank))
bank_file.close()
print('End of program. Thanks for playing!')

"""
for thingimagig in bank:
    print_board(moves_to_board(thingimagig['M'], thingimagig['F']))
    print()
"""

#TODO add wait() once program is completed. This makes it look more realistic.
#TODO once finished, perhaps remove assert statements if program is slow. Otherwise just keep them.