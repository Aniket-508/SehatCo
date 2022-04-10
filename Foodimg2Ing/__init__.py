from flask import Flask, render_template, url_for, flash, redirect, request
from Foodimg2Ing.output import output
import os
import mysql.connector

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/", methods=["POST", "GET"])
def predict():

    imagefile = request.files["imagefile"]
    image_path = os.path.join(
        app.root_path, "static/images/demo_imgs", imagefile.filename
    )
    imagefile.save(image_path)
    img = "/images/demo_imgs/" + imagefile.filename
    title, ingredients, recipe = output(image_path)

    mydb = mysql.connector.connect(
        host="localhost", user="root", password="ghotil100", database="covid19"
    )
    mycursor = mydb.cursor(buffered=True)
    ingrbool = []
    l1 = []
    l2 = []
    for i in range(len(ingredients[0])):
        ingname = ingredients[0][i]
        mycursor.execute(
            "SELECT DISTINCT 1 FROM ingredient WHERE Common_Name='" + ingname + "'"
        )
        r = mycursor.fetchone()
        mydb.commit()
        if r:
            l1.append("true")
        else:
            l1.append("false")

    for i in range(len(ingredients[1])):
        ingname = ingredients[1][i]
        mycursor.execute(
            "SELECT DISTINCT 1 FROM ingredient WHERE Common_Name='" + ingname + "'"
        )
        r = mycursor.fetchone()
        mydb.commit()
        if r:
            l2.append("true")
        else:
            l2.append("false")

    # mydb.commit()
    mycursor.close()
    mydb.close()
    ingrbool.append(l1)
    ingrbool.append(l2)

    tcount = 0
    fcount = 0
    for row in ingrbool:
        for r in row:
            if r == "true":
                tcount = tcount + 1
            else:
                fcount = fcount + 1
    percen = (tcount / (tcount + fcount)) * 100

    return render_template(
        "predict.html",
        title=title,
        ingredients=ingredients,
        ingrbool=ingrbool,
        percen=percen,
        recipe=recipe,
        img=img,
    )


@app.route("/<samplefoodname>")
def predictsample(samplefoodname):
    mydb = mysql.connector.connect(
        host="localhost", user="root", password="ghotil100", database="covid19"
    )

    imagefile = os.path.join(
        app.root_path, "static/images", str(samplefoodname) + ".jpg"
    )
    img = "/images/" + str(samplefoodname) + ".jpg"
    title, ingredients, recipe = output(imagefile)

    mycursor = mydb.cursor(buffered=True)
    ingrbool = []
    l1 = []
    l2 = []
    for i in range(len(ingredients[0])):
        ingname = ingredients[0][i]
        mycursor.execute(
            "SELECT DISTINCT 1 FROM ingredient WHERE Common_Name='" + ingname + "'"
        )
        r = mycursor.fetchone()
        mydb.commit()
        if r:
            l1.append("true")
        else:
            l1.append("false")

    for i in range(len(ingredients[1])):
        ingname = ingredients[1][i]
        mycursor.execute(
            "SELECT DISTINCT 1 FROM ingredient WHERE Common_Name='" + ingname + "'"
        )
        r = mycursor.fetchone()
        mydb.commit()
        if r:
            l2.append("true")
        else:
            l2.append("false")

    # mydb.commit()
    mycursor.close()
    mydb.close()
    ingrbool.append(l1)
    ingrbool.append(l2)

    tcount = 0
    fcount = 0
    for row in ingrbool:
        for r in row:
            if r == "true":
                tcount = tcount + 1
            else:
                fcount = fcount + 1
    percen = (tcount / (tcount + fcount)) * 100

    return render_template(
        "predict.html",
        title=title,
        ingredients=ingredients,
        ingrbool=ingrbool,
        percen=percen,
        recipe=recipe,
        img=img,
    )
