# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from parser.marketwatch import parser as marketwatch_parser
from parser.bloomberg import parser as bloomberg_parser
from parser.yahoo import parser as yahoo_parser

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('process if parsing have started')

    tegs = ['amazon', 'tesla', 'Boeing', 'Facebook', 'NVIDIA', 'Netflix', 'AMD', 'Alphabet',
              'Disney', 'VISA', 'INTEL', 'Mastercard']
    marketwatch_parser(tegs_list=tegs)

    query_list = ['apple', 'amazon', 'tesla', 'Boeing', 'Microsoft', 'Facebook', 'NVIDIA', 'Netflix', 'AMD', 'Alphabet',
                  'Disney', 'VISA', 'INTEL', 'Mastercard']
    bloomberg_parser(query_list=query_list)

    query_list = ['MSFT', 'TSLA', 'GOOG', 'AMZN', 'AMD', 'AAPL', 'BA', 'DIS', 'FB', 'INTC', 'MA', 'NFLX', 'NVDA', 'V']
    yahoo_parser(query_list=query_list)