"""Extract archived PNG prompt graphs and compare target-node prompts; stdlib only."""
import argparse,csv,hashlib,json,struct,zipfile,zlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('archive_dir',type=Path);args=parser.parse_args()
out=root/'supplementary/image-metadata';out.mkdir(exist_ok=True)
catalog={c['id']:c for c in json.loads((root/'evaluation/novel-continuity-v2/catalog.json').read_text())['cuts']}
rows=[];archives=[]
for archive in sorted(args.archive_dir.glob('*-original-cuts.zip')):
 archives.append({'archive':archive.name,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
 with zipfile.ZipFile(archive) as z:
  for name in z.namelist():
   if not name.lower().endswith('.png'):continue
   data=z.read(name);assert data[:8]==b'\x89PNG\r\n\x1a\n';i=8;metadata={}
   while i+12<=len(data):
    size=struct.unpack('>I',data[i:i+4])[0];kind=data[i+4:i+8];chunk=data[i+8:i+8+size]
    assert zlib.crc32(kind+chunk)&0xffffffff==struct.unpack('>I',data[i+8+size:i+12+size])[0]
    if kind==b'tEXt':
     key,value=chunk.split(b'\0',1);metadata[key.decode('latin1')]=value.decode('latin1')
    elif kind==b'zTXt':
     key,rest=chunk.split(b'\0',1);metadata[key.decode('latin1')]=zlib.decompress(rest[1:]).decode('latin1')
    elif kind==b'iTXt':
     key,rest=chunk.split(b'\0',1);flag=rest[0];rest=rest[2:];lang,translated,value=rest.split(b'\0',2);metadata[key.decode('latin1')]=(zlib.decompress(value) if flag else value).decode('utf8')
    i+=size+12
   cid=Path(name).stem;graph=json.loads(metadata['prompt'])
   nodes=[(k,v) for k,v in graph.items() if v.get('class_type')=='OpenAIGPTImageNodeV2' and v.get('_meta',{}).get('title')==cid]
   assert len(nodes)==1,(cid,len(nodes));node_id,node=nodes[0];prompt=node['inputs']['prompt']
   (out/(cid+'.json')).write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n')
   (out/(cid+'.txt')).write_text(prompt)
   rows.append(dict(cut_id=cid,archive=archive.name,member=name,image_sha256=hashlib.sha256(data).hexdigest(),node_id=node_id,prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),exact_catalog_match=prompt==catalog[cid]['prompt'],file_match_ignoring_outer_whitespace=prompt.strip()==(root/'evaluation/novel-continuity-v2/prompts'/f'{cid}.txt').read_text().strip(),model=node['inputs'].get('model'),quality=node['inputs'].get('model.quality'),background=node['inputs'].get('model.background')))
assert len(rows)==len({r['cut_id'] for r in rows})
with (out/'verification.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
report={'archives':archives,'images_checked':len(rows),'catalog_exact_matches':sum(r['exact_catalog_match'] for r in rows),'prompt_file_matches_ignoring_outer_whitespace':sum(r['file_match_ignoring_outer_whitespace'] for r in rows),'all_members_under_v2':all('/novel-continuity-v2/' in r['member'] for r in rows),'interpretation':'Embedded metadata corroborates the archived final-generation inputs; it does not recover first-generation inputs or independently authenticate backend execution.'}
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
