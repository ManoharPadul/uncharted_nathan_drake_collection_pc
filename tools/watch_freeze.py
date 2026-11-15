"""Watches a running test game: when no frame-rate line arrives for 15 seconds while the game
is still running, all thread stacks are saved to out/try/<game>/freeze_stacks.txt (twice, ten
seconds apart, to tell a deadlock from a slow loop).
Usage: python tools/watch_freeze.py [u1]"""
import subprocess
import sys
import time
from pathlib import Path

PORT = Path(__file__).resolve().parent.parent


def running():
    out = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq bb-probe.exe', '/NH'], capture_output=True, text=True).stdout
    return 'bb-probe.exe' in out


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'u1'
    log = PORT / 'out' / 'try' / which / 'run.log'
    result = log.with_name('freeze_stacks.txt')
    while not running():
        time.sleep(1)
    last_count, last_change = -1, time.time()
    while running():
        try:
            count = log.read_text(encoding='utf-8', errors='replace').count('Frame rate:')
        except OSError:
            count = last_count
        if count != last_count:
            last_count, last_change = count, time.time()
        elif count > 0 and time.time() - last_change > 15:
            with result.open('w', encoding='utf-8') as f:
                for attempt in (1, 2):
                    dump = subprocess.run([sys.executable, str(PORT / 'tools' / 'stacks.py'), str(log)],
                                          capture_output=True, text=True)
                    f.write(f'===== dump {attempt} =====\n{dump.stdout}{dump.stderr}\n')
                    f.flush()
                    time.sleep(10)
            print(f'Frames stopped after {count} frame-rate lines; stacks saved to {result}')
            return
        time.sleep(2)
    print('The game ended without a freeze.')


if __name__ == '__main__':
    main()
