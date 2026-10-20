# Research Delta - Desktop and local-first delivery

Review date: 2026-10-19
Owner: desktop-platform
Outcome: recommendation changed
Confidence: high

## Source changes

- Reviewed Tauri 2.12: <https://v2.tauri.app/blog/tauri-2.12/>.
- Reviewed Electron 44: <https://www.electronjs.org/blog/electron-44-0>.

## Decision

Tauri remains attractive for smaller native bundles, but Windows 7 support is no longer an admissible assumption and its newer Rust/Android toolchain floor must be planned. Electron remains appropriate when Chromium/Node consistency is worth the footprint; Electron 44 changes clipboard APIs toward asynchronous W3C semantics and requires migration review.

## Follow-up

- Keep updater, signing, OS-support, and clipboard behavior explicit in desktop architecture decisions.
