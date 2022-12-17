from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

import json
import random

class ConjugationTraining(QMainWindow):
    def __init__(self, trainig_mode, tense):
        super().__init__()
        self.setWindowTitle("Treino")
        self.setGeometry(200,200,380,480)

        with open('database.json', 'r') as f:
            self.data = json.load(f)

        # creat list of words
        if tense == "presente":
            self.tense = "conj"
        elif tense == "pretérito perfeito":
            self.tense = "conj_pp"
        self.random_word_list = list(self.data.items())
        if trainig_mode == "irregular":
            self.random_word_list = [self.random_word_list[i] for i in range(len(self.random_word_list)) if self.random_word_list[i][1]["type"] == "verb" and self.irregular(self.random_word_list[i][1]["bra"], self.random_word_list[i][1][self.tense])]
        elif trainig_mode == "regular":
            self.random_word_list = [self.random_word_list[i] for i in range(len(self.random_word_list)) if self.random_word_list[i][1]["type"] == "verb" and not self.irregular(self.random_word_list[i][1]["bra"], self.random_word_list[i][1][self.tense])]
        else:
            self.random_word_list = [self.random_word_list[i] for i in range(len(self.random_word_list)) if self.random_word_list[i][1]["type"] == "verb"]
        random.shuffle(self.random_word_list)
        self.length = len(self.random_word_list)
        self.index = 0

        # random word
        self.random_word()
        self.miss_counter = 0

        # head label
        head = QLabel("Conjugation : " + tense, self)
        font = QFont('Times', 20)
        font.setBold(True)
        font.setUnderline(True)
        head.setFont(font)
        head.setAlignment(Qt.AlignCenter)

        # label to show word and definition
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

        # layout
        form = QFormLayout()
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
        _, value = self.random_word_list[self.index]
        self.translation, self.random_word_fr, self.random_word_eng = value["bra"], value["fr"], value["eng"]
        self.t1, self.t2, self.t3 = value[self.tense].split('_')
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
        words_fr = self.random_word_fr.split('_')
        words_eng = self.random_word_eng.split('_')

        if text_0 != "" and text_1 != "" and text_2 != "" and text_3 != "":
            if (text_0 in words_fr or text_0 == words_eng) and text_1 == self.t1 and text_2 == self.t2 and text_3 == self.t3:
                self.input_text_0.setFocus()
                self.display_new_word()

            elif self.miss_counter < 2:
                self.miss_counter += 1

            else:
                msg = QMessageBox()
                msg.setText("Correction\n")
                msg.setInformativeText(self.translation +  " : " + ', '.join(words_fr) + "\n" +
                                       "Eu " + self.t1 + "\n" +
                                       "Ele " + self.t2 + "\n" +
                                       "Eles " + self.t3)
                msg.exec_()
                self.input_text_0.setFocus()
                self.display_new_word()

    def display_new_word(self):
        self.miss_counter = 0
        self.input_text_0.clear()
        self.input_text_1.clear()
        self.input_text_2.clear()
        self.input_text_3.clear()

        self.random_word()
        self.word.setText(self.translation)
        self.definition.setText(self.note)

    def irregular(self, verb, conj):
        c1, c2, c3 = conj.split('_')
        # print(c1, c2, c3)
        # print(verb[-2:], c1[:-2], verb[:-2], c1[-1], c2[:-2], verb[:-2], c2[-1], c3[:-2], verb[:-2], c3[-2:])
        # print(self.tense)
        if self.tense == "conj":
            if verb[-2:] == "ar":
                if c1[:-1] == verb[:-2] and c1[-1] == 'o' and c2[:-1] == verb[:-2] and c2[-1] == 'a' and c3[:-2] == verb[:-2] and c3[-2:] == 'am':
                    return False
                else:
                    return True
            elif verb[-2:] == "er" or verb[-2:] == "ir":
                if c1[:-1] == verb[:-2] and c1[-1] == 'o' and c2[:-1] == verb[:-2] and c2[-1] == 'e' and c3[:-2] == verb[:-2] and c3[-2:] == 'em':
                    return False
                else:
                    return True
            else:
                return True
        elif self.tense == "conj_pp":
            if verb[-2:] == "ar":
                if c1[:-2] == verb[:-2] and c1[-2:] == 'ei' and c2[:-2] == verb[:-2] and c2[-2:] == 'ou' and c3[:-4] == verb[:-2] and c3[-4:] == 'aram':
                    return False
                else:
                    return True
            elif verb[-2:] == "er":
                if c1[:-1] == verb[:-2] and c1[-1] == 'i' and c2[:-2] == verb[:-2] and c2[-2:] == 'eu' and c3[:-4] == verb[:-2] and c3[-4:] == 'eram':
                    return False
                else:
                    return True
            elif verb[-2:] == "ir":
                if c1[:-1] == verb[:-2] and c1[-1] == 'i' and c2[:-2] == verb[:-2] and c2[-2:] == 'iu' and c3[:-4] == verb[:-2] and c3[-4:] == 'iram':
                    return False
                else:
                    return True
            else:
                return True