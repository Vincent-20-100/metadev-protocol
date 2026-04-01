# 📜 MetaDev Protocol - Core Rules

## 🌌 Vision
Strict separation between **Product Artifacts** (src, docs, tests) and **Meta-Development Context** (.meta/).

## 🚦 Operational Rules
1. **The .meta/ Sanctuary**: Never pollute the root or `src/` with temporary thoughts, scratch files, or session notes. Everything "in-flight" goes to `.meta/`.
2. **Pilot-Led Development**: Every session begins by reading `.meta/PILOT.md`.
3. **Maturation Pipeline**: 
   - Idea -> `.meta/scratch/`
   - Validation -> `tests/`
   - Production -> `src/`

## 🛠 Tech Stack (Foundational)
- **Tooling**: uv (package management), Copier (templating).
- **Quality**: Ruff (linting), Pytest (testing).