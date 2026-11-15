"""Run a prepared game (tools/try.py first) and follow a script of inputs and screenshots.

Usage: python tools/drive.py u1 "wait 25; shot title; press cross; wait 5; shot menu"
Steps: wait SECONDS | press BUTTON [SECONDS held, default 0.15] | hold BUTTONS... | release |
       shot NAME (out/try/<game>/NAME.png) | toggle MASK (optimizations off, BB_TOGGLE_FILE).
The game is stopped after the last step.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

PORT = Path(__file__).resolve().parent.parent


def frame_shot(dump, trigger, png):
    """The presenter writes the next frame (BB_FRAME_DUMP_TRIGGER) as raw RGBA; works while
    the window is minimized or covered. Frames generated before it (frame generation) are
    saved as <name>_g0.png, <name>_g1.png, ..."""
    before = set(dump.glob('output_*.raw'))
    trigger.write_bytes(b'')
    for _ in range(60):
        time.sleep(0.05)
        new = [p for p in dump.glob('output_*.raw') if p not in before]
        if new:
            raw = new[0]
            width, height = map(int, raw.stem.rsplit('_', 1)[1].split('x'))
            index = raw.stem.split('_')[1]
            from PIL import Image
            images = [(raw, png)] + [
                (dump / f'generated{g}_{index}_{width}x{height}.raw', png.with_name(f'{png.stem}_g{g}.png'))
                for g in range(3)]
            for source, target in images:
                # Written by deferred GPU callbacks, the generated frames before the output.
                for _ in range(40 if source == raw else 4):
                    if source.is_file() and source.stat().st_size >= width * height * 4:
                        break
                    time.sleep(0.05)
                if source.is_file():
                    Image.frombytes('RGBA', (width, height), source.read_bytes()).convert('RGB').save(target)
            # Frame generation inputs of the same frame (depth f32, motion 2 x f16): kept as
            # <name>_fg_depth_WxH.raw and <name>_fg_motion_WxH.raw.
            time.sleep(0.2)
            for fg in dump.glob('fg_*.raw'):
                kind, size = fg.stem.split('_')[1], fg.stem.rsplit('_', 1)[1]
                fg.replace(png.with_name(f'{png.stem}_fg_{kind}_{size}.raw'))
            for leftover in dump.glob('*.raw'):
                leftover.unlink()
            return True
    trigger.unlink(missing_ok=True)
    return False


def main():
    which, script = sys.argv[1], sys.argv[2]
    game_dir = sys.argv[3] if len(sys.argv) > 3 else r'D:\here\CUSA02343'
    out = PORT / 'out' / 'try' / which
    # DRIVE_USER: another saves folder (a copy of a player's saves, to reproduce their state).
    user = Path(os.environ['DRIVE_USER']) if os.environ.get('DRIVE_USER') else PORT / 'out' / 'try' / 'user'
    pad = out / 'pad.txt'
    pad.write_text('', encoding='ascii')
    dump, trigger = out / 'dump', out / 'dump.trigger'
    dump.mkdir(exist_ok=True)
    for old in dump.glob('*.raw'):
        old.unlink()
    (out / 'capture').mkdir(exist_ok=True)
    toggles = out / 'toggles.txt'
    # DRIVE_TOGGLES: optimizations switched off from the start (A/B runs).
    toggles.write_text(str(int(os.environ.get('DRIVE_TOGGLES') or '0', 0)), encoding='ascii')
    env = dict(os.environ, BB_PAD_FILE=str(pad), BB_FPS_LOG='1', BB_FRAME_DUMP_TRIGGER=str(trigger),
               BB_DUMP_DIR=str(dump), BB_CAPTURE_TRIGGER=str(out / 'capture.trigger'),
               BB_CAPTURE_DIR=str(out / 'capture'), BB_TOGGLE_FILE=str(toggles))
    env['PATH'] = r'C:\msys64\clang64\bin' + os.pathsep + env['PATH']
    command = [os.environ.get('DRIVE_EXE') or str(PORT / 'out' / 'bb-probe.exe'), str(out / 'boot-linked.bin'), '--content-profile',
               str(out / 'content.bin'), '--app0', game_dir, '--user', str(user)]
    # DRIVE_GUEST_ARGS: command line arguments for the game (e.g. "forcefps 120").
    if os.environ.get('DRIVE_GUEST_ARGS'):
        exe = {'u1': 'eboot.bin', 'u2': 'big2-ps4_Shipping.elf', 'u3': 'big3-ps4_Shipping.elf'}[which]
        guest_argv = out / 'guest-argv.txt'
        guest_argv.write_text('\n'.join([f'/app0/{exe}', *os.environ['DRIVE_GUEST_ARGS'].split()]) + '\n',
                              encoding='utf-8')
        command += ['--guest-argv', str(guest_argv)]
    # DRIVE_PATCHES: a BBPATCH2 file applied to the executable (diagnostic patches).
    if os.environ.get('DRIVE_PATCHES'):
        command += ['--patches', os.environ['DRIVE_PATCHES']]
    log = (out / 'run.log').open('w', encoding='utf-8', errors='replace')
    game = subprocess.Popen(command, env=env, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    start = time.time()
    try:
        for step in filter(None, (s.strip() for s in script.split(';'))):
            if game.poll() is not None:
                print(f'Game exited with code {game.returncode} before: {step}')
                break
            verb, *args = step.split()
            if verb == 'wait':
                time.sleep(float(args[0]))
            elif verb == 'press':
                pad.write_text(args[0], encoding='ascii')
                time.sleep(float(args[1]) if len(args) > 1 else 0.15)
                pad.write_text('', encoding='ascii')
                time.sleep(0.1)
            elif verb == 'hold':
                pad.write_text(' '.join(args), encoding='ascii')
            elif verb == 'release':
                pad.write_text('', encoding='ascii')
            elif verb == 'shot':
                if not frame_shot(dump, trigger, out / f'{args[0]}.png'):
                    print('        screenshot failed: no frame was presented within 3 seconds')
            elif verb == 'toggle':
                # toggle MASK: optimizations switched off from now on (gpu/shim/bbport_toggles.h;
                # re-read every 250 ms, so the step waits half a second).
                toggles.write_text(str(int(args[0], 0)), encoding='ascii')
                time.sleep(0.5)
            elif verb == 'capture':
                # The renderer's frame analyzer records the next frame (out/try/<game>/capture/).
                (out / 'capture.trigger').write_bytes(b'')
            elif verb == 'waitscene':
                # waitscene SECONDS: until the picture is neither the current one nor dark
                # (timing tests start from the same moment of a scene change).
                from PIL import Image, ImageChops, ImageStat
                probe = out / '_scene.png'
                frame_shot(dump, trigger, probe)
                reference = Image.open(probe).convert('L').resize((160, 90))
                deadline = time.time() + float(args[0])
                while time.time() < deadline:
                    time.sleep(0.5)
                    if not frame_shot(dump, trigger, probe):
                        continue
                    now = Image.open(probe).convert('L').resize((160, 90))
                    if ImageStat.Stat(now).mean[0] > 30 and \
                            ImageStat.Stat(ImageChops.difference(now, reference)).mean[0] > 25:
                        break
            print(f'{time.time() - start:6.1f}s  {step}')
    finally:
        running = game.poll() is None
        if running:
            game.kill()
        game.wait()
        log.close()
    print(('Stopped (still running)' if running else f'Exited with code {game.returncode:#x}') + f'. Log: {out / "run.log"}')


if __name__ == '__main__':
    main()
