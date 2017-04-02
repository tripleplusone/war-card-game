# Import modules
import pandas as pd
import numpy as np
from collections import Counter

###############################################################################
# ############################## Set up #######################################
###############################################################################


# Shuffle cards and deal initial hands
def initial_cards():
    deck = list(range(2, 15))*4
    np.random.shuffle(deck)  # Tried to use sample method...this is easier
    a_cards = deck[:26]
    b_cards = deck[26:]
    return a_cards, b_cards


# Records inital distribution of deck
def card_distro(cards):
    results_dict = dict(Counter(cards))
    return results_dict


# Reshuffle methods; when you have the pile, do you just put it back in the
# order you got it, or do you completely shuffle the pile?
def pile_in_order(pile):
    pile.reverse()
    return pile


def shuffle_pile(pile):
    np.random.shuffle(pile)
    return pile


# Play war; returns the initial hand of player A and if they won or loss
def play_game(reshuffle_method):
    # Initialize
    a_cards, b_cards = initial_cards()
    a_pile, b_pile = [], []
    a_sidepot, b_sidepot = [], []
    num_turns, num_ties = 0, 0
    a_results = card_distro(a_cards)

    # Actual gameplay
    while len(a_cards)*len(b_cards) > 0:
        # Draw card from top of deck
        a_topcard = a_cards.pop()
        b_topcard = b_cards.pop()

        # Scenarios if there's a clear winner
        if a_topcard > b_topcard:
            a_pile.extend(a_sidepot + b_sidepot + [a_topcard, b_topcard])
            a_sidepot, b_sidepot = [], []
            num_turns += 1
        elif a_topcard < b_topcard:
            b_pile.extend(a_sidepot + b_sidepot + [a_topcard, b_topcard])
            a_sidepot, b_sidepot = [], []
            num_turns += 1

        # Tie! First check if enough cards, then proceed
        else:
            if len(a_cards) == 0:
                if len(a_pile) > 0:
                    a_cards = reshuffle_method(a_pile)
                    a_pile = []
                else:
                    a_results['Num Turns'] = num_turns
                    a_results['Num Ties'] = num_ties
                    a_results['Win/Lose'] = 0
                    continue

            if len(b_cards) == 0:
                if len(b_pile) > 0:
                    b_cards = reshuffle_method(b_pile)
                    b_pile = []
                else:
                    a_results['Num Turns'] = num_turns
                    a_results['Num Ties'] = num_ties
                    a_results['Win/Lose'] = 1
                    continue

            a_sidepot.extend([a_topcard, a_cards.pop()])
            b_sidepot.extend([b_topcard, b_cards.pop()])
            num_ties += 1

        # Check if decks are empty
        if len(a_cards) == 0:
            if len(a_pile) > 0:
                a_cards = reshuffle_method(a_pile)
                a_pile = []
            else:
                a_results['Num Turns'] = num_turns
                a_results['Num Ties'] = num_ties
                a_results['Win/Lose'] = 0

        if len(b_cards) == 0:
            if len(b_pile) > 0:
                b_cards = reshuffle_method(b_pile)
                b_pile = []
            else:
                a_results['Num Turns'] = num_turns
                a_results['Num Ties'] = num_ties
                a_results['Win/Lose'] = 1

    return a_results


# Play game multiple times and record results in df
def play_multiple(num_games, reshuffle_method):
    df = pd.DataFrame()
    for i in range(num_games):
        results = play_game(reshuffle_method)
        df = df.append(pd.DataFrame(results, index=[i]))
    df.fillna(0, inplace=True)
    df = df[[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 'Num Turns',
             'Num Ties', 'Win/Lose']]
    df.columns = ['Num 2s', 'Num 3s', 'Num 4s', 'Num 5s', 'Num 6s', 'Num 7s',
                  'Num 8s', 'Num 9s', 'Num 10s', 'Num Jacks', 'Num Queens',
                  'Num Kings', 'Num Aces', 'Num Turns', 'Num Ties', 'Win/Lose']
    return df

###############################################################################
# ############################## Analysis #####################################
###############################################################################

# Run simulations
num_games = 100000
war_results = play_multiple(num_games, shuffle_pile)
# war_results2 = play_multiple(num_games, pile_in_order) # Infinite loops?
war_results.to_csv("war_results.csv", index=False)

# Analyze
print(Counter(war_results['Win/Lose']))
print(war_results['Num Turns'].mean())
print(war_results['Num Ties'].mean())

war_results['Num Turns'].plot.hist()
war_results['Num Ties'].plot.hist()

war_results.plot.scatter('Num Turns', 'Num Ties')

print(war_results.groupby('Num Aces').mean())
