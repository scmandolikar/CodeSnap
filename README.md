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

---

## 🎯 Use Cases

CodeSnap is ideal for:

- **Technical Writers & Bloggers**: Create professional-looking code images for articles and tutorials
- **Developers**: Manage your personal snippet library offline without relying on cloud services
- **Educators**: Organize teaching materials and create beautiful code examples for presentations
- **Code Reviewers**: Save frequently used code patterns and best practices for reference
- **Interview Preparation**: Store and quickly access commonly asked coding problems and solutions
- **Documentation**: Generate consistent, styled code images for project documentation

---

## 📝 Creating requirements.txt

To ensure all dependencies are installed, create a `requirements.txt` file with the following content:

```txt
PyQt6
Pygments
Pillow
black
jsbeautifier
```

Then install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🔧 How It Works

1. **Add Snippets**: Click "New" to create a snippet, add title, select language, assign tags
2. **Organize**: Use the search bar to filter by title, tag, or language. Mark favorites with a star
3. **Edit & Format**: Use the built-in editor with syntax highlighting. Click "Prettify" to auto-format code
4. **Generate Images**: Click "Generate Image" to export snippets as beautiful PNG files with customizable themes
5. **Database**: All snippets are stored locally in an SQLite database (`snippets.db`) in your project directory

---

## 🚀 Upcoming Features

- [ ] Import/Export functionality for sharing snippet collections
- [ ] Cloud sync option for backup and multi-device access
- [ ] Advanced search with regex support
- [ ] Code snippet versioning and history
- [ ] Custom themes for the image generator
- [ ] Keyboard shortcuts for faster workflow
- [ ] Integration with GitHub Gists
- [ ] Multi-language code snippets in a single card

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

Please ensure your code follows Python best practices and includes appropriate comments.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact & Support

Created by **Sushant Mandolikar**

- **Email**: scmandolikar@gmail.com
- **GitHub**: [@scmandolikar](https://github.com/scmandolikar)
- **LinkedIn**: [Sushant Mandolikar](https://www.linkedin.com/in/sushant-mandolikar-71a519256/)

If you find this project useful, please give it a ⭐ on GitHub!

---

*Built with ❤️ by developers, for developers*
