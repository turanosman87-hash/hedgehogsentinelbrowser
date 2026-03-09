import sys
import os
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtWebEngineWidgets import *

# --- 1. OTOMATİK MASAÜSTÜ KURULUM ---
def setup_desktop_icon():
    home = os.path.expanduser("~")
    desktop_path = os.path.join(home, "Desktop", "Hedgehog.desktop")
    script_path = os.path.abspath(__file__)
    desktop_content = f"""[Desktop Entry]
Version=1.0
Name=Hedgehog Sentinel
Exec=python3 {script_path}
Icon=security-high
Terminal=false
Type=Application
"""
    try:
        with open(desktop_path, "w") as f: f.write(desktop_content)
        os.chmod(desktop_path, 0o755)
    except: pass

setup_desktop_icon()

# --- 2. GENİŞLETİLMİŞ GÜVENLİK FİLTRESİ ---
BLOCKED_KEYWORDS = [
    # Yeni Eklenenler
    "facebook.com", "instagram.com", "fb.com", "instagr.am",
    # Mesajlaşma & Sosyal
    "whatsapp", "telegram", "discord", "twitch", "kick", "t.me",
    # Tanışma & Escort
    "tinder", "badoo", "bumble", "azar", "happn", "escort", "sex", "p**n",
    # Kumar & Bahis
    "casino", "bet", "bahis", "poker", "jackpot", "iddaa",
    # Oyunlar
    "roblox", "poki", "miniclip", "game", "oyun", "steam"
]

CLEAN_JS = """
function hedgehogClean() {
    const socialNoise = [
        '#comments', 'ytd-comments', '#chat', '.live-chat', 
        'yt-live-chat-renderer', '#disqus_thread', '.comments-area'
    ];
    socialNoise.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => el.remove());
    });
}
setInterval(hedgehogClean, 2000);
"""

class SentinelPage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        url_str = url.toString().lower()
        if any(key in url_str for key in BLOCKED_KEYWORDS):
            print(f"[SENTINEL] ERİŞİM ENGELLENDİ: {url.host()}")
            return False
        return True

    def createWindow(self, _type):
        return window.add_new_tab()

class BrowserMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedgehog Sentinel Browser")
        self.resize(1280, 850)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Navigasyon Barı
        self.nav_bar = QWidget()
        self.nav_bar.setStyleSheet("background-color: #ffffff; border-bottom: 2px solid #4285F4;")
        nav_layout = QHBoxLayout(self.nav_bar)

        self.back_btn = QPushButton("⬅ Geri")
        self.back_btn.clicked.connect(lambda: self.tabs.currentWidget().back())
        
        self.home_btn = QPushButton("🏠")
        self.home_btn.clicked.connect(self.go_home)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Google'da arayın veya adres yazın...")
        self.url_bar.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 20px; margin: 5px;")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.new_tab_btn = QPushButton("➕")
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab())

        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.url_bar, 1)
        nav_layout.addWidget(self.new_tab_btn)
        
        self.main_layout.addWidget(self.nav_bar)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.main_layout.addWidget(self.tabs)

        # BAŞLANGIÇTA GOOGLE
        self.add_new_tab(QUrl("https://www.google.com"), "Google")

    def add_new_tab(self, qurl=None, label="Yeni Sekme"):
        if qurl is None: qurl = QUrl("https://www.google.com")
        browser = QWebEngineView()
        page = SentinelPage(browser)
        browser.setPage(page)
        
        browser.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
        browser.loadFinished.connect(lambda: browser.page().runJavaScript(CLEAN_JS))
        
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)

        browser.urlChanged.connect(lambda q: self.update_urlbar(q, browser))
        browser.titleChanged.connect(lambda t: self.tabs.setTabText(self.tabs.indexOf(browser), t[:15]))
        return browser

    def go_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com"))

    def close_current_tab(self, i):
        if self.tabs.count() < 2: return
        self.tabs.removeTab(i)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget(): return
        self.url_bar.setText(q.toString())

    def navigate_to_url(self):
        text = self.url_bar.text()
        if "." not in text or " " in text:
            url = QUrl(f"https://www.google.com/search?q={text}")
        else:
            if not text.startswith("http"): text = "https://" + text
            url = QUrl(text)
        self.tabs.currentWidget().setUrl(url)

app = QApplication(sys.argv)
window = BrowserMain()
window.show()
sys.exit(app.exec())
