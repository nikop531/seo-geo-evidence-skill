#!/usr/bin/env python3
"""Offline release checks; no network or third-party skill execution."""
import json,re,xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/seo-geo-evidence'

def validate(root=ROOT):
    skill=root/'skills/seo-geo-evidence';text=(skill/'SKILL.md').read_text()
    assert text.startswith('---\nname: seo-geo-evidence\ndescription: '),'Invalid skill frontmatter'
    assert text.count('\n---\n')==1,'Unexpected frontmatter boundary'
    ET.fromstring(text[text.index('<skill_workflow>'):])
    sources=json.loads((skill/'references/sources.json').read_text())['sources'];ids={s['id'] for s in sources}
    assert len(ids)==len(sources)==6,'Unexpected source registry'
    for s in sources:
        assert s['url'].startswith('https://') and re.fullmatch(r'\d{4}-\d{2}-\d{2}',s['last_checked'])
    for name in re.findall(r'references/[\w.-]+',text): assert (skill/name.rstrip('.')).is_file(),name
    for p in (skill/'references').glob('*.md'):
        for source_id in re.findall(r'(?<![A-Za-z0-9_])(?:G\d{2}|O\d{2}|B\d{2}|R\d{2}|V\d{2}|VID-\d{2})(?![A-Za-z0-9_])',p.read_text()):assert source_id in ids,(p,source_id)
    for p in root.rglob('*'):
        if not p.is_file() or any(x in p.parts for x in ('.git','__pycache__')):continue
        assert not p.is_symlink(),f'Unexpected symlink: {p}'
        if p.name=='.gitignore':continue
        assert not p.name.startswith('.env') and p.suffix not in ('.zip','.log'),f'Private/artifact file: {p}'
        content=p.read_text()
        private_home='/'+'Users'+'/'
        key_header='-----'+'BEGIN '+r'(?:RSA |EC |OPENSSH )?PRIVATE KEY'+'-----'
        assert not re.search(re.escape(private_home)+r'[^/\s]+/|(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{15,}|'+key_header,content),f'Potential sensitive data: {p}'
    version=json.loads((root/'version.json').read_text())
    assert re.fullmatch(r'\d+\.\d+\.\d+',version['version'])
    print(f"PASS: skill XML, references, 6 sources, version {version['version']}, basic private-data scan")

if __name__=='__main__':validate()
