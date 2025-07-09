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

## [0.1.0] – 2025-07-09

### Added
- Initial release of `fastdeploy_cli`.
- `mycli init`
  - Checks AWS CLI (v2), Docker, Nixpacks & AWS Copilot are installed and configured.
  - Prompts user for project/service names, environment, Dockerfile path & port.
  - Writes `_<project>_fd_config.json` with all settings.
- `mycli build`
  - Runs `nixpacks build`, moves generated Dockerfile into project root, and builds final image.
  - Customizes output so that users see the modified `docker run -p PORT:PORT -it` command.
- `mycli deploy`
  - Generates and executes an AWS Copilot `copilot init … --deploy` shell script from your config file.
- `mycli purge`
  - Optionally force-deletes AWS Copilot app, Nixpacks files, Dockerfile, and config JSON.

### Changed
- —

### Fixed
- —

---

### How to release a new version

1. Bump the version in `pyproject.toml` under `[project] → version`.
2. Add an entry under **[Unreleased]** for that new version, date & changes.
3. Commit and tag:
   ```bash
   git commit -am "chore: prepare 0.1.1 release"
   git tag v0.1.1
   git push && git push --tags
