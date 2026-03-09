import sys
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView

# --- HEDGEHOG YASAKLI LİSTESİ ---
BLOCKED = ["facebook.com", "instagram.com", "twitter.com", "x.com", "tiktok.com", "discord.com"]
CLEAN_JS = "function h(){['#comments','ytd-comments','#chat','.live-chat'].forEach(s=>{document.querySelectorAll(s).forEach(el=>el.remove())})}setInterval(h,2000);"

class SentinelPage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if any(site in url.toString().lower() for site in BLOCKED): return False
        return True
    def createWindow(self, _type): return window.add_new_tab()

class HedgehogBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedgehog Sentinel")
        self.resize(1200, 800)
        c = QWidget(); self.setCentralWidget(c)
        l = QVBoxLayout(c); l.setContentsMargins(0,0,0,0)
        nav = QWidget(); nl = QHBoxLayout(nav)
        self.url_bar = QLineEdit(); self.url_bar.returnPressed.connect(self.navigate)
        btn = QPushButton("➕ Sekme"); btn.clicked.connect(lambda: self.add_new_tab())
        nl.addWidget(self.url_bar); nl.addWidget(btn); l.addWidget(nav)
        self.tabs = QTabWidget(); self.tabs.setTabsClosable(True); self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        l.addWidget(self.tabs); self.add_new_tab(QUrl("https://www.google.com"))

    def add_new_tab(self, qurl=QUrl("https://www.google.com")):
        b = QWebEngineView(); p = SentinelPage(b); b.setPage(p)
        b.loadFinished.connect(lambda: b.page().runJavaScript(CLEAN_JS))
        i = self.tabs.addTab(b, "Yükleniyor..."); self.tabs.setCurrentIndex(i)
        b.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()))
        b.setUrl(qurl); return b

    def navigate(self):
        u = self.url_bar.text()
        self.tabs.currentWidget().setUrl(QUrl(u if "://" in u else "https://" + u))

if __name__ == "__main__":
    app = QApplication(sys.argv); global window; window = HedgehogBrowser(); window.show(); sys.exit(app.exec())
