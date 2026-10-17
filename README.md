# Uncharted: The Nathan Drake Collection for Windows

An unofficial, experimental Windows compatibility build for the PS4 versions of
**Uncharted 1, Uncharted 2 and Uncharted 3**, maintained by **Manohar Padul (Mindro)**.

[Downloads](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/releases)
· [Report a bug](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/issues)

> **Development build — version 0.0.1.** Gameplay has been reached, but compatibility,
> rendering, saves, performance and stability are not verified from beginning to end.
> Expect crashes and visual defects. No game files are included.

## How it works

The original PS4 x86-64 game code executes through a Windows-native compatibility
runtime. PS4 system services are implemented on the host, and graphics commands
are translated to Vulkan.

The build does not require launching the standalone shadPS4 application. It **does
include adapted shadPS4 graphics/compatibility code**, along with work from
SuperMedo's Uncharted port and other credited projects. It is not a clean-room
implementation, an official source-code port, or a remake.

## Included in 0.0.1

- Custom Uncharted launcher, game-folder selection, graphics/input settings and shortcuts.
- Save, load and overwrite-selection interface with game-dump artwork support.
- Keyboard, mouse and controller support.
- Vulkan rendering, FSR 1 presentation scaling, TAA and FSR 3.1 options.
- U2/U3 depth-of-field removal and save/cinematic buffer-handoff changes.
- U3 exposure/brightness changes and pub/bathroom material/crash guards.
- Resource/descriptor validation, DMA ordering and deferred sampler-release fixes.
- Shader-cache ownership and resource-table recovery corrections.
- MP3 decoding through FFmpeg alongside ATRAC9 decoding through LibAtrac9.
- Broader EOP frame-reuse wait matching and improved crash/build identification.

These are implemented changes, **not a claim that every affected scene is fixed**.
In particular, the pub guards and save/cinematic changes do not establish that all
U3 crashes or all black weapon textures are resolved.

## Game files

Supply your own decrypted game dump. Do not download or upload game files through
this repository.

Collection layouts normally contain:

```text
Game folder/
├── eboot.bin
├── big2-ps4_Shipping.elf
├── big3-ps4_Shipping.elf
├── sce_sys/
├── u1data/
├── u2data/
└── u3data/
```

Standalone releases use their own `eboot.bin` and game data. Target layouts include
Collection IDs CUSA02320/CUSA02343/CUSA02344 and standalone IDs
CUSA03280/CUSA03281/CUSA03282. Compatibility depends on the exact executable,
update and matching data files; a recognized title ID is not certification.

## Requirements and installation

- Windows 10 or Windows 11, 64-bit, on an x86-64 CPU.
- A Vulkan 1.3-capable GPU and compatible graphics driver.
- Enough available RAM, page-file capacity and VRAM for the selected game/settings.
  Reliable operation on 4 GB VRAM or 8 GB RAM systems has **not** been established.

1. Download `uncharted-windows.zip` from [Releases](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/releases).
2. Extract the entire archive to a writable folder. Do not run it inside the ZIP.
3. Open `Uncharted.exe` and select your game folder on the Game page.
4. Choose the matching game and start it from the launcher.

Keep the launcher, `bin`, `_internal` and other bundled folders together. The
packaged application includes Python and its runtime dependencies; a separate
Python installation is not required to play.

Start testing with 60 FPS selected. This is a target, not a guaranteed result.
Higher frame-rate limits, frame generation and multithreaded paths need additional
testing. A larger output window is not proof of native 1440p/4K guest rendering.

### Optional graphics support

- **DLSS/DLSS Frame Generation:** unavailable in this package; the required bridge
  and NVIDIA runtime files were not built/bundled.
- **FSR 4:** the current package does not include the required external model/shader
  assets. Its presence in a settings list does not establish working support.
- Upscaling/frame-generation options depend on the actual build, assets and GPU.

## Saves, settings and logs

- Default saves/cache location: `user/` beside the launcher, unless another saves
  folder is selected.
- Latest run log: `user/last_run.log` in the active user-data directory.
- Runtime/input settings: `uncharted.ini` and `input.ini`.
- Prepared executable data: `out/`.

Back up saves before changing builds. Do not delete the whole `user` folder to
clear shaders: it can also contain save data. Updates should preserve user data.
Save-selection persistence and in-game behavior still need broader testing.

## Known issues

- U1/U2 streaming/submesh crashes, including `iSubMesh < m_numSubMeshInstances`,
  are **not confirmed resolved**.
- Some builds/dumps halt in `GetCsShaderByNameId` with `No CS shader with name`.
  This is not automatically a Vulkan shader-cache problem.
- U3 pub/gameplay crashes and black or incorrect materials remain under investigation.
- Floating/clipping characters, stretching, Sully's clothing flicker and cloth/hair
  simulation defects are not confirmed fixed across all games/scenes.
- FPS drops, stutter, memory pressure and long-session stability remain open.
- MP3 fixture tests passed; broader game-audio compatibility is still being tested.
  AAC decoding is not implemented in this runtime.

A successful build, a passing focused test or reaching a menu does not prove
full-game compatibility. No stable 60/120 FPS or zero-performance-loss guarantee
is made.

## Reporting a problem

Open an [issue](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/issues) with:

- Release/build used, U1/U2/U3, title ID and game update version.
- CPU, GPU, VRAM, RAM, Windows and graphics-driver versions.
- Chapter/save location, steps to reproduce, and whether death/reload is involved.
- Selected resolution, FPS limit, upscaler and frame-generation settings.
- The **complete new log from that build**, plus screenshots/video when useful.

New logs identify the selected executable, APP_VER and SHA-256. Keep those lines
when reporting bugs. Redact personal paths if needed; never attach game binaries,
keys, system modules or copyrighted assets to public issues.

## Credits, source and licenses

Custom integration, launcher and branding: **Manohar Padul (Mindro)**.

This build uses or adapts work from:

- [shadPS4](https://github.com/shadps4-emu/shadPS4)
- [deadinside28 — bloodborne_pc](https://github.com/deadinside28/bloodborne_pc)
  credited by the base port for video-decoder/DLSS integration work.
- FFmpeg, LibAtrac9, SDL3, Dear ImGui, FidelityFX/FSR and the other dependencies
  identified by their source and bundled notices.

The runtime contains GPL-2.0-or-later code; dependencies retain their own licenses.
Distributions must retain applicable notices and provide corresponding source as
required by those licenses. Upstream links are not a substitute for the matching
source of a modified binary. This documentation repository is not, by itself,
the complete runtime source tree.

Uncharted and related names belong to their respective owners. This project is
not affiliated with or endorsed by Sony Interactive Entertainment, Naughty Dog,
Bluepoint Games or PlayStation.
