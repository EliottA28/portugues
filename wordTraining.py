from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

import json
import numpy as np

class WordTraining(QMainWindow):
    def __init__(self, word_type, screen_dim, mode):
        super().__init__()
        self.setWindowTitle("Word Training")
        self.setGeometry(200,200,635,320)
        
        # enable switch between translation
        self.fr2bra = True
        self.mode = mode

        # load data
        with open('database.json', 'r') as f:
            self.data = json.load(f)

        self.random_word_list = list(self.data.items())
        if word_type == "noun":
            self.random_word_list = [self.random_word_list[i] for i in range(len(self.random_word_list)) if self.random_word_list[i][1]["type"] == "mn" or self.random_word_list[i][1]["type"] == "fn"]
        elif word_type != "all":
            self.random_word_list = [self.random_word_list[i] for i in range(len(self.random_word_list)) if self.random_word_list[i][1]["type"] == word_type]
        self.type = word_type
        self.scores = np.array([self.random_word_list[k][1]['score'] for k in range(len(self.random_word_list))])
        
        # select a word
        self.select_random_word()

        # head label
        head = QLabel("Translate the Words " + '(' + self.type + ')', self)  
        font = QFont('Times', 20)
        font.setBold(True)
        font.setUnderline(True)
        head.setFont(font)
        head.setAlignment(Qt.AlignCenter)

        # label to show word and note
        if self.type == 'all':
            self.word = QLabel(self.random_word_fr + " / " + self.random_word_eng+ ' (' + self.cur_type + ')', self)
        else:
            self.word = QLabel(self.random_word_fr + " / " + self.random_word_eng, self)
        self.word.setAlignment(Qt.AlignCenter)
        self.word.setFont(QFont('Times', 30))

        self.note = QLabel(self.definition, self)
        self.note.setAlignment(Qt.AlignCenter)
        self.note.setFont(QFont('Times', 15))
  
        # line edit
        self.input_text = QLineEdit(self)
        self.input_text.setFont(QFont('Arial', 14))
        self.input_text.returnPressed.connect(self.input_action)

        # reset knowledge button
        self.b1 = QPushButton("Reset Knowledge", self)
        self.b1.clicked.connect(self.reset_knowledge)
        self.b1.adjustSize()

        # switch translation button
        self.b2 = QPushButton("Switch Translation", self)
        self.b2.clicked.connect(self.switch_translation)
        self.b2.adjustSize()

        # layout
        form = QFormLayout()
        
        layout = QGridLayout()
        layout.addLayout(form, 0, 0)
        widget_1 = QWidget()
        widget_1.setLayout(layout)
        self.setCentralWidget(widget_1)

        layout.addWidget(head, 0, 1)
        layout.addWidget(self.word, 1, 1)
        layout.addWidget(self.note, 2, 1)
        layout.addWidget(self.input_text, 3, 1)
        layout.addWidget(self.b1, 4, 0, Qt.AlignLeft | Qt.AlignBottom)
        layout.addWidget(self.b2, 4, 2, Qt.AlignRight | Qt.AlignBottom)

    def select_random_word(self):
        if self.mode == "weighted":
            self.weights = np.exp(-self.scores)/np.sum(np.exp(-self.scores))
            idx = np.random.choice(len(self.random_word_list), p=self.weights)
        elif self.mode == "random":
            idx = np.random.choice(len(self.random_word_list))
        dict = self.random_word_list[idx][1]
        self.word_id = self.random_word_list[idx][0]
        self.translation, self.random_word_fr, self.random_word_eng, self.cur_type = dict["bra"], dict["fr"], dict["eng"], dict["type"]
        self.definition = dict["def"]
        self.synonymes = [i[1]["bra"] for i in self.random_word_list if i[1]["fr"] == self.random_word_fr and i[1]["eng"] == self.random_word_eng and i[1]["def"] == self.definition]

    def reset_knowledge(self):
        self.show_popup()
    
    def show_popup(self):
        msg = QMessageBox()
        msg.setText("Reset weights ?")
        msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Yes)
        msg.buttonClicked.connect(self.popup_button)
        msg.exec_()

    def popup_button(self, i):
        if i.text() == "&Yes":
            for key in self.data.keys():
                if self.type == "noun":
                    if self.data[key]["type"] == 'fn' or self.data[key]["type"] == 'mn':
                        self.data[key]["score"] = 0
                elif self.type == "all":
                    self.data[key]["score"] = 0
                elif self.data[key]["type"] == self.type:
                    self.data[key]["score"] = 0
            with open('database.json', 'w') as f:
                json.dump(self.data, f)
            self.scores = np.zeros(len(self.random_word_list))
            self.display_new_word()

    def input_action(self):
        text = self.input_text.text()
        text = text.lower()
        if text != "" and self.fr2bra:
            if text == self.translation or text in self.synonymes:
                self.update_score(self.word_id, 1)
            else:
                self.update_score(self.word_id, -1)
                self.display_correction(self.random_word_fr +  " : " + self.translation)
            self.display_new_word()
        elif text != "" and not self.fr2bra:
            if text == self.random_word_eng or text == self.random_word_fr:
                self.update_score(self.word_id, 1)
            else:
                self.update_score(self.word_id, -1)
                self.display_correction(self.translation +  " : " + self.random_word_fr + ' / ' + self.random_word_eng)
            self.display_new_word()

    def update_score(self, key, i):
        self.data[key]["score"] = max(0, self.data[key]["score"] + i)
        self.scores = np.array([self.random_word_list[k][1]['score'] for k in range(len(self.random_word_list))])
        with open('database.json', 'w') as f:
            json.dump(self.data, f) 

    def display_new_word(self):
        self.input_text.clear()
        self.select_random_word()
        self.note.setText(self.definition)
        if self.fr2bra:
            if self.type == 'all':
                self.word.setText(self.random_word_fr + " / " + self.random_word_eng +' ('+self.cur_type+')')
            else:
                self.word.setText(self.random_word_fr + " / " + self.random_word_eng)
        else:
            if self.type == 'all':
                self.word.setText(self.translation +' ('+self.cur_type+')')
            else:
                self.word.setText(self.translation)

    def switch_translation(self):
        self.fr2bra = not self.fr2bra
        self.display_new_word()

    def display_correction(self, correction):
        msg = QMessageBox()
        msg.setText("Correction\n")
        msg.setInformativeText(correction + "\n")
        msg.exec_()