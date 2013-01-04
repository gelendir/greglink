import os

from greglink import app, lib, models
from flask import render_template, request, redirect, url_for


@app.route('/')
def index():
    return render_template('index.html')

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

    return "test passed"

@app.route('/<id>/blocked')
def test_blocked(id):
    testcase = lib.find_test(id)
    if not testcase:
        return ("Test not found", 404)

    models.test_blocked(testcase)

    return "test blocked"

@app.route('/<id>/failed')
def test_failed(id):
    testcase = lib.find_test(id)
    if not testcase:
        return ("Test not found", 404)

    models.test_failed(testcase)

    return "test failed"
