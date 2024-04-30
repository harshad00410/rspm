from flask import Flask, render_template, request
import mysql.connector
from ultralytics import YOLO
import cv2
import numpy as np
import os
import datetime


app = Flask(__name__,template_folder='templates')
# Configure your MySQL database connection
dbs= mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harshu@2002",
    database="pothole"
    )
@app.route('/')

def index():
    return render_template('ghome.html')


@app.route('/upload', methods=['POST'])
def upload():

   
    un= request.form.get('un')   
    lat=request.form['lat']
    long=request.form['long']
    mob = request.form['mo']
    file= request.files['file']
    comp= request.form['complaint']
    cursor = dbs.cursor()
    cursor.execute("select max(sid) from user ")
    sid_tuple = cursor.fetchone()
    
    if sid_tuple[0]  is None:
        sid = 1
       
    else:
        sid = sid_tuple[0] + 1
        

    #  Save uploaded file to a temporary location
    file_path = os.path.join(app.root_path, 'static\\uploads', file.filename)
    file.save(file_path)
    current_datetime = datetime.datetime.now()

    # Extract only the date part
    current_date = current_datetime.date()
    status="In-Progress"
    cursor = dbs.cursor()
    pothole_detector = YOLO("potholedetector.pt")
    cursor.execute("INSERT INTO user  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (sid,un,mob,comp,lat,long,file.filename,current_date,status,))
    
        # Load image
    img = cv2.imread(file_path)
    box=pothole_detector(img)[0]
    bb=box.boxes.data.tolist()
    
    for pothole in bb:
            x1, y1, x2, y2, score, class_id = pothole
            # print(class_id)
            width = (x2 * 0.0264583333) - (x1 * 0.0264583333)
            height = (y2* 0.0264583333) - (y1* 0.0264583333)
            # Calculate area
            
            area = width * height
            print("Area of pothole:", area,"cm^2","Width:",width,"Height:",height)
            
            cursor.execute("INSERT INTO areas  VALUES (%s,%s,%s,%s)", (sid,width,height,area))
            
            if class_id == 0 :#and score > 0.5:
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.imshow('Win',img)
                    cv2.waitKey(0)


       
   


   
    dbs.commit()

        # Close the cursor
    cursor.close()
    

    return index()


       

    # Example usage
  
   
@app.route('/upload1', methods=['POST'])
def upload1():
    aun= request.form.get('username')
    
    amob = request.form['phoneNumber']
    apass= request.form.get('password')

    # Create a cursor to execute SQL queries
    cursor = dbs.cursor()

    cursor.execute("INSERT INTO adminuser  VALUES (%s,%s,%s)", (aun,apass,amob))    # Insert data into the database
    
   
    dbs.commit()
    cursor.close()
    return render_template('index.html')
        # Close the cursor
# @app.route('/upload2', methods=['POST'])
# def upload2():
    
#     # Create a cursor to execute SQL queries
#     cursor = dbs.cursor()

#     cursor.execute("SELECT * FROM  user  join areas  on user.sid= areas.sid; ")    # Insert data into the database
#     data = cursor.fetchall()
    
#     dbs.commit()
#     # print(data) 
#     cursor.close()
    
#     # Render the template with data and SID counts
#     return render_template('display.html', data=data, )

@app.route('/upload3',methods=['post'])
def upload3():
     
     return render_template('user.html')
#     un= request.form.get('email') 
#     ps=request.form.get('password')
#     cursor = dbs.cursor()
    
#     uname=cursor.execute("SELECT  auname FROM adminuser ")
#     apass=cursor.execute("SELECT apass  FROM adminuser ")
    
#         # Compare hashes
#     if apass== ps and un==uname:
#         return render_template('user.html')
#     else:
#         data="Enter correct username and password"
#         return "adminlogin.html"
       

#  # print(data) 
@app.route('/upload4', methods=['POST'])
def upload4():
    mo=request.form.get('phoneNumber')

        # Create a cursor to execute SQL queries
    cursor = dbs.cursor()
    
    cursor.execute("select * FROM  user  join areas  on user.sid= areas.sid where mob=%s", (mo,))    # displayin data of user
    data = cursor.fetchall()
    
    
    dbs.commit()
    cursor.close()
    # Create a dictionary to store the count of SID occurrences
    # sid_counts = {r[0]: r[1] for r in data1}
    return render_template('userdisplay.html', data=data)#, sid_counts=sid_counts)  
# @app.route('/upload5', methods=['POST']) 
# def upload5():
#     status= request.form['status']    # Create a cursor to execute SQL queries
#     id= request.form['sid']    # Create a cursor to execute SQL queries
#     cursor = dbs.cursor()
#     cursor.execute("update pothole.user Set status=(%s) where sid=(%s);",(status,id,))
   
#     cursor.execute("SELECT * FROM  user  join areas  on user.sid= areas.sid; ")    # Insert data into the database
#     data = cursor.fetchall()
   
#     dbs.commit()
#     # print(data) 
#     cursor.close()
     
    

#     return render_template('display.html', data=data)

@app.route('/upload6', methods=['POST']) 
def upload6():
     # Create a cursor to execute SQL queries
    cursor = dbs.cursor()
    status= request.form['status']    # Create a cursor to execute SQL queries
    id= request.form['sid']
    cursor.execute("update pothole.user Set status=(%s) where sid=(%s);",(status,id,))
    # cursor.execute("SELECT * FROM  user  join areas  on user.sid= areas.sid; ")  
    # data = cursor.fetchall()
    id1= request.form['delete']    
   
   
    cursor.execute("delete from pothole.areas  where sid=%s;" ,(id1,))

    cursor.execute("delete from pothole.user  where sid=%s;" ,(id1,))

    
    cursor.execute("SELECT * FROM  user  join areas  on user.sid= areas.sid; ")  
    data = cursor.fetchall()
    # print("\n\n",data,"\n\n")
    dbs.commit()
    # print(data) 
    cursor.close()
    return render_template('display.html', data=data)
        
if __name__ == '__main__':
    app.run(debug=True , port=5000)
    #  app.run(debug=True)
