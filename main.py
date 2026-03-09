import sys
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView

# --- HEDGEHOG SENTINEL GÜVENLİK FİLTRESİ ---
# Buraya eklediğin her site anında engellenir
BLOCKED_SITES = [
    "facebook.com", "fb.com", 
    "instagram.com", "instagr.am", 
    "whatsapp.com", "telegram.org",
    "discord.com", "twitch.tv", "kick.com",
    "tiktok.com", "twitter.com", "x.com"
]

# YouTube yorumlarını ve canlı sohbeti yok eden Hedgehog scripti
CLEAN_JS = """
function cleanup() {
    let selectors = ['#comments', 'ytd-comments', '#chat', '.live-chat', '#secondary'];
    selectors.forEach(s => {
        document.querySelectorAll(s).forEach(el => el.remove());
    });
}
setInterval(cleanup, 2000);
"""

class SentinelPage(QWebEnginePage):
    """Web sayfalarını denetleyen Hedgehog Güvenlik Katmanı"""
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        url_str = url.toString().lower()
        if any(site in url_str for site in BLOCKED_SITES):
            print(f"Hedgehog Engelledi: {url_str}")
            return False  # Erişimi engelle
        return True

    def createWindow(self, _type):
        return window.add_new_tab()

class HedgehogBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedgehog Sentinel Browser")
        self.resize(1280, 850)

        # Ana düzen
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # Navigasyon Çubuğu
        nav_bar = QWidget()
        nav_bar.setStyleSheet("background: white; border-bottom: 1px solid #ddd; padding: 5px;")
        nav_layout = QHBoxLayout(nav_bar)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Google'da ara veya URL yaz...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        btn_new_tab = QPushButton("➕ Yeni Sekme")
        btn_new_tab.clicked.connect(lambda: self.add_new_tab())

        nav_layout.addWidget(self.url_bar, 1)
        nav_layout.addWidget(btn_new_tab)
        layout.addWidget(nav_bar)

        # Sekme Yapısı
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tabs)

        # İlk sekmeyi aç
        self.add_new_tab(QUrl("https://www.google.com"), "Google")

    def add_new_tab(self, qurl=None, label="Yeni Sekme"):
        if qurl is None: qurl = QUrl("https://www.google.com")
        
        browser = QWebEngineView()
        page = SentinelPage(browser)
        browser.setPage(page)
        
        # YouTube temizleyiciyi her yükleme bittiğinde çalıştır
        browser.loadFinished.connect(lambda: browser.page().runJavaScript(CLEAN_JS))
        
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        
        browser.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()) if self.tabs.currentWidget() == browser else None)
        browser.setUrl(qurl)
        return browser

    def navigate_to_url(self):
        url = self.url_bar.text()
        if "." not in url:
            url = "https://www.google.com/search?q=" + url
        elif not url.startswith("http"):
            url = "https://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    global window
    window = HedgehogBrowser()
    window.show()
    sys.exit(app.exec())
