from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

import os
import pandas as pd
import matplotlib.pyplot as plt
import csv


app = Flask(__name__)

app.config['SECRET_KEY'] = 'csvsecret'
toolbar = DebugToolbarExtension(app)


@app.route("/", methods=["GET","POST"])
def index():
    """Upload csv file to save in static folder"""
    if request.method == 'POST':
        file = request.files['csvfile']
        if not os.path.isdir('static'):
            os.mkdir('static')
        filepath = os.path.join('static', file.filename)
        file.save(filepath)

        # read csv file
        data = pd.read_csv(filepath, header=0)
        tablelist = list(data.values)
        data_top = data.head()
        return render_template("index.html", tablelist=tablelist, data_top=data_top)

    return render_template('index.html')


@app.route("/dash", methods=['GET', 'POST'])
def dash():
    """retreve the csv file to convert"""
    if request.method == 'POST':
        variable = request.form['variable']
        data = pd.read_csv('static/test.csv')
        size = len(data[variable])
        
        # plot the data
        plt.bar(range(size), data[variable])
        
        # create an image path
        imagepath = os.path.join('static', 'image' + '.png') 

        plt.savefig(imagepath)
        return render_template('image.html', image = imagepath)

    return render_template('dash.html')

    
    


