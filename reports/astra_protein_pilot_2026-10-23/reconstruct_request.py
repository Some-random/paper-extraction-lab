"""Restore the omitted correction reference locally. Makes no model/API-generation call."""
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT=Path(__file__).resolve().parent

def reconstruct():
    request=json.loads((ROOT/'generation_request.public.json').read_text())
    settings=json.loads((ROOT/'generation_settings.json').read_text())
    packet=json.loads(request['input'][1]['content'])
    correction=next(x for x in packet['teacher_reference_sources'] if x['source_id']=='correction')
    with urllib.request.urlopen(correction['url'],timeout=45) as response:
        data=response.read()
    if hashlib.sha256(data).hexdigest()!=settings['correction_xml_sha256']:
        raise ValueError('Published correction bytes changed; review the source before replaying.')
    correction['text']=data.decode()
    request['input'][1]['content']=json.dumps(packet,ensure_ascii=False)
    return request

if __name__=='__main__':
    target=ROOT/'request.reconstructed.local.json'
    request=reconstruct()
    with target.open('x') as handle:
        handle.write(json.dumps(request,ensure_ascii=False,indent=2)+'\n')
    print('Local request reconstructed. No model generation was requested.')
