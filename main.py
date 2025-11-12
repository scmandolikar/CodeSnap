# codesnap/main.py

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
import database_manager as db

def main():
    # Initialize the database
    db.initialize_db()
    
    # Create and run the application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()