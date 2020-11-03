import fileinput

import sys
from credit_card_provider import bank


def read_from_file(input_file):
    b = bank.Bank()
    with open(input_file) as fp:
        for line in fp.readlines():
            b.execute(line)

    b.transaction_log()


def read_from_stdin(std_input):
    b = bank.Bank()
    for line in std_input:
        b.execute(line)

    b.transaction_log()


def main():
    if len(sys.argv) == 2:
        read_from_file(sys.argv[1])
    elif len(sys.argv) == 1:
        read_from_stdin(fileinput.input())


if __name__ == "__main__":
    main()
