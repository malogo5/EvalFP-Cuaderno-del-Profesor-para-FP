# AI Toolkit Architecture Guide

> Version: v0.3
> Last updated: July 2026

---

# 1. Purpose

AI Toolkit is the repository analysis engine used by EvalFP.

Its mission is to analyse a software project once, build a structured knowledge model, and generate multiple AI-oriented documents from that shared model.

The core principle is:

> **Scan once. Analyse once. Generate many.**

---

# 2. Goals

The toolkit aims to:

- Analyse a repository only once.
- Build a reusable knowledge model.
- Generate AI-oriented documentation.
- Avoid duplicated analysis.
- Make future extensions simple and modular.

---

# Architecture Principles

The toolkit is designed around four core ideas:

- Analyse the repository only once.
- Store knowledge in a shared Project model.
- Separate analysis from document generation.
- Prefer composition over duplicated logic.

---

# 3. Non-goals

The toolkit is NOT intended to:

- Build the application.
- Execute project code.
- Replace static analysis tools.
- Fully parse every programming language.
- Become an IDE.

---

# 4. High-Level Architecture

```text
Repository
    │
    ▼
Scanner
    │
    ▼
FileInfo
    │
    ▼
Analyzer
    │
    ▼
Project
    │
    ├── PROJECT_INDEX.md
    ├── CURRENT_CONTEXT.md
    └── Future generators
```

### Current implementation

```text
Scanner
    │
    ▼
Analyzer
    │
    ▼
Project
    │
    ├── PROJECT_INDEX
    └── CURRENT_CONTEXT
```

---

# 5. Components

## Scanner

Responsible for traversing the repository.

Responsibilities:

- Walk the filesystem.
- Ignore excluded folders.
- Detect file language.
- Detect file category.
- Create FileInfo objects.

Scanner must NOT contain project knowledge.

---

## FileInfo

Represents one file.

Current fields:

- path
- relative_path
- name
- parent
- extension
- size
- language
- category

FileInfo only describes a file.

---

## Analyzer

Transforms a collection of FileInfo objects into a Project.

Responsibilities:

- Statistics
- Repository structure
- Documentation
- Configuration
- Technologies
- Future project inference

Analyzer coordinates the analysis.

---

## Detectors

Specialised modules that analyse one file format.

Current detector:

- package_json.py

Future detectors:

- pyproject.py
- requirements.py
- dockerfile.py
- cargo.py
- pom.py

Each detector analyses only one file type.

---

## Project

Represents the knowledge model of the repository.

Current information:

- Repository statistics
- Languages
- Categories
- Directories
- Documentation
- Configuration
- Technologies
- Entry points

Future information:

- Frameworks
- Runtime
- Package manager
- Project type

Project is the single source of truth.

---

## Generators

Transform Project into Markdown documents.

Current generators:

- PROJECT_INDEX
- CURRENT_CONTEXT

Future generators:

- ARCHITECTURE
- API_MAP
- MODULE_SUMMARY
- ONBOARDING
- TECH_DEBT

Generators must never analyse the repository directly.

---

# 6. Data Flow

```text
Repository
      │
      ▼
Scanner
      │
      ▼
FileInfo[]
      │
      ▼
Analyzer
      │
      ▼
Project
      │
      ▼
Generators
      │
      ▼
Markdown
```

---

# 7. Design Principles

## Single Responsibility

Each module has one clear responsibility.

- Scanner scans.
- Analyzer analyses.
- Generators generate.

---

## Shared Knowledge

The repository is analysed only once.

All generators reuse the same Project.

---

## Extensibility

Adding a detector must not require changes to generators.

Adding a generator must not require changes to Scanner.

---

## Predictability

Every generated document must originate from Project.

Analysis logic should never be duplicated.

---

# 8. Directory Structure

```text
tools/ai_toolkit/

scanner.py
analyzer.py
models.py

detectors/

generators/

output/
```

---

# 9. How to Add a Detector

1. Create a new detector.

```text
detectors/my_detector.py
```

2. Analyse a specific file type.
3. Return the detected information.
4. Update the Project through the Analyzer.
5. Reuse that information from generators.

---

# 10. How to Add a Generator

1. Create a new generator.

```text
generators/my_generator.py
```

2. Receive a Project.
3. Generate Markdown.

Generators must never analyse the repository.

---

# 11. Current Status (v0.3)

Implemented:

- Repository Scanner
- Analyzer
- Project model
- package.json detector
- PROJECT_INDEX
- CURRENT_CONTEXT

The toolkit already provides a reusable architecture for future repository intelligence.

---

# 12. Roadmap

## v0.4 – Repository Intelligence

- Detect frameworks.
- Detect runtimes.
- Detect package managers.
- Infer project type.

## v0.5 – Documentation

- Architecture generator.
- API map.
- Module summaries.
- Onboarding documents.

## v1.0 – AI Repository Engine

- Complete repository understanding.
- AI-first documentation.
- Extensible detector ecosystem.

---

# 13. Coding Rules

When extending AI Toolkit:

- Never duplicate repository analysis.
- Reuse information already available in FileInfo.
- Generators must never inspect the filesystem.
- Detectors analyse individual files.
- Analyzer coordinates detectors.
- Project is the single source of truth.
