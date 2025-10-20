# Project Chronology: CV Manager

This document outlines the development history of the CV Manager project, highlighting key changes and the reasoning behind them.

## Phase 1: Initial Setup and Core Functionality (2025-10-18)

*   **Commit `7afdb5b`**: The project was initialized with a basic structure. The initial focus was on creating a system to manage CV data in a structured format (JSON) and generate different CV versions from it.

*   **Commit `e5e7f2b`**: This phase saw the addition of several key features:
    *   **Data Importers**: `linkedin_importer.py` and `orcid_importer.py` were created to pull data from external sources, reducing manual data entry.
    *   **Comprehensive CV Generator**: `comprehensive_cv_generator.py` was added to consolidate data from various sources into a master JSON file.
    *   **Advanced Features**: The project expanded to include functionalities like publication metrics tracking, cover letter generation, and application tracking.

## Phase 2: Refactoring and PDF Generation (2025-10-20)

*   **Commit `cce65e6`**: A major overhaul of the project structure and CV generation process.
    *   **Motivation**: The initial scripts were becoming difficult to manage. A more modular and robust approach was needed.
    *   **Changes**:
        *   The CV generation logic was consolidated and improved.
        *   A key feature was added: `cv_pdf_generator.py`, which automates the creation of multiple CV versions in PDF format, tailored for different purposes (e.g., research, industry, academic, technical).
        *   The project structure was reorganized for better clarity and maintainability.

## Phase 3: Git Repository Cleanup and Documentation (2025-10-20)

*   **Commit `49218ae`**: This commit focused on preparing the project for public release on GitHub.
    *   **Motivation**: Private and intermediate files were unintentionally tracked in the Git repository. These needed to be removed to ensure only public assets were shared.
    *   **Changes**:
        *   Sensitive files like `cover_letter_consulting.pdf`, and older CV versions were removed from the Git history.
        *   The `.gitignore` file was updated to prevent similar files from being tracked in the future.

*   **Post-commit cleanup (not yet committed)**:
    *   **Motivation**: To further organize the project and separate intermediate files from the main codebase.
    *   **Changes**:
        *   An `intermediate_files/` directory was created to store temporary files, build artifacts, and other non-essential data.
        *   This directory was added to `.gitignore`.
        *   Various intermediate files were moved into this new directory, cleaning up the root project folder.
        *   The `.gitignore` file was updated to remove now-redundant entries.
