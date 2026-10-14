"""Source-preserving table normalization for the small biology comparison.

Only typography is canonicalized. Values are not rounded or corrected. Merged
cells, physical line breaks, and superscript/subscript semantics are retained.
The score aligns source row labels and column positions; it is not an OCR
benchmark or a scientific-validation score.
"""
import re
import unicodedata
from itertools import permutations
from collections import OrderedDict
from lxml import etree, html


def semantic_text(node):
    pieces=[node.text or '']
    for child in node:
        tag=etree.QName(child).localname.lower() if isinstance(child.tag,str) else ''
        content=semantic_text(child)
        if tag in ['br','break']:
            pieces.append('\n')
        elif tag=='sup':
            pieces.append('^('+content.strip()+')')
        elif tag=='sub':
            pieces.append('_('+content.strip()+')')
        else:
            pieces.append(content)
        pieces.append(child.tail or '')
    return ''.join(pieces)


def canonical(text,keep_powers=False):
    """Conservative typography normalization; preserve signs and decimals."""
    text=unicodedata.normalize('NFC',text or '').replace('\u00ad','').replace('℃','°C')
    for delimiter in ['\\(','\\)','\\[','\\]']:
        text=text.replace(delimiter,'')
    text=text.translate(str.maketrans({'−':'-','–':'-','—':'-','‑':'-',
        'μ':'µ','ϒ':'γ','Ω':'Ω'}))
    greek={'alpha':'α','beta':'β','gamma':'γ','Delta':'Δ','delta':'δ',
           'mu':'µ','theta':'θ','sigma':'σ'}
    for name,char in greek.items():
        text=re.sub(r'\\'+name+r'\b',char,text)
    text=text.replace('\\pm','±').replace('\\times','×').replace('\\cdot','·')
    text=text.replace('^{\\circ}','°').replace('^\\circ','°')
    text=re.sub(r'\\(?:mathrm|mathit|text|textrm|operatorname|mathbf|textbf)\s*\{([^{}]*)\}',r'\1',text)
    text=re.sub(r'\\(?:mathrm|mathit|text|textrm|operatorname|mathbf|textbf)\s*','',text)
    text=re.sub(r'\\(?:left|right|displaystyle)\b','',text)
    text=re.sub(r'\\[,;! ]','',text)
    text=text.replace('\\%','%').replace('\\_','_').replace('\\#','#').replace('\\&','&')
    # Unicode superscripts remain distinguishable from ordinary digits.
    supers='⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻'
    plain='0123456789+-'
    text=re.sub('['+supers+']+',lambda m:'^('+m[0].translate(str.maketrans(supers,plain))+')',text)
    text=re.sub(r'\^\{([^{}]+)\}',r'^(\1)',text)
    text=re.sub(r'_\{([^{}]+)\}',r'_(\1)',text)
    # Flatten redundant TeX font/group braces; the ^ and _ operators remain.
    text=text.replace('{','').replace('}','')
    text=re.sub(r'\^([+-]?[0-9]+)',r'^(\1)',text)
    text=re.sub(r'\^([a-z])(?=[^a-z]|$)',r'^(\1)',text)
    text=re.sub(r'_\(([^()]*)\)',r'\1',text)
    text=re.sub(r'_([A-Za-z0-9])',r'\1',text)
    text=text.replace('$','')
    text=re.sub(r'\s+','',text).casefold()
    if not keep_powers:
        # Body-cell footnote markers retain their letters, without markup.
        text=re.sub(r'\^\(([a-z])\)',r'\1',text)
        text=re.sub(r'^n\.d\.?([a-z]?)$',r'nd\1',text)
    return text


def parse_table(markup):
    try:
        root=etree.fromstring(markup.encode(),etree.XMLParser(resolve_entities=False,no_network=True))
    except etree.XMLSyntaxError:
        root=html.fromstring(markup.replace('<break/>','<br/>'))
    if root.tag.lower()!='table':
        tables=root.xpath('.//table')
        if not tables:
            raise ValueError('no HTML table')
        root=tables[0]
    rows=root.xpath('.//tr')[:150]
    occupied={}; header_rows=0
    for ri,row in enumerate(rows):
        if row.getparent().tag.lower()=='thead':
            header_rows=ri+1
        ci=0
        for cell in row:
            if not isinstance(cell.tag,str) or cell.tag.lower() not in ['td','th']:
                continue
            while (ri,ci) in occupied:
                ci+=1
            rs=max(1,min(150,int(cell.get('rowspan','1'))))
            cs=max(1,min(50,int(cell.get('colspan','1'))))
            if ci+cs>50:
                raise ValueError('implausible column count')
            text=semantic_text(cell)
            lines=[re.sub(r'[ \t\r]+',' ',s).strip() for s in text.split('\n') if s.strip()]
            record=dict(text='\n'.join(lines),lines=lines,origin_row=ri,
                origin_column=ci,rowspan=rs,colspan=cs,header=cell.tag.lower()=='th')
            for dr in range(rs):
                for dc in range(cs):
                    occupied[(ri+dr,ci+dc)]=record
            ci+=cs
    nr=max((r for r,c in occupied),default=-1)+1
    nc=max((c for r,c in occupied),default=-1)+1
    matrix=[[occupied.get((r,c),dict(text='',lines=[],header=False,origin_row=r,
        origin_column=c,rowspan=1,colspan=1)) for c in range(nc)] for r in range(nr)]
    if not header_rows:
        for row in matrix:
            origins={(c['origin_row'],c['origin_column']) for c in row}
            if header_rows and len(origins)==1 and row[0].get('colspan',1)==nc:
                # A full-width th after column headers is a body group heading.
                break
            if row and all(c['header'] for c in row):
                header_rows+=1
            else:
                break
    return dict(rows=matrix,nrows=nr,ncols=nc,header_rows=header_rows)


def table_records(grid,source_headers=None,source_keys=None):
    """Collapse split physical rows to their original labeled logical cells.

    A full-width group row supplies context (e.g. L1/L2/L3), not data values.
    Repeated strings from the same rowspan origin are counted only once.
    With source_keys, generated HTML headers may use td rather than th; their
    leading rows are recognized by source labels, never by expected values.
    """
    start=grid['header_rows']
    if source_keys and not start:
        labels={canonical(part) for k in source_keys for part in k.split('|')}
        for i,row in enumerate(grid['rows']):
            if row and canonical(row[0]['text']) in labels:
                start=i;break
    headers=[]
    for ci in range(grid['ncols']):
        parts=[]
        for row in grid['rows'][:start]:
            text=row[ci]['text']
            if text and text not in parts:
                parts.append(text)
        headers.append(' / '.join(parts))
    records=OrderedDict();group='';previous=''
    seen={}
    for ri,row in enumerate(grid['rows'][start:],start):
        if not row:
            continue
        first=row[0]
        nonempty=[c for c in row if c['text']]
        origins={(c.get('origin_row'),c.get('origin_column')) for c in nonempty}
        # Equivalent markup may place an empty stub before a group heading.
        if nonempty and len(origins)==1 and nonempty[0].get('colspan',1)>=grid['ncols']-1:
            group=nonempty[0]['text'];previous='';continue
        label=first['text'] or previous
        if not label:
            continue
        previous=label
        key=(group+'|' if group else '')+label
        # Rows under a merged L1 label remain one logical source row.
        ck=canonical(key)
        if ck not in records:
            records[ck]=dict(key=key,row_indices=[],cells=['']*(grid['ncols']-1),
                cell_origins=[[] for _ in range(grid['ncols']-1)])
            seen[ck]=[set() for _ in range(grid['ncols']-1)]
        record=records[ck];record['row_indices'].append(ri)
        for ci,cell in enumerate(row[1:]):
            origin=(cell.get('origin_row',ri),cell.get('origin_column',ci+1))
            if origin in seen[ck][ci]:
                continue
            seen[ck][ci].add(origin)
            if cell['text']:
                record['cells'][ci]+=('\n' if record['cells'][ci] else '')+cell['text']
                record['cell_origins'][ci].append(dict(row=origin[0],column=origin[1]))
    return dict(headers=headers,header_rows=start,records=list(records.values()),ncols=grid['ncols'])


def compare(source,predicted_markup):
    gold=source['logical_table']
    total=sum(len(row['cells']) for row in gold['records'])
    try:
        grid=parse_table(predicted_markup)
        pred=table_records(grid,source_headers=gold['headers'],
            source_keys=[r['key'] for r in gold['records']])
    except Exception as e:
        return dict(matched=0,total=total,error=type(e).__name__+': '+str(e))
    by_key={canonical(r['key']):r for r in pred['records']}
    checks=[]
    for row in gold['records']:
        got=by_key.get(canonical(row['key']))
        for ci,value in enumerate(row['cells']):
            actual=got['cells'][ci] if got and ci<len(got['cells']) else None
            # Column position is fixed. A missing/extra column fails the match.
            ok=pred['ncols']==gold['ncols'] and actual is not None and canonical(actual)==canonical(value)
            checks.append(dict(row_key=row['key'],column=ci+1,header=gold['headers'][ci+1],
                expected=value,actual=actual,matched=ok))
    header_checks=[]
    for ci,value in enumerate(gold['headers']):
        if not value:
            continue
        actual=pred['headers'][ci] if ci<len(pred['headers']) else ''
        def leaf_header(text):
            pieces=text.split(' / ')
            # Keep quantity/unit-bearing parent headers (e.g. IC50 (nM)
            # over two construct columns); discard only plain category names.
            relevant=[part for part in pieces[:-1] if re.search(r'\([^)]*\)|[_^]',part) or canonical(part).startswith('logk')]
            result=set()
            for parts in permutations((relevant+[pieces[-1]])[:4]):
                leaf=canonical(' '.join(parts),True)
                leaf=re.sub(r'\^\(([a-z])\)',r'\1',leaf)
                leaf=re.sub(r'\^\(([+-]?\d+)\)',r'POWER[\1]',leaf)
                result.add(leaf.replace('(','').replace(')',''))
            return result
        def units(text):
            # Unit symbols are case-sensitive: nM and nm are different units.
            return set(re.findall(r'(?<![A-Za-z_])(?:[pµuμnm]?M|MBq|nmol|mol|kDa|Da|kJ|J|K|s|dm)(?![A-Za-z_])',text))
        header_checks.append(dict(column=ci,expected=value,actual=actual,
            matched=canonical(value,True)==canonical(actual,True),
            semantic_leaf_matched=bool(leaf_header(value)&leaf_header(actual)) and units(value)==units(actual)))
    header_ok={h['column']:h['semantic_leaf_matched'] for h in header_checks}
    for cell in checks:
        cell['quantity_and_value_matched']=cell['matched'] and header_ok.get(cell['column'],False)
    return dict(matched=sum(c['matched'] for c in checks),total=total,cells=checks,
        header_matched=sum(c['matched'] for c in header_checks),header_total=len(header_checks),
        header_checks=header_checks,quantity_and_value_matched=sum(c['quantity_and_value_matched'] for c in checks),
        predicted_ncols=pred['ncols'],source_ncols=gold['ncols'],
        predicted_rows=len(pred['records']),source_rows=len(gold['records']))
