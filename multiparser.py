#!/usr/bin/env python
# Goal: Create a CLI using arparse
# Function: Two subcommands, one prints contents of directory passed as argument and one adds the arguments and
# outputs the results

# Resources: this blog post: http://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html

import argparse
import sys
import os
from collections import namedtuple, Counter
import Geohash


class CliPrint(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Print what you tell it to do',
            usage='''python multiparser.py <command> [<args>]

        The commands of this function are
        print_dir     Print contents of dir
        print_list      Add elements in a list
        geohash       Geohash x,y coordinates
        ''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print 'Unrecognized command'
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()


    def print_dir(self):
        """
        Usage: python multiparser.py print_dir --directory <name_of_dir>
        Usage: python multiparser.py print_dir -d <name_of_dir>
        Will print out the contents of the directory passed as argument
        """
        parser = argparse.ArgumentParser(
            description='Print directory in the path')
        # prefixing the argument with -- means it's optional
        parser.add_argument('-d', '--directory', nargs=1)
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (script name) and the subcommand (print_dir)
        args = parser.parse_args(sys.argv[2:])
        dir_contents = os.listdir(args.directory[0])

        print 'Outputing contents of passed directory {0}: {1}'.format(args.directory[0], dir_contents)

    def add_list(self):
        parser = argparse.ArgumentParser(
            description='Sum elements of list')
        # If no -- prefixing is present, it means argument is required and is also positional
        parser.add_argument('-n', '--numbers', nargs='+', type=int)
        args = parser.parse_args(sys.argv[2:])
        added_nums = sum(args.numbers)
        print args
        print 'The sum of the numbers in this list {0} is: {1}' .format(args.numbers, added_nums)

    def count_words(self):
        parser = argparse.ArgumentParser(
                description='Sum occurences of words')
        # If no -- prefixing is present, it means argument is required and is also positional
        parser.add_argument('-w', '--words', nargs='+')
        args = parser.parse_args(sys.argv[2:])
        counter = Counter()
        for word in args.words:
            counter[word] += 1
        print counter

    def geohash(self):
        parser = argparse.ArgumentParser(
            description='Create a named tuple with x,y coordinates from arguments given')

        parser.add_argument('-c', '--coordinates', nargs=2, type=float)
        args = parser.parse_args(sys.argv[2:])
        geom = namedtuple("Geometry", ["x", "y", "geo"])
        print geom(args.coordinates[0], args.coordinates[1], Geohash.encode(args.coordinates[0], args.coordinates[1]))


if __name__ == '__main__':
    CliPrint()
