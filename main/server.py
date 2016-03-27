#this is the file that starts the server and has all of the server commands in it
#!/usr/bin/env python

import psycopg2
import psycopg2.extras
import os
from flask import Flask, session, render_template, request, redirect, url_for
import cgi, cgitb

# may need this for later
#cgitb.enable()

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
@app.route('/aHome', methods=['GET', 'POST'])
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
    return render_template('Theme/aHome.html', user = verifiedUser, userType = userType, Name = names)
#end adminHome------------------------------------------------------------------------------------------------------------------------ 

#admin calendar page------------------------------------------------------    
@app.route('/aCalendar', methods=['GET', 'POST'])
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
    return render_template('Theme/aCalendar.html', user = verifiedUser, userType = userType, Name = names)
#end admin calendar page--------------------------------------------------     

#admin exercises page------------------------------------------------------    
@app.route('/aExercises', methods=['GET', 'POST'])
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
    ## For dubugging ##
    #print(rows[0][0])
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        print "made it to post"
        
        #This is where we iterate through all exercises found in the database to see which one was selected.
        action = request.form['action']
        exercise = request.form['exercise']
        print(action)
        print(exercise)
        if action == 'Edit':
            session['exercise'] = exercise
            return redirect(url_for('adminEditExercisesPage'))
        if action == 'Delete':
            confirm = request.form['confirmD']
            print(confirm)
            if confirm == 'Delete':
                query = "DELETE FROM exercises WHERE exercise_name = '%s'" % (exercise,)
                print(query)
                try:
                    cur.execute("DELETE FROM exercises WHERE exercise_name = %s", (exercise,))
                except:
                    print("Problem inserting into exercises")
                    db.rollback()
                db.commit()
            return redirect(url_for('adminExercisesPage'))
        if action == 'View':
            session['exercise'] = exercise
            return redirect(url_for('adminViewExercisesPage'))
        
    #user and userType are being passed to the website here along with the exercise data as "results".
    return render_template('Theme/aExercises.html', user = verifiedUser, userType = userType, Name = names, results = rows)
#end admin exercises page--------------------------------------------------  

#admin view exercise page------------------------------------------------------    
@app.route('/aViewExercises', methods=['GET', 'POST'])
def adminViewExercisesPage():
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
    if 'exercise' in session:
        exercise = session['exercise']
    else:
        return redirect(url_for('adminExercisesPage'))
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # get all data for the exercise ...
    rows = []
    query = "select exercise_name, muscle_group, description, youtube_link from exercises where exercise_name = '%s'" % (exercise,)
    print query
    cur.execute("select exercise_name, muscle_group, description, youtube_link from exercises where exercise_name = %s",(exercise,))
    rows = cur.fetchall()
    print(rows)
    ## For dubugging ##
    #print(rows[0][0])
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    #user, userType, names, and all data for the exercise are being passed to the website here. 
    return render_template('Theme/aViewExercises.html', user = verifiedUser, userType = userType, Name = names, results = rows, exercise = exercise)
#end admin view exercises page-------------------------------------------------- 

#admin edit exercise page------------------------------------------------------    
@app.route('/aEditExercises', methods=['GET', 'POST'])
def adminEditExercisesPage():
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
    if 'exercise' in session:
        exercise = session['exercise']
    else:
        return redirect(url_for('adminExercisesPage'))
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    badName = False
    exerciseEdited = False
    
    # get all data for the exercise ...
    rows = []
    query = "select exercise_name, muscle_group, description, youtube_link from exercises where exercise_name = '%s'" % (exercise,)
    print query
    cur.execute("select exercise_name, muscle_group, description, youtube_link from exercises where exercise_name = %s",(exercise,))
    rows = cur.fetchall()
    print(rows)
    ## For dubugging ##
    #print(rows[0][0])
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
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
        if cur.fetchone() and exerciseName != exercise:
            badName = True
        elif exerciseName == '':
            badName = True
        else:
            badName = False
            exerciseEdited = True
            query = "UPDATE exercises SET (admin_id, exercise_name, description, muscle_group, youtube_link) = ('%s', '%s', '%s', '%s', '%s') WHERE exercise_name = '%s'" % (session['ID'],exerciseName,description,muscleGroup,youTube,exercise)
            print query
            try:
                cur.execute("UPDATE exercises SET (admin_id, exercise_name, description, muscle_group, youtube_link) = (%s, %s, %s, %s, %s) WHERE exercise_name = %s", (session['ID'],exerciseName,description,muscleGroup,youTube,exercise))
            except:
                print("Problem updating exercises")
                db.rollback()
            db.commit()
            session['exercise'] = exerciseName
            exercise = exerciseName
            # get the newly updated exercies ready for display
            cur.execute("select exercise_name, muscle_group, description, youtube_link from exercises where exercise_name = %s",(exercise,))
            rows = cur.fetchall()
            print("done!")
    #user, userType, names, and all data for the exercise are being passed to the website here. badName and exerciseEdited are for error and success notification.
    return render_template('Theme/aEditExercises.html', user = verifiedUser, userType = userType, Name = names, results = rows, exercise = exercise, badName = badName, exerciseEdited = exerciseEdited)
#end admin edit exercises page--------------------------------------------------

#admin create exercises page------------------------------------------------------    
@app.route('/aCreateExercise', methods=['GET', 'POST'])
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
        elif exerciseName == '':
            badName = True
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
        
    #user and userType are being passed to the website here. badName and exerciseCreated are for error and success notification.
    return render_template('Theme/aCreateExercise.html', user = verifiedUser, userType = userType, Name = names, badName = badName, exerciseCreated = exerciseCreated)
#end admin create exercise page--------------------------------------------------

#admin workouts page------------------------------------------------------    
@app.route('/aWorkouts', methods=['GET', 'POST'])
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
    
    # get all workouts from the database ...
    rows = []
    query = "SELECT workout_name FROM workouts"
    print query
    cur.execute("SELECT workout_name FROM workouts")
    #if cur.fetchone():
    rows = cur.fetchall()
    print(rows)
    ## For dubugging ##
    #print(rows[0][0])
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        print "made it to post"
        
        #This is where we iterate through all workouts found in the database to see which one was selected.
        action = request.form['action']
        workout = request.form['workout']
        print(action)
        print(workout)
        if action == 'Edit':
            session['workout'] = workout
            return redirect(url_for('adminEditWorkoutsPage'))
        if action == 'Delete':
            confirm = request.form['confirmD']
            print(confirm)
            if confirm == 'Delete':
                query = "DELETE FROM exercises WHERE exercise_name = '%s'" % (workout,)
                print(query)
                try:
                    cur.execute("DELETE FROM exercises WHERE exercise_name = %s", (workout,))
                except:
                    print("Problem inserting into exercises")
                    db.rollback()
                db.commit()
            return redirect(url_for('adminWorkoutsPage'))
        if action == 'View':
            session['workout'] = workout
            return redirect(url_for('adminViewWorkoutsPage'))
        
    #user and userType are being passed to the website here along with the workout data as "results".
    return render_template('Theme/aWorkouts.html', user = verifiedUser, userType = userType, Name = names, results = rows)
#end admin workout page--------------------------------------------------  

#admin create workout page------------------------------------------------------    
@app.route('/aCreateWorkout', methods=['GET', 'POST'])
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
    badName = False
    workoutCreated = False

    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        
        workoutName = request.form['ename']
        print(workoutName)
        muscleGroup = request.form['emusclegroup']
        print(muscleGroup)
        description = request.form['edesc']
        print(description)
        youTube = request.form['eyoutube']
        print(youTube)
        
        query = "select exercise_name from exercises WHERE exercise_name = '%s'" % (workoutName,)
        print query
        cur.execute("select exercise_name from exercises WHERE exercise_name = %s", (workoutName,))
        if cur.fetchone():
            badName = True
            
        elif workoutName == '':
            badName = True
        else:
            badName = False
            workoutCreated = True
            query = "INSERT INTO exercises (admin_id, exercise_name, description, muscle_group, youtube_link) VALUES ('%s', '%s', '%s', '%s', '%s')" % (session['ID'],workoutName,description,muscleGroup,youTube)
            print query
            try:
                cur.execute("INSERT INTO exercises (admin_id, exercise_name, description, muscle_group, youtube_link) VALUES (%s, %s, %s, %s, %s)", (session['ID'],workoutName,description,muscleGroup,youTube))
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
        
    #user and userType are being passed to the website here. badName and workoutCreated are for error and success notification.
    return render_template('Theme/aCreateWorkout.html', user = verifiedUser, userType = userType, Name = names, badName = badName, workoutCreated = workoutCreated)
#end admin create workout page--------------------------------------------------

#admin Training Programs page------------------------------------------------------    
@app.route('/aTrainingPrograms', methods=['GET', 'POST'])
def adminTrainingProgramsPage():
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
    query = "SELECT training_program_name, sport, student FROM training_programs"
    print query
    cur.execute("SELECT training_program_name, sport, student FROM training_programs")
    #if cur.fetchone():
    rows = cur.fetchall()
    print(rows)
    ## For dubugging ##
    #print(rows[0][0])
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        print "made it to post"
        
        #This is where we iterate through all exercises found in the database to see which one was selected.
        action = request.form['action']
        exercise = request.form['exercise']
        print(action)
        print(exercise)
        if action == 'Edit':
            session['exercise'] = exercise
            return redirect(url_for('adminEditExercisesPage'))
        if action == 'Delete':
            confirm = request.form['confirmD']
            print(confirm)
            if confirm == 'Delete':
                query = "DELETE FROM exercises WHERE exercise_name = '%s'" % (exercise,)
                print(query)
                try:
                    cur.execute("DELETE FROM exercises WHERE exercise_name = %s", (exercise,))
                except:
                    print("Problem inserting into exercises")
                    db.rollback()
                db.commit()
            return redirect(url_for('adminExercisesPage'))
        if action == 'View':
            session['exercise'] = exercise
            return redirect(url_for('adminViewExercisesPage'))
        
    #user and userType are being passed to the website here along with the exercise data as "results".
    return render_template('Theme/aTrainingPrograms.html', user = verifiedUser, userType = userType, Name = names, results = rows)
#end admin training programs page--------------------------------------------------  

#admin add user page------------------------------------------------------    
@app.route('/aAddUser', methods=['GET', 'POST'])
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
    return render_template('Theme/aAddUser.html', user = verifiedUser, userType = userType, Name = names)
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