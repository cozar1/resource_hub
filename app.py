from flask import Flask, render_template, request
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/images/"

@app.route('/')
def home():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT name,icon FROM Tag")
    tags = cur.fetchall()

    cur.execute("SELECT id, name FROM asset")
    assets = cur.fetchall()

    alist = []
    for asset in assets:
        thing = []
        for i in asset:
            thing.append(i)
        alist.append(thing)

    for asset in alist:
        cur.execute("SELECT name,icon FROM Tag WHERE ID IN (SELECT Tag_ID FROM assetTags WHERE Model_ID = ?)", (asset[0],))
        asset.append(cur.fetchall())
    assets = alist

    conn.close()
    return render_template('home.html', tags=tags, assets=assets,show_navbar=True)


@app.route('/upload', methods=["GET", "POST"])
def upload():
    error = None    
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        # Grab uploaded files
        diffuse_file = request.files.get("diffuse")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Insert the asset
        cursor.execute("INSERT INTO asset(name, description) VALUES(?, ?)", (name, description))
        conn.commit()

        # Get the asset ID
        asset_id = cursor.lastrowid

        conn.close()

        # Save image if it exists
        if diffuse_file and diffuse_file.filename:
            filename = secure_filename(f"{asset_id}d.png")
            diffuse_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return render_template('upload.html', show_navbar=False)

@app.route('/asset/<int:id>')
def asset(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT id,name,description FROM asset WHERE ID = ?", (id,))
    asset = cur.fetchall()

    cur = conn.cursor()
    cur.execute("SELECT CreatorID FROM Credit WHERE AssetID = ?", (id,))
    creator_id = cur.fetchall()
    
    cur = conn.cursor()
    cur.execute("SELECT name FROM Creator WHERE ID = ?", (int(creator_id[0][0]),))
    creator = cur.fetchall()

    cur = conn.cursor()
    cur.execute("SELECT name,icon FROM Tag WHERE ID IN (SELECT Tag_ID FROM assetTags WHERE Model_ID = ?)", (id,))
    assettags = cur.fetchall()
    return render_template('asset.html',show_navbar=False,asset=asset,creator=creator,assettags=assettags)

app.run(debug=True)