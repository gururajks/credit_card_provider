import fileinput

import sys
from credit_card_provider import bank


def read_from_file(input_file):
    current_bank = bank.Bank()
    with open(input_file) as fp:
        for line in fp.readlines():
            current_bank.execute(line)

    output = current_bank.transaction_log()
    for line in output:
        print(line)


def read_from_stdin(std_input):
    current_bank = bank.Bank()
    for line in std_input:
        current_bank.execute(line)

    output = current_bank.transaction_log()
    for line in output:
        print(line)


def main():
    # read from file and expects 2 arguments
    if len(sys.argv) == 2:
        read_from_file(sys.argv[1])
    elif len(sys.argv) == 1:
        read_from_stdin(fileinput.input())


if __name__ == "__main__":
    main()
