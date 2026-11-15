"""Add a game's imports to src/import_names.inc (scoped NID -> symbol name).

Names come from shadPS4's aerolib.inl (public PS4 symbol lists). Usage:
  python tools/import_names.py path/to/aerolib.inl GAME_DIR [executable ...]
"""
import re
import sys
from pathlib import Path

PORT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PORT / 'scripts'))
from link_modules import DEFAULT_MODULES, module, runtime_name  # noqa: E402

INC = PORT / 'src' / 'import_names.inc'
ENTRY = re.compile(r'\{"([^"]+)","([^"]+)"\}')


def main():
    aerolib, game, executables = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:] or ['eboot.bin']
    names = dict(re.findall(r'STUB\("([^"]+)",\s*([^)\s]+)\)', aerolib.read_text(encoding='utf-8', errors='replace')))
    text = INC.read_text(encoding='utf-8')
    known = {m.group(1) for m in ENTRY.finditer(text)}
    added = []
    for path in [game / e for e in executables] + [game / 'sce_module' / f for f in DEFAULT_MODULES]:
        for s in module(path)['symbols']:
            if not s['identity'] or s['section']:
                continue
            scoped = runtime_name(s['identity'])
            symbol = names.get(s['identity'][0])
            if symbol and scoped not in known:
                known.add(scoped)
                added.append(f'{{"{scoped}","{symbol}"}},')
    if added:
        INC.write_text(text.rstrip('\n') + '\n' + '\n'.join(sorted(added)) + '\n', encoding='utf-8')
    print(f'{len(added)} names added to {INC.relative_to(PORT)}')


if __name__ == '__main__':
    main()
