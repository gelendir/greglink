import os
from flask import url_for

ROOT = '/'


def generate_tree(rootpath):
    tree = {}

    root_node = create_folder_node(ROOT)
    tree[ROOT] = root_node

    for path, dirs, files in os.walk(rootpath):
        path = chop_root(rootpath, path)

        folder_nodes = create_folder_nodes(path, dirs)
        file_nodes = create_file_nodes(path, files)

        add_folders_to_tree(tree, path, folder_nodes)

        parent = tree[path]

        add_folders_to_parent(parent, folder_nodes)
        add_files_to_parent(parent, file_nodes)

    return tree[ROOT]['children']


def chop_root(root, path):
    path = path[len(root):]
    if not path.startswith('/'):
        path = "/%s" % path
    return path


def create_folder_nodes(path, folder_names):
    return [create_folder_node(folder_name) for folder_name in folder_names]


def create_folder_node(folder_name):
    return {
        'title': folder_name,
        'isFolder': True,
        'children': []
    }


def create_file_nodes(path, filenames):
    file_nodes = []
    for filename in filenames:
        filepath = os.path.join(path, filename)
        file_nodes.append(create_file_node(filepath, filename))
    return file_nodes


def create_file_node(path, filename):
    return {
        'title': filename,
        'href': url_for('execute_test', path=path),
        'key': path,
    }


def add_folders_to_tree(tree, path, folders):
    for folder in folders:
        treepath = os.path.join(path, folder['title'])
        tree[treepath] = folder


def add_folders_to_parent(parent, folder_nodes):
    parent['children'].extend(folder_nodes)


def add_files_to_parent(parent, file_nodes):
    parent['children'].extend(file_nodes)
