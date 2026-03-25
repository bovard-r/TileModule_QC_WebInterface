#!/usr/bin/python3

import argparse
import oracledb
import os


def get_kops(cursor):
    kops={}
    for row in cursor.execute("""SELECT KIND_OF_PART_ID,LABEL_TYPECODE FROM CMS_HGC_CORE_CONSTRUCT.KINDS_OF_PARTS"""):
        kops[row[1]]=row[0]
    return kops

def get_locs(cursor):
    locs={}
    for row in cursor.execute("""SELECT LOCATION_ID,LOCATION_NAME FROM CMS_HGC_CORE_MANAGEMNT.LOCATIONS"""):
        locs[row[1]]=row[0]
    return locs

def get_qc_tiles(cursor,kops,wtsb,qc,locid):

    sbid=kops[wtsb]
    qcid=kops[qc]
    qctiles={}

    for row in cursor.execute("""SELECT PNT.BARCODE,PNT.BATCH_NUMBER,CHLD.BARCODE FROM CMS_HGC_CORE_CONSTRUCT.PARTS PNT INNER JOIN CMS_HGC_CORE_CONSTRUCT.PHYSICAL_PARTS_TREE ON PNT.PART_ID=CMS_HGC_CORE_CONSTRUCT.PHYSICAL_PARTS_TREE.PART_PARENT_ID INNER JOIN CMS_HGC_CORE_CONSTRUCT.PARTS CHLD ON CHLD.PART_ID=CMS_HGC_CORE_CONSTRUCT.PHYSICAL_PARTS_TREE.PART_ID AND PNT.KIND_OF_PART_ID=:1 AND CHLD.KIND_OF_PART_ID=:2 AND PNT.LOCATION_ID=:3""",(sbid,qcid,locid)):
        qctiles[row[2]]=(row[0],row[1])
    return qctiles

def get_nonqc_tiles(cursor,kops,wtsb,qc,locid):

    sbid=kops[wtsb]
    qcid=kops[qc]
    nonqctiles={}

    for row in cursor.execute("""SELECT PNT.BARCODE,PNT.BATCH_NUMBER FROM CMS_HGC_CORE_CONSTRUCT.PARTS PNT INNER JOIN CMS_HGC_CORE_CONSTRUCT.PHYSICAL_PARTS_TREE ON PNT.PART_ID=CMS_HGC_CORE_CONSTRUCT.PHYSICAL_PARTS_TREE.PART_PARENT_ID INNER JOIN CMS_HGC_CORE_CONSTRUCT.PARTS CHLD ON CHLD.PART_ID=CMS_HGC_CORE_CONSTRUCT.PHYSICAL_PARTS_TREE.PART_ID AND PNT.KIND_OF_PART_ID=:1 AND CHLD.KIND_OF_PART_ID<>:2 AND PNT.LOCATION_ID=:3""",(sbid,qcid,locid)):
        nonqctiles[row[0]]=row[1]
    return nonqctiles
    
if (__name__ == "__main__"):

    parser=argparse.ArgumentParser(description="Sample simple tool for checking existence of parts")
    parser.add_argument('--db',type=str,choices=['CMSR','INT2R'],default='CMSR',help="Select the database")
    parser.add_argument('--here',type=str,default="FNAL Lab 5 and 6",help="Which site")
    parser.add_argument('--mt',type=str,choices=['TI','TC'],required=True,help="Which major type (TI or TC)")
    parser.add_argument('csv',type=str,help='CSV list of barcodes')
    args=parser.parse_args()
    
    oracledb.init_oracle_client()
    connection=oracledb.connect(user="CMS_HGC_PRTTYPE_HGCAL_READER",password=os.environ["HGCAL_READER_PASSWORD"],dsn=args.db)
    
    cursor=connection.cursor()
    # find my location id
    locs=get_locs(cursor)
    kops=get_kops(cursor)
    locid=locs[args.here]

    with open(args.csv,"w") as f:
        f.write("BARCODE,BATCH,ALT_BARCODE\n")

        if (args.mt=='TI'):
            for ring in (18, 20, 22, 24, 'S3', 'S4', 34, 36, 38, 40, 'S5', 'S6'):
                pref="%s-%s"%(args.mt,ring)
                qc_tiles=get_qc_tiles(cursor,kops,pref+"SB",pref+"QC",locid)
                nonqc_tiles=get_nonqc_tiles(cursor,kops,pref+"SB",pref+"QC",locid)
                for tile in qc_tiles:
                    f.write("%s,%s,%s\n"%(tile,qc_tiles[tile][1],qc_tiles[tile][0]))
                for tile in nonqc_tiles:
                    f.write("%s,%s,\n"%(tile,nonqc_tiles[tile]))

        if (args.mt=='TC'):
            for ring in ('06','08',10,12,14,16, 18, 20, 22, 24, 'S3', 'S4', 34, 36, 38, 40, 'S5', 'S6'):
                pref="%s-%s"%(args.mt,ring)
                qc_tiles=get_qc_tiles(cursor,kops,pref+"SB",pref+"QC",locid)
                nonqc_tiles=get_nonqc_tiles(cursor,kops,pref+"SB",pref+"QC",locid)
                for tile in qc_tiles:
                    f.write("%s,%s,%s\n"%(tile,qc_tiles[tile][1],qc_tiles[tile][0]))
                for tile in nonqc_tiles:
                    f.write("%s,%s,\n"%(tile,nonqc_tiles[tile]))
                    
#        f.write("NAME,BARCODE\n")
#        title="320TI%02dSB%%"%(args.ring)
#        for row in cursor.execute("""SELECT NAME_LABEL,BARCODE FROM CMS_HGC_CORE_CONSTRUCT.PARTS WHERE BARCODE LIKE :1 AND LOCATION_ID=:2 ORDER BY BARCODE""",[title,locid]):
#            f.write("%s,%s\n"%row)

    
    
