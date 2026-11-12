# Uncharted: The Nathan Drake Collection for Windows — 1.0.0

**Experimental Windows compatibility build · 12 November 2026**

Custom launcher and integration by **Manohar Padul (Mindro)**.

> This is an experimental compatibility release, not a claim of complete
> compatibility. Crashes, incorrect textures, character/cloth defects and
> performance problems remain. No game files are included. Supply your own
> decrypted PS4 game dump.

## Download and install

Download **uncharted-windows.zip**, extract the complete archive, open
**Uncharted.exe**, select your game folder and choose U1, U2 or U3. Keep all
bundled folders together. Back up saves before replacing an older build.

The release also includes **uncharted-native-source-1.0.0.zip**, the matching
source snapshot for the packaged runtime.

## Included changes

### Launcher and UI

- Launcher version updated to **1.0.0** with Mindro branding and the existing
  dark/gold interface style.
- Separate game-folder selection for U1, U2 and U3, while retaining a shared
  collection-folder option.
- Carried forward the trophy page and earned-trophy notices from the 0.0.1 hot fix,
  with separate game artwork, game selection, save/load/overwrite controls and
  updated game/fix settings pages.
- Retained keyboard, mouse, controller, vibration, language, player-name,
  shortcuts, cheats, live logs and per-game settings.

### Rendering, fixes and stability

- Retained the U2/U3 depth-of-field option and U3 exposure/brightness work.
- Kept U2 exact GPU-result and mesh-raycaster options scoped to U2, with U2 convoy
  handling kept game-specific.
- Preserved small GPU-result readbacks used by weapon/material and brightness
  corrections; black weapons are still not certified fixed in every scene.
- U3 now uses the character raycaster copyback with a gate limited to character
  records. The latest log confirmed that mode was active, but gameplay correctness
  still needs retesting.
- Batched small GPU readbacks by arena so several ranges can share one side-queue
  submission instead of submitting and fencing each range separately. The latest
  supplied U3 log ranges from about 63 to 115 FPS, with heavier samples around
  63–71 FPS, but has no batch diagnostic; it does not measure this new change.
- Included resource/descriptor validation, DMA and frame-handoff ordering,
  transition/cache ownership corrections, job and crash handling, and improved
  startup/build diagnostics from the current runtime.
- Included MP3 decoding through FFmpeg alongside ATRAC9. AAC decoding is not
  implemented.

### Performance and graphics support

- Retained the 60 and 120 FPS targets, frame pacing controls, renderer diagnostics,
  FSR 1 scaling and temporal antialiasing options.
- Bundled the FSR4 shader asset folder. The latest U3 log reports FSR 3.1 active;
  FSR4 selection and shaking are not confirmed resolved.
- This package does not include the DLSS bridge or XeSS runtime.

## Verification and remaining work

The Windows runtime and launcher package built successfully. The ZIP passed its
integrity check, contains the launcher and runtime, and includes 213 FSR4 shader
files. The packaged runtime hash matched the staging runtime.

These checks verify package construction only. No full gameplay session was run
for this release. The latest supplied U3 log is from the still-running pre-batch
distribution: it showed high DispatchDirect wait time and variable host-copy waits,
with no shader/pipeline compilation during the sampled frames. The v1.0.0 batch
change needs a same-scene gameplay comparison. U2 logs vary by scene and show up to
about 119 FPS in lighter sections; busy-scene FPS remains lower. No fixed 60/90/120
FPS performance claim is made.

The matching source snapshot contains the build source and FSR4 shader assets;
generated output, prepared game data, saves, user settings, caches and Git metadata
are excluded.

## Known issues

- U1/U2 streaming/submesh crashes, including
  iSubMesh < m_numSubMeshInstances, are not confirmed fixed.
- Some dumps halt in GetCsShaderByNameId with No CS shader with name.
- Black/incorrect weapons and U3 brightness transitions need visual testing.
- U3 sinking/floating/clipping needs retesting after the targeted gate and batched
  readbacks.
- FSR4 temporal shaking, low FPS, stutter, memory pressure and long-session
  stability remain under investigation.
- Trophy earning, saves, death/reload, chapter changes and complete playthroughs
  were not verified end-to-end in this release.

## Bug reports

Please attach the complete new user/last_run.log from the active user-data folder,
plus game, title ID, update version, hardware, settings, chapter/save point and
reproduction steps. Keep executable identity and hash lines in the log.

Do not upload game files, keys, firmware, system modules or copyrighted assets.

## Credits and license

Custom integration and launcher by **Manohar Padul (Mindro)**. The runtime adapts
GPL-2.0-or-later work from shadPS4, SuperMedo's Uncharted PC port and other
credited projects. Third-party code and assets retain their own licenses. Keep
applicable notices and make corresponding source available when redistributing
the runtime.

This unofficial project is not affiliated with Sony, Naughty Dog, Bluepoint Games
or PlayStation.
