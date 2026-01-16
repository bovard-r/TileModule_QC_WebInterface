#!./cgi_runner.sh

import cgi, html
import base
import add_test_functions
import os
from connect import connect

form = cgi.FieldStorage()
db = connect(0)
cur = db.cursor()

if form.getvalue("typecode"):
    typecode = form.getvalue("typecode")
    if form.getvalue("batch"):
        batch = form.getvalue("batch")
        print('Content-Type: text/plain')
        print('Content-Disposition: attachment; filename=%s-%s_available.csv' % (typecode, batch))
        print()
        cur.execute('SELECT barcode FROM COMPONENT_STOCK WHERE typecode="%s" AND batch="%s" AND component_id NOT IN (SELECT component_id from COMPONENT_USAGE) ORDER BY barcode' % (typecode, batch))
        for barcode in cur.fetchall():
            print(f"{barcode[0]},")
    else:
        print('Content-Type: text/plain')
        print('Content-Disposition: attachment; filename=%s_available.csv' % typecode)
        print()
        cur.execute('SELECT barcode FROM COMPONENT_STOCK WHERE typecode="%s" AND component_id NOT IN (SELECT component_id from COMPONENT_USAGE) ORDER BY barcode' % typecode)
        for barcode in cur.fetchall():
            print(f"{barcode[0]},")

elif form.getvalue("tc"):

    print("Content-type: text/html\n")

    base.header(title='Components List')
    base.top()

    typecode = form.getvalue("tc")

    print("<div class='row'>")
    print('<div class = "col-md-6 pt-4 ps-4 mx-2 my-2">')
    print('<h2>%s</h2>' % typecode)
    print("</div>")
    print("</div>")

    print('<div class="col-md-11 mx-4 my-4"><table class="table table-bordered table-hover table-active">')
    print('<tr><th>Batch<th># Known<th># Available</tr>')

    cur.execute('select distinct batch from COMPONENT_STOCK where typecode="%s" ORDER BY batch' % typecode)
    for batch in cur.fetchall():
        cur.execute(f'select COUNT(component_id) from COMPONENT_STOCK where typecode="{typecode}" and batch="{batch[0]}"')
        total = cur.fetchall()[0][0]

        cur.execute(f'SELECT COUNT(barcode) from COMPONENT_STOCK WHERE typecode="{typecode}" and batch="{batch[0]}" AND component_id NOT IN (SELECT component_id from COMPONENT_USAGE)')
        available = cur.fetchall()[0][0]

        print(f'<tr><td><a href="list_components.py?typecode={typecode}&batch={batch[0]}">{batch[0]}</a></td><td>{total}</td><td>{available}</td></tr>')

    print("</table></div>")

    base.bottom()

else:

    print("Content-type: text/html\n")

    base.header(title='Components List')
    base.top()

    print("<div class='row'>")
    print('<div class = "col-md-6 pt-4 ps-4 mx-2 my-2">')
    print('<h2>Components List</h2>')
    print("</div>")
    print("</div>")

    print('<div class="col-md-11 mx-4 my-4"><table class="table table-bordered table-hover table-active">')
    print('<tr><th>Typecode<th># Known<th># Available<th></tr>')

    cur.execute('select distinct typecode from COMPONENT_STOCK ORDER BY typecode')
    for _type in cur.fetchall():
        cur.execute('select COUNT(component_id) from COMPONENT_STOCK where typecode="%s"' % _type)
        total = cur.fetchall()[0][0]

        cur.execute('SELECT COUNT(barcode) from COMPONENT_STOCK WHERE typecode="%s" AND component_id NOT IN (SELECT component_id from COMPONENT_USAGE)' %_type)
        available = cur.fetchall()[0][0]

        if "TB" in _type[0]:
            print(f'<tr><td><a href="list_components.py?typecode={_type[0]}">{_type[0]}</a></td><td>{total}</td><td>{available}</td><td></td></tr>')
        else:
            print(f'<tr><td><a href="list_components.py?typecode={_type[0]}">{_type[0]}</a></td><td>{total}</td><td>{available}</td><td><a href="list_components.py?tc={_type[0]}">View Batch info</a></td></tr>')

    print("</table></div>")

    base.bottom()
