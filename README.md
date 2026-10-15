# Uncharted: The Nathan Drake Collection — Native PC Project

<p align="center">
  <strong>An experimental Windows-native compatibility project for the original PS4 versions of Uncharted 1, 2, and 3.</strong>
</p>

<p align="center">
  <img alt="Work in progress" src="https://img.shields.io/badge/status-work%20in%20progress-orange">
  <img alt="Windows x64" src="https://img.shields.io/badge/platform-Windows%20x64-blue">
  <img alt="Vulkan" src="https://img.shields.io/badge/graphics-Vulkan-red">
  <img alt="Native gameplay not verified" src="https://img.shields.io/badge/native%20gameplay-not%20yet%20verified-lightgrey">
</p>

> [!IMPORTANT]
> **This project is in active development and is not currently a playable PC release.** Original Uncharted gameplay has **not yet been verified in this independent Windows runtime**. No ready-to-play build or copyrighted game content is provided.

## About

**Uncharted: The Nathan Drake Collection — Native PC Project** is an independent research and development effort to run the original PlayStation 4 editions of:

- **Uncharted: Drake's Fortune Remastered**
- **Uncharted 2: Among Thieves Remastered**
- **Uncharted 3: Drake's Deception Remastered**

The aim is to execute compatible original PS4 **x86-64 game code** on Windows, translate graphics commands through **Vulkan**, and implement the required PS4 operating-system services for genuine gameplay.

This is **not** a remake, an official PC port, or a package of PS4 game files.

**Maintainer:** [ManoharPadul](https://github.com/ManoharPadul)  
**Repository:** [uncharted_nathan_drake_collection_pc](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc)

## Development status

| Component / milestone | Current state |
|---|---|
| PS4 SELF/ELF inspection, memory mapping | Experimental implementation |
| Imports, NIDs, relocations and module linking | Link planning implemented; numerous bindings provisional |
| Guest stack, threading, TLS and Windows ↔ PS4 ABI | Synthetic tests implemented |
| PS4 system-library compatibility (HLE) | Partial |
| Liverpool GPU / Vulkan rendering backend | Synthetic compute, draw and presentation tests |
| Original Collection launcher execution on Windows | **Not yet demonstrated** |
| U1 native gameplay | **Not yet demonstrated** |
| U2 native gameplay | **Not yet demonstrated** |
| U3 native gameplay | **Not yet demonstrated** |

The last reported internal checkpoint (Phase 183) had link-planning targets for **433/433 U1 imports**, but **161 required imports still lacked verified execution-ready bindings**. Planned relocations and passing synthetic tests **do not prove the game boots or runs**.

Some GPU-dependent tests require a separately configured backend and may be skipped when it is absent. Development measurements are subject to change.

## Project goals

The first priority is to make **Uncharted 1** run its original executable and reach stable, playable Windows gameplay. After that, extend the same runtime to **Uncharted 2** and **Uncharted 3**.

Planned capabilities include:

- Original executable and game-asset loading without changing source files.
- Correct guest memory, relocations, startup, TLS, threads and HLE services.
- Original GNM/Liverpool graphics commands rendered through Vulkan.
- Proper shaders, textures, lighting, models and frame presentation.
- Controller input, audio, cinematic playback and game filesystem access.
- Checkpoints, save/reload and reproducibly stable gameplay.

**Playable** means real game-generated visuals and responsive gameplay—not a synthetic render, a fake menu or a successful link audit.

## Architecture (in development)

```text
Original PS4 game files (user-supplied, read-only)
                    |
             SELF / ELF loader
                    |
       Guest memory + module linker
                    |
        PS4 x86-64 guest execution
                    |
     PS4 system-service / HLE layer
                    |
     GNM / Liverpool command handling
                    |
           Vulkan GPU backend
                    |
      Windows display, input and audio
```

This is the **intended end-to-end architecture**. Several components have been tested independently, but original-game execution is not yet demonstrated.

## Building from source

> [!NOTE]
> **The repository is being set up.** Source files, build presets, dependencies and release binaries may not yet be published. The following commands are for developers **after the corresponding project files are uploaded**; they will not produce a playable game from an empty repository.

### Development requirements

- Windows 10/11, 64-bit
- Visual Studio / MSVC C++ build tools
- CMake and CTest
- Vulkan SDK and current Vulkan-capable GPU driver
- MSYS2 CLANG64 for the separate GPU/native components where needed
- Zydis and a separately built backend DLL for applicable developer tests

### Developer workflow

```powershell
git clone https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc.git
cd uncharted_nathan_drake_collection_pc

# After source and CMakePresets.json have been published:
cmake --list-presets=all

# Replace placeholders with actual preset names listed above:
cmake --preset <configure-preset>
cmake --build --preset <build-preset>
ctest --preset <test-preset> --output-on-failure
```

Backend-related tests may require environment variables pointing to **locally built dependencies**:

```powershell
$env:UNCHARTED_BBGPU_BACKEND_DLL = 'C:\path\to\libbb-real-liverpool-backend.dll'
$env:UNCHARTED_ZYDIS_DLL = 'C:\path\to\libZydis.dll'
```

Exact supported build and test commands will be documented when the source is published.

## Roadmap

- [x] Initial independent Windows runtime and import/linker research
- [x] Synthetic guest stack, ABI, memory/TLS and GPU test infrastructure
- [ ] Verify required module lifecycle and startup-critical PS4 services
- [ ] Resolve original-game dependency, import and TLS execution readiness
- [ ] Execute the first original Collection/U1 instruction on Windows
- [ ] Reach the original Collection selector and U1 menu
- [ ] Render real U1 gameplay correctly through Vulkan
- [ ] Enable U1 input, audio, cinematics, checkpoints and saves
- [ ] Demonstrate stable, repeatable playable U1 gameplay
- [ ] Achieve equivalent U2 gameplay compatibility
- [ ] Achieve equivalent U3 gameplay compatibility
- [ ] Publish a documented developer build and compatibility guide

The roadmap is aspirational, with no guaranteed release date.

## Game files and legal notice

**This repository does not provide PS4 game executables, assets, firmware, encryption keys or proprietary Sony/Naughty Dog content.** Users are responsible for obtaining and using their own game files lawfully.

This is an independent technical project **not affiliated with, endorsed by or sponsored by Sony Interactive Entertainment, Naughty Dog or PlayStation**. *Uncharted*, *The Nathan Drake Collection*, *PlayStation* and related names belong to their respective rights holders.

## Credits and references

The development effort studies and, where technically and legally appropriate, adapts concepts from:

- [shadPS4](https://github.com/shadps4-emu/shadPS4) — PS4 compatibility, system libraries and Vulkan renderer.
- [Supermedo / bloodborne_pc](https://github.com/Supermedo/bloodborne_pc) — Windows-native PS4 execution and Vulkan integration reference.
- [deadinside28 / bloodborne_pc](https://github.com/deadinside28/bloodborne_pc) — native Bloodborne port foundation.

Thanks to these developers and the wider compatibility and preservation community.

**Licensing:** Third-party code retains its own licensing and attribution obligations. A project-wide license has not yet been published in this repository. Code derived from GPL-licensed sources must comply with the applicable GPL license terms; consult the eventual `LICENSE` and third-party notices before redistributing source or binaries.

## Contributing and reporting issues

Reproducible reports and contributions are welcome through [GitHub Issues](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/issues).

Please include your Windows version, CPU/GPU, driver, build/commit, relevant logs and reproduction steps. Specify whether an issue was observed in **this independent native runtime** or a reference emulator. Do not attach copyrighted game data, private keys or personal information.

---

<p align="center"><strong>Goal: Bring the original Nathan Drake Collection to Windows through a correct, reproducible native compatibility runtime.</strong></p>
