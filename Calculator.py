import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QGridLayout, QLabel,
                             QPushButton, QLineEdit, QTextEdit, QDialog)
from PyQt5.QtCore import Qt, QTimer


class HistoryWindow(QDialog):
    def __init__(self, history_content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("History")
        self.setGeometry(400, 400, 300, 400)
        self.setStyleSheet("background-color: #2E3440; color: #ECEFF4;")

        layout = QVBoxLayout()

        self.history_display = QTextEdit(self)
        self.history_display.setReadOnly(True)
        self.history_display.setStyleSheet("background-color: #4C566A;"
                                           " color: #ECEFF4;")
        self.history_display.setText(history_content)

        layout.addWidget(self.history_display)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '+', '=',
            '%', '⌫', 'C'
        ]
        self.setGeometry(300, 300, 300, 400)
        self.setStyleSheet("background-color: #2E3440;")
        self.button_objects = []
        self.current_input = ""
        self.history_content = ""
        self.history_button = QPushButton("History", self)
        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.clear_error)

    def initUI(self):
        # Display field
        self.display = QLineEdit(self)
        self.display.setGeometry(20, 20, 260, 50)
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setStyleSheet("background-color: #4C566A;"
                                   "color: #ECEFF4;"
                                   "border: 2px solid #81A1C1;"
                                   "border-radius: 5px;"
                                   "padding: 5px;"
                                   "font-size: 20px;"
                                   )
        self.display.setReadOnly(True)

        # Buttons
        button_size = 50
        spacing = 10
        start_x, start_y = 20, 100

        for i, label in enumerate(self.buttons):
            row = i // 4
            col = i % 4

            btn = QPushButton(label, self)
            btn.setGeometry(start_x + col * (button_size + spacing),
                            start_y + row * (button_size + spacing),
                            button_size, button_size)

            btn.clicked.connect(lambda checked=False,
                                text=label: self.button_clicked(text))

            self.button_objects.append(btn)

        for button in self.button_objects:
            button.setStyleSheet("background-color: #81A1C1;"
                                 "color: #2E3440;"
                                 "border-radius: 5px;"
                                 "border: 2px solid #5E81AC;"
                                 "padding: 5px;"
                                 "font-size: 15px;")

        # History
        self.history_button.setGeometry(200, 340, 50, 40)
        self.history_button.clicked.connect(self.show_history)
        self.history_button.setStyleSheet("background-color: #81A1C1;"
                                          "color: #2E3440;"
                                          "border-radius: 5px;")

    def button_clicked(self, text):
        if text == '=':
            try:
                while (self.current_input and self.current_input[-1]
                       in ['+', '-', '*', '/']):
                    self.current_input = self.current_input[:-1]
                if self.current_input:
                    result = str(eval(self.current_input))
                    history_entry = (f"{self.current_input} = {result}\n")
                    self.history_content += history_entry
                    self.current_input = result
                else:
                    self.current_input = ""
            except ZeroDivisionError:
                self.current_input = "Cannot divide by zero"
                self.timer.start(1000)
            except Exception:
                self.current_input = "ERROR"
                self.timer.start(1000)
        elif text == '%':
            try:
                self.current_input = str(eval(self.current_input) / 100)
            except Exception:
                self.current_input = "ERROR"
                self.timer.start(1000)
        elif text == '⌫':
            self.current_input = self.current_input[:-1]
        elif text == 'C':
            self.current_input = ""
        else:
            self.current_input += text

        self.display.setText(self.current_input)

    def clear_error(self):
        self.current_input = ""
        self.display.setText(self.current_input)
        self.timer.stop()

    def show_history(self):
        self.history_window = HistoryWindow(self.history_content, self)
        self.history_window.show()

    def keyPressEvent(self, event):
        key = event.text()
        if key in ['0', '1', '2', '3', '4', '5', '6',
                   '7', '8', '9', '+', '-', '*', '/', '.', '%']:
            self.button_clicked(key)
        elif key == '\r':
            self.button_clicked('=')
        elif event.key() == Qt.Key_Space:
            self.button_clicked('⌫')
        elif event.key() == Qt.Key_C:
            self.button_clicked('C')


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
