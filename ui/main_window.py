# codesnap/ui/main_window.py

import subprocess
import jsbeautifier
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QTextEdit, QLineEdit, QPushButton,
    QSplitter, QFormLayout, QLabel, QComboBox, QListWidgetItem, QMessageBox,
    QStatusBar, QApplication, QStyle
)
from PyQt6.QtCore import Qt, QSize, QSettings # <-- TIER 3: Import QSettings
from PyQt6.QtGui import QFont, QKeySequence, QShortcut, QPalette, QColor
from core.syntax_highlighter import SyntaxHighlighter
import database_manager as db
from .image_dialog import ImageDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeSnap - Snippet Manager")
        
        # --- TIER 3: Dirty flag to track unsaved changes ---
        self.is_dirty = False

        self.current_snippet_id = None
        self.favorites_only = False

        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready", 3000)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        self.splitter = QSplitter(Qt.Orientation.Horizontal) # Use self.splitter to access it later
        main_layout.addWidget(self.splitter)

        # --- Left Panel ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        # ... (rest of left panel is the same)
        search_filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search snippets...")
        self.search_input.textChanged.connect(self.search_snippets)
        
        self.favorites_button = QPushButton("★")
        self.favorites_button.setToolTip("Show only favorites")
        self.favorites_button.setCheckable(True)
        self.favorites_button.clicked.connect(self.filter_favorites)
        self.favorites_button.setFixedWidth(40)
        
        search_filter_layout.addWidget(self.search_input)
        search_filter_layout.addWidget(self.favorites_button)
        
        self.snippet_list = QListWidget()
        self.snippet_list.currentItemChanged.connect(self.load_snippet)

        left_layout.addLayout(search_filter_layout)
        left_layout.addWidget(self.snippet_list)

        # --- Right Panel ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        title_layout = QHBoxLayout()
        self.title_input = QLineEdit()
        
        self.favorite_toggle_button = QPushButton("☆")
        self.favorite_toggle_button.setToolTip("Mark as favorite")
        self.favorite_toggle_button.setCheckable(True)
        self.favorite_toggle_button.clicked.connect(self.toggle_favorite)
        self.favorite_toggle_button.setVisible(False)
        self.favorite_toggle_button.setFixedWidth(40)
        
        title_layout.addWidget(QLabel("Title:"))
        title_layout.addWidget(self.title_input)
        title_layout.addWidget(self.favorite_toggle_button)

        details_form = QWidget()
        form_layout = QFormLayout(details_form)
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        self.language_input = QComboBox()
        self.language_input.addItems(['python', 'javascript', 'sql', 'html', 'css', 'bash', 'text'])
        self.tags_input = QLineEdit()
        form_layout.addRow(QLabel("Language:"), self.language_input)
        form_layout.addRow(QLabel("Tags (comma-separated):"), self.tags_input)

        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont("Fira Code", 12)) 
        self.code_editor.setTabStopDistance(28) 
        
        palette = self.code_editor.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#272822"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#F8F8F2"))
        self.code_editor.setPalette(palette)

        self.highlighter = SyntaxHighlighter(self.code_editor.document(), language='python', style='monokai')
        self.language_input.currentTextChanged.connect(lambda lang: self.highlighter.set_language(lang))

        # --- TIER 3: Connect signals to set the dirty flag ---
        self.title_input.textChanged.connect(self.set_dirty)
        self.tags_input.textChanged.connect(self.set_dirty)
        self.language_input.currentTextChanged.connect(self.set_dirty)
        self.code_editor.textChanged.connect(self.set_dirty)

        button_layout = QHBoxLayout()
        
        style = self.style()
        self.new_button = QPushButton(style.standardIcon(QStyle.StandardPixmap.SP_FileIcon), "New")
        self.save_button = QPushButton(style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), "Save")
        self.delete_button = QPushButton(style.standardIcon(QStyle.StandardPixmap.SP_TrashIcon), "Delete")
        
        self.copy_button = QPushButton("Copy Code")
        self.prettify_button = QPushButton("Prettify")
        self.export_button = QPushButton("Export as Image...")

        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.prettify_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.export_button)

        self.new_button.clicked.connect(self.new_snippet)
        self.save_button.clicked.connect(self.save_snippet)
        self.delete_button.clicked.connect(self.delete_snippet)
        self.prettify_button.clicked.connect(self.prettify_code)
        self.copy_button.clicked.connect(self.copy_code_to_clipboard)
        self.export_button.clicked.connect(self.open_export_dialog)
        
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_snippet)

        right_layout.addLayout(title_layout)
        right_layout.addWidget(details_form)
        right_layout.addWidget(self.code_editor)
        right_layout.addLayout(button_layout)
        
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        
        # --- TIER 3: Restore window geometry and splitter state ---
        self.settings = QSettings("CodeSnap", "SnippetManager")
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        splitter_state = self.settings.value("splitterState")
        if splitter_state:
            self.splitter.restoreState(splitter_state)
        else:
            self.splitter.setSizes([300, 900]) # Default fallback

        self.refresh_snippet_list()

    # --- TIER 3: Override the closeEvent to handle saving settings and checking for unsaved changes ---
    def closeEvent(self, event):
        if self.check_for_unsaved_changes():
            # Save settings before closing
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.setValue("splitterState", self.splitter.saveState())
            event.accept()  # Proceed with closing
        else:
            event.ignore()  # Cancel the close event

    # --- TIER 3: Methods to manage the dirty state ---
    def set_dirty(self, dirty=True):
        self.is_dirty = dirty
        # Add an asterisk to the window title to indicate unsaved changes
        title = self.windowTitle()
        if dirty and not title.endswith("*"):
            self.setWindowTitle(title + "*")
        elif not dirty and title.endswith("*"):
            self.setWindowTitle(title[:-1])

    def check_for_unsaved_changes(self):
        if not self.is_dirty:
            return True # Proceed, no changes to save

        # Pop up a message box
        msg_box = QMessageBox()
        msg_box.setText("You have unsaved changes.")
        msg_box.setInformativeText("Do you want to save your changes?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Save |
                                   QMessageBox.StandardButton.Discard |
                                   QMessageBox.StandardButton.Cancel)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Save)
        
        ret = msg_box.exec()

        if ret == QMessageBox.StandardButton.Save:
            self.save_snippet()
            return True # Proceed
        elif ret == QMessageBox.StandardButton.Discard:
            return True # Proceed
        else: # Cancel
            return False # Stop the original action

    # ... all other functions from here on are updated to call set_dirty(False) after key actions ...

    def refresh_snippet_list(self):
        # ... (unchanged)
        current_id_to_preserve = self.current_snippet_id
        self.snippet_list.currentItemChanged.disconnect(self.load_snippet)
        self.snippet_list.clear()
        
        snippets = db.get_favorite_snippets() if self.favorites_only else db.get_all_snippets()
            
        item_to_select = None
        for snippet in snippets:
            title = f"★ {snippet['title']}" if snippet['is_favorite'] else snippet['title']
            item = QListWidgetItem(title)
            item.setData(Qt.ItemDataRole.UserRole, snippet['id'])
            self.snippet_list.addItem(item)
            if snippet['id'] == current_id_to_preserve:
                item_to_select = item

        self.snippet_list.currentItemChanged.connect(self.load_snippet)
        
        if item_to_select:
            self.snippet_list.setCurrentItem(item_to_select)

    def search_snippets(self):
        # ... (unchanged)
        query = self.search_input.text()
        self.snippet_list.currentItemChanged.disconnect(self.load_snippet)
        self.snippet_list.clear()

        snippets = db.search_snippets(query, self.favorites_only)

        for snippet in snippets:
            title = f"★ {snippet['title']}" if snippet['is_favorite'] else snippet['title']
            item = QListWidgetItem(title)
            item.setData(Qt.ItemDataRole.UserRole, snippet['id'])
            self.snippet_list.addItem(item)
        
        self.snippet_list.currentItemChanged.connect(self.load_snippet)

    def load_snippet(self, current_item, previous_item):
        # --- MODIFIED --- to check for unsaved changes before loading
        if not self.check_for_unsaved_changes():
            # Reselect the previous item to cancel the change
            if previous_item:
                self.snippet_list.setCurrentItem(previous_item)
            return

        if not current_item:
            self.new_snippet(check_save=False) # Don't check again
            return
        
        snippet_id = current_item.data(Qt.ItemDataRole.UserRole)
        self.current_snippet_id = snippet_id
        snippet = db.get_snippet_by_id(snippet_id)
        
        if snippet:
            self.favorite_toggle_button.setVisible(True)
            self.favorite_toggle_button.setChecked(snippet['is_favorite'])
            self.favorite_toggle_button.setText("★" if snippet['is_favorite'] else "☆")
            
            self.title_input.setText(snippet['title'])
            self.language_input.setCurrentText(snippet['language'])
            self.tags_input.setText(snippet['tags'])
            self.code_editor.setPlainText(snippet['code'])
            self.highlighter.set_language(snippet['language'])
            
            self.set_dirty(False) # Mark as clean after loading

    def new_snippet(self, check_save=True):
        if check_save and not self.check_for_unsaved_changes():
            return

        self.snippet_list.clearSelection()
        self.current_snippet_id = None
        self.title_input.clear()
        self.language_input.setCurrentIndex(0) 
        self.tags_input.clear()
        self.code_editor.clear()
        self.highlighter.set_language('python')
        self.favorite_toggle_button.setVisible(False)
        self.title_input.setFocus()
        self.set_dirty(False) # Mark as clean

    def save_snippet(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Missing Title", "Please provide a title.")
            return

        language = self.language_input.currentText()
        tags = self.tags_input.text().strip()
        code = self.code_editor.toPlainText()

        if self.current_snippet_id:
            db.update_snippet(self.current_snippet_id, title, language, tags, code)
        else:
            db.add_snippet(title, language, tags, code)
        
        self.set_dirty(False) # Mark as clean after saving
        self.refresh_snippet_list()
        self.statusBar().showMessage(f"Snippet '{title}' saved!", 3000)

    def delete_snippet(self):
        if not self.current_snippet_id: return
        title = self.title_input.text()
        if QMessageBox.question(self, 'Delete', f"Delete '{title}'?") == QMessageBox.StandardButton.Yes:
            db.delete_snippet(self.current_snippet_id)
            self.new_snippet(check_save=False) # Don't check for save, we just deleted it
            self.refresh_snippet_list()
            self.statusBar().showMessage(f"Snippet '{title}' deleted.", 3000)

    def toggle_favorite(self):
        # ... (unchanged)
        if not self.current_snippet_id: return
        new_status = db.toggle_favorite_status(self.current_snippet_id)
        self.favorite_toggle_button.setChecked(new_status)
        self.favorite_toggle_button.setText("★" if new_status else "☆")
        self.refresh_snippet_list()
        self.statusBar().showMessage("Favorite status changed.", 2000)

    def filter_favorites(self):
        # ... (unchanged)
        self.favorites_only = self.favorites_button.isChecked()
        if self.favorites_only:
            self.favorites_button.setStyleSheet("color: gold;")
            self.favorites_button.setToolTip("Show all snippets")
        else:
            self.favorites_button.setStyleSheet("")
            self.favorites_button.setToolTip("Show only favorites")
        self.refresh_snippet_list()

    def prettify_code(self):
        # ... (unchanged, but will now set the dirty flag)
        language = self.language_input.currentText()
        source_code = self.code_editor.toPlainText()

        if not source_code.strip():
            self.statusBar().showMessage("Nothing to prettify.", 3000)
            return
        
        try:
            formatted_code = ""
            if language == 'python':
                result = subprocess.run(
                    ['black', '-q', '-'], 
                    input=source_code, 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                formatted_code = result.stdout
            
            elif language in ['javascript', 'html', 'css']:
                opts = jsbeautifier.default_options()
                opts.indent_size = 2
                opts.preserve_newlines = True
                opts.max_preserve_newlines = 2
                opts.wrap_line_length = 100

                if language == 'javascript':
                    formatted_code = jsbeautifier.beautify(source_code, opts)
                elif language == 'html':
                    formatted_code = jsbeautifier.beautify_html(source_code, opts)
                elif language == 'css':
                    formatted_code = jsbeautifier.beautify_css(source_code, opts)
            
            else:
                self.statusBar().showMessage(f"No prettifier available for '{language}'.", 3000)
                return
            
            if formatted_code and formatted_code != source_code:
                self.code_editor.setPlainText(formatted_code)
                self.statusBar().showMessage("Code prettified successfully!", 3000)
                # Prettifying counts as a change
                self.set_dirty()

        except subprocess.CalledProcessError as e:
            self.statusBar().showMessage("Black formatter failed: Code may have a syntax error.", 5000)
            print(f"Black formatter error: {e.stderr}")
        except FileNotFoundError:
            self.statusBar().showMessage("Error: 'black' is not installed or not in your PATH.", 5000)
        except Exception as e:
            self.statusBar().showMessage(f"An error occurred during formatting: {e}", 5000)
            print(f"Formatting error: {e}")

    def copy_code_to_clipboard(self):
        # ... (unchanged)
        code = self.code_editor.toPlainText()
        if not code:
            self.statusBar().showMessage("Nothing to copy.", 3000)
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(code)
        self.statusBar().showMessage("Code copied to clipboard!", 3000)

    def open_export_dialog(self):
        # ... (unchanged)
        code = self.code_editor.toPlainText()
        if not code:
            QMessageBox.warning(self, "No Code", "There's no code to export as an image.")
            return
        language = self.language_input.currentText()
        dialog = ImageDialog(code, language, self)
        dialog.exec()