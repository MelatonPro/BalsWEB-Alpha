import sys
import os
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from cryptography.fernet import Fernet

class BalsWEB(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Setup
        self.setWindowTitle("BalsWEB (MemeChromium) - Probably the most not funny browser but it's trying its best :(")
        self.setGeometry(100, 100, 1280, 720)

        # Central Widget: Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.new_tab)
        self.setCentralWidget(self.tabs)

        # Load Settings
        self.settings = QSettings("MemeChromium", "Settings")
        self.startup_url = self.settings.value("startup_url", "https://www.melaton.pro/balsweb/balsweb-opened")
        self.new_tab_url = self.settings.value("new_tab_url", "https://www.melaton.pro/balsweb/newtab")
        self.password_file = "passwords.enc"
        self.encryption_key = self.get_encryption_key()

        # Load Startup Page
        self.load_startup_page()

        # Navigation Bar
        self.nav_bar = QToolBar("Navigation")
        self.nav_bar.setIconSize(QSize(24, 24))
        self.addToolBar(self.nav_bar)

        # Add Navigation Buttons
        self.add_nav_buttons()

        # Settings Menu
        self.menu_bar = self.menuBar()
        self.settings_menu = self.menu_bar.addMenu("⚙️ Settings")
        self.add_settings_menu()

        # Inject Memes
        self.inject_memes()

    def load_startup_page(self):
        browser = QWebEngineView()
        browser.setUrl(QUrl(self.startup_url))
        browser.urlChanged.connect(lambda q, b=browser: self.update_url(q, b))
        i = self.tabs.addTab(browser, "Home")
        self.tabs.setCurrentIndex(i)

    def new_tab(self, *args):
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
        back_btn = QAction("⬅️ Back", self)
        back_btn.triggered.connect(self.navigate_back)
        self.nav_bar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction("➡️ Forward", self)
        forward_btn.triggered.connect(self.navigate_forward)
        self.nav_bar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction("🔄 Reload", self)
        reload_btn.triggered.connect(self.reload_page)
        self.nav_bar.addAction(reload_btn)

        # Home Button
        home_btn = QAction("🏠 Home", self)
        home_btn.triggered.connect(self.go_home)
        self.nav_bar.addAction(home_btn)

        # Address Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_bar.addWidget(self.url_bar)

        # New Tab Button
        new_tab_btn = QAction("➕ New Tab", self)
        new_tab_btn.triggered.connect(self.new_tab)
        self.nav_bar.addAction(new_tab_btn)

    def add_settings_menu(self):
        set_startup_url_action = QAction("Set Startup Website", self)
        set_startup_url_action.triggered.connect(self.set_startup_url)
        self.settings_menu.addAction(set_startup_url_action)

        set_new_tab_url_action = QAction("Set New Tab Website", self)
        set_new_tab_url_action.triggered.connect(self.set_new_tab_url)
        self.settings_menu.addAction(set_new_tab_url_action)

        manage_passwords_action = QAction("Manage Saved Passwords", self)
        manage_passwords_action.triggered.connect(self.manage_passwords)
        self.settings_menu.addAction(manage_passwords_action)

        reset_urls_action = QAction("Reset to Default URLs", self)
        reset_urls_action.triggered.connect(self.reset_urls)
        self.settings_menu.addAction(reset_urls_action)

    def set_startup_url(self):
        url, ok = QInputDialog.getText(self, "Set Startup Website", "Enter your startup website URL:")
        if ok and url:
            self.settings.setValue("startup_url", url)
            self.startup_url = url
            QMessageBox.information(self, "Startup URL Set", f"Startup website set to: {url}")

    def set_new_tab_url(self):
        url, ok = QInputDialog.getText(self, "Set New Tab Website", "Enter your new tab website URL:")
        if ok and url:
            self.settings.setValue("new_tab_url", url)
            self.new_tab_url = url
            QMessageBox.information(self, "New Tab URL Set", f"New tab website set to: {url}")

    def reset_urls(self):
        self.settings.setValue("startup_url", "https://startup-website.com")
        self.settings.setValue("new_tab_url", "https://new-tab-website.com")
        self.startup_url = "https://startup-website.com"
        self.new_tab_url = "https://new-tab-website.com"
        QMessageBox.information(self, "URLs Reset", "Startup and new tab URLs have been reset to default.")

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))

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
        # Status Bar Meme
        self.statusBar().showMessage("🔥 Memes incoming... Stay tuned! 🐸")

        # Meme Button
        meme_action = QAction("🐸 Random Meme", self)
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
    browser = BalsWEB()
    browser.show()
    sys.exit(app.exec_())
