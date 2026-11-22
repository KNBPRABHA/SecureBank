from flask import Flask, request, jsonify, session,redirect, url_for, make_response,render_template_string #importing the Flask class and request and jsonify modules from the flask package
import os
from flask_wtf.csrf import CSRFProtect #importing the CSRFProtect class from the flask_wtf.csrf module to enable CSRF protection for the application

app=Flask(__name__) #creates a flask app instance
csrf=CSRFProtect(app) #enables CSRF protection for the application

app.secret_key=os.environ.get("SECRET_KEY")

users={
    "Sam":"Sam123",
    "John":"John456",
    "Alice":"aLice789"
}

@app.route("/login",methods=["GET","POST"]) #defining the route for /login endpoint and specifying that it accepts both POST and GET requests
def login():
    if request.method=="POST": #checking if the request method is POST
        username=request.form.get("username") #getting the username from the form data
        password=request.form.get("password") #getting the password from the form data
        if username in users and users[username]==password: #checking if the username exists in the users dictionary and if the password matches
            session["username"]=username #storing the username in the session to indicate that the user is logged in
             #redirecting to the home page after successful login

            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials" #returning an error message for invalid credentials

    return render_template_string("""
    <form method="POST">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
  """)

@app.route("/dashboard") #defining the route for /dashboard endpoint
def dashboard():
    if "username" not in session: #checking if the user is not logged in
        return redirect(url_for("login")) #redirecting to the login page if the user is not logged in
    return render_template_string("""
        <h2>Welcome to SecureBank, {{ username }}!</h2>

        <form method="POST" action="{{ url_for('logout')}}">
            <input type="hidden" name="csrf_token" value="{{csrf_token()}}">

            <button type="submit">Logout</button>
            </form>
            """, username=session["username"])
@app.route("/")  #defining the route called decorator tells flask when someone sends a HTTP request to /, execute the function associated with this route
def home(): #defining the function that will be executed when the route is accessed
    return "Welcome to Secure Bank application!"

@app.route('/users',methods=["GET"]) #defining the route for /users endpoint and specifying that it only accepts GET requests
def get_users():
    return {
        "users": [
            {"id":1, "name":"Sam"},
            {"id":2, "name":"John"},
            {"id":3, "name":"Alice"}
        ]
    }
accounts={
    101: {"id":101, "name":"Sam", "balance":1000},
    102: {"id":102, "name":"John", "balance":1500},
    103: {"id":103, "name":"Alice", "balance":2000}
}

#logged_in_user="Sam" #variable to store the name of the logged-in user

@app.route('/account/<int:account_id>',methods=["GET"]) #defining the route for /accounts/<account_id> endpoint and specifying that it only accepts GET requests
def get_account(account_id):

    logged_in_user=session.get("username") #getting the logged-in user's name from the session

    if not logged_in_user: #checking if the user is not logged in
        return {"error":"Please login first"}, 401 #returning an error message for unauthorized access
    #return accounts.get(account_id)
    account=accounts.get(account_id)
    if account is None:
        return {"error": "Account not found"}, 404
    if account["name"] != logged_in_user:
        return {"error": "Access denied"}, 403
    return accounts[account_id]

@app.route("/logout",methods=["POST"]) #defining the route for /logout endpoint and specifying that it only accepts POST requests
def logout():
    session.clear()

    return render_template_string("""
        <h2>You have been logged out successfully.</h2>
        <form method="GET" action="{{ url_for('login')}}">
            <button type="submit">Login</button>
        </form>
        """)



@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'"
    )
    return response




print(app.config["SESSION_COOKIE_HTTPONLY"])

if __name__=="__main__": #start the flask application only if this script is run directly ie.when we execute app.py file, not when we import it as a module in another script
    app.run(debug=False)