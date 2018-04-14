#!/usr/bin/env python

from pykinator.bot import PykinatorBot

pkb = PykinatorBot()

initial_question = pkb.start()

print(initial_question)
response = input("> ")

while (not pkb.game_over):
    if pkb.can_guess:
        print("guessing: ", response)
        print(pkb.guess(response))
        continue

    print(pkb.answer(response))
    response = input("> ")
