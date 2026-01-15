#!./cgi_runner.sh
print("Content-Type: text/html")

import cgi, html
import cgitb; cgitb.enable()
import base
from connect import connect
import sys
sys.path.insert(0, '../../hgcal-label-info/label-authority/')
import label_authority as la
import csv
import pandas as pd

#cgi header

form = cgi.FieldStorage()

action = form.getvalue("action")

db = connect(1)
cur = db.cursor()

output = []

file_item = form["attach"]
df = pd.read_csv(file_item.file)

df["typecode"] = df["Barcode"].str[4:6] + "-" + df["Barcode"].str[6:8]
df["batch"] = df["Barcode"].str[8:12] + "-" + df["Barcode"].str[12:13]
df["identifier"] = df["typecode"].str[0:] + "-" + df["batch"].str[0:]

for tc, type_df in df.groupby("typecode"):
    for batch, batch_df in type_df.groupby("batch"):

        val = form.getvalue("%s" % (tc + "-" + batch))

        if val == "yes":
            for x in batch_df["Barcode"].tolist():
                sn = str(x)
                sn = sn.lstrip('\ufeff')
                cur.execute("insert into COMPONENT_STOCK (barcode, typecode, batch, entered) values ('%s', '%s', '%s', NOW())" % (sn, tc, batch))

        else:
            temp = pd.DataFrame({"Barcode": batch_df["Barcode"]})
            output.append(temp)

db.commit()

try:
    output_df = pd.concat(output, ignore_index=True)
    print("Content-Type: text/plain")
    print("Content-Disposition: attachment; filename=barcodes.csv")
    print()
    print(','.join(output_df.columns))
    for i, row in output_df.iterrows():
        line = ','.join(str(x) for x in row)
        print(line)

except:
    print("Location: home_page.py")
    print()
