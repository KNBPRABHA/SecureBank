from flask import Flask, request, jsonify, session,redirect, url_for, make_response #importing the Flask class and request and jsonify modules from the flask package
import os
app=Flask(__name__) #creates a flask app instance
password="admin123"
#app.secret_key="mysecretkey_for_my_application" #setting a secret key for the application, used for session management and security purposes
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
            return f"Welcome, {username}! Login successful." #redirecting to the home page after successful login
        else:
            return "Invalid credentials" #returning an error message for invalid credentials
    return """
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
"""

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

@app.route("/logout")
def logout():
    session.clear()
    return "You have been logged out successfully."

@app.route("/cookie-test")
def cookie_test():

    response = app.make_response("""
        <h2>Cookie Visibility Test</h2>
        <p>Cookies accessible to JavaScript:</p>
        <pre id="output"></pre>

        <script>
            document.getElementById("output").textContent =
                document.cookie;
        </script>
    """)

    response.set_cookie(
        "demo_visible",
        "hello-from-securebank",
        httponly=False,
        samesite="Lax"
    )

    return response

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