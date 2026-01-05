# Changelog

All notable changes to Waft will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2026-01-05

### Added
- Initial release of Waft framework
- `waft new <name>` command to create new projects with full structure
- `waft verify` command to verify project structure
- Automatic `_pyrite` folder structure creation (active/, backlog/, standards/)
- Template generation for:
  - Justfile with standard recipes
  - GitHub Actions CI workflow
  - CrewAI agents starter template
- Full `uv` integration for Python project management
- SubstrateManager for environment management
- MemoryManager for `_pyrite` structure management
- TemplateWriter for project scaffolding

[0.0.1]: https://github.com/ctavolazzi/waft/releases/tag/v0.0.1

