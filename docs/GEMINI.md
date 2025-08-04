# Gemini Context: LCPI-CLI Project

## Project Overview

This directory contains the `lcpi-core` project, a versatile command-line platform for engineering calculations. The system is built in Python and uses a modular, plugin-based architecture to support various engineering domains like steel construction (`cm`), wood (`bois`), concrete (`beton`), and sanitation (`assainissement`).

The core application provides the main entry point (`lcpi`), a plugin manager, a reporting engine, and other shared utilities. Each plugin operates as a semi-autonomous module with its own specific commands and calculation logic. Project and calculation parameters are primarily defined in YAML (`.yml`) files.

**Key Technologies:**
*   **Language:** Python 3.8+
*   **CLI Framework:** Typer
*   **Configuration:** YAML
*   **Key Libraries:** pandas, reportlab, Jinja2, rich, cryptography

## Building and Running

### Installation
The project uses a custom installation script that handles dependency installation (online/offline) and sets up the core in editable mode.

*   **Run installation:**
    ```bash
    install.bat
    ```
    or
    ```bash
    python scripts/install_and_run_lcpi_core.py
    ```

### Common Commands

*   **Initialize a new project:**
    ```bash
    lcpi init <project_name> --template <template_name>
    ```
    *Example:* `lcpi init my_project --template complet`

*   **Check system configuration:**
    ```bash
    lcpi doctor
    ```

*   **Manage plugins:**
    *   List plugins: `lcpi plugins list`
    *   Install a plugin: `lcpi plugins install <plugin_name>`
    *   Uninstall a plugin: `lcpi plugins uninstall <plugin_name>`

*   **Run a calculation:**
    Calculations are run via plugins on specific YAML definition files.
    *Example:* `lcpi beton calc-poteau data/beton/poteau_exemple.yml`

*   **Generate a project report:**
    The `report` command scans the project, runs all relevant calculations, and generates a summary PDF.
    ```bash
    lcpi report .
    ```

## Development Conventions

*   **Plugin-based Architecture:** New functionalities should be added within plugins. Each plugin resides in `src/lcpi/plugins/` and contains its own command structure and business logic.
*   **YAML for Data:** All input data for calculations (e.g., beam dimensions, material properties) is defined in `.yml` files.
*   **Structured Output:** Plugins should support a `--json` flag to output results in a structured format for inter-process communication, particularly for the reporting engine.
*   **Interactive Mode:** Major plugins are expected to have an `interactive` command for a guided user experience.

## Project History (Summary from Journal de Bord)

*   **Phase 1 (Foundation):** The initial project structure (`lcpi_platform`), core (`lcpi-core`), and plugin skeletons were created.
*   **Phase 4 (Plugin Migration):** Business logic from the old `nanostruct` project was migrated into the new "pure" functions within the `cm`, `bois`, `beton`, and `assainissement` plugins. The `calc` and `check` commands were made functional.
*   **Chantier 2 (Reporting Engine):** A `lcpi report` command was created to scan project files, execute calculations, and generate a unified PDF report using JSON-formatted outputs from the plugins.
*   **Chantier 3 (Feature Expansion):** Existing logic for concrete slabs (`radiers`) was integrated into the `beton` plugin.
*   **Chantier 4 (Interactive Mode):** Interactive command-line modes were implemented for the `cm`, `bois`, and `beton` plugins.
*   **Chantier 5 (Core Launcher):** The startup process was refined to be cleaner. The core can now start without plugins, which must be explicitly installed by the user, making the initial experience more modular.
