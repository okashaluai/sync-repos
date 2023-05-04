import os
import shutil
import subprocess
import urllib.request  
import re
from distutils import dir_util
import stat


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def rm_dir(path):
    """_summary_

    Args:
        path (_type_): _description_
    """
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=False, onerror=onerror )
    pass

# def branch_browse(url):
#     webUrl = urllib.request.urlopen(url)  


def branch_exists(remote_repo_url, branch_name):
    """_summary_

    Args:
        remote_repo_url (_type_): _description_
        branch_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    branches  = subprocess.check_output(['git', 'ls-remote' , remote_repo_url,  branch_name ], shell=True)
    wc_l = len(re.findall('refs/heads/'+branch_name+'$', branches.decode('utf-8')))
    if wc_l:
        return True
    else: return False

def find_last_slash(str):
    """_summary_

    Args:
        str (_type_): _description_

    Returns:
        _type_: _description_
    """
    res = -1
    for i in range(len(str)):
        if str[i] == '/':
            res = i
    return res

def parse_branch_name(full_ref):
    """_summary_

    Args:
        full_ref (_type_): _description_

    Returns:
        _type_: _description_
    """
    index = find_last_slash(full_ref)
    branch_name = ""
    if index > -1:
        branch_name = full_ref[index + 1:]
    return branch_name


def copy_dir(from_dir, to_dir):
    """_summary_

    Args:
        from_dir (_type_): _description_
        to_dir (_type_): _description_
    """
    shutil.copytree(src=from_dir, dst=to_dir, dirs_exist_ok=True)
    pass


def move_dir(src_dir, dst_dir):
    """_summary_

    Args:
        src_dir (_type_): _description_
        dst_dir (_type_): _description_
    """
    shutil.copytree(src_dir, dst_dir)
    if os.path.exists(src_dir):
        shutil.rmtree(src_dir, ignore_errors=False, onerror=onerror )

    # dir_util.copy_tree(src=from_dir, dst=to_dir)
    
    # rm_dir(from_dir)
    pass


def push_to_remote(local_repo_path):
    """_summary_

    Args:
        local_repo_path (_type_): _description_
    """
    subprocess.run(['git', '-C',local_repo_path, 'add', '.'], shell=True)
    subprocess.run(['git', '-C', local_repo_path, 'commit', '-m', 'Merge from: internal repo' ], shell=True)
    subprocess.run(['git', '-C',local_repo_path, 'push' , 'origin'], shell=True)
    pass
