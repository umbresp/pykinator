#!/usr/bin/env python

from pykinator.core import Pykinator

import sys


class PykinatorCli(Pykinator):

    def __init__(self, **kwargs):

        Pykinator.__init__(self, **kwargs)


    def run(self):

        print("Type 'quit' to stop playing\n"
              "or 'guess' to force a guess\n"
              "\nhave fun!\n\n")

        print(self.start())
        response = input("> ")

        while (not self.game_over):
            if response in ["quit","exit","q"]:
                print("goodbye.")
                sys.exit()

            if response in ["guess", "done"]:
                self.guessing = True
                print(self.guess())
                response = input("> ")
                continue

            if self.guessing:
                print(self.guess(response))
                continue

            print(self.answer(response))
            response = input("> ")


if __name__ == "__main__":

    pkc = PykinatorCli()
    pkc.run()
