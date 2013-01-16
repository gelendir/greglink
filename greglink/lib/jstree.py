import os

def to_urlpath(root, path):
    urlpath = path[len(root):]
    if not urlpath.startswith('/'):
        urlpath = "/%s" % urlpath
    return urlpath

def create_node(name, urlpath):
    node = {
        'data': name,
        'attr': {
            'href': urlpath
        }
    }

    return node

def create_filenode(root, path, filename):
    urlpath = to_urlpath(root, os.path.join(path, filename))
    node = create_node(filename, urlpath)
    return node

def create_dirnode(root, path, files):
    urlpath = to_urlpath(root, path)
    name = os.path.basename(path)
    node = create_node(name, urlpath)

    children = [create_filenode(root, path, f) for f in files]
    node['children'] = children

    return node

def generate_tree(rootpath):
    tree = {}

    for path, dirs, files in os.walk(rootpath):
        node = create_dirnode(rootpath, path, files)

        if path == rootpath:
            tree[path] = node
        else:
            parent = os.path.dirname(path)
            tree[parent]['children'].append(node)

    return tree[rootpath]
