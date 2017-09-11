#!/usr/bin/env python

from __future__ import print_function

import argparse
import re
import sys

def script_args():
  parser = argparse.ArgumentParser(description='Test')
  parser.add_argument('--words', '-w', nargs='*', type=str,
    help='A list of strings corresponding to 5 d6 rolls to determine diceware words.')
  parser.add_argument('--supplementary', '-s', nargs='*', type=str, default=[],
    help='A list of strings corresponding to 4 d6 rolls to force substitution of numbers/non-alphanumeric characters.')
  
  return parser.parse_args()

def find_word(fname=None, roll=None):
  fname = (fname if fname is not None else './config/en_eff.wordlist.txt')
  roll = (roll if roll is not None else roll)
  with open(fname, 'r') as f:
    for line in f.readlines():
      if roll in line:
        return line.split()[1]

def find_supplementary(word_list=[], roll=[]):
  word_list = (word_list if word_list != [] else word_list)
  roll = (roll if roll != [] else roll)
  supplementary_chars = [
    ['~', '!', '#',  '$', '%', '^'],
    ['&', '*', '(',  ')', '-', '='],
    ['+', '[', ']', '\\', '{', '}'],
    [':', ';', '"', '\'', '<', '>'],
    ['?', '/', '0',  '1', '2', '3'],
    ['4', '5', '6',  '7', '8', '9']
  ]
  word_index = (roll[0] + 1) % len(word_list) - 1
  selected_word = word_list[word_index]
  length_word = len(selected_word)
  char_roll = roll[1] + 1
  char_index = (char_roll - 1) if char_roll <= length_word else char_roll % length_word - 1
  selected_char = selected_word[char_index]
  supplementary_char = supplementary_chars[roll[3]][roll[2]]
  new_word = ''.join(
    [(supplementary_char if i == char_index else selected_word[i]) 
    for i in range(0, len(selected_word))])
  return [new_word if word == selected_word else word for word in word_list]


def parse_roll(roll='111111', d='6'):
  """Takes a string of numbers and returns array of integers. Roll is 0 to (d-1)"""
  pattern = re.compile('^[1-{}]+$'.format(d))
  if pattern.match(roll):
    return [(int(die) - 1) for die in list(roll)]
  else:
    return None

def main(argv=None):
  """Main execution loop"""
  argv = (argv if argv is not None else script_args())
  words = [find_word('./config/eff-default_wordlist.txt', roll) for roll in argv.words]
  for roll in argv.supplementary:
    words = find_supplementary(words, parse_roll(roll))
  print(words)
  print(''.join(words))

if __name__ == "__main__":
  sys.exit(main())
