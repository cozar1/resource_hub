from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT name,icon FROM Tag")
    tags = cur.fetchall()

    cur.execute("SELECT id, title FROM asset")
    assets = cur.fetchall()

    alist = []
    for asset in assets:
        thing = []
        for i in asset:
            thing.append(i)
        alist.append(thing)

    print(alist)
    for asset in alist:
        cur.execute("SELECT name,icon FROM Tag WHERE ID IN (SELECT Tag_ID FROM assetTags WHERE Model_ID = ?)", (asset[0],))
        asset.append(cur.fetchall())
    assets = alist

    print(assets)
    conn.close()
    return render_template('home.html', tags=tags, assets=assets,show_navbar=True)


@app.route('/upload')
def upload():
    return render_template('upload.html',show_navbar=False)

@app.route('/asset/<int:id>')
def asset(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT id,title,description FROM asset WHERE ID = ?", (id,))
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

    print(assettags)

    return render_template('asset.html',show_navbar=False,asset=asset,creator=creator,assettags=assettags)

app.run(debug=True)