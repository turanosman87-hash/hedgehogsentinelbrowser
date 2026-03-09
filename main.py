import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

class HedgehogBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedgehog Sentinel")
        self.resize(1200, 800)
        self.browser = QWebEngineView()
        # Engellenecek siteler listesi
        self.blocked = ["facebook.com", "instagram.com", "x.com", "tiktok.com"]
        self.browser.urlChanged.connect(self.check_url)
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

    def check_url(self, q):
        url = q.toString().lower()
        if any(site in url for site in self.blocked):
            self.browser.setHtml("<h1>Hedgehog Sentinel: Bu siteye erisim engellendi.</h1>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HedgehogBrowser()
    window.show()
    sys.exit(app.exec())
