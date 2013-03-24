import argparse
import unittest

def run_tests():
    unittest.main(module='test.compare_test', exit=False, argv=['ponypackchangelog.py', '-v'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do stuff')
    parser.add_argument('-t', '--run-tests', action='store_true')
    args = parser.parse_args()
    if (args.run_tests):
        run_tests()
    
    input('Press enter to finish ..')