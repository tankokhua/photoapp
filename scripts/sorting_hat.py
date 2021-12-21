#!/usr/bin/python
 
import csv
import sys

masterlist = map(lambda x:x.lower().strip(), open('oct2.txt').readlines())
 
results = []
csvfile = open('attendees.csv', 'r') 
if 1:
     reader = csv.reader(csvfile)
     cnt = 0
     for row in reader:
        if cnt == 0:
           header = row
           fields = {}
           for idx, f in enumerate(row):
               fields.setdefault(f, idx)
        else:
           results.append(row)
        cnt+=1
#"Attendee no.","Date","Surname","First Name","Email","QTY",
#"Ticket Type","Date Attending","Order no.","Order Type",
#"Total Paid (USD)","Fees Paid (USD)","Eventbrite Fees (USD)",
#"CC Processing (USD)","Attendee Status",
#"Are you using your own USS annual pass?","Meal preferences",
#"Please elaborate on your preference","Will you be driving to USS?"
attendees = ['eileentanyl']
committee = ['tankokhua','ckoh','keshav','limbeebee','lampuisuan','sereneho']
helpers  = ['enghai', 'siangleong']
not_going = ['chankl', 'vernonlim']
for x in results:
    email = x[fields["Email"]]
    username = email.replace('@micron.com', '')
    if username in committee+helpers+not_going:
       continue
    attendees.append(username)

houses = {}
for idx, user in enumerate(attendees):
    house=['ravenclaw', 'hufflepuff', 'gryffindor', 'slytherin']
    houses.setdefault(house[idx%4], []).append(user)

houses['gryffindor'].remove('ckyew')
houses['gryffindor'].append('raymondang')
houses['gryffindor'].remove('mccolina')
houses['gryffindor'].insert(5, 'mtlee')
houses['gryffindor'].append('clorenz')

houses['hufflepuff'].remove('raymondang')
houses['hufflepuff'].insert(11,'ckyew')
houses['hufflepuff'].remove('seahyc')
houses['hufflepuff'].insert(25, 'yping')

houses['slytherin'].append('mccolina')
houses['slytherin'].append('seahyc')
houses['slytherin'].remove('angus')
houses['slytherin'].remove('wfcleong')
houses['slytherin'].insert(30, 'vernonlim')

hno= {
       "ravenclaw":1,
       "hufflepuff":2,
       "gryffindor":3,
       "slytherin":4,
      }
cnt = 0
f = open('usernames.txt','w')
for house in houses:
    print house + " %d [%d]\n" % (hno[house], len(houses[house])) + ', '.join(houses[house])
    print
    for user in houses[house]:
        f.write("%s %d\n" % (user, hno[house]))
    cnt += len(houses[house])
f.close()
print "Total", cnt

#1:"Ravenclaw",
#2:"Hufflepuff",
#3:"Gryffindor",
#4:"Slytherin",
