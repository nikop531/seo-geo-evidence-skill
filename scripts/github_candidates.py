#!/usr/bin/env python3
"""Read-only, bounded GitHub skill candidate metadata collection."""
import argparse, datetime, json, subprocess, time
from pathlib import Path

QUERIES = [f'{topic} skill in:name,description archived:false fork:false' for topic in ('seo', 'geo', 'aeo')]

def collect(as_of):
    start=time.monotonic(); errors=[]; pool={}; calls=0
    def api(endpoint, *args):
        nonlocal calls
        if time.monotonic()-start>120: raise TimeoutError('120 second collection budget reached')
        calls+=1
        return json.loads(subprocess.check_output(['gh','api',endpoint,*args],text=True,timeout=20,stderr=subprocess.PIPE))
    for query in QUERIES:
        try:
            result=api('search/repositories','-X','GET','-f',f'q={query}','-f','sort=stars','-f','order=desc','-f','per_page=20')
            if result.get('incomplete_results'): errors.append({'query':query,'status':'incomplete_results'})
            for r in result.get('items',[]): pool[r['full_name']]=r
        except (subprocess.SubprocessError,TimeoutError,ValueError,KeyError) as e:
            errors.append({'query':query,'status':'failed','error_type':type(e).__name__})
    ranked=sorted(pool.values(),key=lambda r:(-r['stargazers_count'],r['full_name']))
    selected=[]; inspected=[]
    for r in ranked[:12]:
        if len(selected)==3:break
        try:
            tree=api(f"repos/{r['full_name']}/git/trees/{r['default_branch']}?recursive=1")
            if tree.get('truncated'):
                errors.append({'repo':r['full_name'],'status':'tree_truncated'});continue
            paths=[n['path'] for n in tree.get('tree',[]) if n['path'].endswith('SKILL.md') and (any(t in n['path'].lower() for t in ('seo','geo','aeo')) or n['path']=='SKILL.md')]
            inspected.append({'repo':r['full_name'],'eligible_paths':len(paths)})
            paths.sort(key=lambda path:(path.startswith('extensions/'),path.count('/'),path))
            if paths:selected.append({'repo':r['full_name'],'url':r['html_url'],'stars':r['stargazers_count'],'license':(r.get('license') or {}).get('spdx_id'),'pushed_at':r.get('pushed_at'),'tree_sha':tree['sha'],'skill_paths':paths[:8],'basis':'repository stars; skill content not yet reviewed'})
        except (subprocess.SubprocessError,TimeoutError,ValueError,KeyError) as e:
            errors.append({'repo':r['full_name'],'status':'failed','error_type':type(e).__name__})
    return {'as_of':as_of,'queries':QUERIES,'coverage':'partial' if errors or len(selected)<3 else 'complete_within_declared_pool','scope':'up to 20 per query; at most 12 repository trees; not global top 3','api_calls':calls,'inspected':inspected,'candidates':selected,'errors':errors}

def main():
    p=argparse.ArgumentParser();p.add_argument('--as-of',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    datetime.date.fromisoformat(a.as_of)
    dest=Path(a.output)
    if dest.exists():raise SystemExit('Output already exists; choose a new snapshot path.')
    result=collect(a.as_of);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(dest),'coverage':result['coverage'],'candidates':len(result['candidates']),'api_calls':result['api_calls']}))
    if not result['candidates']:raise SystemExit(1)
if __name__=='__main__':main()
