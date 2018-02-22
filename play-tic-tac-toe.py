import curses
import time
import random


def refresh_gameboard(placement, stdscr):
    gameboard = """
 1 | 2 | 3          {0} | {1} | {2} 
---+---+---        ---+---+---
 4 | 5 | 6          {3} | {4} | {5}
---+---+---        ---+---+---
 7 | 8 | 9          {6} | {7} | {8}"""
    stdscr.refresh()
    stdscr.addstr(0, 0, gameboard.format(*placement))


def ai_options(user_spaces, opts, in_use, ai_choice):
    occupied_spaces = [x for x in in_use if x in opts]
    
    # Check if the user has won
    if len(user_spaces) == 3:
        ai_choice.append(0)
        return
    # Check if computer has won
    elif len(user_spaces) == 0 and len(occupied_spaces) == 3:
        ai_choice.append(-1)  
        return
    # Defensive Options    
    if len(user_spaces) == 2:
        for item in opts:
            if item not in occupied_spaces:
                ai_choice.append(item)
    # Offensive Options
    elif len(user_spaces) == 0 and len(occupied_spaces) == 2:
        for item in opts:
            if item not in occupied_spaces:
                ai_choice.append(10 + item)
    elif len(user_spaces) == 0 and len(occupied_spaces) == 1:
        for item in opts:
            if item not in occupied_spaces:
                ai_choice.append(20 + item)
    

def board_analysis(in_use_by_user, in_use):
    col1 = [1, 4, 7]
    col2 = [2, 5, 8]
    col3 = [3, 6, 9]
    row1 = [1, 2, 3]
    row2 = [4, 5, 6]
    row3 = [7, 8, 9]
    diag1 = [1, 5, 9]
    diag2 = [3, 5, 7]

    ucol1 = []
    ucol2 = []
    ucol3 = []
    urow1 = []
    urow2 = []
    urow3 = []
    udiag1 = []
    udiag2 = []

    for item in in_use_by_user:
        if item == 1:
            ucol1.append(item)
            urow1.append(item)
            udiag1.append(item)
        if item == 2:
            ucol2.append(item)
            urow1.append(item)
        if item == 3:
            ucol3.append(item)
            urow1.append(item)
            udiag2.append(item)
        if item == 4:
            ucol1.append(item)
            urow2.append(item)
        if item == 5:
            ucol2.append(item)
            urow2.append(item)
            udiag1.append(item)
            udiag2.append(item)
        if item == 6:
            ucol3.append(item)
            urow2.append(item)
        if item == 7:
            ucol1.append(item)
            urow3.append(item)
            udiag2.append(item)
        if item == 8:
            ucol2.append(item)
            urow3.append(item)
        if item == 9:
            ucol3.append(item)
            urow3.append(item)
            udiag1.append(item)

    ai_choice = []
    if len(in_use) == 1:
        if 5 in in_use:
            ai_choice.append(1)
            ai_choice.append(3)
            ai_choice.append(7)
            ai_choice.append(9)
        else:
            ai_choice.append(5)
        return ai_choice

    ai_options(ucol1, col1, in_use, ai_choice)
    ai_options(ucol2, col2, in_use, ai_choice)
    ai_options(ucol3, col3, in_use, ai_choice)
    ai_options(urow1, row1, in_use, ai_choice)
    ai_options(urow2, row2, in_use, ai_choice)
    ai_options(urow3, row3, in_use, ai_choice)
    ai_options(udiag1, diag1, in_use, ai_choice)
    ai_options(udiag2, diag2, in_use, ai_choice)
    return ai_choice


def end_game(ai_choice, stdscr, players=1):
    if 0 in ai_choice:
        if players == 2:
            stdscr.addstr(0, 0, "         Player 1 wins!")
        else:
            stdscr.addstr(0, 0, "           You win!")
        stdscr.refresh()
        return True
    if -1 in ai_choice:
        if players == 2:
            stdscr.addstr(0, 0, "         Player 2 wins!")
        else:
            stdscr.addstr(0, 0, "           You lose")
        stdscr.refresh()
        return True
    return False 


def user_turn(stdscr, in_use, in_use_by_user, available, player_one=True):
    next_move = 0
    usr_input = ""
    while next_move not in in_use:
        stdscr.addstr(7, 0, "Choose a position:  ")
        stdscr.refresh()
        stdscr.clrtoeol()
        try:
            usr_input = stdscr.getstr(7, 19)[0]
            next_move = int(usr_input)
            if next_move != 0 and next_move not in in_use:
                stdscr.clrtoeol()
                in_use.append(next_move)
                if player_one:
                    in_use_by_user.append(next_move)
                    available.remove(next_move)
            else:
                stdscr.addstr(8, 0, str(next_move) + " is already in use")
                next_move = 0
        except ValueError:
            if usr_input.lower().startswith("q"):
                raise TypeError("Quitting now...")
    return next_move


def ai_turn(stdscr, in_use, in_use_by_user, available):
    ai_choice = board_analysis(in_use_by_user, in_use)
    next_move = 0

    if len(ai_choice) == 0:
        next_move = random.choice(available)
        in_use.append(next_move)
        available.remove(next_move)
    else:
        if end_game(ai_choice, stdscr):
            return 0

        # Finish first, then attack if no defence needed
        defending_moves = [x for x in ai_choice if x < 10]
        finishing_moves = [x - 10 for x in ai_choice if 10 < x < 20]
        attacking_moves = [x - 20 for x in ai_choice if x > 20]

        if len(finishing_moves) > 0:
            next_move = random.choice(finishing_moves)
        elif len(defending_moves) > 0:
            strategic_defend = [x for x in defending_moves if
                                x in attacking_moves]
            if len(strategic_defend) > 0:
                next_move = random.choice(defending_moves)
            else:
                next_move = random.choice(defending_moves)
        elif len(attacking_moves) > 0:
            next_move = random.choice(attacking_moves)

        in_use.append(next_move)
        available.remove(next_move)

    return next_move


def play(number_of_players):
    # New game setup
    available = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    placement = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    in_use_by_user = []
    in_use = []
    i = 0
    continue_playing = True

    # Start the ncurses session. Game auto-ends in 9 turns
    stdscr = curses.initscr()
    curses.cbreak()
    refresh_gameboard(placement, stdscr)

    try:
        for i in range(9):

            # Player 1 turn
            if i % 2 == 0:
                turn = "X"
                next_move = user_turn(stdscr, in_use, in_use_by_user,
                                      available)

            # Player 2 turn
            else:
                turn = "O"
                if number_of_players == 2:
                    next_move = user_turn(stdscr, in_use, in_use_by_user,
                                          available, False)
                else:
                    next_move = ai_turn(stdscr, in_use, in_use_by_user,
                                        available)
                    if next_move == 0:
                        break

            placement[next_move - 1] = turn
            refresh_gameboard(placement, stdscr)

            ai_choice = board_analysis(in_use_by_user, in_use)
            if end_game(ai_choice, stdscr, players=number_of_players):
                break

            time.sleep(0.5)
        if i == 8:
            stdscr.addstr(0, 0, "          Tie game!")
            stdscr.refresh()
            stdscr.clrtoeol()
        stdscr.addstr(7, 0, "Would you like to play again? (y/n) ")
        stdscr.refresh()
        stdscr.clrtoeol()
        continue_playing_input = stdscr.getstr(7, 37)[0]

        if continue_playing_input != "y":
            continue_playing = False
    except TypeError as e:
        stdscr.addstr(9, 0, str(e))
        stdscr.refresh()
        time.sleep(1)
        continue_playing = False
    except ValueError:
        continue_playing = False
    finally:
        curses.nocbreak()
        curses.endwin()

    print "Thank you for playing"
    return continue_playing


if __name__ == "__main__":
    total_players = int(raw_input("1 or 2 players? "))
    play_again = True
    while play_again:
        play_again = play(total_players)
