import os
from tempfile import NamedTemporaryFile
import shutil
from ast import literal_eval
import csv


pathfile = os.getcwd()
fieldnames = ['item','price','counter']
def clients_feedback():
        file = open(pathfile+"/feedback.txt",'r')
        Lines = file.readlines()
        for line in Lines:
                print(line)
def getprice(price):
        amount =0
        for key,value in price.items():
                for k ,v in  value.items():
                        amount += int(v)
        return amount

def showitems(items):
        print("your items for pyment: ")
        for key,value in items.items():
                for k ,v in value.items():
                        print(key,"- ",k,", " , v)


def retuendicbyline(line , num):
        i =0
        itemdic = {}
        oneitem = {}
        item =''
        price =''
        found =0
        for i in line:
                if i != '-' and found == 0:
                        item+= i
                else:
                        found =1
                        if i != '-':
                                price += i
        price = price[:-1]
        oneitem[item] = price
        itemdic[num] = oneitem
        return itemdic

def returnalltext():
    i = 0
    dictitems = {}
    file = open(pathfile + "/items.txt", 'r')
    Lines = file.readlines()
    for line in Lines:
        dictline = retuendicbyline(line, i)
        dictitems.update(literal_eval(str(dictline)))
        i += 1
    file.close()
    return dictitems


def counter(key, value):
    found = 0
    with open('chooscustomer.csv', 'r', newline='') as csvfil, open('chooscustomer.csv', 'a+',
                                                                    newline='') as csvfilwrite:
        csvReader = csv.DictReader(csvfil, fieldnames=fieldnames, delimiter=' ', quotechar='|')
        csvWrite = csv.DictWriter(csvfilwrite, fieldnames=fieldnames)
        headers = next(csvReader, None)
        if str(headers) == 'None':
            csvWrite.writeheader()
        # print("refaa")
        for row in csvReader:
            print(row['item'][0])
            if row['item'][0] == key:
                newcount = int(row['item'][1]) + 1
                csvWrite.writerow({'item': key, 'price': value, 'counter': newcount})
                found = 1
            if found != 1:
                csvWrite.writerow({'item': key, 'price': value, 'counter': 1})

def iterate(k, v):
    dicthelp = {}
    i =0
    found=0
    fields = ['item', 'price', 'counter']
    with open('chooscustomer.csv', 'r') as csvfile :
        reader = csv.DictReader(csvfile, fieldnames=fields)
        headers = next(reader, None)
        if str(headers) == 'None':
            tempfile =open('chooscustomer.csv', 'w')
            writer = csv.DictWriter(tempfile, fieldnames=fields)
            writer.writeheader()
            found =1
        for row in reader:
            dicthelp[i] = row
            i+=1
        if len(dicthelp) > 0:
            tempfile = open('chooscustomer.csv', 'w')
            writer = csv.DictWriter(tempfile, fieldnames=fields)
            writer.writeheader()
            for key, value in dicthelp.items():
                if value['item'] != str(k):
                    writer.writerow(value)
                else:
                    x = int(value['counter']) + 1
                    row = {'item': k+ '', 'price': v+ '', 'counter': x}
                    writer.writerow(row)
                    found =1
        if found != 1:
            row1 = {'item': k+ '', 'price': v+ '', 'counter': str(1)}
            writer.writerow(row1)
        #     if row['item'] == str(key):
        #         found = 1
        #         print('updating row', row['item'])
        #         x = int(row['counter']) + 1
        #         row['price'], row['counter'] = value, x
        #         rowhelp = {'item': row['item'], 'price': row['price'], 'counter': row['counter']}
        #         writer.writerow(rowhelp)
        # if found != 1:
        #         row1 = {'item': key + '', 'price': value + '', 'counter': str(1)}
        #         writer.writerow(row1)
        shutil.move(tempfile.name, 'chooscustomer.csv')
    csvfile.close(),tempfile.close()

def yourchoose(allitemsbynum, chooseitem):
    print(" choose items to buy by number of item , enter 0 when finished: ")
    num = int(input())
    while num != 0:
        # if num in chooseitem:
        #     newitem = {}
        #     for key, value in chooseitem[num].items():
        #         newitem[key] = int(value) + int(allitemsbynum[num][key])
        #         # counter(key,value)
        #         iterate(key, value)
        #         chooseitem[num] = newitem
        # else:
        chooseitem[num] = allitemsbynum[num]
        for key, value in chooseitem[num].items():
                # counter(key,value)
                iterate(key, value)
        num = int(input())
    return chooseitem

def additems():
        items = []
        print("write name of product ,Enter enter to finish")
        product = input("set name of product: ")
        file = open(pathfile + "/newitems.txt", 'a')
        while len(product) > 0:
            items.append(str(product))
            product = input("set another name of product, put Enter if u finish: ")
        file.write(str(items))
        file.write('\n')
        file.close()


def main():
    chooseitem = {}
    print("Welcome to store CLI")
    print("this all items for buy by store CLI")
    showitems(literal_eval(str(returnalltext())))
    allitemsbynum = literal_eval(str(returnalltext()))
    chooseitem2 = literal_eval(str(yourchoose(allitemsbynum, chooseitem)))
    print("checkout for pyment is ", getprice(chooseitem2), " Shekels")
    print("if wants to submit a review of the supermarket.y/n")
    ans = input("Enter y to get yes OR n to get no: ")
    if ans == 'y':
        showitems(literal_eval(str(returnalltext())))
        chooseitem2 = literal_eval(str(yourchoose(allitemsbynum, chooseitem)))
        print("new checkout for pyment is ", getprice(chooseitem2), " Shekels")
    print("do you want to propose new items")
    answer = input("Enter y to get yes OR n to get no: ")
    if answer == 'y':
        additems()
    comment = input("can take comment else put enter: ")
    feed = input("Rate the supermarket out of 1-5: ")
    if len(comment) > 0:
        comm = open(pathfile + "/comments.txt", 'a')
        comm.write(comment + '\n')
        comm.close()
    if len(feed) > 0:
        feedb = open(pathfile + "/feedback.txt", 'a')
        feedb.write(feed + '\n')
    print("thanks from store CLI")
main()
clients_feedback()
