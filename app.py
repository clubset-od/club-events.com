from flask import Flask,render_template,request,redirect,url_for
from flaskext.mysql import MySQL
import os
from werkzeug.utils import secure_filename
app=Flask(__name__)
mysql=MySQL()
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
app.config['MYSQL_DATABASE_HOST']="localhost"
app.config['MYSQL_DATABASE_USER']="root"
app.config['MYSQL_DATABASE_PASSWORD']=""
app.config['MYSQL_DATABASE_DB']="clubset_od"

mysql.init_app(app)


@app.route("/adlogin",methods=['POST','GET'])                                                          
def adlogin():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if username=='admin' and password=='admin':
            return redirect('adhome')
        else:
            error='invalid'
    else:
        return render_template("adlogin.html")

@app.route("/adhome")                                                          
def adhome():
    return render_template("adhome.html")


@app.route("/adadddewan",methods=['POST','GET'])                                                          
def adadddewan():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        clubname=request.form['clubname']
        dewanname=request.form['dewanname']
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("INSERT INTO `adddewan`(`username`, `password`, `clubname`, `dewanname`)  VALUES(%s,%s,%s,%s)",(username,password,clubname,dewanname))
        con.commit()
        return redirect('adhome')
    else:
        return render_template("adadddewan.html")

@app.route("/adaddevent",methods=['POST','GET'])                                                          
def adaddevent():
    if request.method=='POST':
        eventname=request.form['eventname']
        clubname=request.form['clubname']
        dewanname=request.form['dewanname']
        department=request.form['department']
        place=request.form['place']
        date=request.form['date']
        time=request.form['time']
        description=request.form['description']
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("INSERT INTO `addevent`( `eventname`, `clubname`, `dewanname`, `department`,`place`, `date`, `time`, `description`)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(eventname,clubname,dewanname,department,place,date,time,description))
        con.commit()
        return redirect('adviewevent')
    else:
        return render_template("adaddevent.html")

@app.route("/adviewevent",methods=['POST','GET'])                                                          
def adviewevent():
    id=request.args.get("id")
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent`")
    data=cur.fetchall()
    return render_template("adviewevent.html",view=data)


@app.route("/stlogin",methods=['POST','GET'])                                                         
def stlogin():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("SELECT * FROM `streg` WHERE `username`='"+username+"' AND `password`='"+password+"'")
        data=cur.fetchone()
        if data[5]==username and data[6]==password:
            return redirect(url_for('sthome',id=data[0]))
        else:    
            error='invalid'
    else:
        return render_template("stlogin.html")

@app.route("/stcordlogin",methods=['POST','GET'])                                                          
def stcordlogin():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("SELECT * FROM `adddewan` WHERE `username`='"+username+"' AND `password`='"+password+"'")
        data=cur.fetchone()
        if data[1]==username and data[2]==password:
            return redirect(url_for('stcoordinator',id=data[0]))
        else:
            error='invalid'
    else:
        return render_template("stcordlogin.html")

@app.route("/stcoordinator")                                                          
def stcoordinator():
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` ")
    data=cur.fetchall()     
    return render_template("stcoordinator.html",stu=data)

@app.route("/sthome")                                                         
def sthome():
    stid=request.args.get('id')
    return render_template("sthome.html",stuid=stid)

@app.route("/stbusiness")                                                         
def stbusiness():
    stid=request.args.get('id')
    id=request.args.get("id")
    club="Business club"
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` WHERE `clubname`='"+club+"'")
    data=cur.fetchall()
    return render_template("stbusiness.html",stuid=stid,view=data)

@app.route("/strotaract")                                                         
def strotaract():
    stid=request.args.get('id')
    club="Rotaract club"
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent`   WHERE `clubname`='"+club+"'")
    data=cur.fetchall()
    return render_template("strotaract.html",stuid=stid,view=data)    

@app.route("/stfinearts")                                                         
def stfinearts():
    stid=request.args.get('id')
    club="Fine arts club"
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` WHERE `clubname`='"+club+"'")
    data=cur.fetchall()
    return render_template("stfinearts.html",stuid=stid,view=data)  

@app.route("/stsports")                                                         
def stsports():
    stid=request.args.get('id')
    club="Sports club"
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` WHERE `clubname`='"+club+"'")
    data=cur.fetchall()
    return render_template("stsports.html",stuid=stid,view=data)  

@app.route("/streg",methods=['GET','POST'])                                                          
def streg():
    if request.method=='POST':
        name=request.form['name']
        regno=request.form['regno']
        department=request.form['department']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
        phoneno=request.form['phoneno']
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("INSERT INTO `streg`(`name`, `regno`, `department`, `email`, `username`, `password`, `phoneno`) VALUES(%s,%s,%s,%s,%s,%s,%s)",(name,regno,department,email,username,password,phoneno))
        con.commit()
        return redirect('stlogin')
    else:
        return render_template("streg.html")   

@app.route("/steventreg",methods=['GET','POST'])                                                          
def steventreg():
    eventid=request.args.get('id')
    stid=request.args.get('stid')
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` WHERE  `id`= '"+eventid+"' ")
    data=cur.fetchone()
    con1=mysql.connect()
    cur1=con1.cursor()
    cur1.execute("SELECT * FROM `streg` WHERE  `id`= '"+stid+"' ")
    data1=cur1.fetchone()
    if request.method=='POST':
        stid=request.form['stid']
        name=request.form['name']
        regno=request.form['regno']
        email=request.form['email']
        eventid=request.form['eventid']
        eventname=request.form['eventname']
        clubname=request.form['clubname']
        dewanname=request.form['dewanname']
        department=request.form['department']
        place=request.form['place']
        date=request.form['date']
        time=request.form['time']
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("INSERT INTO `eventreg`(`stid`, `name`, `regno`, `email`, `eventid`, `eventname`, `clubname`, `dewanname`,`department`, `place`, `date`, `time`)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(stid,name,regno,email,eventid,eventname,clubname,dewanname,department,place,date,time))
        con.commit()
        return redirect(url_for('stvieweventreg',id=stid))
    else:
        return render_template("steventreg.html",view=data,stu=data1,stuid=stid)



@app.route("/stvieweventreg",methods=['POST','GET'])                                                          
def stvieweventreg():
    id=request.args.get("id")
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `eventreg` where `stid`='"+id+"' ")
    data=cur.fetchall()
    return render_template("stvieweventreg.html",view=data,stuid=id)

@app.route("/stattendance",methods=['POST','GET'])                                                          
def stattendance():
    evid=request.args.get('id')
    stid=request.args.get('stid')
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` WHERE `id`='"+evid+"'")
    data=cur.fetchone()
    if request.method=='POST':
        APP_PATH_ROUTE=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(APP_PATH_ROUTE,'attendence')
        UPLOAD_FOLDER='{}/static/attendence/'.format(APP_PATH_ROUTE)
        app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
        files=request.files['files']
        f=os.path.join(UPLOAD_FOLDER,files.filename)
        files.save(f)
        filename=secure_filename(files.filename)
        conn=mysql.connect()
        cur=conn.cursor()
        cur.execute("UPDATE `addevent` SET `attendence`='"+filename+"' where `id`='"+evid+"'")
        conn.commit()
        return redirect('stcoordinator')
    else:
        return render_template("stattendance.html",stuid=stid,od=data)


@app.route("/stcertificate",methods=['POST','GET'])                                                          
def stcertificate():
    oid=request.args.get('id')
    stid=request.args.get('stid')
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `odreg` WHERE `id`='"+oid+"'")
    data=cur.fetchone()
    if request.method=='POST':
        feedback=request.form['feedback']
        APP_PATH_ROUTE=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(APP_PATH_ROUTE,'certificate')
        UPLOAD_FOLDER='{}/static/certificate/'.format(APP_PATH_ROUTE)
        app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
        files=request.files['files']
        f=os.path.join(UPLOAD_FOLDER,files.filename)
        files.save(f)
        filename=secure_filename(files.filename)
        conn=mysql.connect()
        cur=conn.cursor()
        cur.execute("UPDATE `odreg` SET  `certificate`='"+filename+"',`feedback`='"+feedback+"' where `id`='"+oid+"'")
        conn.commit()
        return redirect(url_for('docstudent',id=stid))
    else:
        return render_template("stcertificate.html",stuid=stid,od=data)    



   
@app.route("/odapply",methods=['POST','GET'])                                                          
def odapply(): 
    id=request.args.get("id")
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `eventreg` where `id`= '"+id+"' ")
    data=cur.fetchone()
    if request.method=='POST':
        regid=request.form['regid']
        stid=request.form['stid']
        name=request.form['name']
        regno=request.form['regno']
        email=request.form['email']
        eventid=request.form['eventid']
        eventname=request.form['eventname']
        clubname=request.form['clubname']
        dewanname=request.form['dewanname']
        department=request.form['department']
        place=request.form['place']
        date=request.form['date']
        time=request.form['time']
        hod="Not Approved"
        clubdewan="Not Approved"
        classdewan="Not Approved"
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("INSERT INTO `odreg`( `regid`, `stid`, `name`, `regno`, `email`, `eventid`, `eventname`, `clubname`, `dewanname`,`department`, `place`, `date`, `time`, `hod`, `clubdewan`, `classdewan`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(regid,stid,name,regno,email,eventid,eventname,clubname,dewanname,department,place,date,time,hod,clubdewan,classdewan))
        con.commit()
        return redirect(url_for('docstudent',id=stid))
    else:
        return render_template("odapply.html",stu=data)


@app.route("/hodlogin",methods=['POST','GET'])                                                          
def hodlogin():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if username=='hod' and password=='hod':
            return redirect('hodhome')
        else:
            error='invalid'
    else:
        return render_template("hodlogin.html")

@app.route("/hodhome")                                                          
def hodhome():
    return render_template("hodhome.html")

@app.route("/hodupdateod",methods=['POST','GET'])                                                          
def hodupdateod():
    stid=request.args.get("id")
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `odreg` WHERE `id`='"+stid+"' ")
    data=cur.fetchone()
    if request.method=='POST':
        hod=request.form['hod']
        clubdewan=request.form['clubdewan']
        classdewan=request.form['classdewan']
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("UPDATE `odreg` SET `hod`='"+hod+"',`clubdewan`='"+clubdewan+"',`classdewan`='"+classdewan+"' where `id`= '"+stid+"' ")
        con.commit()
        return redirect('hodapproveod')
    else:
        return render_template("hodupdateod.html",stu=data)        

@app.route("/hodapproveod",methods=['POST','GET'])                                                          
def hodapproveod():
    id=request.args.get("id")
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `odreg` ")
    data=cur.fetchall()
    return render_template("hodapproveod.html",stu=data)    

@app.route("/classdewanlogin",methods=['POST','GET'])                                                          
def classdewanlogin():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if username=='staff' and password=='staff':
            return redirect('classdewanhome')
        else:
            error='invalid'
    else:
        return render_template("classdewanlogin.html") 

@app.route("/classdewanhome")                                                          
def classdewanhome():
    return render_template("classdewanhome.html")

@app.route("/classdewanemail",methods=['POST','GET'])                                                          
def classdewanemail():
    stid=request.args.get("id")
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `odreg` WHERE `id`='"+stid+"' ")
    data=cur.fetchone()
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        eventname=request.form['eventname']
        clubdewan=request.form['clubdewan']
        hod=request.form['hod']
        classdewan=request.form['classdewan']
        subject = "OD APPROVAL"
        body = 'Dear'  +name+'.\n Here with i responsed for your OD APPROVAL for the event :'+eventname+'\n\n classdewan :'+classdewan+'\n hod:'+hod+'\n clubdewan:'+clubdewan+'\n\n ALL THE BEST FOR YOUR EVENT'
        #body="OD APPROVAL IS APPROVED"
        sender_email = "clubsetod@gmail.com"
        receiver_email = email
        password = "Clubset@68"


        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject



        message.attach(MIMEText(body, "plain"))
        
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        return redirect('clubdewanapproveod')
    else:
        return render_template("classdewanemail.html",stu=data)

@app.route("/classdewanupdateod",methods=['POST','GET'])                                                          
def classdewanupdateod():
    stid=request.args.get("id")
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `odreg` WHERE `id`='"+stid+"' ")
    data=cur.fetchone()
    if request.method=='POST':
        hod=request.form['hod']
        clubdewan=request.form['clubdewan']
        classdewan=request.form['classdewan']
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("UPDATE `odreg` SET `hod`='"+hod+"',`clubdewan`='"+clubdewan+"',`classdewan`='"+classdewan+"' where `id`='"+stid+"' ")
        con.commit()
        return redirect('classdewanapproveod')
    else:
        return render_template("classdewanupdateod.html",stu=data)         

@app.route("/classdewanapproveod",methods=['POST','GET'])                                                          
def classdewanapproveod():
    id=request.args.get("id")
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `odreg` ")
    data=cur.fetchall()      
    return render_template("classdewanapproveod.html",stu=data)       

@app.route("/clubviewatt",methods=['POST','GET'])                                                          
def clubviewatt():  
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` ")
    data=cur.fetchall()      
    return render_template("clubviewatt.html",stu=data)          

@app.route("/clubdewanlogin",methods=['POST','GET'])                                                          
def clubdewanlogin():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("SELECT * FROM `adddewan` WHERE `username`='"+username+"' AND `password`='"+password+"'")
        data=cur.fetchone()
        if data[1]==username and data[2]==password:
            return redirect(url_for('clubdewanhome',id=data[0]))
        else:
            error='invalid'
    else:
        return render_template("clubdewanlogin.html")

@app.route("/clubdewanhome")                                                          
def clubdewanhome():
    return render_template("clubdewanhome.html")    

@app.route("/clubdewanapproveod",methods=['POST','GET'])                                                          
def clubdewanapproveod():
    id=request.args.get("id")
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `odreg` ")
    data=cur.fetchall()      
    return render_template("clubdewanapproveod.html",stu=data)

@app.route("/clubdewanupdateod",methods=['POST','GET'])                                                          
def clubdewanupdateod():
    stid=request.args.get("id")
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `odreg` WHERE `id`='"+stid+"' ")
    data=cur.fetchone()
    if request.method=='POST':
        hod=request.form['hod']
        clubdewan=request.form['clubdewan']
        classdewan=request.form['classdewan']
        con=mysql.connect()
        cur=con.cursor()
        cur.execute("UPDATE `odreg` SET `hod`='"+hod+"',`clubdewan`='"+clubdewan+"',`classdewan`='"+classdewan+"' where `id`='"+stid+"' ")
        con.commit()
        return redirect('clubdewanapproveod')
    else:
        return render_template("clubdewanupdateod.html",stu=data) 

   

@app.route("/docclassdewan")                                                          
def docclassdewan():
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` ")
    data=cur.fetchall()   
    return render_template("docclassdewan.html",stu=data) 

@app.route("/docstudent",methods=['POST','GET'])                                                          
def docstudent():
    stid=request.args.get('id')
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `odreg` WHERE `stid`='"+stid+"'")
    data=cur.fetchall()
    return render_template("docstudent.html",stuid=stid,od=data)

@app.route("/front")                                                          
def front():
    return render_template("front.html")                                   

@app.route("/fbusiness")                                                          
def fbusiness():
    clubname="Business club"
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` WHERE `clubname`='"+clubname+"'")
    data=cur.fetchall()
    return render_template("fbusiness.html",event=data)

@app.route("/frotaract")                                                          
def frotaract():
    clubname="Rotaract club"
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` WHERE `clubname`='"+clubname+"'")
    data=cur.fetchall()
    return render_template("frotaract.html",event=data)

@app.route("/ffinearts")                                                          
def ffinearts():
    clubname="Fine arts club"
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` WHERE `clubname`='"+clubname+"'")
    data=cur.fetchall()
    return render_template("ffinearts.html",event=data)

@app.route("/fsports")                                                          
def fsports():
    clubname="Sports club"
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `addevent` WHERE `clubname`='"+clubname+"'")
    data=cur.fetchall()
    return render_template("fsports.html",event=data)


@app.route("/viewcertificates")                                                          
def viewcertificates():
    eveid=request.args.get('id')
    con=mysql.connect()
    cur=con.cursor()
    cur.execute("SELECT * FROM `odreg` WHERE `eventid`='"+eveid+"'")

    data=cur.fetchall()
    return render_template("viewcertificates.html",certificate=data)



if __name__=="__main__":
    app.run(debug=True)    