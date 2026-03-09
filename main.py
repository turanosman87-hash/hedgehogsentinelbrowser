import sys
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView

# --- HEDGEHOG SENTINEL GÜVENLİK ---
BLOCKED = ["facebook.com", "instagram.com", "fb.com", "instagr.am", "whatsapp", "telegram", "discord", "twitch", "kick", "tinder", "badoo", "bumble", "azar", "escort", "sex", "p**n", "casino", "bet", "bahis", "poker", "roblox", "poki", "game", "steam"]
CLEAN_JS = "function h(){['#comments','ytd-comments','#chat','.live-chat'].forEach(s=>{document.querySelectorAll(s).forEach(el=>el.remove())})}setInterval(h,2000);"

class SentinelPage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        u = url.toString().lower()
        if any(k in u for k in BLOCKED): return False
        return True
    def createWindow(self, _type): return window.add_new_tab()

class HedgehogBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedgehog Sentinel")
        self.resize(1280, 850)
        container = QWidget(); self.setCentralWidget(container)
        layout = QVBoxLayout(container); layout.setContentsMargins(0,0,0,0); layout.setSpacing(0)
        nav = QWidget(); nav.setStyleSheet("background: #ffffff; border-bottom: 2px solid #4285F4; padding: 10px;")
        nav_l = QHBoxLayout(nav)
        self.url_bar = QLineEdit(); self.url_bar.setPlaceholderText("Google’da arayın...")
        self.url_bar.setStyleSheet("padding: 10px; border-radius: 20px; border: 1px solid #ccc;")
        self.url_bar.returnPressed.connect(self.navigate)
        new_t = QPushButton("➕ Sekme"); new_t.clicked.connect(lambda: self.add_new_tab(QUrl("https://www.google.com")))
        nav_l.addWidget(self.url_bar, 1); nav_l.addWidget(new_t); layout.addWidget(nav)
        self.tabs = QTabWidget(); self.tabs.setDocumentMode(True); self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(lambda i: self.tabs.count()>1 and self.tabs.removeTab(i))
        layout.addWidget(self.tabs)
        QTimer.singleShot(100, lambda: self.add_new_tab(QUrl("https://www.google.com"), "Google"))

    def add_new_tab(self, qurl=None, label="Google"):
        b = QWebEngineView(); p = SentinelPage(b); b.setPage(p)
        b.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
        b.loadFinished.connect(lambda: b.page().runJavaScript(CLEAN_JS))
        idx = self.tabs.addTab(b, label); self.tabs.setCurrentIndex(idx)
        b.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()) if b == self.tabs.currentWidget() else None)
        b.setUrl(qurl if qurl else QUrl("https://www.google.com")); return b

    def navigate(self):
        t = self.url_bar.text()
        u = QUrl(f"https://www.google.com/search?q={t}") if "." not in t or " " in t else QUrl(t if "://" in t else "https://"+t)
        self.tabs.currentWidget().setUrl(u)

if __name__ == "__main__":
    app = QApplication(sys.argv); global window; window = HedgehogBrowser(); window.show(); sys.exit(app.exec())
