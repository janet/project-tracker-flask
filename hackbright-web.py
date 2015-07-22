from flask import Flask, request, render_template

import hackbright

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()

app = Flask(__name__)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    
    projects = hackbright.get_projects_by_github(github)

    # return "%s is the GitHub account for %s %s" % (github, first, last)
    html = render_template("student_info.html", 
                            first=first, 
                            last=last, 
                            github=github,
                            projects=projects)
    return html

@app.route("/student-add")
def student_add():
    """Add a student."""

    # if first,last,github is None:
    #     return render_template("")


    html = render_template("student_add.html")
    return html

@app.route("/student-added", methods=['POST'])
def student_added_template():
    first = request.form.get('firstname')
    last = request.form.get('lastname')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)

    return render_template("student_added.html",
                            first=first, 
                            last=last, 
                            github=github)

if __name__ == "__main__":
    app.run(debug=True)