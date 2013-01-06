import os

from greglink import app
from greglink.models.testcase import TestCase, load_file
from greglink.models.locator import all_tests, find_test
from greglink import models
from flask import render_template, request, redirect, url_for


@app.route('/')
def index():
    testcases = all_tests()
    return render_template('index.html', testcases=testcases)

@app.route('/<id>/execute')
def execute_test(id):
    testcase = find_test(id)
    if not testcase:
        return ("Test not found", 404)

    return render_template('execute_test.html', testcase=testcase)

@app.route('/<id>/passed')
def test_success(id):
    testcase = find_test(id)
    if not testcase:
        return ("Test not found", 404)

    models.test_success(testcase)
    return redirect('/')

@app.route('/<id>/blocked')
def test_blocked(id):
    testcase = find_test(id)
    if not testcase:
        return ("Test not found", 404)

    models.test_blocked(testcase)
    return redirect('/')

@app.route('/<id>/failed')
def test_failed(id):
    testcase = find_test(id)
    if not testcase:
        return ("Test not found", 404)

    models.test_failed(testcase)
    return redirect('/')

