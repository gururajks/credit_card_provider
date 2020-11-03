import fileinput

import sys
from credit_card_provider import bank


def read_from_file(input_file):
    b = bank.Bank()
    with open(input_file) as fp:
        for line in fp.readlines():
            b.execute(line)

    b.transaction_log()


def main():
    # if len(sys.argv) == 2:
    #     read_from_file(sys.argv[1])
    # elif len(sys.argv) == 1:
    #     read_from_file(fileinput.input())
    read_from_file("transaction_input")
    # c = another_check.Another_Check()


if __name__ == "__main__":
    main()
