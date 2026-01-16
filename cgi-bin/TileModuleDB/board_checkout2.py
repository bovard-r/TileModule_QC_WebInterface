#!./cgi_runner.sh

import cgi, html
import cgitb; cgitb.enable()
import base
import board_check_functions
import os
from connect import connect, get_base_url, connect_admin

base_url = get_base_url()
db = connect(1)
cur = db.cursor()

#cgi header
print("Content-type: text/html\n")

base.header(title='Board Shipment Submission')
base.top()

# grabs the information from the form and calls board_checkout() to enter info into the DB
form = cgi.FieldStorage()

try:
    person_id = base.cleanCGInumber(form.getvalue("person_id"))
except:
    person_id = form.getvalue('person_id')
    cur.execute('select person_id from People where person_name="%s"' % person_id)
    try:
        person_id = cur.fetchall()[0][0]
    except:
        raise Exception("This user does not exist in the Testing Database.")
        
if form.getvalue("comments"):
    comments = form.getvalue("comments")
else:
    location = form.getvalue("location")
    comments = "Shipped to " + location

try:
    csv_file = form.getvalue('boards')

    serial_numbers = csv_file.decode('utf-8')
    serial_numbers = [line.strip() for line in serial_numbers.splitlines()]

    upload = True
    for i, sn in enumerate(serial_numbers):
        cur.execute('select board_id from Board where full_id="%s"' % sn)
        try:
            board_id = cur.fetchall()[0][0]
        except:
            print('<div class="row">')
            print('<div class="col-md-12 pt-4 ps-5 mx-2 my-2">')
            print("<h3>No board with serial number {}</h3>".format(sn))
            print('</div>')
            print('</div>')
            upload = False
            continue

        board_check_functions.board_checkout(board_id, person_id, comments)

    if upload:
        print('<div class="row">')
        print('<div class="col-md-12 pt-4 ps-5 mx-2 my-2">')
        print('<h3>Boards shipped successfully!</h3>')
        print('</div>')
        print('</div>')

except:

    if form.getvalue("barcode"):
        cur.execute('select board_id from Board where full_id="%s"' % form.getvalue("barcode"))
        board_id = cur.fetchall()[0][0]

        board_check_functions.board_checkout(board_id, person_id, comments)

        print('<div class="row">')
        print('<div class="col-md-12 pt-4 ps-5 mx-2 my-2">')
        print('<h3>Board shipped successfully!</h3>')
        print('</div>')
        print('</div>')

    else:

        print('<div class="row">')
        print('<div class="col-md-12 pt-4 ps-5 mx-2 my-2">')
        print('<h3>Issue getting form, try uploading again </h3>')
        print('</div>')
        print('</div>')


base.bottom()
