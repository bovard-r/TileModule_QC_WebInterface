#!./cgi_runner.sh
import cgi, html
import cgitb
import base
import sys

from connect import connect
from connect import connect_admin

db = connect(0)
cur = db.cursor()

print("content-type: text/html\n\n")

base.header(title='Update Required Tests')
base.top()

form = cgi.FieldStorage()

action = form.getvalue("action")

if action == "submit":

    mt = form.getvalue("major_type")
    test = form.getvalue("test_type")
    password = form.getvalue("password")

    db = connect_admin(password)
    cur = db.cursor()

    cur.execute("select type_id from Board_type where type_sn like '%s'" % (mt + "%"))
    x = cur.fetchall()
    for type_id in x:

        cur.execute(f"select * from Type_test_stitch where type_id={type_id[0]} and test_type_id={test}")
        rows = cur.fetchall()
        if not rows:
            cur.execute("insert into Type_test_stitch (type_id, test_type_id) values (%s, %s)" % (type_id[0], test))
            print('<h4> Test stitched successfully </h4>')

        else:
            print('<h4> Error: Test already added for this board! </h4>')

    db.commit()


else:

    print('<form action="stitch_update.py" method="post" enctype="multipart/form-data">')
    print("<div class='row'>")
    print('<div class = "col-md-6 pt-4 ps-4 mx-2 my-2">')
    print('<h2>Add a required test</h2>')
    print("</div>")
    print("</div>")

    print("<div class='row'>")
    print('<div class="col-md-3 pt-2 ps-5 mx-2 my-2">')
    print('<label>Major Type')
    print('<select class="form-control" name="major_type">')

    print("<option value='TM'>Module</option>")
    print("<option value='TQ'>Protomodule</option>")
    print("<option value='TB'>PCB</option>")
                        
    print('</select>')
    print('</label>')
    print('</div>')
    print("</div>")

    cur.execute("select test_type, name from Test_Type order by relative_order ASC;")
    print('<div class="col-md-3 pt-2 ps-5 mx-2 my-2">')
    print('<label>Test Type')
    print('<select class="form-control" name="test_type">')
    for test_type in cur:
        print('<option value="%s">%s</option>' % (test_type[0], test_type[1]))
    print('</select>')
    print('</label>')
    print('</div>')
    print('</div>')
 
    print("<div class='row'>")
    print('<div class = "col-md-3 pt-2 ps-5 mx-2 my-2">')
    print("<label for='password'>Admin Password</label>")
    print("<input type='password' name='password'>")
    print("</div>")
    print("</div>")

    print("<div class='row'>")
    print('<div class = "col-md-6 pt-2 ps-5 mx-2 my-2">')
    # submits the form on click
    print('<button class="btn btn-dark" type="submit" name="action" value="submit">Stitch Test Type to board type</button>')
    print("</div>")
    print("</div>")
    print("<div class='row pt-4'>")
    print("</div>")
    print("</form>")

base.bottom()
