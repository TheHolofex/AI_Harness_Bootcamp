#!/usr/bin/env python3
"""Minimal regenerable brief skeleton students may extend or re-direct an agent to build."""
from pathlib import Path
CORPUS = Path(__file__).parent / 'corpus'
def load():
    files = sorted(p for p in CORPUS.glob('*.md') if not p.name.startswith('DELTA'))
    return {f'C{i+1}': p for i,p in enumerate(files)}, files
def main():
    idx, files = load()
    print('# Daily Status Brief (generated)\n')
    print('Sources: ' + ', '.join(f'[{k}] {p.name}' for k,p in idx.items()))
    print('\n## Notes\n')
    for k,p in idx.items():
        text = p.read_text(encoding='utf-8').strip().splitlines()
        body = ' '.join(ln for ln in text if not ln.startswith('#'))[:240]
        print(f'- [{k}] {body}…')
    print('\n_Regenerate: python sample_regenerate.py_')
if __name__ == '__main__':
    main()
