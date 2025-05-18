import sys
import os
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from cryptography.fernet import Fernet

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
        # Local icons directory
        icons_dir = "icons"

        back_btn = QAction(QIcon(os.path.join(icons_dir, "back.png")), "Back", self)
        back_btn.triggered.connect(self.navigate_back)
        self.nav_bar.addAction(back_btn)

        forward_btn = QAction(QIcon(os.path.join(icons_dir, "forward.png")), "Forward", self)
        forward_btn.triggered.connect(self.navigate_forward)
        self.nav_bar.addAction(forward_btn)

        reload_btn = QAction(QIcon(os.path.join(icons_dir, "reload.png")), "Reload", self)
        reload_btn.triggered.connect(self.reload_page)
        self.nav_bar.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join(icons_dir, "home.png")), "Home", self)
        home_btn.triggered.connect(self.go_home)
        self.nav_bar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_bar.addWidget(self.url_bar)

        new_tab_btn = QAction(QIcon(os.path.join(icons_dir, "new_tab.png")), "New Tab", self)
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

    def manage_passwords(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Saved Passwords")
        dialog_layout = QVBoxLayout(dialog)

        password_list = QListWidget()
        dialog_layout.addWidget(password_list)

        # Load existing passwords
        passwords = self.load_passwords()
        for site, password in passwords.items():
            password_list.addItem(f"{site}: {password}")

        add_btn = QPushButton("Add Password")
        add_btn.clicked.connect(lambda: self.add_password(dialog))
        dialog_layout.addWidget(add_btn)

        remove_btn = QPushButton("Remove Password")
        remove_btn.clicked.connect(lambda: self.remove_password(dialog, password_list))
        dialog_layout.addWidget(remove_btn)

        dialog.exec_()

    def add_password(self, parent_dialog):
        site, ok1 = QInputDialog.getText(parent_dialog, "Add Password", "Enter site name:")
        password, ok2 = QInputDialog.getText(parent_dialog, "Add Password", "Enter password:")
        if ok1 and ok2 and site and password:
            passwords = self.load_passwords()
            passwords[site] = password
            self.save_passwords(passwords)
            QMessageBox.information(parent_dialog, "Password Added", f"Password for {site} saved!")

    def remove_password(self, parent_dialog, password_list):
        selected_item = password_list.currentItem()
        if selected_item:
            site = selected_item.text().split(":")[0]
            passwords = self.load_passwords()
            if site in passwords:
                del passwords[site]
                self.save_passwords(passwords)
                QMessageBox.information(parent_dialog, "Password Removed", f"Password for {site} removed!")

    def get_encryption_key(self):
        if not os.path.exists("key.key"):
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)
        else:
            with open("key.key", "rb") as key_file:
                key = key_file.read()
        return key

    def load_passwords(self):
        if os.path.exists(self.password_file):
            with open(self.password_file, "rb") as f:
                encrypted_data = f.read()
            fernet = Fernet(self.encryption_key)
            decrypted_data = fernet.decrypt(encrypted_data).decode()
            return eval(decrypted_data)
        return {}

    def save_passwords(self, passwords):
        fernet = Fernet(self.encryption_key)
        encrypted_data = fernet.encrypt(str(passwords).encode())
        with open(self.password_file, "wb") as f:
            f.write(encrypted_data)
