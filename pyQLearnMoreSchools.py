import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from PyQt5.QtGui import QFont

class DataEntryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle('University Application Data Entry')
        self.setGeometry(100, 100, 400, 450)

        layout = QVBoxLayout()

        # Define fields - mix of LineEdits and ComboBoxes
        self.fields = {
            'University': QLineEdit(self),
            'Location': QComboBox(self),
            '2025 QS Ranking': QLineEdit(self),
            'iB': QLineEdit(self),
            'AP': QLineEdit(self),
            'A-Level': QLineEdit(self),
            '国内高中平时成绩': QLineEdit(self),
            '高考成绩': QLineEdit(self),
            '托福': QLineEdit(self),
            '雅思': QLineEdit(self),
            'AST': QLineEdit(self),
            'Budget': QLineEdit(self),
            '文社类': QLineEdit(self),
            '理工类': QLineEdit(self),
        }
        
        # Set options for the comboboxes
        self.fields['Location'].addItems(['美国', '英国', '欧洲', '澳大利亚', '加拿大', '新加坡', '中国香港',])

        # Add widgets dynamically
        for field_name, widget in self.fields.items():
            label = QLabel(f'{field_name}:')
            layout_h = QHBoxLayout()
            layout_h.addWidget(label)
            layout_h.addWidget(widget)
            layout.addLayout(layout_h)

        # Submit button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
    
    def load_data(self):
        try:
            self.data = pd.read_csv('university_data.csv').to_dict('records')
        except FileNotFoundError:
            self.data = []

    def submit_data(self):
        entry = {name: widget.currentText() if isinstance(widget, QComboBox) else widget.text() for name, widget in self.fields.items()}
        
        if any(not value.strip() for value in entry.values()):
            QMessageBox.warning(self, 'Error', 'All fields must be filled out')
            return
        
        self.data.append(entry)

        # Clear inputs
        for widget in self.fields.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
        
        self.save_to_csv()

    def save_to_csv(self):
        df = pd.DataFrame(self.data)
        df.to_csv('university_data.csv', index=False)
        QMessageBox.information(self, 'Saved', 'Data has been saved to CSV.')

def main():
    app = QApplication(sys.argv)
    font = QFont('Helvetica', 12)
    app.setFont(font)
    ex = DataEntryApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()