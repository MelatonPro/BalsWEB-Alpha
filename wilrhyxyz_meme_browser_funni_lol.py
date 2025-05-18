import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

class MemeBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Setup
        self.setWindowTitle("WilRhy Funni Browser")
        self.setGeometry(100, 100, 1280, 720)

        # Browser Widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://example.com"))  # Default page
        self.setCentralWidget(self.browser)

        # Navigation Bar
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        # Back Button
        back_btn = QAction("⬅️ Back", self)
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction("➡️ Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction("🔄 Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)

        # Address Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # Meme Easter Eggs
        self.inject_memes()

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def inject_memes(self):
        # Display a meme in the browser title
        self.setWindowTitle("WilRhyXYZ Funni Browser - Aka the worst browser in history")

        # Inject memes into the loading screen
        loading_msg = QLabel("🔥 Loading... but did you know cats can't type? 🐱")
        loading_msg.setAlignment(Qt.AlignCenter)
        self.statusBar().addWidget(loading_msg, 1)

        # Meme on a 404 page
        self.browser.setHtml("""
            <h1 style='text-align:center; color: red;'>404 Error!</h1>
            <p style='text-align:center;'>We couldn't find the page... But here's a very funni meme instead because why not:</p>
            <img src='https://i.imgur.com/vxc1spW.jpeg' style='display:block; margin:auto; max-width:80%;'>
        """)

        # TODO: Add more memes or pull memes dynamically from a folder.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = MemeBrowser()
    browser.show()
    sys.exit(app.exec_())
