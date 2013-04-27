from datetime import datetime
import os
import tempfile
import zipfile
import urllib.request
import hashlib
import ntpath
import logging

def folder_name(base:str, dt:datetime) -> str:
    return "{0}-{1}-{2}-{3}-{4}{5}".format(base, dt.year, dt.month, dt.day, dt.hour, dt.minute)

def download_pack() -> str:    
    pack = 'http://tinyurl.com/ponypack'
    response = urllib.request.urlopen(pack)
    filename = tempfile.mktemp() + '.zip'
    local = open(filename, 'wb')
    logging.debug("downloading pack from {0} to {1}".format(pack, filename))
    local.write(response.read())
    local.close()
    return filename

def extract_pack(zip_file:str, output_dir:str):
    logging.debug("extracting pack from {0} to {1}".format(zip_file, output_dir))
    zip = zipfile.ZipFile(zip_file, 'r')
    zip.extractall(output_dir)
    zip.close()

def path_leaf(path):
    """ http://stackoverflow.com/questions/8384737/python-extract-file-name-from-path-no-matter-what-the-os-path-format """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def get_file_list(dir:str) -> dict:
     file_list = [os.path.join(dir, f) for f in os.listdir(dir) if f != 'theme']
     file_list = [f for f in file_list if os.path.isfile(f)]
     # return a dict of filename -> file hash
     return dict([(path_leaf(f), hashlib.md5(open(f, 'rb').read()).hexdigest()) for f in file_list])

def get_pack(target_dir:str = None):
    target_dir = target_dir or tempfile.mkdtemp()
    logging.debug("fetching pack into {0}".format(target_dir))
    zip = download_pack()
    extract_pack(zip, target_dir)
    logging.debug("removing {0}".format(zip))
    os.remove(zip)

def descend_into_single_directory(path:str) -> str:
    files = os.listdir(path)
    if len(files) == 1 and os.path.isdir(os.path.join(path, files[0])):
        return descend_into_single_directory(os.path.join(path, files[0]))
    else:
        return path

def check_dir(dir:str) -> dir:
    dir = descend_into_single_directory(dir)

    if (dir is None): raise ValueError('source / target directory must be specified')
    if (not os.path.isdir(dir)): raise NotADirectoryError(dir + ' is not a directory')
    if (not os.path.isfile(os.path.join(dir, 'theme'))): raise ValueError('theme file not found in directory '+dir)

    return dir

def get_latest_html(dir:str) -> str:
    files = [(file, os.path.getmtime(file)) 
             for file in [os.path.join(dir, f) for f in os.listdir(dir)] 
             if os.path.isfile(os.path.join(dir, file)) and file.endswith(".html")]
    return _get_latest(files)

def get_latest_subdir(dir:str) -> str:
    files = [(file, os.path.getmtime(file)) 
             for file in [os.path.join(dir, f) for f in os.listdir(dir)] 
             if os.path.isdir(file)] 
    return _get_latest(files)

def _get_latest(files_with_times : [(str, datetime)]) -> str:
    files_with_times.sort(key=lambda x : x[1], reverse=True)
    if len(files_with_times) == 0: return None
    return files_with_times[0][0]

def fetch_quest(base_dir:str) -> (str, str):
    """ given a working dir, return the two folders that should be compared"""
    source_dir = get_latest_subdir(base_dir)
    target_dir = os.path.join(base_dir, folder_name("ponypack", datetime.now()))
    get_pack(target_dir)
    return (source_dir, target_dir)
    