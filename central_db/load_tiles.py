#!/usr/bin/python

import connect
import csv
import argparse

db=connect.connect(1)
cur=db.cursor()

def get_all_tiles(cur):
    cur.execute("SELECT barcode FROM COMPONENT_STOCK WHERE typecode LIKE 'TI-%'")
    all_tiles=set()
    for row in cur:
        all_tiles.add(row[0])
    cur.execute("SELECT barcode FROM COMPONENT_STOCK WHERE typecode LIKE 'TC-%'")
    all_tiles=set()
    for row in cur:
        all_tiles.add(row[0])
    return all_tiles

def load_tiles(filename, all_tiles,cur):
    basequery="INSERT INTO COMPONENT_STOCK (barcode, typecode, batch, alt_barcode) VALUES "
    irow=0
    added=0
    col={}
    with open(filename,"r") as f:
        query = basequery
        csvreader = csv.reader(filter(lambda row: len(row)>2 and row[0]!='#' and row[1]!='#',f))
        for row in csvreader:
            if irow==0:
                col[row[0]]=0
                col[row[1]]=1
                col[row[2]]=2
                irow=irow+1
                continue
            barcode=row[col["BARCODE"]]
            if barcode in all_tiles:
                print("Already have %s"%barcode)
                continue
            tc=barcode[3:5]+"-"+barcode[5:7]
            batch=row[col["BATCH"]]
            alt=row[col["ALT_BARCODE"]]
            if alt is None or len(alt)<5:
                query=query+'("%s","%s","%s",NULL), '%(barcode,tc,batch)
            else:
                query=query+'("%s","%s","%s","%s"), '%(barcode,tc,batch,alt)
            irow=irow+1
        if irow>1:
            query=query[:-2]
#            print(query)
            cur.execute(query)
    print("Added %d tiles to the database"%(irow-1))
            
parser = argparse.ArgumentParser()
parser.add_argument('csv',help='path to the input csv file')

args = parser.parse_args()

all_cur_tiles=get_all_tiles(cur)
#print(all_cur_tiles)
load_tiles(args.csv, all_cur_tiles, cur)
db.commit()
