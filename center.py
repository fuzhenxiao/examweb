from flask import Flask
from flask import render_template,redirect,url_for
from flask import request
from flask import jsonify
import json
import traceback
import sqlite3

app=Flask(__name__)
conn = sqlite3.connect("sqlite.db")
conn.execute('CREATE TABLE IF NOT EXISTS user(username1 TEXT, password1 TEXT)')
conn.close()
conn2 = sqlite3.connect("username&paper.db")
conn2.execute('CREATE TABLE IF NOT EXISTS paper(username2 TEXT, paper TEXT)')
conn2.close()
print ("Table created successfully")


@app.route('/',methods=['GET','POST'])
def login():
	return render_template('login.html')

@app.route('/check',methods=['GET','POST'])
def check():
	if request.method=='POST':
		uname=request.form['username']
		pword=request.form['password']
		conn = sqlite3.connect("sqlite.db")
		cursor=conn.cursor()
		cursor.execute('select * from user where username1=?', (uname,))
		values=cursor.fetchall()
		print(values)
		if values==[]:
			cursor.close()
			conn.close()
			return jsonify({'auth':'false','usname':uname})
		else:
			right_p=values[0][1]
			cursor.close()
			conn.close()
			if pword==right_p:
				return jsonify({'auth':'true','usname':uname})
			else:
				return jsonify({'auth':'false','usname':uname})
	else:
		return redirect('/')

@app.route('/sign',methods=['GET','POST'])
def sign():
	if request.method=='POST':
		uname=request.form['username']
		pword=request.form['password']
		if uname==None or uname=='':
			return jsonify({'auth':'false','usname':uname})
		conn = sqlite3.connect("sqlite.db")
		cursor=conn.cursor()
		cursor.execute('select * from user where username1=?', (uname,))
		values=cursor.fetchall()
		if len(values)==0:
			cursor.execute("INSERT INTO user VALUES (?,?)",(uname,pword))
			conn.commit()
			return jsonify({'auth':'true','usname':uname})
		else:
			return jsonify({'auth':'false','usname':uname})
		cursor.close()
		conn.close()
	else:
		return redirect('/')


@app.route('/editpage/<name>',methods=['GET','POST'])
def editpage(name):
	name=name[1:-1]
	print('name:',name)
	return render_template('editpage.html',username=name)

@app.route('/askpaper',methods=['GET','POST'])
def askpaper():
	if request.method=='POST':
		uname=request.form['uname']
		conn = sqlite3.connect("username&paper.db")
		cursor=conn.cursor()
		cursor.execute('select * from paper where username2=?', (uname,))
		values=cursor.fetchall()
		if len(values)==0:
			cursor.close()
			conn.close()
			return jsonify({'auth':'false','qlist':''})
		else:
			qlist=values[-1]
			print('qlist',qlist)
			cursor.close()
			conn.close()
			return jsonify({'auth':'true','qlist':qlist})


@app.route('/savepaper',methods=['GET','POST'])
def savepaper():
	if request.method=='POST':
		Q_AND_A=request.form['Q_AND_A']
		uname=request.form['uname']
		conn = sqlite3.connect("username&paper.db")
		cursor=conn.cursor()
		print('to save qanda:',Q_AND_A,type(Q_AND_A))
		cursor.execute("INSERT INTO paper VALUES (?,?)",(uname,Q_AND_A))
		conn.commit()
		cursor.close()
		conn.close()
		#Q_AND_A=json.loads(Q_AND_A) #[{},{},{}.....]
	return jsonify({'auth':'true',})


@app.route('/exam/<usr>',methods=['GET','POST'])
def exam(usr):
	if request.method=='POST':
		uname=request.form['uname']
		conn = sqlite3.connect("username&paper.db")
		cursor=conn.cursor()
		cursor.execute('select * from paper where username2=?', (uname,))
		values=cursor.fetchall()
		if len(values)==0:
			cursor.close()
			conn.close()
			return jsonify({'auth':'false','qlist':''})
		else:
			qlist=values[-1]
			print('qlist',qlist)
			cursor.close()
			conn.close()
			return jsonify({'auth':'true','qlist':qlist})
	else:
		return render_template('exampage.html')

if __name__=='__main__':
	app.debug=True
	try:
		app.run()
	except Exception:
		traceback.print_exc()
	input()

