#!./cgi_runner.sh

import cgi, html
import cgitb
cgitb.enable()

import base
from connect import connect
import settings
import os.path
import sys
import json

# >>> ADDED
import io
import zipfile

db=connect(0)
cur=db.cursor()

# >>> ADDED
def _safe_filename(name, default_name="attachment.json"):
    if not name:
        return default_name
    name = os.path.basename(name)
    if not name.strip():
        return default_name
    return name


# >>> ADDED
def _make_zip_bytes(filename, content_bytes):
    memfile = io.BytesIO()
    with zipfile.ZipFile(memfile, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, content_bytes)
    return memfile.getvalue()

def _write_binary(data):
    try:
        sys.stdout.flush()
    except:
        pass

    try:
        sys.stdout.buffer.write(data)   # Python 3
        sys.stdout.buffer.flush()
    except AttributeError:
        sys.stdout.write(data)          # Python 2


def _send_zip(zip_name, zip_bytes):
    sys.stdout.write("Content-Type: application/zip\r\n")
    sys.stdout.write('Content-Disposition: attachment; filename="%s"\r\n' % zip_name)
    sys.stdout.write("Content-Length: %d\r\n" % len(zip_bytes))
    sys.stdout.write("\r\n")
    _write_binary(zip_bytes)


if __name__ == "__main__": 
    form = cgi.FieldStorage()
    attach_id = base.cleanCGInumber(form.getvalue('attach_id'))

    # >>> ADDED
    zip_requested = form.getvalue('zip')

    # gets attachment data from DB
    if(attach_id != 0):
        cur.execute("SELECT test_id, attachmime, originalname, attach FROM Attachments WHERE attach_id=%d" % (attach_id));

    # checks to make sure there is attachment data received
    if not cur.with_rows:
        print("Content-type: text/html\n")
        base.header("Attachment Request Error")
        base.top()
        print('<div class="col-md-6 ps-4 pt-4 mx-2 my-2">')
        print("<h1>Attachment not available</h1>")
        print('</div>')
        base.bottom()
    else:    
        thevals=cur.fetchall()
        # grabs attached data
        f = thevals[0][3]
        # checks if there is an attachment
        # >>> ADDED
        originalname = _safe_filename(thevals[0][2])

        if not f:
            print("Content-type: text/html\n")
            base.header("Attachment Request Error")
            base.top(True)
            print("<h1>Attachment not found</h1>")
            base.bottom()        
        else:
            # decodes the attachment and displays it
            try:
                # >>> ADDED: optional zip output, original behavior kept otherwise
                if zip_requested:
                    pretty_json = json.dumps(json.loads(f.decode("utf-8")), indent=1).encode("utf-8")

                    if not originalname.lower().endswith(".json"):
                        originalname += ".json"

                    zip_bytes = _make_zip_bytes(originalname, pretty_json)
                    zip_name = os.path.splitext(originalname)[0] + ".zip"

                    # >>> CHANGED: write headers cleanly, then flush
                    sys.stdout.write("Content-Type: application/zip\r\n")
                    sys.stdout.write('Content-Disposition: attachment; filename="%s"\r\n' % zip_name)
                    sys.stdout.write("Content-Length: %d\r\n" % len(zip_bytes))
                    sys.stdout.write("\r\n")

                    # >>> ADDED: flush before writing binary
                    sys.stdout.flush()

                    # >>> CHANGED: always write binary safely
                    sys.stdout.buffer.write(zip_bytes)
                    sys.stdout.buffer.flush()

                    cur.close()
                    sys.exit(0)
                
                else:
                    print('Content-type: %s \n\n' % (thevals[0][1]))
                    print(json.dumps(json.loads(f.decode("utf-8")), indent=1))
            
            except json.decoder.JSONDecodeError:
                print("Content-type: text/html\n")
                base.header("Attachment Request Error")
                base.top()
                print('<div class="col-md-6 ps-4 pt-4 mx-2 my-2">')
                print('Error: Test data length exceeds 65535 characters.')
                print('</div>')
                base.bottom()
            except Exception as e:
                print("Content-type: text/html\n")
                print("<html><body>")
                print("<h1>ZIP Debug Error</h1>")
                print("<pre>%s</pre>" % html.escape(str(e)))
                print("</body></html>")           
        
    cur.close()

def run(attach_id):
    # gets attachment data from DB
    if(attach_id != 0):
        cur.execute("SELECT test_id, attachmime, originalname, attach FROM Attachments WHERE attach_id=%d" % (attach_id));

    # checks to make sure there is attachment data received
    if not cur.with_rows:
        print('<!doctype html>')
        print('<html lang="en">')
        print('<head>')
        print('<title> Attachment not available </title>')
        print('</head>')
        print('<body>')
        print("<h1>Attachment not available</h1>")
        print('</body>')
        print('</html>')
    else:    
        thevals=cur.fetchall()
        # grabs attached data
        f = thevals[0][3]
        # checks if there is an attachment
        if not f:
            print('<!doctype html>')
            print('<html lang="en">')
            print('<head>')
            print('<title> Attachment Request Error </title>')
            print('</head>')
            print('<body>')
            print("<h1>Attachment not found</h1>")
            print('</body>')
            print('</html>')
        else:
            print('<!doctype html>')
            print('<html lang="en">')
            print('<head>')
            print('<title> Attachment </title>')
            print('</head>')
            print('<body>')
            print('<pre>')
            print(json.dumps(json.loads(f.decode("utf-8")), indent=1))
            print('</pre>')
            print('</body>')
            print('</html>')

# writes a file for the attachment
def save(attach_id, as_zip=False):
    db=connect(0)
    cur=db.cursor()

    cur.execute("SELECT test_id, attachmime, originalname FROM Attachments WHERE attach_id=%d" % (attach_id));

    if not cur.with_rows:
        print("<h1>Attachment not available</h1>")
    else:    
        thevals=cur.fetchall();
        attpath=settings.getAttachmentPathFor(thevals[0][0],attach_id)
        if not os.path.isfile(attpath):
            print("<h1>Attachment not found</h1>")
        else:
            # >>> CHANGED: use open(...) instead of file(...)
            with open(attpath, "rb") as infile:
                file_bytes = infile.read()

            # >>> ADDED: optional zip output, original raw output preserved
            if as_zip:
                originalname = _safe_filename(thevals[0][2])
                zip_bytes = _make_zip_bytes(originalname, file_bytes)
                zip_name = os.path.splitext(originalname)[0] + ".zip"

                sys.stdout.write("Content-type: application/zip\r\n")
                sys.stdout.write('Content-Disposition: attachment; filename="%s"\r\n' % zip_name)
                sys.stdout.write("Content-Length: %d\r\n\r\n" % len(zip_bytes))

                if hasattr(sys.stdout, "buffer"):
                    sys.stdout.buffer.write(zip_bytes)
                else:
                    sys.stdout.write(zip_bytes)
            else:
                # ORIGINAL FUNCTIONALITY
                sys.stdout.write(file_bytes)





# def save(attach_id):
#     db=connect(0)
#     cur=db.cursor()

#     cur.execute("SELECT test_id, attachmime, originalname FROM Attachments WHERE attach_id=%d" % (attach_id));

#     if not cur.with_rows:
#         print("<h1>Attachment not available</h1>")
#     else:    
#         thevals=cur.fetchall();
#         attpath=settings.getAttachmentPathFor(thevals[0][0],attach_id)
#         if not os.path.isfile(attpath):
#             print("<h1>Attachment not found</h1>")
#         else:
#             statinfo = os.stat(attpath)
#             sys.stdout.write(file(attpath,"rb").read() )
    cur.close()

