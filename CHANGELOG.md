# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- —

### Changed
- —

### Fixed
- —


## [0.1.2] – 2025-07-09

### Changed
- Renamed console-script entry point from `mycli` → `fastdeploy`
  (so commands are now `fastdeploy init`, `fastdeploy build`, etc.)
- Updated documentation, examples, README and help text to use `fastdeploy` instead of `mycli`.


## [0.1.1] – 2025-07-05

### Changed
- Migrated build system from `setup.py` to `pyproject.toml` (PEP 517/518) using setuptools + wheel.
- Added **[project]** metadata, dependencies, and `console_scripts` entry in `pyproject.toml`.


## [0.1.0] – 2025-07-01

### Added
- Initial release of `fastdeploy_cli`.
- **`init`** — verifies prerequisites (AWS CLI v2, Docker, Nixpacks, Copilot), prompts for project config, writes `<project>_fd_config.json`.
- **`build`** — uses Nixpacks to generate and build a Dockerfile, moves it to project root, shows `docker run -p PORT:PORT -it` hint.
- **`deploy`** — generates and runs an AWS Copilot `init … --deploy` script.
- **`purge`** — deletes Copilot app, Nixpacks artifacts, Dockerfile, and config JSON.
