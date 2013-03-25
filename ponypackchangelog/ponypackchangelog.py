import argparse
import unittest

def test_module(mod:str):
    unittest.main(module=mod, exit=False, argv=['ponypackchangelog.py', '-v'])

def run_tests():
    test_module('test.compare_test')
    test_module('test.themefile_test')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do stuff')
    parser.add_argument('-t', '--run-tests', action='store_true')
    args = parser.parse_args()

    if (args.run_tests):
        run_tests()
    
    input('Press enter to finish ..')