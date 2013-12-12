import sys
import argparse
import unittest
import os
import pprint
from datetime import datetime

from impl import *
import logging
import logging.handlers
import queue
import shutil

def test_module(mod:str):
    unittest.main(module=mod, exit=False, argv=['ponypackchangelog.py', '-v'])

def run_tests():
    logging.debug("running tests")
    test_module('test.compare_test')
    test_module('test.themefile_test')

def run_compare(source_dir:str, target_dir:str):
    if target_dir is None: target_dir = foldermanagement.get_pack()
    
    logging.debug("running comparison between {0} and {1}".format(source_dir, target_dir))

    source_dir = foldermanagement.check_dir(source_dir)
    target_dir = foldermanagement.check_dir(target_dir)
    themediffs = compare.compare(themefile.from_file(os.path.join(source_dir, 'theme')), 
                                 themefile.from_file(os.path.join(target_dir, 'theme')))
    themediffs = [(emote,result) for emote,result in themediffs.items() if result != '<same>']

    return (themediffs, None) # todo filediffs

def pretty_print(results:[(str,str)], html = False, header = None) -> str:
    result_string = ""
    
    if html and header:
        result_string += "<h2>{0}</h2>\n".format(header)

    for result in results:
        if (isinstance(result[1], tuple)):
            result_string += 'Emote ' + result[0] + ' was changed from ' + result[1][0] + ' to ' + result[1][1] + '\n'
        if result[1] == '<same>':
            continue
        if result[1] == '<added>':
            result_string += 'Emote ' + result[0] + ' was added\n'
        if result[1] == '<removed>':
            result_string += 'Emote ' + result[0] + ' was removed\n'

        if html:
            result_string += "<br />"

    return result_string

def _del(filename):
    print("deleting "+filename+" ..")
    if os.path.lexists(filename):
        os.remove(filename)
        print(".. done")

def ponypackchangelog(base_dir:str):
    source,target = foldermanagement.fetch_quest(base_dir)
    diffs = run_compare(source, target)
    if len(diffs[0]) == 0: 
        logging.debug("No diffs, deleting {0}".format(target))
        shutil.rmtree(target)
        return # no diffs, nothing to do
    logging.info(pretty_print(diffs[0]))
    prev_html = read_previous_html(base_dir)
    
    htmlfname = target.rstrip("\\/") + ".html"
    htmlf = open(htmlfname, 'w')
    htmlf.write(pretty_print(diffs[0], html=True, header=foldermanagement.folder_name("Pony Pack ", datetime.now())))
    if prev_html is not None:
        htmlf.write("\n\n")
        htmlf.write(prev_html)
        
    if hasattr(os, "symlink"):
        cur = os.path.join(base_dir, "current")
        index = os.path.join(base_dir, "index.html")
        _del(cur)
        _del(index)
        print("link "+target+" to "+cur)
        os.symlink(target, cur, target_is_directory=True)
        print("link "+htmlfname+" to "+index)
        os.symlink(htmlfname, index, target_is_directory=False)

def read_previous_html(base_dir:str) -> str:
    prev_file = foldermanagement.get_latest_html(base_dir)
    if prev_file is None: return None
    with open(prev_file, 'r') as hfile:
        return hfile.read()

def email_log(logq:queue):
    loglist = []
    while not logq.empty():
        loglist.append(logq.get_nowait())
    logstrings = ["[{0}] {1}".format(le.levelname,le.message) for le in loglist]
    email_helper.send_email("[ponypackchangelog] ran at {0}".format(datetime.now()), "\n".join(logstrings))

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    
    logq = queue.Queue()
    if hasattr(logging.handlers, "QueueHandler"):
        logging.getLogger().addHandler(logging.handlers.QueueHandler(logq))

    parser = argparse.ArgumentParser(description='Do stuff')
    parser.add_argument('-t', '--run-tests', action='store_true')
    parser.add_argument('basedir', nargs='?', type=str)
    args = parser.parse_args()

    if (args.run_tests):
        run_tests()
    else:
        ponypackchangelog(args.basedir)

    if os.name != 'nt':
        email_log(logq)
