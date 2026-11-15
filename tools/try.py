"""Run one Uncharted game in the loader and show how far it gets.

Usage: python tools/try.py [u1|u2|u3] [--gpu] [--seconds N] [--game DIR]
Without --gpu the game runs CPU-only (no window). With --seconds the game is stopped after N
seconds (a screenshot is saved first to out/try/<game>/shot.png). Output: out/try/<game>/run.log
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

PORT = Path(__file__).resolve().parent.parent
EXECUTABLES = {'u1': 'eboot.bin', 'u2': 'big2-ps4_Shipping.elf', 'u3': 'big3-ps4_Shipping.elf'}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('which', nargs='?', default='u1', choices=EXECUTABLES)
    parser.add_argument('--gpu', action='store_true', help='open the game window (Vulkan)')
    parser.add_argument('--game', default=r'D:\here\CUSA02343')
    parser.add_argument('--timeout', default='60')
    parser.add_argument('--seconds', type=float, help='stop the game after this many seconds')
    args = parser.parse_args()
    out = PORT / 'out' / 'try' / args.which
    user = PORT / 'out' / 'try' / 'user'
    user.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONUTF8='1')
    env['PATH'] = r'C:\msys64\clang64\bin' + os.pathsep + env['PATH']
    exe = EXECUTABLES[args.which]
    print(f'Preparing {exe} ...')
    for script, extra in (('prepare.py', ['--exe', exe]), ('link_modules.py', ['--exe', exe]),
                          ('content_profile.py', ['--sku', 'full'])):
        subprocess.run([sys.executable, str(PORT / 'scripts' / script), args.game, '--out', str(out), *extra],
                       env=env, check=True, capture_output=True)
    command = [str(PORT / 'out' / 'bb-probe.exe'), str(out / 'boot-linked.bin'), '--content-profile',
               str(out / 'content.bin'), '--app0', args.game, '--user', str(user), '--timeout', args.timeout]
    if not args.gpu:
        command.append('--cpu-only')
    print('Running' + (' with the game window' if args.gpu else ' CPU-only (no window)') + ' ...')
    log = out / 'run.log'
    with log.open('w', encoding='utf-8', errors='replace') as f:
        game = subprocess.Popen(command, env=env, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        try:
            code = game.wait(timeout=args.seconds)
        except subprocess.TimeoutExpired:
            if args.gpu:
                subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(PORT / 'tools' / 'shot.ps1'),
                                '-Out', str(out / 'shot.png')], capture_output=True)
                print(f'Screenshot: {out / "shot.png"}')
            game.kill()
            code = game.wait()
            print(f'Stopped after {args.seconds:g} seconds (still running).')
    time.sleep(0.2)
    lines = log.read_text(encoding='utf-8', errors='replace').splitlines()
    interesting = [l for l in lines if l.startswith(('STOP', 'API:', 'Fault', 'ERROR', 'Entering', 'GPU:'))
                   or ('Runtime:' in l and not l.rstrip().endswith('=0') and '=0,' not in l)]
    print('\n'.join(interesting[-25:]))
    print(f'\nExit code {code}. Full log: {log}')


if __name__ == '__main__':
    main()
