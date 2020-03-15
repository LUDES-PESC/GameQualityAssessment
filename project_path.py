def make_absolute_path(relative_path):
    import os.path
    root_dir = os.path.dirname(__file__)
    if ('A' < root_dir[0] and root_dir[0] < 'Z') or ('a' < root_dir[0] < 'z'):
        root_dir = root_dir[2:]
        root_dir = root_dir.replace('\\','/')
    abspath = os.path.abspath(os.path.join(root_dir,relative_path))
    return abspath