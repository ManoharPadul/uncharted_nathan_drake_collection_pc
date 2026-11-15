"""List the PS4 imports of each Uncharted executable that the runtime does not provide yet.

Prepares and links every executable into out/missing/<name>, asks bb-probe --list-missing
for imports the C runtime leaves unresolved, and drops those the GPU/network library
registers (its LIB_FUNCTION NIDs, read from the sources CMake builds).
Usage: python tools/missing.py [GAME_DIR]
"""
import os
import re
import subprocess
import sys
from pathlib import Path

PORT = Path(__file__).resolve().parent.parent
EXECUTABLES = ('eboot.bin', 'big2-ps4_Shipping.elf', 'big3-ps4_Shipping.elf')
GPU_FILES = ['shadps4/core/libraries/gnmdriver/gnmdriver.cpp', 'shadps4/core/libraries/videoout/video_out.cpp',
             'shadps4/core/libraries/kernel/equeue.cpp', 'shadps4/core/libraries/avplayer/*.cpp',
             'shadps4/core/libraries/network/**/*.cpp', 'shadps4/core/libraries/np/**/*.cpp', 'shim/**/*.cpp']
EXCLUDED = re.compile(r'np_trophy|trophy_ui|np_sns_facebook_dialog|np_profile_dialog/|np_commerce/')


def gpu_nids():
    nids = set()
    for pattern in GPU_FILES:
        for path in (PORT / 'gpu').glob(pattern):
            if not EXCLUDED.search(path.as_posix()):
                nids.update(re.findall(r'LIB_(?:FUNCTION|OBJ)\("([^"]+)"', path.read_text(encoding='utf-8', errors='replace')))
    return nids


def main():
    game = Path(sys.argv[1] if len(sys.argv) > 1 else r'D:\here\CUSA02343')
    env = dict(os.environ, PYTHONUTF8='1')
    env['PATH'] = r'C:\msys64\clang64\bin' + os.pathsep + env['PATH']  # probe DLLs (SDL3, FFmpeg, libc++)
    gpu = gpu_nids()
    for exe in EXECUTABLES:
        out = PORT / 'out' / 'missing' / exe.split('-')[0].split('.')[0]
        for script in ('prepare.py', 'link_modules.py'):
            subprocess.run([sys.executable, str(PORT / 'scripts' / script), str(game), '--out', str(out), '--exe', exe],
                           env=env, check=True, capture_output=True)
        result = subprocess.run([str(PORT / 'out' / 'bb-probe.exe'), str(out / 'boot-linked.bin'), '--cpu-only',
                                 '--list-missing'], env=env, capture_output=True, text=True)
        if result.returncode not in (0, 20):
            sys.exit(f'bb-probe failed with exit code {result.returncode:#x}: {result.stderr.strip()}')
        missing = [line.split(' ', 2)[1:] for line in result.stdout.splitlines() if line.startswith('missing ')]
        missing = [(name, symbol) for name, symbol in missing if name.split('#')[0] not in gpu]
        (out / 'missing.txt').write_text(''.join(f'{n} {s}\n' for n, s in missing), encoding='utf-8')
        print(f'== {exe}: {len(missing)} missing')
        by_library = {}
        for name, symbol in missing:
            library = name.split('#', 1)[1]
            by_library.setdefault(library, []).append(symbol.replace(' (data)', '*'))
        for library, symbols in sorted(by_library.items(), key=lambda kv: -len(kv[1])):
            print(f'  {library}: ' + ', '.join(sorted(symbols)))


if __name__ == '__main__':
    main()
