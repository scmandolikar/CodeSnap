# 📸 CodeSnap: Snippet Manager & Image Generator

CodeSnap is an offline, desktop application for developers to manage reusable code snippets. It combines a powerful organizational tool with a built-in "Carbon-like" image generator to create beautiful, presentation-ready images of your code.

This project solves two common problems: managing a messy library of code snippets and creating professional-looking images of code for documentation, tutorials, or presentations.

---

## ✨ Key Features

* **Offline First:** Your snippets are stored locally in an SQLite database. No internet connection needed.
* **Organize Your Way:**
    * Add/Edit/Delete snippets.
    * Assign titles, languages, and comma-separated tags.
    * Mark your most-used snippets as **Favorites**.
* **Powerful Editor:**
    * Syntax highlighting for multiple languages (Python, JS, HTML, CSS, etc.).
    * Dark-mode editor theme.
    * "Prettify" button to auto-format Python, JS, HTML, and CSS code.
* **Full-Text Search:** Quickly find any snippet by title, tag, or language.
* **"Carbon-Style" Image Generator:**
    * Export any snippet as a high-resolution PNG.
    * Customize the theme from dozens of Pygments styles.
    * Toggle line numbers.
    * Adjust font size.
* **Polished UI:**
    * Clean, two-pane layout.
    * "Copy Code" button for one-click access.
    * Remembers window size and position.
    * Warns you about unsaved changes.

## 🛠️ Tech Stack

* **Language:** Python
* **GUI:** PyQt6
* **Database:** SQLite3 (local)
* **Core Libraries:**
    * `Pygments` for all syntax highlighting.
    * `Pillow` for image creation.
    * `black` and `jsbeautifier` for the "Prettify" feature.

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR-USERNAME/codesnap.git](https://github.com/YOUR-USERNAME/codesnap.git)
    cd codesnap
    ```
2.  **Create a virtual environment and activate it:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file. See below.)*

4.  **Download a font:**
    * This project uses the **Fira Code** font for its beautiful programming ligatures.
    * Download `FiraCode-Regular.ttf` from [Fira Code GitHub Releases](https://github.com/tonsky/FiraCode/releases).
    * Place the `.ttf` file in the `assets/fonts/` directory.

5.  **Run the application:**
    ```bash
    python main.py
    ```