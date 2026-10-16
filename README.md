# Uncharted: The Nathan Drake Collection — Native PC Project

<p align="center">
  <strong>An experimental native Windows compatibility project for Uncharted 1, Uncharted 2, and Uncharted 3.</strong>
</p>

<p align="center">
  <img alt="Work in progress" src="https://img.shields.io/badge/status-experimental%20development-orange">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows%20x64-blue">
  <img alt="Graphics API" src="https://img.shields.io/badge/graphics-Vulkan-red">
  <img alt="Early development" src="https://img.shields.io/badge/release-early%20experimental%20build-yellow">
</p>

> [!WARNING]
> **This is an experimental, unofficial development project. Compatibility, stability, performance, and gameplay are still under development.** Expect crashes, missing textures, rendering defects, incomplete features, and other issues. This project is not affiliated with Sony Interactive Entertainment, Naughty Dog, or PlayStation.

## About the Project

**Uncharted: The Nathan Drake Collection — Native PC Project** is an independent research and development effort focused on bringing the original PlayStation 4 versions of the following games to Windows through a native compatibility runtime:

- **Uncharted: Drake's Fortune Remastered** — Uncharted 1
- **Uncharted 2: Among Thieves Remastered** — Uncharted 2
- **Uncharted 3: Drake's Deception Remastered** — Uncharted 3

The long-term objective is to execute the original games through a Windows-native runtime, with appropriate handling of PS4 executable code, system services, memory, graphics, input, and other platform requirements.

The goal is **not to run the games through shadPS4 as the runtime**. Instead, the project aims to develop its own Windows execution and compatibility layers. The final architecture and compatibility requirements remain under active development.

This is a technical compatibility project, not an official PC port or a remake.

- **Maintainer:** [ManoharPadul](https://github.com/ManoharPadul)
- **Repository:** [uncharted_nathan_drake_collection_pc](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc)
- **Issues and bug reports:** [GitHub Issues](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/issues)

## Current Development Status

The project is experimental. Progress may differ between game versions and individual builds.

| Game / Component | Status |
|---|---|
| Uncharted 1 | Experimental gameplay progress; full compatibility and stability require further verification |
| Uncharted 2 | Experimental; crashes and gameplay/rendering issues remain |
| Uncharted 3 | Experimental; gameplay/rendering issues remain |
| Texture rendering | Ongoing investigation and fixes |
| Character and environment collision | Requires further testing |
| Native runtime and PS4 compatibility services | Under active development |
| Vulkan graphics backend | Under development and testing |
| Long-term stability and performance | Not yet established across all three games |

A game reaching a particular scene or showing gameplay does not establish that the entire game is playable from beginning to end. Compatibility must be verified through repeatable testing.

## Project Goals

The primary objective is to establish a reliable native Windows execution path, starting with Uncharted 1 and then improving compatibility with Uncharted 2 and Uncharted 3.

Planned development areas include:

- Original game executable loading and guest-code execution.
- PS4 memory management, module loading, relocations, threading, and TLS.
- PS4 system-library compatibility and required system services.
- Graphics command handling and Vulkan rendering.
- Correct textures, shaders, lighting, models, and frame presentation.
- Controller input, audio, cinematics, and filesystem access.
- Save and reload functionality, checkpoints, and stable game progression.
- Crash diagnostics, reproducible tests, and performance profiling.

**Native compatibility is not established by a successful build, a synthetic graphics test, or a menu alone.** The objective is real gameplay with correct rendering, working controls, and repeatable stability.

## Architecture

The intended architecture is built around a Windows-native runtime:

```text
Original PS4 game files
(user-supplied, read-only)
           |
           v
    SELF / ELF loader
           |
           v
 Guest memory and module linker
           |
           v
 PS4 x86-64 guest execution
           |
           v
 PS4 system-service compatibility
           |
           v
 GNM / Liverpool graphics handling
           |
           v
      Vulkan backend
           |
           v
 Windows display, input and audio
```

This diagram represents the intended architecture, not a claim that every component is complete. The loader, compatibility services, guest execution, and graphics pipeline must work together for reliable gameplay.

## Testing and Bug Reports

Community testing can help identify regressions and prioritize fixes.

When reporting an issue, please provide:

- Windows version.
- CPU and GPU.
- GPU driver version.
- Project build or commit.
- Which game you tested: U1, U2, or U3.
- The scene or gameplay section where the issue occurred.
- Steps to reproduce the problem.
- Relevant logs, including `last_run.log` when available.
- Whether the issue occurs consistently or intermittently.

If a particular build includes configuration instructions, follow those instructions before testing. Avoid graphics upscaling options or other settings that are specifically documented as incompatible with that build.

Please distinguish issues observed in this project from issues observed in a reference emulator. This helps keep bug reports relevant and reproducible.

Do not upload copyrighted game files, private keys, or personal information to public issues.

## Development Roadmap

- [x] Begin independent Windows-native runtime research.
- [x] Develop initial guest-runtime and compatibility test infrastructure.
- [ ] Improve executable loading and module initialization.
- [ ] Complete startup-critical PS4 service compatibility.
- [ ] Verify required imports, relocations, and TLS behavior.
- [ ] Establish reliable original-game execution.
- [ ] Improve Uncharted 1 gameplay compatibility.
- [ ] Fix remaining rendering, texture, and collision issues.
- [ ] Improve Uncharted 2 compatibility and stability.
- [ ] Improve Uncharted 3 compatibility and stability.
- [ ] Improve input, audio, cinematics, and save support.
- [ ] Publish reproducible developer builds and compatibility documentation.

Roadmap items describe development goals and may change as new technical issues are discovered. No release date is guaranteed.

## Building from Source

Build instructions depend on the source files, dependencies, build configuration, and backend components available in the repository.

Potential development requirements include:

- Windows 10 or Windows 11, 64-bit.
- Visual Studio and MSVC C++ build tools.
- CMake and CTest.
- Vulkan SDK and a compatible GPU driver.
- Additional libraries and development tools required by the current implementation.

**Check the repository for the actual build files and documented commands before attempting to compile.** A successful compilation does not guarantee that any of the three games will boot or run.

## Game Files and Legal Notice

This project does not intend to distribute proprietary game assets, PS4 game executables, firmware, encryption keys, or other copyrighted Sony or Naughty Dog content.

Users are responsible for obtaining and using their own game files in accordance with applicable law.

This is an independent, unofficial project and is not affiliated with, endorsed by, or sponsored by Sony Interactive Entertainment, Naughty Dog, or PlayStation. *Uncharted*, *The Nathan Drake Collection*, *PlayStation*, and related names are trademarks or property of their respective owners.

## Credits and References

The project draws on public technical research and compatibility work from the wider PS4 emulation and preservation community, including:

- [shadPS4](https://github.com/shadps4-emu/shadPS4) — PS4 compatibility research and graphics implementation reference.
- [Supermedo / bloodborne_pc](https://github.com/Supermedo/bloodborne_pc) — reference for native Windows execution and graphics integration.
- [deadinside28 / bloodborne_pc](https://github.com/deadinside28/bloodborne_pc) — related native-port development reference.

References are provided for attribution and technical context. Their inclusion does not imply that this project is endorsed by those developers or that any particular code is included in this repository.

Third-party code retains its own license requirements. Any code reused or adapted must comply with the applicable license and attribution obligations. Check the repository's license and third-party notices before redistributing source code or binaries.

## Contributing

Bug reports, reproducible test results, technical discussion, and code contributions are welcome through [GitHub Issues](https://github.com/ManoharPadul/uncharted_nathan_drake_collection_pc/issues).

The long-term goal is to build a reliable, reproducible Windows-native compatibility runtime for the original Nathan Drake Collection, progressing toward correct and stable gameplay across all three games.

<p align="center">
  <strong>Independent development. Experimental compatibility. One step closer to Nathan Drake on PC.</strong>
</p>
