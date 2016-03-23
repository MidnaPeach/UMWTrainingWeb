#this is the file that starts the server and has all of the server commands in it

import psycopg2
import psycopg2.extras
import os
from flask import Flask, session, render_template, request, redirect, url_for

app = Flask(__name__)

app.secret_key = os.urandom(24).encode('hex')

loginError = False
verifiedUser = ''
userType = ''


#connectToDB--------------------------------------------------------------------------------------------
def connectToDB():
    connectionString = 'dbname=umw_training user=website password=umw16p91V2Hkl8m9 host=localhost'
    print connectionString
    try:
        print("Connected to database")
        print(psycopg2.connect(connectionString))
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")
#end connect to DB---------------------------------------------------------------------------------------

#login---------------------------------------------------------------------------------------------------    
@app.route('/', methods=['GET', 'POST'])
def login():
    session['username'] = ""
    pw = ""
    if 'loginError' in session:
        loginError = session['loginError']
    else:
        loginError = False
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
      print "HI"
      session['username'] = request.form['username']
      print(session['username'])

      pw = request.form['pw']
      query = "select * from users WHERE user_name = '%s' AND password = crypt('****************', password)" % (session['username'],)
      print query
      cur.execute("select * from users WHERE user_name = %s AND password = crypt(%s, password)", (session['username'], pw))
      if cur.fetchone():
         verifiedUser = session['username']
         session['loginError'] = False
         cur.execute("select * from admin WHERE user_name = %s", (verifiedUser,))
         if cur.fetchone():
            session['userType'] = 'admin'
            query = "select admin_id from admin WHERE user_name = '%s'" % (session['username'],)
            print query
            cur.execute("select admin_id from admin WHERE user_name = %s", (session['username'],))
            session['ID'] = cur.fetchall()
            session['ID'] = session['ID'][0][0]
            print session['ID']
         cur.execute("select * from students WHERE user_name = %s", (verifiedUser,))
         if cur.fetchone():
            session['userType'] = 'student'
            query = "select student_id from students WHERE user_name = '%s'" % (session['username'],)
            print query
            cur.execute("select student_id from students WHERE user_name = %s", (session['username'],))
            session['ID'] = cur.fetchall()
            session['ID'] = session['ID'][0][0]
            print session['ID']
         cur.execute("select * from coaches WHERE user_name = %s", (verifiedUser,))
         if cur.fetchone():
            session['userType'] = 'coach'
            query = "select coach_id from coaches WHERE user_name = '%s'" % (session['username'],)
            print query
            cur.execute("select coach_id from coaches WHERE user_name = %s", (session['username'],))
            session['ID'] = cur.fetchall()
            session['ID'] = session['ID'][0][0]
            print session['ID']
         cur.execute("select * from trainers WHERE user_name = %s", (verifiedUser,))
         if cur.fetchone():
            session['userType'] = 'trainer'
            query = "select trainer_id from trainers WHERE user_name = '%s'" % (session['username'],)
            print query
            cur.execute("select trainer_id from trainers WHERE user_name = %s", (session['username'],))
            session['ID'] = cur.fetchall()
            session['ID'] = session['ID'][0][0]
            print session['ID']
         
         if session['userType'] == 'admin':
            return redirect(url_for('adminHome'))
         if session['userType'] == 'student':
            return redirect(url_for('studentHome'))
      else:
         verifiedUser = ''
         session['username'] = ''
         session['loginError'] = True
         loginError = session['loginError']
    return render_template('index.html', user = verifiedUser, loginError = loginError)

    #return render_template('index.html')
#end login----------------------------------------------------------------------------------------------------

#**********************************
#*************ADMIN****************
#**********************************

#admin home---------------------------------------------------------------------------------------------------    
@app.route('/ahome', methods=['GET', 'POST'])
def adminHome():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "select * from users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("select * from users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('adminHome'))
        else:
            verifiedUser = ''
            session['username'] = ''

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    #user and userType are being passed to the website here
    return render_template('Theme/ahome.html', user = verifiedUser, userType = userType, Name = names)
#end adminHome------------------------------------------------------------------------------------------------------------------------ 

#admin calendar page------------------------------------------------------    
@app.route('/acalendar', methods=['GET', 'POST'])
def adminCalendarPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "select * from users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("select * from users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('adminHome'))
        else:
            verifiedUser = ''
            session['username'] = ''

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    #user and userType are being passed to the website here
    return render_template('Theme/acalendar.html', user = verifiedUser, userType = userType, Name = names)
#end admin calendar page--------------------------------------------------     

#admin exercises page------------------------------------------------------    
@app.route('/aexercises', methods=['GET', 'POST'])
def adminExercisesPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # get all exercises from the database ...
    rows = []
    query = "select exercise_name, muscle_group, youtube_link from exercises"
    print query
    cur.execute("select exercise_name, muscle_group, youtube_link from exercises")
    #if cur.fetchone():
    rows = cur.fetchall()
    print(rows)
        #verifiedUser = session['username']
        #return redirect(url_for('adminHome'))
    #else:
        #verifiedUser = ''
        #session['username'] = ''
    
    
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "select * from users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("select * from users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('adminHome'))
        else:
            verifiedUser = ''
            session['username'] = ''

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    #user and userType are being passed to the website here
    return render_template('Theme/aexercises.html', user = verifiedUser, userType = userType, Name = names, results = rows)
#end admin exercises page--------------------------------------------------  

#admin create exercises page------------------------------------------------------    
@app.route('/acreateexercise', methods=['GET', 'POST'])
def adminCreateExercisePage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    badName = False
    exerciseCreated = False

    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        
        exerciseName = request.form['ename']
        print(exerciseName)
        muscleGroup = request.form['emusclegroup']
        print(muscleGroup)
        description = request.form['edesc']
        print(description)
        youTube = request.form['eyoutube']
        print(youTube)
        
        query = "select exercise_name from exercises WHERE exercise_name = '%s'" % (exerciseName,)
        print query
        cur.execute("select exercise_name from exercises WHERE exercise_name = %s", (exerciseName,))
        if cur.fetchone():
            badName = True
            #return redirect(url_for('adminCreateExercisePage'))
        else:
            badName = False
            exerciseCreated = True
            query = "INSERT INTO exercises (admin_id, exercise_name, description, muscle_group, youtube_link) VALUES ('%s', '%s', '%s', '%s', '%s')" % (session['ID'],exerciseName,description,muscleGroup,youTube)
            print query
            try:
                cur.execute("INSERT INTO exercises (admin_id, exercise_name, description, muscle_group, youtube_link) VALUES (%s, %s, %s, %s, %s)", (session['ID'],exerciseName,description,muscleGroup,youTube))
            except:
                print("Problem inserting into exercises")
                db.rollback()
            db.commit()
            
            print("done!")

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    #user and userType are being passed to the website here
    return render_template('Theme/acreateexercise.html', user = verifiedUser, userType = userType, Name = names, badName = badName, exerciseCreated = exerciseCreated)
#end admin create exercise page--------------------------------------------------

#admin workouts page------------------------------------------------------    
@app.route('/aworkouts', methods=['GET', 'POST'])
def adminWorkoutsPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "select * from users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("select * from users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('adminHome'))
        else:
            verifiedUser = ''
            session['username'] = ''

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    #user and userType are being passed to the website here
    return render_template('Theme/aworkouts.html', user = verifiedUser, userType = userType, Name = names)
#end admin workout page--------------------------------------------------  

#admin create workout page------------------------------------------------------    
@app.route('/acreateeworkout', methods=['GET', 'POST'])
def adminCreateWorkoutPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "select * from users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("select * from users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('adminHome'))
        else:
            verifiedUser = ''
            session['username'] = ''

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    #user and userType are being passed to the website here
    return render_template('Theme/acreateworkout.html', user = verifiedUser, userType = userType, Name = names)
#end admin create workout page--------------------------------------------------

#admin add user page------------------------------------------------------    
@app.route('/aadduser', methods=['GET', 'POST'])
def adminAddUserPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "select * from users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("select * from users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('adminHome'))
        else:
            verifiedUser = ''
            session['username'] = ''

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    #user and userType are being passed to the website here
    return render_template('Theme/aadduser.html', user = verifiedUser, userType = userType, Name = names)
#end admin add user page--------------------------------------------------  

#**********************************
#*************STUDENT**************
#**********************************

#student home---------------------------------------------------------------------------------------------------
@app.route('/shome', methods=['GET', 'POST'])
def studentHome():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "select * from users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("select * from users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('studentHome'))
        else:
            verifiedUser = ''
            session['username'] = ''
            
    if userType == 'student':
        # getting the user's first and last name(only students)
        cur.execute("select first_name, last_name from students WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    #user and userType are being passed to the website here
    return render_template('Theme/shome.html', user = verifiedUser, userType = userType, Name = names)
#end studentHome------------------------------------------------------------------------------------------------------------------------    
    
#student calendar page---------------------------------------------------------------------------------------------------
@app.route('/scalendar', methods=['GET', 'POST'])
def studentCalendarPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "select * from users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("select * from users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('studentHome'))
        else:
            verifiedUser = ''
            session['username'] = ''
            
    if userType == 'student':
        # getting the user's first and last name(only students)
        cur.execute("select first_name, last_name from students WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason (I think it's because it's a tuple?)
        names=cur.fetchall()
        print(names)
    
    #user and userType are being passed to the website here
    return render_template('Theme/scalendar.html', user = verifiedUser, userType = userType, Name = names)
#end studentCalendarPage------------------------------------------------------------    
    
    
    
    
    
    
    
    
    
    
#keep this at the bottom. We think it starts the server    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)