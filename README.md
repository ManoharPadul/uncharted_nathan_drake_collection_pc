# Uncharted: The Nathan Drake Collection for Windows

An unofficial experimental Windows compatibility build for the PS4 versions of
**Uncharted 1, Uncharted 2 and Uncharted 3**, maintained by **Manohar Padul (Mindro)**.

[Download v1.0.1](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/releases/tag/1.0.1)
· [All releases](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/releases)
· [Report a bug](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/issues)

The release also includes the matching source snapshot,
**uncharted-native-source-1.0.1.zip**.

> **v1.0.1 remains experimental.** Gameplay starts, but full-game compatibility,
> visuals, saves, performance and long-session stability have not been verified.
> Expect crashes and rendering defects. No game files are included.

## How it works

The original PS4 x86-64 game code runs through a Windows-native compatibility
runtime. System services are implemented on the host and graphics commands are
translated to Vulkan. The build includes adapted shadPS4 renderer/runtime code and
work from SuperMedo's Uncharted PC port and other credited projects. It is not an
official PC port, remake or clean-room implementation.

## Included in v1.0.1

### Launcher and game management

- Custom Uncharted interface with Play, Game, Graphics, Performance, Controls,
  Fixes, Trophies, Advanced and Log pages.
- Shared collection folder or separate game folders for U1, U2 and U3.
- Game-dump artwork, save/load/overwrite selection, trophy lists and earned-trophy
  notifications.
- Keyboard, mouse and controller support, remapping, vibration, player name,
  language, cheats and shortcuts.

### Rendering and game-specific options

- Vulkan renderer with 60/120 FPS targets, presentation options, FSR 1 scaling,
  TAA, AMD FSR 3.1/4, NVIDIA DLSS Super Resolution and Intel XeSS options.
- FSR 3 and NVIDIA DLSS Frame Generation paths. The package includes NVIDIA DLSS
  310.9.1.0 Super Resolution and Frame Generation runtimes, plus the Intel XeSS
  runtime. The XeSS DLL reports file version 2.0.2.68. Availability depends on the
  GPU, driver and selected mode.
- Temporal-upscaler sharpening and jitter controls, including separate DLSS/XeSS
  jitter-sign handling and the FSR 4 jitter-sign option.
- U2/U3 depth-of-field control and U3 exposure/brightness corrections.
- U2 exact GPU-result and mesh-raycaster options, plus targeted U2 convoy handling.
- Small GPU-result readbacks for weapon/material and brightness issues.
- U3 character-raycaster copyback with a targeted end-of-pipe gate. Small result
  readbacks are batched by arena to reduce repeated queue submissions.
- Shader/resource validation, cache-ownership and transition-handling corrections,
  improved crash reporting and game-build identification.
- MP3 decoding through FFmpeg and ATRAC9 support; AAC is not implemented.
- FSR4 shader assets are included. FSR4 stability is still under verification:
  the latest U3 log reported FSR 3.1 active, and FSR4 shaking has not been confirmed
  resolved.

These are included code paths and options, **not a guarantee that every visual issue
is fixed in every chapter**.

## Download and install

1. Download **uncharted-windows.zip** from the [v1.0.1 release](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/releases/tag/1.0.1).
2. Extract the full archive to a writable folder. Do not run the application from
   inside the ZIP.
3. Open **Uncharted.exe**, choose the game dump on the Game page, and select U1,
   U2 or U3.
4. Keep the launcher, bin, _internal and other bundled folders together.

Supply your own decrypted game files. Collection layouts normally include
eboot.bin, big2-ps4_Shipping.elf, big3-ps4_Shipping.elf, sce_sys and the game data
folders. Standalone builds use their own executable and data. A recognized title ID
does not certify compatibility with every update or dump.

## Requirements

- Windows 10 or Windows 11, 64-bit, on an x86-64 CPU.
- Vulkan 1.3-capable GPU with a current graphics driver.
- Enough system memory, page-file capacity and VRAM for the game and selected
  settings. Stable operation on low-memory systems is not established.

Start with the 60 FPS target. Higher targets and frame generation are experimental;
60, 90 or 120 FPS is not guaranteed across scenes or hardware. Lowering the window
size does not necessarily lower the game's internal render resolution.

## Saves, settings and logs

- Saves and shader caches are kept in the selected user-data folder, normally
  user/ beside the launcher.
- The latest run log is user/last_run.log in that active folder.
- Runtime and input settings are stored in uncharted.ini and input.ini.
- Prepared game data is stored in out/.

Back up saves before updating. Do not delete the entire user folder to clear shader
caches; it may also contain save data. Updates should preserve user data.

## Known issues

- **U3 FPS and frame pacing:** the latest supplied capture ran from
  `dist/uncharted-windows` with the same runtime hash as v1.0.0, so the batched
  readback path was active. It reports 56.5–120 FPS across 56 windows; the last
  heavy windows were about 62.9–70.7 FPS. Stage B was busy about 89–95%, and
  DispatchDirect accounted for about 30–45% of stage-A wait cycles, which points
  to CPU-side recorder pressure. The first three batch diagnostics each had one
  range, so this capture does not demonstrate multiple ranges combined or a
  before/after gain. Detailed frame instrumentation was enabled and can affect
  timing; compare with it off.
- **U2 FPS:** earlier logs ranged from about 97 to 119 FPS depending on scene.
  Exact synchronous GPU results can cost speed in busy scenes; U2 train/submesh
  assertions are not confirmed fixed.
- **Characters:** U3 raycaster synchronization is enabled by default, but sinking,
  floating and clipping still need scene-by-scene gameplay verification.
- **Weapons and brightness:** the tested black-gun/material case is fixed by the
  small-result path. Other scenes and all U3 brightness transitions still need checking.
- **FSR4:** assets are bundled, but temporal shaking and the selected runtime path
  still need verification. Do not assume the option is stable.
- **DLSS Frame Generation:** a recent test with DLSS Frame Generation enabled ended
  in a GPU timeout/reset (LiveKernelEvent 141). Frame Generation is experimental;
  turn it off if the driver reset or crash recurs. DLSS Super Resolution is a
  separate path.
- The latest texture A/B comparison no longer showed flicker after restoring the
  texture-coherency paths. This was a focused test, not verification of every
  scene or game.
- DLSS-NR/“DLSS 5” and OptiScaler are not included in this build.
- U1/U2 streaming crashes, U3 pub/gameplay crashes, cloth/hair defects, memory
  pressure and long-session stability remain under investigation.

A successful build, menu launch or focused test does not prove a complete
playthrough or stable frame rate.

## Report a problem

Open an [issue](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/issues)
with the game, title ID, game update, chapter/save point, reproduction steps,
hardware, graphics settings and the complete log from that build. Keep the startup
executable/hash lines. Do not attach game binaries, keys, firmware or copyrighted
game assets.

## Credits and notices

Custom launcher and integration by **Manohar Padul (Mindro)**. This project adapts
work from [SuperMedo's Uncharted PC port](https://github.com/Supermedo/uncharted_pc),
[shadPS4](https://github.com/shadps4-emu/shadPS4),
[bc160201983's Uncharted port](https://github.com/bc160201983/Uncharted-The-Nathan-Drake-Collection-PC-port),
and the contributors and dependencies credited in the source and release notices.
Third-party components retain their own licenses. The runtime includes
GPL-2.0-or-later code; preserve applicable notices and corresponding source when
redistributing it. The matching source snapshot is attached to the v1.0.1 release.

Uncharted and related names belong to their respective owners. This project is not
affiliated with or endorsed by Sony Interactive Entertainment, Naughty Dog,
Bluepoint Games or PlayStation.
