import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class HTMLViewer(QMainWindow):
    def __init__(self, html_file):
        super().__init__()

        self.setWindowTitle("HTML Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.webview = QWebEngineView()
        self.webview.setHtml(self.read_html_file(html_file))

        layout = QVBoxLayout()
        layout.addWidget(self.webview)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def read_html_file(self, html_file):
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()
        return html_content

if __name__ == "__main__":
    html_file_path = "D:/file.html"

    app = QApplication(sys.argv)
    viewer = HTMLViewer(html_file_path)
    viewer.show()

    sys.exit(app.exec_())
