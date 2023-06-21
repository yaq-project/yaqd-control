# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Changed
- Upgraded appdirs to platformdirs
- Warn for unexpected characters in daemon names

### [2022.4.0]

### Fixed
- fixed bug where edit-config did not correctly call certain `%EDITOR%`s on Windows

### [2021.10.0]

### Changed
- pinned to toml>=0.10.2 for type stubs
- Use `rich` for `yaqd status` table with live updating and parallel queries

## [2021.5.0]

### Fixed
- bug with spaces in usernames on Windows
- Execution of commands on powershell, for which `where.exe` was hidden by the shell

### Added
- new option --debug to all commands
- pass-through for nssm
- new --format flag on list: supports json and toml output
- happi support also via yaqd list -f happi
- enhancement for daemon inputs: yaqd-daemon and daemon both valid inputs

## [2020.10.0]

### Added
- enablement: MacOS support

### Fixed
- proper handling of executable discovery on Windows

## [2020.07.1]

### Changed
- Distribute with `-` instead of `_`

## [2020.07.0]

### Fixed
- Correct python version supported (>=3.7)

## [2020.06.0]

### Changed
- migrated to flit build system
- now use yaqc-python rather than implementing custom rpc calls

## [2020.05.0]

### Added
- support for edit-config with notepad on Windows
- new documentation at https://control.yaq.fyi

### Changed
- pin msgpack version above 1.0
- from now on, yaqd-control will used date based versioning
- Includes nssm when built on Windows (not dependent on passing arguments)
- refactored ci

## [0.2.0]

### Added
- make version option avaliable

### Changed
- build separate wheel with NSSM for windows, do not ship in generic wheel
- switch to msgpack from JSON, see [YEP-100](https://yeps.yaq.fyi/100/)

## [0.1.1]

### Added
- gitlab ci
- mypy

### Changed
- manifest file: license actually distributed

## [0.1.0]

### Added
- initial release

[Unreleased]: https://gitlab.com/yaq/yaqd-control/-/compare/v2022.4.0...main
[2022.4.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v2021.10.0...v2022.4.0
[2021.10.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v2021.5.0...v2021.10.0
[2021.5.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v2020.10.0...v2021.5.0
[2020.10.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v2020.07.0...v2020.10.0
[2020.07.1]: https://gitlab.com/yaq/yaqd-control/-/compare/v2020.07.0...v2020.07.1
[2020.07.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v2020.06.0...v2020.07.0
[2020.06.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v2020.05.0...v2020.06.0
[2020.05.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v0.2.0...v2020.05.0
[0.2.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v0.1.1...v0.2.0
[0.1.1]: https://gitlab.com/yaq/yaqd-control/-/compare/v0.1.0...v0.1.1
[0.1.0]: https://gitlab.com/yaq/yaqd-control/-/tags/v0.1.0
