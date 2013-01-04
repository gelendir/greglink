import os

from greglink import app, lib, models
from flask import render_template, request, redirect, url_for


@app.route('/')
def index():
    testcases = lib.all_tests()
    for testcase in testcases:
        status = models.test_status(testcase['id'])
        if status:
            testcase['status'] = status

    return render_template('index.html', testcases=testcases)

@app.route('/<id>/execute')
def execute_test(id):
    testcase = lib.find_test(id)
    if not testcase:
        return ("Test not found", 404)

    return render_template('execute_test.html', testcase=testcase)

@app.route('/<id>/passed')
def test_success(id):
    testcase = lib.find_test(id)
    if not testcase:
        return ("Test not found", 404)

    models.test_success(testcase)
    return redirect('/')

@app.route('/<id>/blocked')
def test_blocked(id):
    testcase = lib.find_test(id)
    if not testcase:
        return ("Test not found", 404)

    models.test_blocked(testcase)
    return redirect('/')

@app.route('/<id>/failed')
def test_failed(id):
    testcase = lib.find_test(id)
    if not testcase:
        return ("Test not found", 404)

    models.test_failed(testcase)
    return redirect('/')

