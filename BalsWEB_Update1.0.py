import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MemeChromium(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and icon
        self.setWindowTitle("MemeChromium Browser")
        self.setGeometry(200, 100, 1000, 600)
        self.setWindowIcon(QIcon('chrome_icon.png'))  # Custom icon can be a meme icon or any image

        # Central widget and layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        # Tab Widget (for multiple tabs like Chrome)
        self.tabs = QTabWidget(self)
        self.layout.addWidget(self.tabs)

        # Initializing the first tab with a web engine view
        self.browser_view = QWebEngineView()

        # Replace this with a valid meme website URL (or a local meme folder)
        try:
            self.browser_view.setUrl("https://www.reddit.com/r/memes/")  # A working meme website
        except Exception as e:
            print(f"Error loading meme website: {e}")
        
        self.tabs.addTab(self.browser_view, "MemeTab")

        # Search bar and buttons
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter meme URL or search...")
        self.layout.addWidget(self.url_input)

        self.search_button = QPushButton("Go", self)
        self.search_button.clicked.connect(self.load_url)
        self.layout.addWidget(self.search_button)

        # Label for displaying the random meme
        self.meme_label = QLabel(self)
        self.layout.addWidget(self.meme_label)

        self.setCentralWidget(self.central_widget)

        # Load a random meme image on startup
        self.load_random_meme()

    def load_url(self):
        url = self.url_input.text()
        if url:
            try:
                self.browser_view.setUrl(url)
            except Exception as e:
                print(f"Error loading URL: {e}")
        
    def load_random_meme(self):
        meme_folder = "memes_folder"  # Replace with the path to your memes folder
        try:
            memes = os.listdir(meme_folder)
            memes = [meme for meme in memes if meme.lower().endswith(('jpg', 'jpeg', 'png', 'gif'))]
            if memes:
                random_meme = random.choice(memes)
                meme_path = os.path.join(meme_folder, random_meme)

                pixmap = QPixmap(meme_path)
                self.meme_label.setPixmap(pixmap)
                self.meme_label.setAlignment(Qt.AlignCenter)
            else:
                print("No meme images found in the folder.")
        except Exception as e:
            print(f"Error loading random meme: {e}")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        # Apply a custom stylesheet to make it look like Chrome but with a unique twist
        app.setStyleSheet("""
            QMainWindow {
                background-color: #F4F4F4;  /* Light background */
                border: 1px solid #CCCCCC;
            }
            QTabWidget::pane {
                background-color: #FFFFFF;
            }
            QLineEdit {
                background-color: white;
                padding: 5px;
                font-size: 14px;
                border: 1px solid #CCCCCC;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                border: 1px solid #CCCCCC;
                padding: 10px;
                background-color: #FFFFFF;
            }
        """)

        window = MemeChromium()
        window.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error initializing application: {e}")
