from flask import Flask
from flask import render_template
import sqlite3
from flask import request,url_for
from flask import redirect,Response

app=Flask(__name__)


@app.route('/')
def mainpage():
	resp=Response("""<html> <head> <title>ajuna's webpage </title> </head> 
                      <h1 style="font-size:50">Register your car</h1>
                      <p ><a href="/details"> Add your car's details</a></p>
                      <p><a href="/sortname"> View details of cars sorted by owner's name</a></p>
		      <p><a href="/sortdistrict"> View details of cars sorted by district</a></p>
                      <p><a href="/search"> Search car details</a></p>
                      <p><a href="/remove"> Remove car details</a></p>
                       </html>""",status=200,mimetype='html')
	return resp

@app.route('/details', methods=['POST', 'GET'])
def details():
  if request.method == 'GET':
	return render_template('car-reg.html')
	
  if request.method == 'POST':
    	name=request.form['owner_name']
	district=request.form['district']
	car=request.form['car']
	number=request.form['number']
	lisence=request.form['lisence']

	data=(name, district, car, number, lisence)

	con = sqlite3.connect("register.db")
	cur=con.cursor()
   	cur.execute("CREATE TABLE IF NOT EXISTS information(name text, district text, car text, number text, lisence text)")
    	cur.execute("INSERT INTO information VALUES(?, ?, ?, ?, ?)", data)
	con.commit()
	con.close()
		
	return redirect(url_for('mainpage'))	

@app.route('/sortname', methods=['POST', 'GET'])
def sortname():
 if request.method == 'GET':
	con = sqlite3.connect('register.db')    
    
    	cur = con.cursor()    
    	cur.execute("SELECT * FROM information ORDER BY name ASC")

    	rows = cur.fetchall()
	entries = [dict(name=row[0], district=row[1], car=row[2], number=row[3], lisence=row[4]) for row in rows]
	return render_template('show_entries.html', entries=entries)


@app.route('/sortdistrict', methods=['POST', 'GET'])
def sortdistrict():
 if request.method == 'GET':
	con = sqlite3.connect('register.db')    
    
    	cur = con.cursor()    
    	cur.execute("SELECT * FROM information ORDER BY district ASC")

    	rows = cur.fetchall()
	entries = [dict(name=row[0], district=row[1], car=row[2], number=row[3], lisence=row[4]) for row in rows]
	return render_template('show_entries.html', entries=entries)

  
@app.route('/search', methods=['POST', 'GET'])
def search():
  if request.method == 'GET':
	resp = Response("""<html><body>
					<form action='/search' method="post">	
					<div> Owner's Name <input type="text" name = "search" ></input></div>
					<div><input type="submit" value="submit"></div>
					</form>		
					</body></html>""", status=200, mimetype='html')
	return resp

  if request.method == 'POST':
	search=request.form['search']
	con = sqlite3.connect('register.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM information WHERE name=:name", {"name": search})
	
	rows = cur.fetchall()
	entries = [dict(name=row[0], district=row[1], car=row[2], number=row[3], lisence=row[4]) for row in rows]
	return render_template('show_entries.html', entries=entries)
    	      
	
@app.route('/remove', methods=['POST', 'GET'])
def remove():
  if request.method == 'GET':
	resp = Response("""<html><body>
					<form action='/remove' method="post">	
					<div> Owner's Name <input type="text" name = "remove" ></input></div>
					<div><input type="submit" value="submit"></div>
					</form>		
					</body></html>""", status=200, mimetype='html')
	return resp	

  if request.method == 'POST':
	remove=request.form['remove']
	con = sqlite3.connect('register.db')
	cur = con.cursor()
	cur.execute("DELETE FROM information WHERE name=:name", {"name": remove})
	con.commit()
	con.close()
	resp = Response("""<html><body>
					<div>"""+remove+"""'s details removed</div>
					<p><a href="/">Home</a></p>
					</body></html>""",mimetype='html')
	return resp 


  
if __name__=='__main__':
	app.debug = True	
	app.run()
