import sys
import random
import PyQt6
import PyQt6.QtCore
import PyQt6.QtWidgets
from wordleGUI import Ui_WordleWizard
import wordleSolver

class StartupDialog(PyQt6.QtWidgets.QDialog):
    def __init__(self):
        #create window
        super().__init__()
        self.setWindowTitle("Starting Word")
        self.setFixedSize(300,150)
        layout = PyQt6.QtWidgets.QVBoxLayout()

        #create widgets
        self.label = PyQt6.QtWidgets.QLabel("Enter your starting word!\n (You may also leave the textbox blank to start\n with 1 of 5 random strong starting words)")
        self.input_field = PyQt6.QtWidgets.QLineEdit()
        self.button = PyQt6.QtWidgets.QPushButton("OK")

        #attach widgets
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.button.clicked.connect(self.accept)

    def get_input(self):
        return self.input_field.text()


class WordleWizard(PyQt6.QtWidgets.QMainWindow):
    def __init__(self, starting_word):
        super().__init__()

        # setting up Ui instance
        self.ui = Ui_WordleWizard()
        self.ui.setupUi(self)

        
        self.ui.reset_button.clicked.connect(self.restart)

        self.prev_guess = ""
        # getting passed starting word
        if starting_word == "" or len(starting_word) != 5 or not starting_word.isalpha():
            self.prev_guess = random.choice(['raise', 'slate', 'crate', 'irate', 'trace'])
        else:
            self.prev_guess = starting_word.lower()

        
        self.original_guess = self.prev_guess
        self.active_row = 1
        self.feedback = ''
        self.candidates = []

        #creating map of buttons for ease of use later  (row, column): button name
        self.buttons = {}
        for i in range(1,7):
            for j in range(1,6):
                name = f'button{i}_{j}'
                self.buttons[(i,j)] = getattr(self.ui, name)
        for (row, column), button in self.buttons.items():
            button.clicked.connect(lambda checked=False, r=row, c=column : self.square_clicked(r, c))
        
        #initialize
        self.restart()


    def restart(self):
        #resets all relevant info
        self.active_row = 1
        self.candidates = wordleSolver.all_words
        self.prev_guess = self.original_guess

        for button in self.buttons.values():
            button.setText("")
            button.setStyleSheet("background-color: rgb(86, 85, 91); color: black;")
        self.updateButtons()
    

    def square_clicked(self, row, column):
        #handles colour changes for button click
        button = self.buttons[(row, column)]
        current_style = button.styleSheet()

        #cycling grey -> yellow -> green
        if "background-color: rgb(86, 85, 91)" in current_style or current_style == "":
            button.setStyleSheet("background-color: rgb(204, 204, 0);")
        elif "background-color: rgb(204, 204, 0)" in current_style:
            button.setStyleSheet("background-color: rgb(0, 204, 0);")
        else:
            button.setStyleSheet("background-color: rgb(86, 85, 91);")
        
    def keyPressEvent(self, event):
        #On enter freezes previous rows and sends feedback to wordleSolver.py for next word
        if event.key() == PyQt6.QtCore.Qt.Key.Key_Return or event.key() == PyQt6.QtCore.Qt.Key.Key_Enter:
            if self.active_row < 6:
                self.getFeedback()
                res = wordleSolver.guessing(self.feedback, self.prev_guess, self.active_row, self.candidates)
                self.prev_guess = res[0]
                self.candidates = res[1]
                self.active_row += 1
                self.updateButtons()
    
    def getFeedback(self):
        #Creates feedback string to be sent to the solver file
        temp = ['B','B','B','B','B']
        for (row, column), button in self.buttons.items():
            if row == self.active_row:
                current_style = button.styleSheet()
                if "background-color: rgb(204, 204, 0)" in current_style:
                    temp[column-1] = 'Y'
                elif "background-color: rgb(0, 204, 0)" in current_style:
                    temp[column-1] = 'G'
        self.feedback = ''.join(temp)
    
    def updateButtons(self):
        for (row, column), button in self.buttons.items():
            if row == self.active_row:
                #buttons in the active row
                button.setEnabled(True)
                button.setStyleSheet("""
                QPushButton {
                    background-color: rgb(86, 85, 91);
                    color: black;
                }
                QPushButton:pressed {
                    background-color: rgb(120, 120, 130);
                }
                """)
                button.setText(f'{self.prev_guess[column-1]}')
            else:
                #buttons not in active row
                button.setEnabled(False)
                current_style = button.styleSheet()
                if "background-color: rgb(86, 85, 91)" in current_style or current_style == "":
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: rgb(60, 60, 65);
                            color: black;
                        }
                    """)
                elif "background-color: rgb(204, 204, 0)" in current_style:
                    button.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(140, 140, 0);
                        color: black;
                    }
                    """)
                elif "background-color: rgb(0, 204, 0)" in current_style:
                    button.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(0, 102, 0);
                        color: black;
                    }
                    """)
                else:
                    None


def main():
    app = PyQt6.QtWidgets.QApplication(sys.argv)

    dialog = StartupDialog()
    if dialog.exec():
        window = WordleWizard(dialog.get_input())
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()