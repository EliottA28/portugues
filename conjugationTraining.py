from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

import json
import random

class ConjugationTraining(QMainWindow):
    def __init__(self, trainig_mode):
        super().__init__()
        self.setWindowTitle("Treino")
        self.setGeometry(200,200,700,500)
        
        with open('database.json', 'r') as f:
            self.data = json.load(f)

        self.random_word_list = list(self.data.items())
        if trainig_mode == "irregular":
            self.random_word_list = [self.random_word_list[i] for i in range(len(self.random_word_list)) if self.random_word_list[i][1]["type"] == "verb" and self.irregular(self.random_word_list[i][0], self.random_word_list[i][1]["conj"])]
        elif trainig_mode == "regular":
            self.random_word_list = [self.random_word_list[i] for i in range(len(self.random_word_list)) if self.random_word_list[i][1]["type"] == "verb" and not self.irregular(self.random_word_list[i][0], self.random_word_list[i][1]["conj"])]
        else:
            self.random_word_list = [self.random_word_list[i] for i in range(len(self.random_word_list)) if self.random_word_list[i][1]["type"] == "verb"]
        random.shuffle(self.random_word_list)
        self.length = len(self.random_word_list)
        self.index = 0

        # random word
        self.random_word()
        self.miss_counter = 0

        form = QFormLayout()

        head = QLabel("Conjugation", self)
  
        font = QFont('Times', 20)
        font.setBold(True)
        font.setUnderline(True)
        head.setFont(font)
        head.setAlignment(Qt.AlignCenter)

        # creating label to show word
        self.word = QLabel(self.translation, self)
        self.word.setAlignment(Qt.AlignCenter)
        self.word.setFont(QFont('Times', 30))

        self.definition = QLabel(self.note, self)
        self.definition.setAlignment(Qt.AlignCenter)
        self.definition.setFont(QFont('Times', 15))
  
        # creating a line edit
        self.input_text_0 = QLineEdit(self)
        self.input_text_0.setFont(QFont('Arial', 14))
        self.input_text_0.returnPressed.connect(self.next)
        self.input_text_1 = QLineEdit(self)
        self.input_text_1.setFont(QFont('Arial', 14))
        self.input_text_1.returnPressed.connect(self.next)
        self.input_text_2 = QLineEdit(self)
        self.input_text_2.setFont(QFont('Arial', 14))
        self.input_text_2.returnPressed.connect(self.next)
        self.input_text_3 = QLineEdit(self)
        self.input_text_3.setFont(QFont('Arial', 14))
        self.input_text_3.returnPressed.connect(self.bAction)

        self.b = QPushButton("Check")
        self.b.clicked.connect(self.bAction)

        form.addRow(head)
        form.addRow(self.word)
        form.addRow(self.definition)
        form.addRow(QLabel("Verb Translation (fr or eng)"), self.input_text_0)
        form.addRow(QLabel("Eu"), self.input_text_1)
        form.addRow(QLabel("Ele/Ela/A gente/Você"), self.input_text_2)
        form.addRow(QLabel("Eles/Elas/Vocês"), self.input_text_3)
        form.addRow(self.b)
        
        layout = QGridLayout()
        layout.addLayout(form, 0, 0)
        widget_1 = QWidget()
        widget_1.setLayout(layout)
        self.setCentralWidget(widget_1)

    def random_word(self):
        key, value = self.random_word_list[self.index]
        self.translation, self.random_word_fr, self.random_word_eng = key, value["fr"], value["eng"]
        self.t1, self.t2, self.t3 = value['conj'].split('_')
        self.index += 1
        self.note = value['def']
        if self.index > self.length-1:
            self.index = 0

    def next(self):
        self.focusNextChild()

    def bAction(self):
        text_0 = self.input_text_0.text()
        text_0 = text_0.lower()
        text_1 = self.input_text_1.text()
        text_1 = text_1.lower()
        text_2 = self.input_text_2.text()
        text_2 = text_2.lower()
        text_3 = self.input_text_3.text()
        text_3 = text_3.lower()

        if text_0 != "" and text_1 != "" and text_2 != "" and text_3 != "":
            if (text_0 == self.random_word_fr or text_0 == self.random_word_eng) and text_1 == self.t1 and text_2 == self.t2 and text_3 == self.t3:
                # clearing line edit text
                self.input_text_0.setFocus()
                self.display_new_word()

            elif self.miss_counter < 2:
                self.miss_counter += 1

            else:
                msg = QMessageBox()
                msg.setText("Correction\n")
                msg.setInformativeText(self.translation +  " : " + self.random_word_fr + "\n" +
                                       "Eu " + self.t1 + "\n" +
                                       "Ele " + self.t2 + "\n" +
                                       "Eles " + self.t3)
                msg.exec_()
                self.input_text_0.setFocus()
                self.display_new_word()
                print("error")

    def display_new_word(self):
        self.miss_counter = 0
        self.input_text_0.clear()
        self.input_text_1.clear()
        self.input_text_2.clear()
        self.input_text_3.clear()

        # random word
        self.random_word()

        # setting text to label
        self.word.setText(self.translation)
        self.definition.setText(self.note)

    def irregular(self, verb, conj):
        c1, c2, c3 = conj.split('_')
        print(c1, c2, c3)
        print(verb[-2:], c1[:-1], verb[:-2], c1[-1], c2[:-1], verb[:-2], c2[-1], c3[:-2], verb[:-2], c3[-2:])
        if verb[-2:] == "ar":
            if c1[:-1] == verb[:-2] and c1[-1] == 'o' and c2[:-1] == verb[:-2] and c2[-1] == 'a' and c3[:-2] == verb[:-2] and c3[-2:] == 'am':
                print(False)
                return False
            else:
                print(True)
                return True
        elif verb[-2:] == "er" or verb[-2:] == "ir":
            if c1[:-1] == verb[:-2] and c1[-1] == 'o' and c2[:-1] == verb[:-2] and c2[-1] == 'e' and c3[:-2] == verb[:-2] and c3[-2:] == 'em':
                print(False)
                return False
            else:
                print(True)
                return True
        else:
            print(True)
            return True