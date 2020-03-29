from flask import Flask,request,make_response
from flask_cors import CORS
import mysql.connector
from runenv import load_env
import os
import mysql.connector
import json
import bcrypt

app=Flask(__name__)
CORS(app)

user= os.environ.get('user')
host= os.environ.get('host')
password= os.environ.get('password')
database= os.environ.get('database')
config = {
'user':user,
'host':host,
'password':password,
'database':database
}
 
#todo route is used to fetch from ToDo table and display in view route
@app.route('/todo', methods=['POST'])
def givedata():
    if request.method == 'POST':
        details=request.get_json()
        username=details['username']
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        Table=[]
        mycursor.execute("SELECT ID,USERNAME,DATE_FORMAT(TASKDATE,'%d/%m/%y'),DATE_FORMAT(TASKTIME,'%H:%i'),TASK FROM TODOV2 WHERE USERNAME = %s",(username,))
        for x in mycursor:
            Table.append(list(x))
        table_json=[]
        for row in Table:
            temp={'taskid':row[0],'username':row[1],'taskdate':row[2],'tasktime':row[3],'taskname':row[4]}
            table_json.append(temp)
        return json.dumps(table_json)

    if request.method == "OPTIONS":
       response = make_response()
       response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
       response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
       response.headers.add('Access-Control-Allow-Methods', "POST")
       response.headers.add('Access-Control-Allow-Credentials', 'true')
       return response

#when a new user needs to be created user/signup route will be used
@app.route('/user/signup',methods=['POST','OPTIONS'])
def adduser():
   if request.method == "POST":
       details=request.get_json()
       username=details['username']
       password=details['password']
       salt=os.environ.get('salt')
       print(username,password)
       hashed = bcrypt.hashpw(password.encode('utf-8'),salt.encode('utf-8'))
       mydb=mysql.connector.connect(**config)
       mycursor=mydb.cursor()
       mycursor.execute("INSERT INTO USERS(USERNAME,PASSWORD) VALUES(%s,%s)",(username,hashed))
       mydb.commit()
       return ({"username":username})

   if request.method == "OPTIONS":
       response = make_response()
       response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
       response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
       response.headers.add('Access-Control-Allow-Methods', "POST")
       response.headers.add('Access-Control-Allow-Credentials', 'true')
       return response

#for an existing user when he/she needs to login
#validation is made in user/login route
@app.route('/user/login',methods=['POST','OPTIONS'])
def authuser():
   if request.method == "POST":
       details=request.get_json()
       username=details['username']
       password=details['password']
       salt=os.environ.get('salt')
       print(username,password)
       hashed = bcrypt.hashpw(password.encode('utf-8'),salt.encode('utf-8'))
       mydb=mysql.connector.connect(**config)
       mycursor=mydb.cursor()
       mycursor.execute("SELECT PASSWORD FROM USERS WHERE USERNAME=%s",(username,))
       hashpwd=mycursor.fetchone()[0]
       if(hashpwd==hashed.decode()):
          return ({"noerror":"valid","username":username})
       else:
          return ({"noerror":"invalid"})

   if request.method == "OPTIONS":
       response = make_response()
       response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
       response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
       response.headers.add('Access-Control-Allow-Methods', "POST")
       response.headers.add('Access-Control-Allow-Credentials', 'true')
       return response


#to add a new todo in ToDo table for the logged in user todo/add route is used
@app.route('/todo/add',methods=['POST','OPTIONS'])
def addtotable():
   if request.method == "POST":
       details=request.get_json()
       username=details['username']
       taskdate=details['date']
       tasktime=details['time']
       taskname=details['taskname']
       mydb=mysql.connector.connect(**config)
       mycursor=mydb.cursor()
       mycursor.execute("INSERT INTO TODOV2(USERNAME,TASKDATE,TASKTIME,TASK) VALUES(%s,%s,%s,%s)",(username,taskdate,tasktime,taskname))
       mydb.commit()
       return ({"username":username,"taskname":taskname})

   if request.method == "OPTIONS":
       response = make_response()
       response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
       response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
       response.headers.add('Access-Control-Allow-Methods', "POST")
       response.headers.add('Access-Control-Allow-Credentials', 'true')
       return response
       
# to convert the data into actual json format todo/convert route is used
# the converted data will be sent to perform edit operation
@app.route('/todo/convert',methods=['POST','OPTIONS'])
def convertdata():
   if request.method == "POST":
       details=request.get_json()
       taskid=details['taskid']
       username=details['username']
       taskdate=details['taskdate']
       tasktime=details['tasktime']
       taskname=details['taskname']
       print(taskid,taskdate,taskname,tasktime,username)
       year=int(taskdate[len(taskdate)-2:])
       if(year>0 and year<69):
           taskdate="20"+taskdate[len(taskdate)-2:]+"-"+taskdate[3:5]+"-"+taskdate[:2]
       else:
           taskdate="19"+taskdate[len(taskdate)-2:]+"-"+taskdate[3:5]+"-"+taskdate[:2]
       print(taskid,taskdate,taskname,tasktime,username)
       return ({"taskid":taskid,"username":username,"taskname":taskname,"taskdate":taskdate,"tasktime":tasktime})
   
   if request.method == "OPTIONS":
       response = make_response()
       response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
       response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
       response.headers.add('Access-Control-Allow-Methods', "POST")
       response.headers.add('Access-Control-Allow-Credentials', 'true')
       return response

# data which needs to be edited is received from convert route's response
#and sent to edit route, after editing the data is sent to ToDo table in this route
@app.route('/todo/edit',methods=['POST','OPTIONS'])
def editdata():
   if request.method == "POST":
       details=request.get_json()
       taskid=details['taskid']
       username=details['username']
       taskdate=details['taskdate']
       tasktime=details['tasktime']
       taskname=details['taskname']
       print(taskid,taskdate,taskname,tasktime,username)
       mydb=mysql.connector.connect(**config)
       mycursor=mydb.cursor()
       print("Entered Here :)")
       mycursor.execute("UPDATE TODOV2 SET TASKDATE=%s,TASK=%s,TASKTIME=%s WHERE ID=%s AND USERNAME=%s",(taskdate,taskname,tasktime,taskid,username,))
       mydb.commit()
       return (details)
   
   if request.method == "OPTIONS":
       response = make_response()
       response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
       response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
       response.headers.add('Access-Control-Allow-Methods', "POST")
       response.headers.add('Access-Control-Allow-Credentials', 'true')
       return response

# data which needs to be deleted is sent to this route to delete from ToDo table
@app.route('/todo/delete',methods=['POST','OPTIONS'])
def deletefromtable():
    if request.method == "POST":
       details=request.get_json()
       taskid=details['taskid']
       username=details['username']
       taskdate=details['taskdate']
       tasktime=details['tasktime']
       taskname=details['taskname']
       print(taskid,username,taskname,taskdate,tasktime)
       mydb=mysql.connector.connect(**config)
       mycursor=mydb.cursor()
       mycursor.execute("DELETE FROM TODOV2 WHERE ID=%s",(taskid,))
       mydb.commit()
       return details

    if request.method == "OPTIONS":
       response = make_response()
       response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
       response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
       response.headers.add('Access-Control-Allow-Methods', "POST")
       response.headers.add('Access-Control-Allow-Credentials', 'true')
       print('Before Returning')
       return response

if __name__ == '__main__':
    app.run(debug=True,port=3001)
