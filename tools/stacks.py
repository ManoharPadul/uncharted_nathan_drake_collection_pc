"""All thread stacks of the running bb-probe with names: host functions (llvm-symbolizer on
out/bb-probe.exe), guest offsets (eboot image, base from the run log), system DLL+offset.
Usage: python tools/stacks.py [RUN_LOG] [--all]   (default log: out/try/u1/run.log)
Without --all, threads parked in an ordinary wait with no guest frames are summarized."""
import re
import subprocess
import sys
from pathlib import Path

PORT = Path(__file__).resolve().parent.parent
CLANG = Path(r'C:\msys64\clang64\bin')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    show_all = '--all' in sys.argv
    log = Path(args[0]) if args else PORT / 'out' / 'try' / 'u1' / 'run.log'
    match = re.search(r'Guest image at (?:0x)?([0-9a-fA-F]+)', log.read_text(encoding='utf-8', errors='replace'))
    guest = int(match.group(1), 16) if match else None
    tool = PORT / 'out' / 'stacks.exe'
    if not tool.exists() or tool.stat().st_mtime < (PORT / 'tools' / 'stacks.c').stat().st_mtime:
        subprocess.run([str(CLANG / 'clang.exe'), '-O2', str(PORT / 'tools' / 'stacks.c'), '-o', str(tool),
                        '-ldbghelp', '-lpsapi'], check=True)
    pid = subprocess.run(['powershell', '-NoProfile', '-Command', '(Get-Process bb-probe).Id'],
                         capture_output=True, text=True).stdout.split()
    if not pid:
        sys.exit('bb-probe is not running')
    text = subprocess.run([str(tool), pid[0]], capture_output=True, text=True).stdout
    modules = [(int(b, 16), int(s, 16), n) for b, s, n in re.findall(r'^module (\w+) (\w+) (.+)$', text, re.M)]
    exe = next(((b, s) for b, s, n in modules if n.lower() == 'bb-probe.exe'), None)
    addresses = {int(a, 16) for a in re.findall(r'\b([0-9a-f]{6,})\b', '\n'.join(
        l for l in text.splitlines() if l.startswith('  ')))}
    host = sorted(a for a in addresses if exe and exe[0] <= a < exe[0] + exe[1])
    names = {}
    if host:
        r = subprocess.run([str(CLANG / 'llvm-symbolizer.exe'), '--obj', str(PORT / 'out' / 'bb-probe.exe'),
                            '--functions=short', '--no-inlines', '--relative-address'],
                           input='\n'.join(hex(a - exe[0]) for a in host), capture_output=True, text=True)
        blocks = r.stdout.strip().split('\n\n')
        for a, block in zip(host, blocks):
            lines = block.splitlines()
            names[a] = lines[0] if lines and lines[0] != '??' else f'bb-probe+{a - exe[0]:#x}'

    def name(a):
        if a in names:
            return names[a]
        if guest is not None and guest <= a < guest + 0x20000000:
            return f'guest+{a - guest:#x}'
        for b, s, n in modules:
            if b <= a < b + s:
                return f'{n}+{a - b:#x}'
        return hex(a)

    quiet = 0
    for block in re.split(r'^(?=thread )', text, flags=re.M):
        if not block.startswith('thread'):
            continue
        header, *walks = block.strip().splitlines()
        frames = []
        for w in walks:
            kind, *values = w.split()
            frames.append((kind, [name(int(v, 16)) for v in values]))
        has_guest = any(f.startswith('guest+') for _, fs in frames for f in fs)
        if not show_all and not has_guest and all(len(fs) < 2 for _, fs in frames):
            quiet += 1
            continue
        print(header)
        for kind, fs in frames:
            print(f'  {kind:6} ' + ' < '.join(fs[:14]))
    if quiet:
        print(f'({quiet} threads without guest frames not shown; --all shows them)')


if __name__ == '__main__':
    main()
