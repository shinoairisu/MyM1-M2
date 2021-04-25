# -*- coding: utf-8 -*-
from flask import Flask
import gpuinfo
import req

app=Flask(__name__)

@app.route("/")
def index():
	return req.getter()

@app.route("/gpu")
def getGPU():
	g=gpuinfo.gpuinfo()
	e=""
	for i in g:
		e=e+i+"<br/>"
	return e

if __name__ == '__main__':
	app.run("0.0.0.0",9580)