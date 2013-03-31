import sys
import argparse
import unittest
import os
import pprint

sys.path.append("impl")
import compare
import themefile
import foldermanagement
import logging

def test_module(mod:str):
    unittest.main(module=mod, exit=False, argv=['ponypackchangelog.py', '-v'])

def run_tests():
    logging.debug("running tests")
    test_module('test.compare_test')
    test_module('test.themefile_test')

def run_compare(source_dir:str, target_dir:str):
    if target_dir is None: target_dir = foldermanagement.get_pack()
    
    logging.debug("running comparison between {0} and {1}".format(source_dir, target_dir))

    foldermanagement.check_dir(source_dir)
    foldermanagement.check_dir(target_dir)
    themediffs = compare.compare(themefile.from_file(os.path.join(source_dir, 'theme')), 
                                 themefile.from_file(os.path.join(target_dir, 'theme')))
    themediffs = [(emote,result) for emote,result in themediffs.items() if result != '<same>']

    return (themediffs, None) # todo filediffs

def pretty_print(results:[(str,str)]):
    for result in results:
        if (isinstance(result[1], tuple)):
            print('Emote ' + result[0] + ' was changed from ' + result[1][0] + ' to ' + result[1][1])
        if result[1] == '<same>':
            continue
        if result[1] == '<added>':
            print('Emote ' + result[0] + ' was added')
        if result[1] == '<removed>':
            print('Emote ' + result[0] + ' was removed')



if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Do stuff')
    parser.add_argument('-t', '--run-tests', action='store_true')
    parser.add_argument('sourcedir', nargs='?', type=str)
    parser.add_argument('targetdir', nargs='?', type=str)
    args = parser.parse_args()

    if (args.run_tests):
        run_tests()
    else:
        pretty_print(run_compare(args.sourcedir, args.targetdir)[0])
    
    input('Press enter to finish ..')