import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

class MemeBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Setup
        self.setWindowTitle("BalsWEB - Probably the most not funny browser but its trying its best :(")
        self.setGeometry(100, 100, 1280, 720)

        # Central Widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.new_tab)
        self.setCentralWidget(self.tabs)

        # Create First Tab
        self.new_tab()

        # Navigation Bar
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        # Back Button
        back_btn = QAction("⬅️ Back (you know this)", self)
        back_btn.triggered.connect(self.navigate_back)
        nav_bar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction("➡️ Forward (YOU ALSO KNOW THIS)", self)
        forward_btn.triggered.connect(self.navigate_forward)
        nav_bar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction("🔄 Reload (if the site stats are bad or whatever reason)", self)
        reload_btn.triggered.connect(self.reload_page)
        nav_bar.addAction(reload_btn)

        # New Tab Button
        new_tab_btn = QAction("➕ im guessing you know this button but its, New Tab", self)
        new_tab_btn.triggered.connect(self.new_tab)
        nav_bar.addAction(new_tab_btn)

        # Address Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        # Inject Memes and Fun Features
        self.inject_memes()

    def new_tab(self, *args):
        browser = QWebEngineView()
        browser.setUrl(QUrl("https://www.melaton.pro/balsweb/balsweb-opened"))  # Default start page
        browser.urlChanged.connect(lambda q, b=browser: self.update_url(q, b))
        i = self.tabs.addTab(browser, "New Tab 🐸")
        self.tabs.setCurrentIndex(i)

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, q, browser):
        if self.current_browser() == browser:
            self.url_bar.setText(q.toString())
            self.tabs.setTabText(self.tabs.currentIndex(), q.host())

    def navigate_back(self):
        self.current_browser().back()

    def navigate_forward(self):
        self.current_browser().forward()

    def reload_page(self):
        self.current_browser().reload()

    def current_browser(self):
        return self.tabs.currentWidget()

    def inject_memes(self):
        # Change Window Icon to a Meme
        self.setWindowIcon(QIcon("https://i.imgur.com/4Z6z9T5.jpeg"))

        # Add Easter Egg Meme
        self.statusBar().showMessage("🔥 Did you know? Memes are love, memes are life. 🐸")

        # TODO: Load memes dynamically or customize error pages.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = MemeBrowser()
    browser.show()
    sys.exit(app.exec_())
