import sys
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


class MemeChromium(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Setup
        self.setWindowTitle("BalsWEB - Probably the most not funny browser but its trying its best :(")
        self.setGeometry(100, 100, 1280, 720)

        # Central Widget: Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.new_tab)
        self.setCentralWidget(self.tabs)

        # Load Startup Website
        self.startup_url = "https://www.melaton.pro/balsweb/balsweb-opened"  # Change to your startup website
        self.new_tab_url = "https://www.melaton.pro/balsweb/newtab"  # Change to your new tab website
        self.load_startup_page()

        # Navigation Bar
        self.nav_bar = QToolBar("Navigation")
        self.nav_bar.setIconSize(QSize(24, 24))
        self.addToolBar(self.nav_bar)

        # Add Navigation Buttons
        self.add_nav_buttons()

        # Inject Memes
        self.inject_memes()

    def load_startup_page(self):
        # Load the startup page in the first tab
        browser = QWebEngineView()
        browser.setUrl(QUrl(self.startup_url))
        browser.urlChanged.connect(lambda q, b=browser: self.update_url(q, b))
        i = self.tabs.addTab(browser, "Home")
        self.tabs.setCurrentIndex(i)

    def new_tab(self, *args):
        # Create a new tab with the new tab URL
        browser = QWebEngineView()
        browser.setUrl(QUrl(self.new_tab_url))
        browser.urlChanged.connect(lambda q, b=browser: self.update_url(q, b))
        i = self.tabs.addTab(browser, "New Tab 🐸")
        self.tabs.setCurrentIndex(i)

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def add_nav_buttons(self):
        # Back Button
        back_btn = QAction(QIcon("https://img.icons8.com/ios-filled/50/back.png"), "Back", self)
        back_btn.triggered.connect(self.navigate_back)
        self.nav_bar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction(QIcon("https://img.icons8.com/ios-filled/50/forward.png"), "Forward", self)
        forward_btn.triggered.connect(self.navigate_forward)
        self.nav_bar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction(QIcon("https://img.icons8.com/ios-filled/50/refresh.png"), "Reload", self)
        reload_btn.triggered.connect(self.reload_page)
        self.nav_bar.addAction(reload_btn)

        # Home Button
        home_btn = QAction(QIcon("https://img.icons8.com/ios-filled/50/home.png"), "Home", self)
        home_btn.triggered.connect(self.go_home)
        self.nav_bar.addAction(home_btn)

        # Address Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_bar.addWidget(self.url_bar)

        # New Tab Button
        new_tab_btn = QAction(QIcon("https://img.icons8.com/ios-filled/50/add-tab.png"), "New Tab", self)
        new_tab_btn.triggered.connect(self.new_tab)
        self.nav_bar.addAction(new_tab_btn)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, q, browser):
        if self.current_browser() == browser:
            self.url_bar.setText(q.toString())
            self.tabs.setTabText(self.tabs.currentIndex(), q.host() or "New Tab 🐸")

    def navigate_back(self):
        self.current_browser().back()

    def navigate_forward(self):
        self.current_browser().forward()

    def reload_page(self):
        self.current_browser().reload()

    def go_home(self):
        self.current_browser().setUrl(QUrl(self.startup_url))

    def current_browser(self):
        return self.tabs.currentWidget()

    def inject_memes(self):
        # Custom Window Icon
        self.setWindowIcon(QIcon("https://i.imgur.com/4Z6z9T5.jpeg"))

        # Status Bar Meme
        self.statusBar().showMessage("🔥 Memes incoming... Stay tuned! 🐸")

        # Meme Button
        meme_action = QAction("Random Meme 🐸", self)
        meme_action.triggered.connect(self.show_meme)
        self.nav_bar.addAction(meme_action)

    def show_meme(self):
        memes = [
            "https://i.imgur.com/4Z6z9T5.jpeg",  # Meme 1
            "https://i.imgur.com/ZL4DzM8.jpeg",  # Meme 2
            "https://i.imgur.com/3jN0XjQ.jpeg",  # Meme 3
        ]
        random_meme = random.choice(memes)
        self.current_browser().setHtml(f"""
            <html>
            <body style="text-align: center; background-color: #222; color: white;">
                <h1>Random Meme Generator</h1>
                <img src="{random_meme}" style="max-width: 90%; max-height: 80vh;">
                <p><a href="{random_meme}" style="color: yellow;">Click here for the source</a></p>
            </body>
            </html>
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    browser = MemeChromium()
    browser.show()
    sys.exit(app.exec_())
