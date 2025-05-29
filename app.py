from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def Addthingy():
    with sqlite3.connect("database.db") as conn:
        conn.cursor().execute("INSERT INTO asset (title, description, normal, diffuse) VALUES (?, ?, ?, ?)", ("cohen", "This is a cohen", "cohen.png", "cohendiffuse.png"))

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
    return render_template('home.html', tags=tags, assets=assets)


@app.route('/add', methods=["GET", "POST"])
def add():
    name = request.form.get('name')
    return render_template('home.html', title=name)


@app.route("/test")
def test():
    Addthingy()
    return app.redirect("/")


app.run(debug=True)