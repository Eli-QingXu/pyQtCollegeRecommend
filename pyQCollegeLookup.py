
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QCheckBox, QMessageBox
import pandas as pd

class CollegeRecommender(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.df = pd.read_csv("university_data.csv")  # Load the data

    def initUI(self):
        layout = QVBoxLayout()

        # Location checkboxes
        self.locationCheckboxes = []
        for loc in ["美国", "英国", "欧洲","澳大利亚", "加拿大", "新加坡", "中国香港"]:  # Add all locations you have
            cb = QCheckBox(loc, self)
            self.locationCheckboxes.append(cb)
            layout.addWidget(cb)

        # QS Ranking input
        self.qsRanking = QLineEdit(self)
        layout.addWidget(QLabel('2025QS排名(最低):'))
        layout.addWidget(self.qsRanking)

        # Budget input
        self.budget = QLineEdit(self)
        layout.addWidget(QLabel('最高预算(万人民币):'))
        layout.addWidget(self.budget)

        # Major selection
        self.majorCombo = QComboBox(self)
        self.majorCombo.addItems(["文社类", "理工类"])
        layout.addWidget(QLabel('学科:'))
        layout.addWidget(self.majorCombo)

        # Grade type selection
        self.gradeTypeCombo = QComboBox(self)
        self.gradeTypeCombo.addItems(["A-Level", "AP", "iB", "国内高中平时成绩", "高考成绩"])
        layout.addWidget(QLabel('成绩类型:'))
        layout.addWidget(self.gradeTypeCombo)

        # Grade value input
        self.gradeValue = QLineEdit(self)
        layout.addWidget(QLabel('成绩分数(换算为100分制):'))
        layout.addWidget(self.gradeValue)

        # Search Button
        btn = QPushButton('为我推荐学校', self)
        btn.clicked.connect(self.find_colleges)
        layout.addWidget(btn)

        # Result Label
        self.text_Label = QLabel("推荐结果:")
        layout.addWidget(self.text_Label)
        self.resultLabel = QLabel("结果1")
        layout.addWidget(self.resultLabel)

        self.setLayout(layout)
        self.setWindowTitle('AI大学推荐工具')
        self.show()

    def find_colleges(self):
        selected_locations = [cb.text() for cb in self.locationCheckboxes if cb.isChecked()]
        qs_ranking = int(self.qsRanking.text())
        budget = int(self.budget.text())
        major = self.majorCombo.currentText()
        grade_type = self.gradeTypeCombo.currentText()
        grade_value = int(self.gradeValue.text())
        # Determine the database column for the selected grade type
        grade_column = f'{grade_type}'

        # Filter the dataframe according to the user input
        result = self.df[
            (self.df['Location'].isin(selected_locations)) &
            (self.df['2025 QS Ranking'] <= qs_ranking) &
            (self.df['Budget'] <= budget) &
            # (self.df['Major'] == major) &
            (self.df[grade_column] <= grade_value)  # Compare against the dynamically chosen grade column
        ]

        if not result.empty:
            # sort the results in Major recommendation scores
            sorted_result = result.sort_values(by=major,ascending=False).head(3)
            # Select only the 'University' and '2025 QS Ranking' columns for display
            display_result = sorted_result.loc[:, ['University', '2025 QS Ranking']]
            display_text = display_result.to_string(index=False, header=False)
            self.resultLabel.setText(display_text)
        else:
            self.resultLabel.setText('抱歉，请重新输入')

def main():
    app = QApplication(sys.argv)
    font = QFont('Helvetica', 12)
    app.setFont(font)
    ex = CollegeRecommender()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()