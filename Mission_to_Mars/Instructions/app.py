from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrap_mars
import json
from bson import ObjectId

app = Flask(__name__, template_folder='templates')

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

#setup route
@app.route("/")
def index():
    #get info from db
    mars_data = mongo.db.marsData.find_one()
    #print(mars_data)
    return render_template("index.html", mars=mars_data)

#setup route
@app.route("/scrape")
def scrape():
    #db collection
    marsCollection = mongo.db.marsData
    
    #keep rerunning script, drop table if exist in mongo
    mongo.db.marsData.drop()
    
    
    #return "You reached the scrape route
    #call mars script
    mars_data = scrap_mars.scrape_all()
    #print(mars_data)
    
    #load dictionary into mongo DB
    marsCollection.insert_one(mars_data)
    
    #back to index route
    return redirect("/")
   
if __name__=="__main__":
    app.run()