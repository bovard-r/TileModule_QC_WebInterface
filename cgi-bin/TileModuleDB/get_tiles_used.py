#!./cgi_runner.sh
import sys
import connect
from collections import Counter

# Yes CGI is deprecated, but that's how things are
import cgi
import cgitb
import html
import base

tile_config={
    'D8F' : {
        25: (24, 24, 24, 24, 24, 24, 'S4', 'S4'),
        24: (24, 24, 24, 24, 24, 24, 'S4', 'S4'),
        23: (22, 'S4', 22, 22, 'S4', 22, 'S4', 22),
        22: (22, 22, 22, 22, 22, 22, 22, 22),
        21: (20, 20, 20, 20, 20, 20, 20, 20),
        20: (20, 20, 20, 20, 20, 20, 20, 20),
        19: (18, 18, 18, 18, 18, 18, 18, 18),
        18: (18, 'S3', 18, 18, 18, 18, 'S3', 18),
    },
    'B2F' : {
        17: (16, 16, 'S3', 'S3', 16, 16, 16, 16),
        16: (16, 16, 'S3', 'S3', 16, 16, 'S3', 16),
        15: (14, 'S3', 14, 14, 'S3', 14, 14, 14),
        14: (14, 14, 14, 14, 14, 14, 14, 14),
        13: (12, 12, 12, 12, 12, 12, 12, 12),
        12: (12, 12, 12, 12, 12, 12, 12, 12),
        11: (10, 10, 10, 10, 10, 10, 10, 10),
        10: (10, 10, 10, 10, 10, 10, 10, 10),
        9 : (8, 8, 8, 8, 8, 8, 8, 8),
        8 : (8, 8, 8, 8, 8, 8, 8, 8),
        7 : (6, 'S2', 6, 6, 6, 6, 'S2', 6),
        6 : (6, 6, 6, 6, 6, 6, 6, 6)
    },
    'G3F' : {
        36 : (36, 36, 36, 36, 36, 36, 36, 36),
        35 : (34, 'S5', 34, 34, 'S5', 34, 'S5', 34),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    },
    'G3L' : {
        36 : (None, 36, 36, 36, 36, 36, 36, 36),
        35 : (None, 'S5', 34, 34, 'S5', 34, 34, 'S5'),
        34 : (None, 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    },
    'G3R' : {
        36 : (36, 36, 36, 36, 36, 36, 36, None),
        35 : (34, 'S5', 34, 34, 'S5', 34, 'S5',None),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', None)
    },
    'G5F' : {
        38 : (38, 38, 38, 38, 38, 38, 38, 38),
        37 : (36, 'S6', 36, 36, 36, 36, 'S6', 36),
        36 : (36, 36, 36, 36, 36, 36, 36, 36),
        35 : (34, 'S5', 34, 34, 'S5', 34, 34, 'S5'),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    },
    'G5L' : {
        38 : (None, 38, 38, 38, 38, 38, 38, 38),
        37 : (None, 'S6', 36, 36, 36, 36, 'S6', 36),
        36 : (None, 36, 36, 36, 36, 36, 36, 36),
        35 : (34, 'S5', 34, 34, 'S5', 34, 34, 'S5'),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    },
    'G5R' : {
        38 : (38, 38, 38, 38, 38, 38, 38, None),
        37 : (36, 'S6', 36, 36, 36, 36, 'S6', None),
        36 : (36, 36, 36, 36, 36, 36, 36, None),
        35 : (34, 'S5', 34, 34, 'S5', 34, 34, 'S5'),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    },
    'G7F' : {
        40 : (40, 40, 40, 40, 40, 40, 40, 40),
        39 : (38, 'S6', 36, 38, 38, 38, 'S6', 38),
        38 : (38, 38, 38, 38, 38, 38, 38, 38),
        37 : (36, 36, 36, 36, 36, 36, 36, 36),
        36 : (36, 36, 36, 36, 36, 36, 36, 36),
        35 : (34, 'S5', 34, 34, 'S5', 34, 34, 'S5'),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    },
    'G7L' : {
        40 : (None, 40, 40, 40, 40, 40, 40, 40),
        39 : (None, 'S6', 36, 38, 38, 38, 'S6', 38),
        38 : (None, 38, 38, 38, 38, 38, 38, 38),
        37 : (36, 36, 36, 36, 36, 36, 36, 36),
        36 : (36, 36, 36, 36, 36, 36, 36, 36),
        35 : (34, 'S5', 34, 34, 'S5', 34, 34, 'S5'),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    },
    'G7R' : {
        40 : (40, 40, 40, 40, 40, 40, 40, None),
        39 : (38, 'S6', 36, 38, 38, 38, 'S6', None),
        38 : (38, 38, 38, 38, 38, 38, 38, None),
        37 : (36, 36, 36, 36, 36, 36, 36, 36),
        36 : (36, 36, 36, 36, 36, 36, 36, 36),
        35 : (34, 'S5', 34, 34, 'S5', 34, 34, 'S5'),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    },
    'G8F' : {
        41 : (40, 40, 40, 40, 40, 40, 40, 40),
        40 : (40, 40, 40, 40, 40, 40, 40, 40),
        39 : (38, 'S6', 36, 38, 38, 38, 'S6', 38),
        38 : (38, 38, 38, 38, 38, 38, 38, 38),
        37 : (36, 36, 36, 36, 36, 36, 36, 36),
        36 : (36, 36, 36, 36, 36, 36, 36, 36),
        35 : (34, 'S5', 34, 34, 'S5', 34, 34, 'S5'),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    },
    'G8L' : {
        41 : (None, 40, 40, 40, 40, 40, 40, 40),
        40 : (None, 40, 40, 40, 40, 40, 40, 40),
        39 : (38, 'S6', 36, 38, 38, 38, 'S6', 38),
        38 : (38, 38, 38, 38, 38, 38, 38, 38),
        37 : (36, 36, 36, 36, 36, 36, 36, 36),
        36 : (36, 36, 36, 36, 36, 36, 36, 36),
        35 : (34, 'S5', 34, 34, 'S5', 34, 34, 'S5'),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    },
    'G8R' : {
        41 : (40, 40, 40, 40, 40, 40, 40, None),
        40 : (40, 40, 40, 40, 40, 40, 40, None),
        39 : (38, 'S6', 36, 38, 38, 38, 'S6', 38),
        38 : (38, 38, 38, 38, 38, 38, 38, 38),
        37 : (36, 36, 36, 36, 36, 36, 36, 36),
        36 : (36, 36, 36, 36, 36, 36, 36, 36),
        35 : (34, 'S5', 34, 34, 'S5', 34, 34, 'S5'),
        34 : ('S5', 'S5', 'S5', 'S5', 'S5', 'S5', 'S5', 34)
    }
}

def header(of, which):
    print("Content-type: text/html\n")

    base.header("Tile Assignment")

    of.write('''
    <html><head>
    <style>
    td, select {
    text-align: center; font-size: x-large; font-family: sans-serif;
    background-color: #FFFFFF;
    }
    .missing {
    background-color: #111111;
    }
    .submitter {
    font-size: x-large; font-family: sans-serif;
    }
    th, .ring {
    text-align: center; font-size: xx-large; font-family: sans-serif;
    background-color: #1111ff; color: yellow; 
    }
    .stile {
    background-color: yellow;
    }
    </style>
    </head><body>
    ''')
    

def format_id(id):
    return id[0:3]+"-"+id[3:5]+"-"+id[5:9]+"-"+id[9:]

def gather_tile_info(cur):
    query="SELECT COUNT(*), batch, typecode from COMPONENT_STOCK WHERE alt_barcode is NULL AND component_id NOT IN (SELECT component_id from COMPONENT_USAGE) GROUP BY typecode, batch"
    cur.execute(query)
    tileinfo={}
    for row in cur:
        if row[2] not in tileinfo:
            tileinfo[row[2]]={}
        tileinfo[row[2]][row[1]]=int(row[0])
    return tileinfo

def find_qc_tile(cur, barcode):
    query="SELECT alt_barcode FROM COMPONENT_STOCK where barcode='%s'  AND component_id NOT IN (SELECT component_id from COMPONENT_USAGE)"%barcode
    cur.execute(query)
    for row in cur:
        return row[0]
    return None

def pick_tiles(cur, tiletype, batches):
    tiles={}
    for batch in batches:
        query="SELECT barcode FROM COMPONENT_STOCK WHERE typecode='%s' AND batch='%s' AND alt_barcode is NULL AND component_id NOT IN (SELECT component_id from COMPONENT_USAGE) ORDER BY barcode LIMIT %d"%(tiletype,batch[2:],batches[batch])
        cur.execute(query)
        tiles[batch]=[]
        for row in cur:
            tiles[batch].append(row[0])
    return tiles

def make_tile_array(cur,of,tmbc,tbbc,mat):
    base.top()

    tm=tmbc[5:8]

    tileinfo=gather_tile_info(cur)
    if mat=='M':
        ttype='TI'
    else:
        ttype='TC'

    of.write('<h1>Tile Assignment for %s</h1>'%format_id(tmbc))
    
    of.write('<form id="tileform" method="GET" action="get_tiles_used.py">\n')
    of.write('<input type=hidden name="barcode" value="%s">\n'%tmbc)
    of.write('<input type=hidden name="tb_barcode" value="%s">\n'%tbbc)
    of.write('<input type=hidden name="step" value="tile_assignment_verify">\n')
    of.write("<table border=2 width=100%%>\n")

    of.write("<tr><th><th>7<th>6<th>5<th>4<th>3<th>2<th>1<th>0</tr>\n")

    selects=[]
    bc=[]
    width=10.0
    for ring in sorted(tile_config[tm].keys(), reverse=True):        
        of.write("<tr><td class=ring><b>%d</b>"%ring)
        iphi=7
        for tile in tile_config[tm][ring]:
            tilestr=None
            if tile is None:
                of.write("<td width=%.1f%% class=missing>"%width)
                continue
            elif isinstance(tile,str):
                of.write("<td width=%.1f%% class=stile>%s<br>"%(width,tile))
                tilestr=tile
            else:
                of.write("<td width=%.1f%%>%s<br>"%(width,tile))
                tilestr="%02d"%(tile)
            name="tile_%02d_%02d"%(iphi,ring)
            of.write('<select name=%s><option value="QC">QC'%name)
            info=tileinfo['%s-%s'%(ttype,tilestr)]
            maxbatchn=max(info, key=info.get)
            for sb in info:
                of.write('<option value="SB%s" %s>SB%s'%(sb,"selected" if sb==maxbatchn else "",sb))
            of.write('</select>\n')
            selects.append(name)
            name="bc_%02d_%02d"%(iphi,ring)            
            of.write("<br><input type='text' size=15 name=%s id=%s>\n"%(name,name))
            bc.append(name)
            iphi=iphi-1
        width=width-0.5
        of.write("<td width=5%%><div width=%.1f%% bgcolor=#ffffff> </div></tr>\n"%(width))

    of.write("</table>\n")
    of.write("<p>\n<center><input class=submitter type=submit value='Submit Tile Assignment'></center>\n")
    of.write("</form>\n")
    of.write("<script>\n")
    of.write('''
    function show(el, state) {
	if (state === undefined) {
		state = true;
	}
    if (state === true) {
		el.style.display = '';
    } else {
        el.style.display = 'none';
    }
}
function enableIfSelected() {
    var select = this,
    optionValue = select.options[select.selectedIndex].value,
    el;
    const bcname="bc"+this.name.slice(4,5+5);
    el=document.getElementById(bcname);
    show(el, ("QC" === optionValue));
 }
function attachEnableIfSelected(select) {
	select.onchange = enableIfSelected;
	select.onchange();
}''')
    of.write("var form=document.getElementById('tileform');\n")
    for i in range(0,len(selects)):
        of.write("attachEnableIfSelected(form.elements.%s);\n"%(selects[i]))
    of.write("</script>\n")

    base.bottom()

def check_pcb(cur,pcb_bc,qbc):
    # check that the PCB BC exists
    cur.execute("SELECT EXISTS(SELECT 1 FROM Board WHERE full_id='%s')"%(pcb_bc))
    if cur.fetchone()[0]==0:
        return (404,"Tile PCB %s does not exist!"%pcb_bc)
    # check that qbc does not exist
    cur.execute("SELECT EXISTS(SELECT 1 FROM Board WHERE full_id='%s')"%(qbc))
    if cur.fetchone()[0]==1:
        return (403,"Protomodule %s already exists!"%qbc)
    # check that the PCB BC is not used for anything else
    cur.execute("SELECT EXISTS(SELECT 1 FROM COMPONENT_STOCK INNER JOIN COMPONENT_USAGE on COMPONENT_STOCK.component_id=COMPONENT_USAGE.component_id where barcode='%s' )"%(pcb_bc))
    if cur.fetchone()[0]==1:
        return (403,"PCB %s already used for another protomodule already exists!"%pcb_bc)
    # check that the PCB has passed QC Tests
    cur.execute('''
        select board_id
        from Board
        where full_id="%s"
    ''' % pcb_bc)
    board_id = cur.fetchall()[0][0]

    cur.execute('''
        select T.board_id, T.test_type_id, T.successful
        from Test T
        join (
            select board_id, test_type_id, MAX(test_id) as latest_test_id
            from Test
            group by board_id, test_type_id
        ) latest on T.test_id = latest.latest_test_id
        where T.board_id=%s
    ''' % board_id)

    test_results = {}
    for board_id, test_type_id, successful in cur.fetchall():
        test_results.setdefault(board_id, {})[test_type_id] = successful

    cur.execute('''
        select BT.type_sn, TT.test_type, TT.name
        from Type_test_stitch TTS
        join Test_Type TT on TTS.test_type_id = TT.test_type
        join Board_type BT on BT.type_id = TTS.type_id
    ''')
    stitch_types_by_subtype = {}
    for type_id, test_type_id, test_name in cur.fetchall():
        stitch_types_by_subtype.setdefault(type_id, []).append((test_type_id, test_name))

    stitch_types = stitch_types_by_subtype.get(pcb_bc[3:8], [])

    failed = {}
    outcomes = {}
    for test_type_id, test_name in stitch_types:
        result = test_results.get(board_id, {}).get(test_type_id)
        outcomes[test_name] = result == 1 or result == '1'
        failed[test_name] = result == 0

    num_tests_passed = sum(outcomes.values())
    num_tests_req = len(outcomes)
    num_tests_failed = sum(failed.values())

    if num_tests_passed != num_tests_req:
        return (403,"PCB has not passed the required QC tests!")

    return None
    
def verify_selection(cur, of, info):
    base.top()
    byring={}
    bytile={}
    assigned={}
    tm=info.getvalue("barcode")[5:8]
    if info.getvalue("barcode")[8]=='C':
        pref="TC-"
    else:
        pref="TI-" # needs work!!!!
    mymemory={}
    for name in info.keys():
        value=info.getvalue(name)
        if name[:4]!='tile': continue
        iphi=int(name[5:7])
        ring=int(name[8:10])
        if ring not in byring:
            byring[ring]=[None]*8
        byring[ring][iphi]=value
        tiletype=tile_config[tm][ring][iphi]
        if tiletype not in bytile:
            bytile[tiletype]=Counter()
        if value=='QC':
            sb_tile=find_qc_tile(cur,info.getvalue("bc_%02d_%02d"%(iphi,ring)))
            if sb_tile is None:
                of.write("<h1>Unable to find tile with barcode '%s' for %s,%s</h1>"%(info.getvalue("bc_%02d_%02d"%(iphi,ring)),ring,iphi))
                return
            mymemory['tile_%02d_%02d'%(iphi,ring)]=sb_tile
        else:
            bytile[tiletype][value]+=1

    for tiletype in bytile:
        if isinstance(tiletype,str):
            tiletypestr=tiletype
        else:
            tiletypestr="%02d"%(tiletype)
        assigned[tiletype]=pick_tiles(cur, pref+tiletypestr, bytile[tiletype])
    
    of.write("<table><tr><th>Ring<th>IPhi<th>Batch<th>Barcode</tr>")
    for ring in sorted(byring.keys()):
        for iphi in range(0,8):
            if byring[ring][iphi] is not None:
                barcode=""
                tiletype=tile_config[tm][ring][iphi]
                if tiletype is None:
                    continue
                byr=byring[ring][iphi]
                if byr=='QC':
                    barcode=mymemory['tile_%02d_%02d'%(iphi,ring)]
                else:
                    if len(assigned[tiletype][byr])==0:
                        print("Ran out of %s at %d,%d!<br>"%(tiletype,iphi,ring))
                        continue
                    barcode=assigned[tiletype][byr][0]
                    mymemory['tile_%02d_%02d'%(iphi,ring)]=barcode
                    del assigned[tiletype][byr][0]
                                                                  
                of.write("<tr><td>%s<td>%d<td>%s<td>%s</tr>\n"%(ring,iphi,byring[ring][iphi],barcode))
    of.write("</table>")
    of.write('<form id="tileform" method="GET" action="get_tiles_used.py">\n')
    of.write('<input type=hidden name="barcode" value="%s">\n'%info.getvalue("barcode"))
    of.write('<input type=hidden name="tb_barcode" value="%s">\n'%info.getvalue("tb_barcode"))
    of.write('<input type=hidden name="step" value="tile_assignment_commit">\n')
    for (item,value) in mymemory.items():
        of.write('<input type=hidden name="%s" value="%s">\n'%(item,value))
    of.write("<p>\n<center><input class=submitter type=submit value='Commit Tile Assignment'></center></form>\n")
    base.bottom()

def commit_selection(db, of, info):
    cur=db.cursor()
    making=info.getvalue("barcode")
    make_from=info.getvalue("tb_barcode")

    # insert the protomodule as a board
    cur.execute("INSERT INTO Board (sn,full_id,type_id,location,manufacturer_id) VALUES ('%s','%s','%s','Fermilab',(SELECT manufacturer_id FROM Manufacturers WHERE name='Fermilab'))"%(making[10:],making,making[3:9]))
    # register the protomodule as a component...
    cur.execute("INSERT INTO COMPONENT_STOCK (barcode,typecode) VALUES ('%s','%s')"%(making,making[3:9]))
    db.commit()
    cur.execute("SELECT board_id from Board where full_id='%s'"%making)
    board_id=int(cur.fetchone()[0])
    cur.fetchall()

    # link tileboard to protomodule
    cur.execute("INSERT INTO COMPONENT_USAGE (component_id, used_in, used_in_barcode) VALUES ((SELECT component_id from COMPONENT_STOCK where barcode='%s'),%d,'%s')"%(make_from,board_id,making))
    
    for item in info.keys():
        if item[:4]!='tile':
            continue
        iphi=int(item[5:7])
        ring=int(item[8:10])
        # fancy insert didn't work
        #        query='INSERT INTO COMPONENT_USAGE (component_id, used_in_barcode, used_iphi, used_ring) VALUES ( (SELECT component_id FROM COMPONENT_STOCK WHERE barcode="%s"),"%s",%d,%d)'%(info.getvalue(item),making,iphi,ring)
        query='SELECT component_id FROM COMPONENT_STOCK WHERE barcode="%s" OR alt_barcode="%s"'%(info.getvalue(item),info.getvalue(item),)
        cur.execute(query)
        id=None
        for row in cur:
            id=int(row[0])
        if id is None:
            of.write("Problem with %d %d -> %s"%(iphi,ring,info.getvalue(item)))
            continue
                     
        query='INSERT INTO COMPONENT_USAGE (component_id, used_in_barcode, used_iphi, used_ring, used_in) VALUES (%d,"%s",%d,%d,%d)'%(id,making,iphi,ring,board_id)            
        cur.execute(query)
    db.commit()
    print("Refresh: 0; url=module.py?full_id=%s\n\n"%(making))

def do_test(bc):
    print("Refresh: 0; url=home_page.py\n\n")

    
def write_xml(of, cur, tbm):

    cur.execute('SELECT name,kind_of_part from Board_type where type_sn=(SELECT type_id from Board where full_id="%s")'%tbm)
    (basename,kop)=cur.fetchone()

    cur.execute('SELECT used_when from COMPONENT_USAGE WHERE used_in_barcode="%s" and used_ring is NULL'%tbm)
    (when)=cur.fetchone()[0]
    
    of.write('  <PART>\n')
    of.write('    <KIND_OF_PART>%s</KIND_OF_PART>\n'%(kop))
    of.write('    <BARCODE>%s</BARCODE>\n'%tbm)
    of.write('    <SERIAL_NUMBER>%s</SERIAL_NUMBER>\n'%tbm)
    of.write('    <LOCATION>FNAL Lab 5 and 6</LOCATION>\n')
    of.write('    <INSTITUTION>Fermi National Accelerator Lab.</INSTITUTION>\n')
    of.write('    <MANUFACTURER>FNAL</MANUFACTURER>\n')
    of.write('    <NAME_LABEL>%s %s</NAME_LABEL>\n'%(basename,tbm))
    of.write('    <PRODUCTION_DATE>%s</PRODUCTION_DATE>\n'%(when.strftime("%Y-%m-%d")))
    batch=tbm[11]
    of.write('    <BATCH_NUMBER>%s</BATCH_NUMBER>\n'%batch)
    of.write('    <CHILDREN>\n')

    query="SELECT COMPONENT_STOCK.barcode, COMPONENT_USAGE.used_iphi, COMPONENT_USAGE.used_ring, COMPONENT_STOCK.alt_barcode FROM COMPONENT_STOCK INNER JOIN COMPONENT_USAGE ON COMPONENT_STOCK.component_id=COMPONENT_USAGE.component_id WHERE COMPONENT_USAGE.used_in_barcode='%s'"%tbm
#    of.write(query)
    cur.execute(query)
    rows=cur.fetchall()
#    of.write(str(len(rows)))
    for (bc,iphi,ring,abc) in rows:
        if abc is not None:
            bc=abc
#        of.write(bc)
        if bc[3:5] not in ('TI','TC','TB'):
            continue
        of.write('      <PART>\n')
        #320TIS5SBN01177 320TI40SBN01859
        if bc[3:5]=='TB':
            cur.execute('SELECT kind_of_part from Board_type where type_sn=(SELECT type_id from Board where full_id="%s")'%bc)
            (kop,)=cur.fetchone()            
        else:
            kop='Super-batched Wrapped '
            if bc[3:5]=='TI':
                kop+='Molded Tile '
            else:
                kop+='Cast Tile '
            if bc[5]=='S':
                kop+='Special %s'%bc[6]
            else:
                kop+='BH Ring%02d'%int(bc[5:7])
        of.write('        <KIND_OF_PART>%s</KIND_OF_PART>\n'%kop)
        of.write('        <SERIAL_NUMBER>%s</SERIAL_NUMBER>\n'%bc)
        if bc[3:5]!='TB':
            of.write('        <PREDEFINED_ATTRIBUTES>\n')
            of.write('          <ATTRIBUTE><NAME>iring</NAME><VALUE>%d</VALUE></ATTRIBUTE>\n'%ring)
            of.write('          <ATTRIBUTE><NAME>iphi_local</NAME><VALUE>%d</VALUE></ATTRIBUTE>\n'%iphi)
            of.write('        </PREDEFINED_ATTRIBUTES>\n')
        of.write('      </PART>\n')
    of.write('    </CHILDREN>\n')
    of.write('  </PART>\n')

db=connect.connect(0)
cur=db.cursor()
form=cgi.FieldStorage()

step=form.getvalue('step','start')

if step=='get-xml':
    module=form.getvalue('barcode')
    
    print("Content-type: text/xml")
    print('Content-Disposition: attachment; filename="%s.xml"\n'%module)

    print("<ROOT>\n<PARTS>")
    write_xml(sys.stdout, cur, module)
    print("</PARTS>\n</ROOT>")

if step=='tile_assignment':
    pcb_bc=form.getvalue('pcb_barcode')
    qbc="320TQ"+pcb_bc[5:8]+form.getvalue('mat')+pcb_bc[8]+pcb_bc[10:15]
    retval=check_pcb(cur,pcb_bc,qbc)
    if retval is not None:
        if retval[0]==404:
            print("Status: 404 Not Found\n\n")
        elif retval[0]==403:
            print("Status: 403 Forbidden\n\n")
        print("<h1>%s</h1>"%retval[1])
        exit(1)
    header(sys.stdout, form.getvalue('step'))
    make_tile_array(cur, sys.stdout,qbc, pcb_bc, form.getvalue('mat'))
elif step=='tile_assignment_verify':
    header(sys.stdout, form.getvalue('step'))
    verify_selection(cur, sys.stdout,form)
elif step=='test':
    do_test(form.getvalue('barcode'))
elif step=='tile_assignment_commit':
#    print("Content-type: text/html\n")
#    cgitb.enable()
    db=connect.connect(1)
#    header(sys.stdout, form.getvalue('step'))
    commit_selection(db,sys.stdout,form)

