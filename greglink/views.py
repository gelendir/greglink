import os

from greglink import app
from greglink.models.testcase import TestCase
from greglink import models, testload
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
    testcases = testload.all_tests(path)
    folders = all_folders(path)
    return render_template('index.html', testcases=testcases, folders=folders)

@app.route('/<path:path>/execute')
def execute_test(path):
    testcase = testload.find_test(path)
    if not testcase:
        return ("Test not found", 404)

    return render_template('execute_test.html', testcase=testcase)

@app.route('/<path:path>/passed')
def test_success(path):
    testcase = testload.find_test(path)
    if not testcase:
        return ("Test not found", 404)

    models.save_success(testcase)
    return redirect('/')

@app.route('/<path:path>/blocked')
def test_blocked(path):
    testcase = testload.find_test(path)
    if not testcase:
        return ("Test not found", 404)

    models.save_blocked(testcase)
    return redirect('/')

@app.route('/<path:path>/failed')
def test_failed(path):
    testcase = testload.find_test(path)
    if not testcase:
        return ("Test not found", 404)

    models.save_failed(testcase)
    return redirect('/')

@app.route('/<path:path>/bla')
def test_bla(path):
    return path

