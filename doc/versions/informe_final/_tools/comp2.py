import zipfile, sys, json
from lxml import etree
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
src,dst,cfg = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
z=zipfile.ZipFile(src); items={n:z.read(n) for n in z.namelist()}; z.close()
root=etree.fromstring(items['word/styles.xml'])
for s in root.iter(W+'style'):
    sid=s.get(W+'styleId')
    nm=s.find(W+'name'); nmv=nm.get(W+'val') if nm is not None else None
    key = sid if sid in cfg else (nmv if nmv in cfg else None)
    if not key: continue
    pPr=s.find(W+'pPr')
    if pPr is None:
        pPr=etree.Element(W+'pPr'); s.insert(0,pPr)
    sp=pPr.find(W+'spacing')
    if sp is None:
        sp=etree.Element(W+'spacing'); pPr.insert(0,sp)
    for k,v in cfg[key].items():
        sp.set(W+k, str(v))
        if k=='line': sp.set(W+'lineRule','exact')
    print('  %-14s %s' % (key, {a.split('}')[1]:b for a,b in sp.attrib.items()}))
items['word/styles.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
zo=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
for n,d in items.items(): zo.writestr(n,d)
zo.close()
