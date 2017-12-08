"""We use closures and function variables a lot in Javascript. 
We don’t use them as often in Python, but we can. 
Here is some Python code that does use them. What does it print?"""

def object_like():
    this = { "count": 0 }
    def incr():
        this["count"] += 1
    this["incr"] = incr
    def reset():
        this["count"] = 0
    this["reset"] = reset
    def val():
        return this["count"]
    this["val"] = val
	return this

unobj = object_like()
unobj["incr"]()
unobj["incr"]()
unobj["incr"]()
v = unobj["val"]()
print(v)
#prints 3


"""The flask application excerpted below is using the wrong approach to manage persistent state. 
It might pass a set of simple test cases, and yet fail when deployed for production use. 
What will go wrong? """

# Default values
COLOR = "all"
SIZE = "all"
##########################
# Pages & other requests
##########################
@app.route("/index")
@app.route("/")
def index():
    flask.flash("Colors selected: {}".format(COLOR))
    flask.flash("Sizes selected: {}".format(SIZE))
    return flask.render_template("sweaters.html")
@app.route("/select_sweaters", methods=[’POST’])
def select_sweaters():
    global COLOR
    global SIZE
    SIZE = flask.request.form.get(’size’)
    COLOR = flask.request.form.get(’color’)
    return flask.redirect(flask.url_for(’index’))
"""the global variables would change if someone else on the same page (at the same time) 
selected something different than you, after you selected your preference. """


"""Here is some brittle, repetitious code for checking pre-requisites. 
Updating it with new pre- requisites will be error-prone. 
Rewrite function may_take so that changes in pre-requisites are easier and less error-prone. 
(Leave functions grade_ok and has_passed as-is.) """

# Transcripts look like this:
transcript_1 = [("CIS 210", "A"), ("CIS 211", "B"), ("CIS 212", "A-"),
                ("CIS 314", "B"), ("Math 231", "B"), ("Math 232", "C")]
def grade_ok(required, earned):
    """Returns True iff earned grade is at least required grade."""
    grade_ordering = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C",
                      "P", "C-", "D+", "D", "D-", "F+", "N", "F", "F-"]
    return grade_ordering.index(required) >= grade_ordering.index(earned)
def has_passed(course, min_grade, transcript):
    """Does the transcript include a high enough grade in the required course?"""
    for taken in transcript:
        title, earned_grade = taken
        if title == course and grade_ok(min_grade, earned_grade):
            return True
    return False
# Brittle code needs rewrite
#
def may_take(requested, transcript):
    """May the student with this transcript take the requested course?"""
    if requested == "CIS 211":
        return has_passed("CIS 210", "B", transcript)
    elif requested == "CIS 212":
        return has_passed("CIS 211", "B", transcript)
    elif requested == "CIS 314":
        return has_passed("CIS 212", "B", transcript)
    elif requested == "CIS 313":
        return (has_passed("CIS 212", "B", transcript) and
               has_passed("Math 232", "B-", transcript))
    elif requested == "CIS 315":
        return has_passed("CIS 313", "C", transcript)
    elif requested == "CIS 415":
        return has_passed("CIS 314", "C", transcript)
    elif requested == "CIS 422":
        return has_passed("CIS 313", "C", transcript)
    # more cases here
    else:
        return True  # meaning there are no pre-requisites

#example solution:
PREREQ = { "CIS 211": [("CIS 210", "B")], "CIS 212": [("CIS 211", "B")],
           "CIS 313": [("CIS 212", "B"), ("Math 232", "B-")],
           "CIS 314": [("CIS 212", "B")], "CIS 315": [("CIS 313", "C")],
           "CIS 415": [("CIS 314", "C")], "CIS 422": [("CIS 313", "C")] }
def may_take(requested, transcript):
    """May the student with this transcript take the requested course?"""
    if requested not in PREREQ:
        return True
    for prereq in PREREQ[requested]:
        course, min_grade = prereq
        if not has_passed(course, min_grade, transcript):
            return False
    return True

"""Suppose person X in Cincinnati and and person Y in Seattle are using our Flask application at the same time. 
Person X submits a form, and our application stores some data in the session object:"""
  session[’select_status’] = request.form.get(’select’)
"""Person Y then submits a form, and our application again stores some data in the session ob ject:"""
  session[’select_status’] = request.form.get(’select’)
"""Does the data submitted by person Y replace the data submitted by person X? 
Will person X accidentally see person Y’s data? If not, why not?

example:
Person X and person Y have different session objects, even if their requests are being pro- cessed concurrently. 
Between requests, the session object is stashed in the browser as a cookie, so that person X and person Y continue to have their own individual sessions and never see or modify each other’s data."""


#I’d like to create some good automated tests for a Flask application that includes this ajax handling function. 
#Rewrite it so that I can more easily automate the testing.
FACULTY = [("Ariola, Zena", "ariola@cs.uoregon.edu"),
           ("Childs, Hank", "hank@cs.uoregon.edu"),
           ("Dou, Dejing", "dou@cs.uoregon.edu"),
           # ... several more elided ...
           ("Wu, Xiaodi", "xiaodiwu@cs.uoregon.edu"),
           ("Young, Michal", "michal@cs.uoregon.edu")]
           
@app.route("/_get_email")
def _get_email():
  lname = request.args.get(’lname’, ’’, type=str)
  low = 0
  high = len(FACULTY) - 1
  while low <= high:
    mid = (low + high) // 2
    fac_name, fac_email = FACULTY[mid]
    if fac_name.startswith(lname):
      return jsonify(result=fac_email)
    if lname > fac_name:
      low = mid + 1
    else:
      high = mid - 1
  return jsonify(result="???")
#Testing this code as written requires generating requests and scanning results in JSON form. 
#(That’s at least better than scanning HTML of generated pages, as we would need to do if it called render template instead of jsonify.) 
#It’s much better to factor the lookup functionality from the request handling, like this:

 @app.route("/_get_email")
def _get_email():
  lname = request.args.get(’lname’, ’’, type=str)
  result = email_lookup(lname)
  return jsonify(result=result)
def email_lookup(lname):
  low = 0
  high = len(FACULTY) - 1
  while low <= high:
    mid = (low + high) // 2
    fac_name, fac_email = FACULTY[mid]
    if fac_name.startswith(lname):
      return fac_email
    if lname > fac_name:
      low = mid + 1
    else:
      high = mid - 1
  return "???"