import sys
import os
import platform
from PyQt6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit, QPushButton, QWidget, QFileDialog, QMessageBox)
from PyQt6 import QtGui
import qdarktheme

# checks os so file path is correctly named
def os_check(dirname, item):
    if platform.system() == "Windows":
        item_path = f"{dirname}\\{item}"
        return item_path
    else:
        item_path = f"{dirname}/{item}"
        return item_path

class FileRenameApp(QWidget):
    def __init__(self, window_title, width, length):
        super().__init__(parent=None)
        
        self.setWindowTitle(window_title)
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setGeometry(500, 300, width, length)
        self.setStyleSheet("QLabel{font-size: 12pt;}")
        qdarktheme.setup_theme("auto")

        self.initUI()

    # set up grid for ui and adds widgets
    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(10)

        self.replace_widgets()
        self.browse_widgets()

    # creates the labels and input box
    def replace_widgets(self):
        # to replace and replace with widgets
        self.grid.addWidget(QLabel("To replace:"), 0, 0)
        self.grid.addWidget(QLabel("Replace with:"), 1, 0)

        self.to_replace = QLineEdit()
        self.replace_with = QLineEdit()

        self.replace_with.setToolTip("Leave blank if you don't want to replace with anything")
        self.replace_with.setToolTipDuration(0)
        self.setStyleSheet("QToolTip {background-color: black;}")

        self.grid.addWidget(self.to_replace, 0, 1)
        self.grid.addWidget(self.replace_with, 1, 1)

    # creates browse button and get_directory function returns dir chosen
    def browse_widgets(self):
        # browse folder and line
        self.grid.addWidget(QLabel("Folder:"), 2, 0)

        self.browse_line = QLineEdit()
        self.grid.addWidget(self.browse_line, 2, 1)

        self.browse_button = QPushButton("Select folder")
        self.grid.addWidget(self.browse_button, 3, 0, 1, 2)
        self.browse_button.clicked.connect(self.get_directory)


        self.confirmbutton = QPushButton("Rename files")
        self.grid.addWidget(self.confirmbutton, 4, 0, 1, 2)
        self.confirmbutton.clicked.connect(self.rename_files)

    # creates message boxes, depends on condition for box
    def message_boxes(self, condition, count=0):
        if condition == "success":
            success_msg = QMessageBox()
            success_msg.setWindowTitle("Success")
            success_msg.setText(f"Renamed {count} files")
            success_msg.exec()

        if condition == "attributeerror":
            attributeerror_msg = QMessageBox()
            attributeerror_msg.setWindowTitle("Failed")
            attributeerror_msg.setText(f"Choose a folder")
            attributeerror_msg.exec()

        if condition == "nofile":
            nofile_msg = QMessageBox()
            nofile_msg.setWindowTitle("Failed")
            nofile_msg.setText(f"File not found")
            nofile_msg.exec()

    # returns direcotry path and sets to right os
    def get_directory(self):
        self.dirname = QFileDialog.getExistingDirectory(self, "Select folder", "/")
        # returns full path
        self.dirname = os.path.abspath(os.path.expanduser(self.dirname))

        self.browse_line.setText(self.dirname)

    # renames the files
    def rename_files(self):
        self.to_replace_s = self.to_replace.text()
        self.replace_with_s = self.replace_with.text()

        try:
            directory = os.listdir(self.dirname)
            count = 0
            for item in directory:
                item_path = os_check(self.dirname, item)

                if os.path.isfile(item_path) and len(self.to_replace_s) > 0 and self.to_replace_s in item:
                    new_item_name = item.replace(self.to_replace_s, self.replace_with_s)
                    new_item_path = os_check(self.dirname, new_item_name)
                    os.rename(item_path, new_item_path)
                    count += 1

            self.message_boxes("success", count)

        except AttributeError:
            self.message_boxes("attributeerror")

        except FileNotFoundError:
            self.message_boxes("nofile")

def main():
    app = QApplication([])
    filerename = FileRenameApp("Bulk File Renamer", 300, 300)
    filerename.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
