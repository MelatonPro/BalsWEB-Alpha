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

        # Create the first tab
        self.new_tab()

        # Navigation Bar
        self.nav_bar = QToolBar("Navigation")
        self.nav_bar.setIconSize(QSize(24, 24))
        self.addToolBar(self.nav_bar)

        # Navigation Buttons
        self.add_nav_buttons()

        # Settings Menu
        self.menu_bar = self.menuBar()
        self.settings_menu = self.menu_bar.addMenu("⚙️ Settings")
        self.add_settings_menu()

        # Meme Features
        self.inject_memes()

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

    def add_settings_menu(self):
        # Set Custom Homepage
        set_homepage_action = QAction("Set Custom Homepage", self)
        set_homepage_action.triggered.connect(self.set_custom_homepage)
        self.settings_menu.addAction(set_homepage_action)

        # Reset to Default Homepage
        reset_homepage_action = QAction("Reset Homepage", self)
        reset_homepage_action.triggered.connect(self.reset_homepage)
        self.settings_menu.addAction(reset_homepage_action)

    def new_tab(self, *args):
        browser = QWebEngineView()
        browser.setUrl(QUrl("https://example.com"))  # Default page
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
            self.tabs.setTabText(self.tabs.currentIndex(), q.host() or "New Tab 🐸")

    def navigate_back(self):
        self.current_browser().back()

    def navigate_forward(self):
        self.current_browser().forward()

    def reload_page(self):
        self.current_browser().reload()

    def go_home(self):
        home_url = QSettings("MemeChromium", "Settings").value("homepage", "https://example.com")
        self.current_browser().setUrl(QUrl(home_url))

    def current_browser(self):
        return self.tabs.currentWidget()

    def set_custom_homepage(self):
        text, ok = QInputDialog.getText(self, "Set Homepage", "Enter your custom homepage URL:")
        if ok and text:
            QSettings("MemeChromium", "Settings").setValue("homepage", text)
            QMessageBox.information(self, "Homepage Set", f"Custom homepage set to: {text}")

    def reset_homepage(self):
        QSettings("MemeChromium", "Settings").setValue("homepage", "https://example.com")
        QMessageBox.information(self, "Homepage Reset", "Homepage reset to the default.")

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
    QCoreApplication.setOrganizationName("MemeChromium")
    QCoreApplication.setApplicationName("MemeChromium")
    browser = MemeChromium()
    browser.show()
    sys.exit(app.exec_())
