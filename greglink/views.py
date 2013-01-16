import os
import json

from greglink import app
from greglink.models import TestCase
from greglink.lib.jstree import generate_tree
from greglink.loading import all_tests, find_test
from greglink import models
from flask import render_template, request, redirect, url_for


def all_folders(path='/'):
    realpath = os.path.join(app.config['TEST_ROOT'], *(path.split("/")))
    folders = [ "%s/%s" % (path.strip("/"), x)
                for x in os.listdir(realpath)
                if os.path.isdir(os.path.join(realpath,x))]

    return folders

@app.route('/')
def index():
    return list_tests('/')

@app.route('/<path:path>')
def list_tests(path):
    testcases = all_tests(path)
    folders = all_folders(path)
    return render_template('index.html', testcases=testcases, folders=folders)

@app.route('/<path:path>/execute')
def execute_test(path):
    testcase = find_test(path)
    if not testcase:
        return ("Test not found", 404)

    return render_template('execute_test.html', testcase=testcase)

@app.route('/<path:path>/passed')
def test_success(path):
    testcase = find_test(path)
    if not testcase:
        return ("Test not found", 404)

    models.save_success(testcase)
    return redirect('/')

@app.route('/<path:path>/blocked')
def test_blocked(path):
    testcase = find_test(path)
    if not testcase:
        return ("Test not found", 404)

    models.save_blocked(testcase)
    return redirect('/')

@app.route('/<path:path>/failed')
def test_failed(path):
    testcase = find_test(path)
    if not testcase:
        return ("Test not found", 404)

    models.save_failed(testcase)
    return redirect('/')

@app.route('/jstree')
def jstree():
    tree = generate_tree(app.config['TEST_ROOT'])
    return (json.dumps(tree), 200)

