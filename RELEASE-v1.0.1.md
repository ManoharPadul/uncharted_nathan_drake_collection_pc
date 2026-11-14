# Uncharted: The Nathan Drake Collection for Windows — 1.0.1

**Experimental Windows compatibility build · 14 November 2026**

Custom launcher and integration by **Manohar Padul (Mindro)**.

> This remains an experimental compatibility release. It does not claim full-game
> compatibility, stable performance, or that every visual defect is fixed. Supply
> your own decrypted PS4 game dump; no game files are included.

## Downloads

- **uncharted-windows.zip** — Windows launcher, native runtime, required libraries,
  FSR4 assets, and the optional DLSS and XeSS runtimes.
- **uncharted-native-source-1.0.1.zip** — matching project source and FSR4 assets.

Extract the complete Windows archive to a writable folder and run **Uncharted.exe**.
Keep the bundled folders together. Select a shared collection folder or separate
folders for U1, U2 and U3. Back up saves before replacing an older build.

## Changes in 1.0.1

### Upscalers and image controls

- Added the DLSS bridge and NVIDIA DLSS Super Resolution runtime **310.9.1.0**.
  The renderer requests NVIDIA Preset K. Availability depends on the GPU, driver
  and game mode.
- Added the NVIDIA DLSS Frame Generation runtime **310.9.1.0** as a separate,
  optional path.
- Added Intel XeSS runtime support. The bundled libxess.dll reports file version
  **2.0.2.68**.
- Kept the FSR4 shader assets and FSR 3.1 Frame Generation path in the package.
- Added temporal-upscaler sharpness and jitter controls, including a separate
  DLSS/XeSS jitter-sign control and the FSR4 jitter-sign option. These controls
  change renderer settings; they do not guarantee that every scene will be sharper
  or temporally stable.
- DLSS-NR/“DLSS 5” and OptiScaler are not included.

### Texture stability and carried-forward fixes

- Restored the texture-coherency and scene-transition paths that stopped flicker
  in the user's A/B comparison. That test covered a specific scene; it does not
  certify every game area or eliminate all texture issues.
- Carries forward the U2/U3 depth-of-field options, U3 exposure/brightness work,
  U2 exact GPU-result and mesh-raycaster options, weapon/material readbacks, and
  the U3 character-raycaster copyback and targeted synchronization gate.
- Carries forward batched small GPU-result readbacks, intended to reduce repeated
  queue submissions. Performance improvement varies by scene and has not been
  established with a controlled before/after benchmark.
- Keeps the launcher UI changes: separate per-game folders, trophy lists and
  notifications, game artwork, save selection, and the existing fixes/settings
  pages.

## Build and package checks

The Windows native runtime and launcher package built successfully. The release
archive includes the launcher, runtime, NVIDIA DLSS and Frame Generation DLLs,
Intel XeSS DLL, FSR4 assets and license notices. Developer .cmd files, local
game settings, saves, prepared game data and DLSS-NR/OptiScaler files are excluded.
The source archive contains the project source and FSR4 assets; proprietary vendor
runtime DLLs are provided only in the Windows package under their respective
licenses.

These checks confirm that the package was assembled. They do not replace an
end-to-end gameplay test. DLSS Super Resolution has been observed in the supplied
logs, but this release was not verified through a complete playthrough. XeSS
activation and the image-quality controls still need scene-by-scene confirmation.

## Known issues

- A recent test with DLSS Frame Generation enabled ended with a GPU timeout/reset
  reported as **LiveKernelEvent 141**. Frame Generation remains experimental. Turn
  it off if the driver reset or crash recurs; DLSS Super Resolution is a separate
  path.
- FPS and frame pacing remain scene-dependent. Supplied U2/U3 logs show workload
  waits and substantial variation; no fixed 90 or 120 FPS claim is made. Start at
  the 60 FPS target.
- FSR4 temporal shaking and the exact selected runtime path are not fully verified.
- U3 sinking/floating/clipping, untested weapon/material cases, brightness transitions, U2/U3
  streaming crashes, and texture behavior in other scenes still need gameplay
  checks.
- Trophies, save/load, death/reload, chapter transitions and full playthroughs
  have not all been verified end-to-end.

## Bug reports

Open an [issue](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/issues)
with the game, title ID, update version, chapter/save point, hardware, settings,
reproduction steps and the complete user/last_run.log from this build. Keep the
executable identity and hash lines. Do not upload game files, keys, firmware,
system modules or copyrighted game assets.

## Credits and license

Custom launcher and integration by **Manohar Padul (Mindro)**. This runtime adapts
GPL-2.0-or-later work from shadPS4, SuperMedo's Uncharted PC port and other
credited projects. Third-party code and assets retain their own licenses.
Preserve applicable notices and make corresponding source available when
redistributing the runtime. NVIDIA DLSS and Intel XeSS binaries retain their
vendor license terms.

This unofficial project is not affiliated with Sony, Naughty Dog, Bluepoint Games
or PlayStation.
