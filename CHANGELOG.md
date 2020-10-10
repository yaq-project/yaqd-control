# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

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

[Unreleased]: https://gitlab.com/yaq/yaqd-control/-/compare/v2020.10.0...master
[2020.10.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v2020.07.0...v2020.10.0
[2020.07.1]: https://gitlab.com/yaq/yaqd-control/-/compare/v2020.07.0...v2020.07.1
[2020.07.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v2020.06.0...v2020.07.0
[2020.06.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v2020.05.0...v2020.06.0
[2020.05.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v0.2.0...v2020.05.0
[0.2.0]: https://gitlab.com/yaq/yaqd-control/-/compare/v0.1.1...v0.2.0
[0.1.1]: https://gitlab.com/yaq/yaqd-control/-/compare/v0.1.0...v0.1.1
[0.1.0]: https://gitlab.com/yaq/yaqd-control/-/tags/v0.1.0
