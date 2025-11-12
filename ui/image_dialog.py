# codesnap/ui/image_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox,
    QSpinBox, QCheckBox, QPushButton, QFileDialog, QMessageBox
)
from pygments.styles import get_all_styles
from core.image_generator import generate_image
import os

FONT_PATH = os.path.join("assets", "fonts", "FiraCode-Regular.ttf")

class ImageDialog(QDialog):
    def __init__(self, code, language, parent=None):
        super().__init__(parent)
        self.code = code
        self.language = language
        self.setWindowTitle("Export Code as Image")
        
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.style_combo = QComboBox()
        self.style_combo.addItems(sorted(list(get_all_styles())))
        self.style_combo.setCurrentText("monokai")

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(12, 36)
        self.font_size_spin.setValue(16)
        
        self.line_numbers_check = QCheckBox()
        self.line_numbers_check.setChecked(True)

        form_layout.addRow("Theme:", self.style_combo)
        form_layout.addRow("Font Size:", self.font_size_spin)
        form_layout.addRow("Show Line Numbers:", self.line_numbers_check)
        
        self.export_button = QPushButton("Export to PNG")
        self.export_button.clicked.connect(self.export)

        layout.addLayout(form_layout)
        layout.addWidget(self.export_button)

    def export(self):
        style = self.style_combo.currentText()
        font_size = self.font_size_spin.value()
        line_numbers = self.line_numbers_check.isChecked()

        # Check if the font file exists
        if not os.path.exists(FONT_PATH):
            QMessageBox.critical(self, "Font Not Found", f"The font file was not found at:\n{os.path.abspath(FONT_PATH)}\nPlease add a .ttf font to that location.")
            return

        image = generate_image(self.code, self.language, style, FONT_PATH, font_size, line_numbers)
        
        if image:
            # Open "Save As" dialog
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "code_snippet.png", "PNG Images (*.png)"
            )
            
            if file_path:
                image.save(file_path)
                QMessageBox.information(self, "Success", f"Image saved to {file_path}")
                self.accept() # Close the dialog
        else:
            QMessageBox.critical(self, "Error", "Failed to generate the image.")