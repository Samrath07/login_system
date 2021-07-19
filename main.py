from flask import Flask, render_template, request, redirect,jsonify
import pymongo as connection

app = Flask(__name__)

# Connecting to the mongoDB database server
default_url = "mongodb://localhost:27017/"
db_name = "Login_Details"
db_connect = connection.MongoClient(default_url)
print("Connected to the MongoDB server")



# Verfying whether database exists or not
def checkDB(db_name,db_connect):
    db_list = db_connect.list_database_names()
    print(db_list)
    if db_name in db_list:
        #print(db_name  + " exists")
        return True
    else:
        #print(db_name + " does not exists")
        return False


# to check whether database exists
if(checkDB(db_name, db_connect) == False):

    database = db_connect[db_name]
    print("Database created", database)
    
else:
    print("Database exists")
    

# verifying collection exists or not
collection_name = "User_Details"
database = db_connect[db_name]
def check_collection(db_name,collection_name,database):
    collection_list = database.list_collection_names()
    print(collection_list)

    if collection_name in collection_list:
        #print(collection_name + " exists")
        return True
    else:
        #print(collection_name + " does not exists")
        return False


# Creating a collection
if (check_collection(db_name, collection_name, database) == False):
    collection = database[collection_name]
    print("Collection created")
else:
    print("Collection exists")

# Rendering the home Page
@app.route('/',methods = ['GET','POST'])
def homePage():
    return render_template('login.html')


# Creating the login if the value exists 
@app.route('/login', methods = ['GET','POST'])
def loginPage():
    collection = database[collection_name]
    if request.method == 'POST':
        user_email = request.form['email']
        print(user_email)
        user_password = request.form['password']
        print(user_password)
        for value in collection.find():
            if value['Email'] == user_email and value['Password'] == user_password:
                return render_template('welcome.html')
        return render_template('register.html')
       

# User registration 
@app.route('/register',methods = ['GET','POST'])
def register():
    collection = database[collection_name]

    if request.method == "POST":

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        record = {
           "Username":username,
           "Email":email,
           "Password":password
        }
        userdetails = collection.insert_one(record)
        print("Value inserted in the database successfully", userdetails)

        return render_template('registered.html')






if __name__ == "__main__":
    app.run(debug=True)


'''
1. create connection
2. create database -> LoginDetails
3. create collection -> UserDetails
4. insert values in collection
5. Working of the loginPage
    - / route render LoginPage
    - enter the email and password
    - when the post request happens
    - check whether the record exists in the collection or not
    - if exists render a welcomePage
    - else redirect to the /register
6. Working of registerPage
    - enter the username,email and password
    - insert the username, email and password on this page
    - and show the registeration successful on screen
    - then redirect to the loginPage
'''