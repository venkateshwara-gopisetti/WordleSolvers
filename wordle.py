# -*- coding: utf-8 -*-
"""
Created on Sat May 14 00:19:35 2022

@author: Venkat
"""

# =============================================================================
# Importing Libraries
# =============================================================================

import argparse

from src.wordle_objects import WordleServer, WordleBot

def main():
    """
    Main function to interact with CLI.
    Returns
    -------
    None.
    """
    parser = argparse.ArgumentParser(
        prog="Wordle Solver",
        description="A cli utility to start the wordle solver bot.",
        epilog="Checkout the homepage for more updates."
    )
    parser.add_argument("-t", "--task",
                        help="Task for the bot, \
                            if not provided random word is selected from corpus",
                        type=str)
    parser.add_argument("-v",
                        "--verbose",
                        help="Print all the intermediate guesses.",
                        action="store_true")
    args = parser.parse_args()

    wordleserver = WordleServer(args.task)
    bot = WordleBot()
    total_iterations, _ = bot.solver1(server=wordleserver, verbose=args.verbose)
    print("Total Iterations -",total_iterations)

if __name__=="__main__":
    main()
