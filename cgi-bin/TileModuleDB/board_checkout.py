#!./cgi_runner.sh

import cgi, html
import base
import home_page_list
import board_check_functions 
import numpy
from connect import connect

db = connect(0)
cur = db.cursor()

#cgi header
print("Content-type: text/html\n")

base.header(title='Board Checkout')
base.top()

form = cgi.FieldStorage()

if form.getvalue("full_id"):
    barcode = form.getvalue("full_id")

    print('<form action="board_checkout2.py" method="post" enctype="multipart/form-data">')
    print('<div class="row">')
    print('<div class="col-md-12 pt-4 ps-5 mx-2 my-2">')
    print('<h2>Mark %s as shipped</h2>' % barcode)
    print('</div>')
    print('</div>')

    print(f"<input type='hidden' name='barcode' value='{barcode}'>")

    # gives options for tester
    cur.execute("Select person_id, person_name from People;")

    print('<div class="row">')
    print('<div class="col-md-3 pt-2 ps-5 mx-2 my-2">')
    print('<label>Tester')
    print('<select class="form-control" name="person_id">')
    for person_id in cur:
        print("<option value='%s'>%s</option>" % ( person_id[0] , person_id[1] ))
                        
    print('</select>')
    print('</label>')
    print('</div>')

    print("<div class='row'>")
    print('<div class="col-md-9 pt-2 ps-5 mx-2 my-2">')
    print('<label>Location</label><p>')
    print('<textarea rows="1" cols="20" name="location"></textarea>')
    print('</div>')
    print('</div>')

    print('<div class="row">')
    print('<div class="col-md-6 pt-2 ps-5 mx-2 my-2">')
    print('<input type="submit" class="btn btn-dark" value="Submit">')
    print('</div>')
    print('</div>')

    print('</form>')

else:

    print('<form action="board_checkout2.py" method="post" enctype="multipart/form-data">')
    print('<div class="row">')
    print('<div class="col-md-12 pt-4 ps-5 mx-2 my-2">')
    print('<h2>Log Board Shipment</h2>')
    print("<h5>Takes in a csv with one column of the board barcodes to be shipped, and the location they're going to.</h5>")
    print('</div>')
    print('</div>')

    # gives options for tester
    cur.execute("Select person_id, person_name from People;")

    print('<div class="row">')
    print('<div class="col-md-3 pt-2 ps-5 mx-2 my-2">')
    print('<label>Tester')
    print('<select class="form-control" name="person_id">')
    for person_id in cur:
        print("<option value='%s'>%s</option>" % ( person_id[0] , person_id[1] ))
                        
    print('</select>')
    print('</label>')
    print('</div>')
    print('<div class="row">')
    print('<div class="col-md-2 pt-2 ps-5 mx-2 my-2">')
    print("<b>Boards CSV:</b>")
    print('</div><div class="col-md-5 pt-2 ps-5 mx-2 my-2">')
    print("<input type='file' class='form-control' name='boards'>")
    print('</div>')

    print("<div class='row'>")
    print('<div class="col-md-9 pt-2 ps-5 mx-2 my-2">')
    print('<label>Location</label><p>')
    print('<textarea rows="1" cols="20" name="location"></textarea>')
    print('</div>')
    print('</div>')

    print('<div class="row">')
    print('<div class="col-md-6 pt-2 ps-5 mx-2 my-2">')
    print('<input type="submit" class="btn btn-dark" value="Submit">')
    print('</div>')
    print('</div>')

    print('</form>')

base.bottom()
