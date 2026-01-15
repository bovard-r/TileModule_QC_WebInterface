#!./cgi_runner.sh

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
print("Content-type: text/html\n")

form = cgi.FieldStorage()

action = form.getvalue("action")

db = connect(0)
cur = db.cursor()

base.header(title='Board Check In')
base.top()

if action == "submit":

    file_item = form["attach"]
    df = pd.read_csv(file_item.file)
    csv_data = df.to_csv(index=False)

    df["typecode"] = df["Barcode"].str[4:6] + "-" + df["Barcode"].str[6:8]
    df["batch"] = df["Barcode"].str[8:12] + "-" + df["Barcode"].str[12:13]
    df["identifier"] = df["typecode"].str[0:] + "-" + df["batch"].str[0:]

    print('<form action="tile_stock2.py" method="post" enctype="multipart/form-data">')
    print("<div class='row'>")
    print('<div class = "col-md-6 pt-4 ps-4 mx-2 my-2">')
    print('<h2>Verify amounts of tiles are correct</h2>')
    print("</div>")
    print("</div>")
    print(f'<input type="hidden" name="attach" value="{csv_data}">')

    print('<div class="row">')
    print('<div class="col-md-12">')
    print('<div class="col-md-11 ps-5 py-4my-2"><table class="table table-hover">')
    print('<tr>')
    print('<th> Typecode </th>')
    print('<th> Batch </th>')
    print('<th> Number sent </th>')
    print('<th> Correct? </th>')
    print('</tr>')

    for tc, type_df in df.groupby("typecode"):
        for batch, batch_df in type_df.groupby("batch"):
            count = len(batch_df)
            print('<tr>')
            print('<td>')
            print(tc)
            print('</td>')
            print('<td>')
            print(batch)
            print('</td>')
            print('<td>')
            print(count)
            print('</td>')
            print('<td>')
            print('''
<fieldset>
    <label>
      <input type="radio" name="%(x)s" value="yes" checked>
      Yes
    </label>

    <label>
      <input type="radio" name="%(x)s" value="no">
      No
    </label>

  </fieldset>
            ''' % {'x': tc + "-" + batch})
            print('</td>')
            print('</tr>')

    print('</table>')
    print('</div>')
    print('</div>')
    print('</div>')

    print("<div class='row'>")
    print('<div class = "col-md-6 pt-2 ps-5 mx-2 my-2">')
    # submits the form on click
    print('<button class="btn btn-dark" type="submit" name="action" value="submit">Confirm Tile Stock</button>')
    print("</div>")
    print("</div>")
    print("<div class='row pt-4'>")
    print("</div>")
    print("</form>")

else:

    print('<form action="create_tile_stock.py" method="post" enctype="multipart/form-data">')
    print("<div class='row'>")
    print('<div class = "col-md-6 pt-4 ps-4 mx-2 my-2">')
    print('<h2>Add new Tile stock</h2>')
    print("</div>")
    print("</div>")

    print('<div class="row">')
    print('<div class="col-md-2 pt-2 ps-5 mx-2 my-2">')
    print("<b>CSV File of Barcodes from STT:</b>")
    print('</div><div class="col-md-5 pt-2 ps-5 mx-2 my-2">')
    print("<input type='file' class='form-control' name='attach' accept='.csv'>")
    print('</div>')
    print('</div>')

    print("<div class='row'>")
    print('<div class = "col-md-6 pt-2 ps-5 mx-2 my-2">')
    # submits the form on click
    print('<button class="btn btn-dark" type="submit" name="action" value="submit">Create Tile Stock</button>')
    print("</div>")
    print("</div>")
    print("<div class='row pt-4'>")
    print("</div>")
    print("</form>")


base.bottom()
