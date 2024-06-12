# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response,send_file,render_template_string

app = Flask(__name__)


@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("80")) #,port=int("80") #,ssl_context='adhoc' ,debug=True
