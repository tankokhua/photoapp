#!/usr/bin/python
import csv
import sys

kinds = ['Order']
if len(sys.argv)==2:
   datafiles = [sys.argv[1]]
else:
   datafiles = map(lambda x:"datadir/%ss.csv" % x.lower(), kinds) 


menu = {
         "Beefy Jack Burger"    : 6.90,
         "Chargrill Chicken"    : 8.90,
         "Crispy Fried Fish"    : 9.50,
         "Plain Water"          : 0.30,
         "Pepsi"                : 1.80,
         "7-Up"                 : 1.80,
         "Mug Rootbeer"         : 1.80,
         "Mug Grape"            : 1.80,
         "Hot Tea"              : 1.50,
         "Specialty Tea"        : 1.80,
         "Espresso"             : 1.50,
         "Freshly Brewed Coffee": 1.90,
       }

def readcsv(file):
    reader = csv.reader(open(file, 'rb'))
    header = False
    db = {}
    for row in reader:
        if not header:
           header = True
           cnt  = 0
           for item in row:
               db.setdefault('props', {}).setdefault(item, cnt)
	       cnt+=1
        else:
	   db.setdefault('data', []).append(row)
    return db

order_db = readcsv(datafiles[0])

orders = {}
#drink,main_course,attempts,user,key,date,sides
for order in order_db['data']:
    user        = order[order_db['props']['user']]
    main_course = order[order_db['props']['main_course']]
    sides       = order[order_db['props']['sides']]
    drink       = order[order_db['props']['drink']]
    orders.setdefault(user, {}).setdefault('main_course', main_course)
    orders.setdefault(user, {}).setdefault('sides', sides)
    orders.setdefault(user, {}).setdefault('drink', drink)

total = 0
cnt = 0
for user in orders.keys():
    print user 
    main_course = orders[user]["main_course"]
    sides       = orders[user]["sides"]
    drink       = orders[user]["drink"]
    print "\tMain Course: %s" % main_course
    print "\tSides      : %s" % ", ".join(sides.split('|'))
    print "\tDrink      : %s" % drink
    cost = menu[main_course] + menu[drink]
    print "\tCost       : %.2f\n" % cost
    total += cost
    cnt += 1

print "\nTotal: %.2f [%.2f]" % (total, total/cnt)

