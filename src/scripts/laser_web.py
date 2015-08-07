#!/usr/bin/env python
__author__ = 'andrii.kudriashov@gmail.com'

from flask import Flask

app = Flask('Hokuyo')


@app.route('/')
def home():
    return "hello flask"

if __name__ == '__main__':
    app.run()



