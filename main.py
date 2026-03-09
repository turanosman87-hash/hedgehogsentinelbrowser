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
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HedgehogBrowser()
    window.show()
    sys.exit(app.exec())
