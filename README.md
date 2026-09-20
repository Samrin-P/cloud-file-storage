# CloudFileStorage - Flask Engineering Log

This is a local web application built to handle user registration, user logins, and isolated file management. I built this project to move away from generic tutorials and get my hands dirty with real-world state management, request contexts, and relational databases using Python and Flask.

## The Tech Behind It
* **Backend:** Python 3 (Structured entirely inside an isolated `venv` workspace)
* **Framework:** Flask (Leveraging dynamic routing, templates, and request handlers)
* **Database:** SQLite3 (Local file-based SQL storage tracking user credentials)

---

## Real Engineering Challenges & How I Solved Them

Building this wasn’t just smooth sailing. Here are the core technical blockers I ran into during development and how I engineered my way around them:

### 1. Managing Flask Contexts & NameErrors
During early route building for user logins, the application crashed frequently with `NameError: name 'redirect' is not defined`. 
* **The Root Cause:** I was trying to leverage Flask utilities across split routing logic without explicit dependency declaration.
* **The Fix:** Re-architected the main workspace initialization file (`app.py`) to tightly bundle the core app lifecycle decorators: `from_flask import Flask, redirect, url_for, render_template, request`.

### 2. Broken File Templates (`TemplateNotFound`)
At one point, the server completely refused to render my HTML pages (`dashboard.html`, `index.html`), throwing critical routing exceptions.
* **The Root Cause:** My project architecture layout was misaligned. The HTML files were loose in the wrong directories, causing Flask's template finder engine to fail.
* **The Fix:** I restructured the project root. I moved all visual layouts strictly inside a root-level `templates/` folder, placed asset uploads inside an `uploads/` bucket directory, and pushed my `.gitignore` out to the root to keep the virtual environment from dirtying the Git tree.

### 3. Dynamic File Downloading vs. Static Strings
I wanted users to be able to download files from their dashboard. My first attempt hardcoded structural file routes like `@app.route("/download/<sample_database.xlsx>")`, which threw syntax routing exceptions because of the literal dot extension.
* **The Fix:** I refactored the endpoint to use a fully dynamic URL variable mapping block (`/download/<filename>`). This captures the targeted string explicitly and forwards it to Flask's native `send_from_directory` utility, enabling safe downloading for *any* type of file attachment.

---

## How to Spin This Up Locally

1. Clear your local tree, open your terminal, and activate your Windows environment shell:
   ```powershell
   .\venv\Scripts\activate
   ```
2. Make sure Flask is installed in your local runtime instance:
   ```bash
   pip install flask
   ```
3. Initialize the local database and launch the dev server thread:
   ```bash
   python app.py
   ```
4. Fire up your browser and point it to: `http://127.0.0`
