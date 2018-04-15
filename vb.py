import random,threading,sys,time,pymongo
from flask import Flask,render_template,request
from pymongo import MongoClient
client=MongoClient()
db=client.dpdata
collection=db.phname
app=Flask(__name__)
names=[]
def insertdata(name):
	for i in range(5):		
		collection.insert({"id":i,"name":name[i]})
	return
import time,random
import threading

class philosopher(threading.Thread):
	running=True
	def __init__(self,name,forkonleft,forkonright):
		threading.Thread.__init__(self)
		self.name=name
		self.forkonleft=forkonleft
		self.forkonright=forkonright
		#print name,forkonleft,forkonright
	def run(self):
		while(self.running):
			time.sleep(random.uniform(5,10))
			print "philosopher %s is hungry" % self.name
			self.checkfork()
	def checkfork(self):
		fork1=self.forkonleft
		fork2=self.forkonright
		while (self.running):
			fork1.acquire(True)
			locked=fork2.acquire(False)
			if(locked):
				print "Successfully got two forks....."
				break
			fork1.release()
		else:
			return
		self.eating()
		fork1.release()
		fork2.release()
	def eating(self):
		print "philosopher %s Starts Eating ..."% self.name
		time.sleep(random.uniform(1,10))
		print "philosopher %s leaves Eating ..."% self.name

def DiningPhilosophers(names):
    forks = [threading.Lock() for n in range(5)]  
    philosophers = [philosopher(names[i], forks[i % 5], forks[(i + 1) % 5]) for i in range(5)]
    random.seed(507129)
    philosopher.running = True
    for p in philosophers:
	p.start()
    
    time.sleep(100)   
    philosopher.running = False 
    print ("Now we're finishing.")
    return

@app.route('/')
def display():
	return render_template("try.html")

@app.route('/',methods=['POST'])
def collect():
	ph1=request.form['name1']
	ph2=request.form['name2']
	ph3=request.form['name3']
	ph4=request.form['name4']
	ph5=request.form['name5']
	names.append(ph1)
	names.append(ph2)
	names.append(ph3)
	names.append(ph4)
	names.append(ph5)
	insertdata(names)
	DiningPhilosophers(names)
	return "Now we're finishing."
	

app.run("localhost",debug=True)
