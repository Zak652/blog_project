from flask import render_template

from . import app
from .database import session, Entry

PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )


#Single Entry view
@app.route("/entry/<id>")
def single_entry_view(id):

    entry = session.query(Entry)
    entry = entry.filter(Entry.id == id).all()
    entry = entry[0]

    return render_template("single_entry.html", entry = entry)


# Get Entry
@app.route("/entry/add", methods=["GET"])
def add_entry_get():
    return render_template("add_entry.html")


# Post Entry to DB
from flask import request, redirect, url_for

@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))

#Edit Entry
@app.route("/entry/<id>/edit", methods=["GET"])
def edit_entry(id):

    entry2edit = session.query(Entry)
    entry2edit = entry2edit.filter(Entry.id == id).all()
    entry2edit = entry2edit[0]

    title = entry2edit.title
    content = entry2edit.content

    return render_template("edit_entry.html", title = title, content = content)

@app.route("/entry/<id>/edit", methods=['POST'])
def update_entry(id):

    entryupdate = Entry(
        id = id,
        title = request.form["title"],
        content = request.form["content"]
        )
    session.merge(entryupdate)
    session.commit()
    return redirect(url_for("entries"))

#Delete Entry
@app.route("/entry/<id>/delete")
def entry_to_delete(id):
    
    entry2delete = session.query(Entry)
    entry2delete = entry2delete.filter(Entry.id == id).all()
    entry2delete = entry2delete[0]

    return render_template("delete_entry.html", entry = entry2delete)

from flask import flash

@app.route("/entry/<id>/deleted")
def delete_entry(id):

    del_entry = session.query(Entry).filter(Entry.id == id).first()

    session.delete(del_entry)
    session.commit()

    return redirect(url_for("entries"))