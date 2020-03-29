from flask import Flask,request,make_response
from flask_cors import CORS
import mysql.connector
from runenv import load_env
import os
import mysql.connector
import json

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
 

@app.route('/todo', methods=['GET'])
def givedata():
    if request.method == 'GET':
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        Table=[]
        mycursor.execute("SELECT TASKID,USERNAME,DATE_FORMAT(TASKDATE,'%d/%m/%y'),DATE_FORMAT(TASKTIME,'%H:%i'),TASK FROM TODO")
        for x in mycursor:
            Table.append(list(x))
        table_json=[]
        for row in Table:
            temp={'taskid':row[0],'username':row[1],'taskdate':row[2],'tasktime':row[3],'taskname':row[4]}
            table_json.append(temp)
        return json.dumps(table_json)

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
       print("Entered Here :)")
       mycursor.execute("INSERT INTO TODO(USERNAME,TASKDATE,TASKTIME,TASK) VALUES(%s,%s,%s,%s)",(username,taskdate,tasktime,taskname))
       mydb.commit()
       return ({"username":username,"taskname":taskname})

   if request.method == "OPTIONS":
       response = make_response()
       response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
       response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
       response.headers.add('Access-Control-Allow-Methods', "POST")
       response.headers.add('Access-Control-Allow-Credentials', 'true')
       print('Before Returning')
       return response

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
       print("Entered Here :)")
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
       print('Before Returning')
       return response

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
       mycursor.execute("UPDATE TODO SET USERNAME=%s,TASKDATE=%s,TASK=%s,TASKTIME=%s WHERE TASKID=%s",(username,taskdate,taskname,tasktime,taskid))
       mydb.commit()
       return (details)
   
   if request.method == "OPTIONS":
       response = make_response()
       response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
       response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
       response.headers.add('Access-Control-Allow-Methods', "POST")
       response.headers.add('Access-Control-Allow-Credentials', 'true')
       print('Before Returning')
       return response

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
       print("Entered Here :)")
       mycursor.execute("DELETE FROM TODO WHERE TASKID=%s",(taskid,))
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
