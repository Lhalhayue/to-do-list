import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("PyQt6 Hello World")
window.resize(350, 180)

label = QLabel("Hello, welcome to PyQt6!")
button = QPushButton("Click Me")
button.clicked.connect(lambda: label.setText("Button clicked!"))

layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)
window.setLayout(layout)

window.show()
sys.exit(app.exec())
