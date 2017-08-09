#reading csv data
#for cohort analysis
#monthly report
#6.16.17

import csv
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
from paretochart import pareto

#years from Jan 2009- June 2017 for member-since data
newMemYears = 9

#months in a year
months = 12

#years of daily login data Sept 2016 - June 2017
loginYears = 2

#start year for new member data
startYear = 2009

#start year for daily login data
dailyStartYear = 2016

#current date
currentYr = 2017
currentMon = 6

#backDate of data for cohort analysis (in years)
backDate = 3


infile = open('tbl_member_since.csv', 'rb')
reader = csv.reader(infile)


#node structure, holds id, start date, and next node pointer
class Node:

	def __init__(self, ids=None, startDate=None, nextNode=None):
		self.id = int(ids)
		self.startDate = startDate
		self.next = nextNode

	def get_id(self):
		return self.id

	def set_id(self, newid):
		self.id = newid

	def get_start(self):
		return self.startDate

	def set_start(self, newStart):
		self.startDate = newStart

	def get_next(self):
		return self.next

	def set_next(self, newNext):
		self.next = newNext


#linked list w head, tail, and size
class LinkedList:

	def __init__(self):
		self.head = Node(-1, -1, None)
		self.tail = self.head
		self.size = 0
		self.idx = self.head

	def addFront(self, node):
		temp = Node(node.get_id(), node.get_start(), node.get_next())
		temp.set_next(self.head.get_next())
		self.head.set_next(temp)
		self.size += 1
		if self.size == 1:
			self.tail = self.head

	# returns equal node or none
	def searchId(self, node):
		current = self.head
		i = 0
		if self.size == 0:
			return None
		while current.get_id() != node.get_id():
			i += 1
			if i > self.size:
				return False 
			current = current.get_next()
		#print "match! ", current.get_id(), " ", node.get_id() 
		return True

	def searchStart(self, start):
		current = self.head
		i = 0;
		while current.get_start() != start:
			if i == self.size:
				return None
			current = current.get_next()
			i += 1
		return current

	def getSize(self):
		return self.size

	def getHead(self):
		return self.head

	#iterate over the linked list
	def iterate(self):
		if self.idx == None:
			return None
		self.idx = self.idx.get_next()
		return self.idx

	def resetIterator(self):
		self.idx = self.head

#*****unused function******
	#if ID not found, finds node w id directly left (less) of where new ID should go
	#otw, finds equal node and does not insert
	#inserts new node in sorted order if applicable
	def idSortedAdd(self, node):
		temp = Node(node.get_id(), node.get_start(), node.get_next())
		oneLess = self.head
		i = 0
		#print "temp: ", temp.get_id()
		while oneLess.get_next()!= None and oneLess.get_next().get_id() < temp.get_id() and oneLess.get_next().get_id() != -1:
			#print oneLess.get_id(), " next: ", oneLess.get_next().get_id()
			oneLess = oneLess.get_next()
			i += 1
			#print "size: ", self.size, " i: ", i
			if i >= self.size:
				break
		if oneLess.get_next() != None and oneLess.get_next().get_id() == temp.get_id():
			return
			#don't enter duplicate data points
			#possible check for errors in member data entry
		temp.set_next(oneLess.get_next())
		oneLess.set_next(temp)
		#if adding at end, update tail
		self.size += 1
		if i == self.size:
			self.tail = oneLess.get_next()
		if self.size == 1:
			self.tail = self.head.get_next()

	def prints(self):
		self.resetIterator()
		for i in range(self.size):
			print self.iterate().get_id()

#make array of members w start dates
#col 1-12 = months (really 0-11)
#rows 1-2 = year 2016-2017
startDateList = [[LinkedList() for i in range(months)] for j in range(newMemYears)]

#make class for date day/month/year
class Date:

	def __init__(self, mon, dy, yr):
		self.month = int(mon)
		self.day = int(dy)
		self.year = int(yr)

	def getMonth(self):
		return self.month

	def setMonth(self, mon):
		self.month = mon

	def getDay(self):
		return self.day

	def setDay(self, dy):
		self.day = dy

	def getYear(self):
		return self.year

	def setYear(self, yr):
		self.year = yr

#read in member-since data
rownum = 0
for row in reader:
	if rownum == 0:
		header = row
	else:
		colnum = 0
		memID = 0
		for col in row:
			#extract id and start date
			if colnum == 0: 
				#save memberID
				memID = col
			elif colnum == 1:
				#get date
				string = col.split("-")
				#print string
				date = Date(string[1], string[2], string[0])
				#store date and id in proper list item Node
				linklist = startDateList[date.getYear() - startYear][date.getMonth() - 1]
				linklist.addFront(Node(memID, date, None))
			colnum += 1
	rownum += 1

infile.close()

#read in daily login data; store in 2d array/list 
#starting in sept 2016: for each member who signed up n months ago
#search list of active users that day 
#each time an id is matched, activecount += 1
#% = activeCount/total members signed up n months ago 
# n in range 1 - 12 (arbitrary) 
infile2 = open('tbl_daily_active_users.csv', 'rb')
reader2 = csv.reader(infile2)

i = 0
j = 0
#^ necessary?
dailyLoginList = [[LinkedList() for i in range(months)] for j in range(loginYears)]

rownum = 0
for row in reader2:
	if rownum == 0:
		header = row
	else:
		colnum = 0
		date = None
		for col in row:
			#store data in data structure- linked list?-one for each month? 
			#extract id and start date
			if colnum == 0: 
				#get date
				string = col.split("-")
				#isolate day by deleting the timestamp at the end
				dayString = string[2].split(" ")
				string[2] = dayString[0]
				date = Date(string[1], string[2], string[0])
				#store date and id in proper list item Node
			elif colnum == 1:
				#save memberID
				#sort?
				dailyLoginList[date.getYear() - dailyStartYear][date.getMonth() - 1].addFront(Node(col, date, None))
			colnum += 1
	rownum += 1
infile2.close()

#store active ids in sorted 2d array of day and id # from smallest to largest 
#search sorted id list
yr = 0
#magic number :/
startMonth = 8
retRate = [[0.00 for i in range(months - 2)] for j in range(months - 2)]
churn = [[0.00 for i in range(months - 2)] for j in range(months - 2)] # needed?

j = 0
for j in range(months - 2):
	#print "break"
	mon = j + startMonth - (months * yr)
	if mon == months:
		yr += 1
		mon = 0
	print "Date:", mon + 1, "/", yr + dailyStartYear, "New Users", startDateList[yr + 7][mon].getSize()
	denom = 1;
	for i in range(months - j - 2):
		#magic numberrrr
		startDateList[yr + 7][mon].resetIterator()
		for k in range(startDateList[yr + 7][mon].getSize()):
			it = startDateList[yr + 7][mon].iterate()
			if it != None and dailyLoginList[yr + int((i + mon)/12)][(mon + i) % 12].searchId(it):
				retRate[i][j] += 1.00
				#duplicates?? sorted add???
				#6/23/17
		churn[i][j] = float(startDateList[yr + 7][mon].getSize()) - retRate[i][j]
		#try
		if i == 0:
			denom = retRate[i][j]
		retRate[i][j] /= denom
		#print "   Percent users active", i, "months later in", (mon + i) % 12 + 1, "/", yr + dailyStartYear + int((i + mon)/12), ":", retRate[j][i]
	
#write data out to csv ??

#use dataframe and seaborns to create heatmap

# np.random.seed(0)
# sns.set()
# uniform_data = np.random.rand(10, 12)
# ax = sns.heatmap(uniform_data)
# example ^^

indexs = [(' {}/{} '.format((i + startMonth) % 12 + 1, 16 + int((i + startMonth)/12))) for i in range(months - 2)]
df = pd.DataFrame(retRate, index=[i for i in range(months - 2)], columns=indexs)

sns.set(style='white')

plt.figure(figsize=(months - 2, months - 2))
plt.title('Cohorts: User Retention by Months After Sign-Up')
plt.xlabel('Months After Sign-Up')
plt.ylabel('Sign-Up Date')

#label axes in heat map 
#6/27/17
sns.heatmap(df.T, annot=True, mask=df.T == 0.00, fmt='.0%')

plt.show()


df2 = pd.DataFrame(churn, index=[i for i in range(months - 2)], columns=indexs)
df2 = df2[df2 > 0]
df2 = df2.T
#df3 = pd.DataFrame([0.00 for i in range(months - 2)], index=['avg'], columns=[i for i in range(months - 2)])
#dropoff %
df2 = df2.mean()
i = 8
while i >= 0:
    #get change difference
    df2[i + 1] = df2[i + 1] - df2[i]
    i -= 1

#try this to fix pareto
df2[0] = 0

pareto(df2)
plt.show()
#two lines/percentages???

