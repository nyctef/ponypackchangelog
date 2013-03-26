import sys
import argparse
import unittest
import os
import hashlib
import ntpath
import pprint
import tempfile
import urllib2
import zipfile

sys.path.append("impl")
import compare
import themefile

def test_module(mod:str):
    unittest.main(module=mod, exit=False, argv=['ponypackchangelog.py', '-v'])

def run_tests():
    test_module('test.compare_test')
    test_module('test.themefile_test')

def check_dir(dir:str):
    if (dir is None): raise ValueError('source / target directory must be specified')
    if (not os.path.isdir(dir)): raise NotADirectoryError(dir + ' is not a directory')
    if (not os.path.isfile(os.path.join(dir, 'theme'))): raise ValueError('theme file not found in directory '+dir)

def run_compare(source_dir:str, target_dir:str):
    check_dir(source_dir)
    check_dir(target_dir)
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

def path_leaf(path):
    """ http://stackoverflow.com/questions/8384737/python-extract-file-name-from-path-no-matter-what-the-os-path-format """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def get_file_list(dir:str) -> dict:
     file_list = [os.path.join(dir, f) for f in os.listdir(dir) if f != 'theme']
     file_list = [f for f in file_list if os.path.isfile(f)]
     return dict([(path_leaf(f), hashlib.md5(open(f, 'rb').read()).hexdigest()) for f in file_list])

def extract_pack(zip_file:str, output_dir:str):
    with zipfile.ZipFile(zip_file, 'r') as zip:
        zip.extractall(output_dir)

def download_pack() -> str:
    response = urllib2.urlopen('http://tinyurl.com/ponypack')
    filename = tempfile.mktemp + '.zip'
    local = open(filename, 'w')
    local.write(response.read())
    local.close()
    return filename

if __name__ == '__main__':
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