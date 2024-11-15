import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

def on_button_click():
    label.setText("Button clicked!")

app = QApplication(sys.argv)

# Create the main window
window = QWidget()
window.setWindowTitle('PyQt5 Basic UI Example')
window.setGeometry(100, 100, 300, 200)  # x, y, width, height

# Create a vertical layout
layout = QVBoxLayout()

# Create a label and a button
label = QLabel('Hello, PyQt5!')
button = QPushButton('Click Me')
button.clicked.connect(on_button_click)

# Add widgets to the layout
layout.addWidget(label)
layout.addWidget(button)

# Set the layout for the window
window.setLayout(layout)

# Show the window
window.show()

# Execute the application
sys.exit(app.exec_())
