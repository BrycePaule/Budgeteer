from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QMainWindow, QFileDialog)

from Expense_Splitter import Expense_Splitter

class WidgetGallery(QWidget):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.create_buttons()
        self.create_explorer_window()
        self.show()

        main_layout = QGridLayout()
        main_layout.addWidget(self.explorer_box, 0, 0, 0, 2)
        main_layout.addWidget(self.button_box, 0, 2, 0, 3)

        self.setLayout(main_layout)
        self.setWindowTitle('Budgeteer')
        self.changeStyle('Fusion')


    def create_explorer_window(self):
        self.explorer_box = QGroupBox()

        csv_filter = 'csv(*.csv)'
        explorer = QFileDialog(filter=csv_filter)

        layout = QVBoxLayout()
        layout.addWidget(explorer)

        self.explorer_box.setLayout(layout)


    def create_buttons(self):
        self.button_box = QGroupBox()

        splitter = Expense_Splitter()

        collate_button = QPushButton('Collate')
        collate_button.setDefault(True)
        collate_button.clicked.connect(splitter.run())

        layout = QVBoxLayout()
        layout.addWidget(collate_button)

        self.button_box.setLayout(layout)


    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()


    def changePalette(self):
        QApplication.setPalette(QApplication.style().standardPalette())

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
