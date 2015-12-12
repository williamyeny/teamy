from flask import Flask, request, render_template, redirect, flash, session, make_response
import random, string

app = Flask(__name__)

teamList = {}
users = {}

def loggedIn():
  return not request.cookies.get("name") is None

@app.route("/")
def home():
  if request.cookies.get('session') is None:
    resp = make_response(render_template("landingpage.html"))
    resp.set_cookie('session', ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30)))
    return resp
  return render_template("landingpage.html")

@app.route("/register", methods=["POST"])
def register():
  name = request.form["name"]
  resp = make_response(redirect("teams"))
  resp.set_cookie('name', name)
  return resp
  

@app.route("/teams")
def teams():
  if loggedIn():
    userid = request.cookies["session"]

    return render_template("teams.html", tList=teamList, users = users, userid = userid)
  else:
    return redirect("/")

@app.route("/create")
def create():
  if loggedIn():
    return render_template("create.html")
  else:
    return redirect("/")

@app.route("/join-team", methods=["POST"])
def joinTeam():
  users[request.cookies["session"]] = request.form["id"]
  teamList[request.form["id"]]["members"].append({
      "userid":request.cookies["session"],
      "name":request.cookies["name"],
    }) 
  return redirect("teams")

@app.route("/delete-team", methods=["POST"])
def deleteTeam():
  users.pop(request.cookies["session"], None)
  teamList.pop(request.cookies["session"], None)
  return redirect("teams")

@app.route("/leave-team", methods=["POST"])
def leaveTeam():
  teamList[request.form["id"]]["members"].remove({"userid":request.cookies["session"], "name":request.cookies["name"],})
  users.pop(request.cookies["session"], None)
  return redirect("teams")
    
@app.route("/make-team", methods=["POST"])
def makeTeam():
  teamList[request.cookies["session"]] = {
    "name":request.cookies["name"] ,
    "tname":request.form["tname"],
    "desc":request.form["desc"]
  }
  teamList[request.cookies["session"]]["members"] = [{"userid":request.cookies["session"],"name":request.cookies["name"]}]
  users[request.cookies["session"]] = request.cookies["session"]
  
  return redirect("teams")

app.secret_key = 'oRaNgE'
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=4567, debug=True)