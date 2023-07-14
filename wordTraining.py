from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
import config

import json
import numpy as np
import random

class WordTraining(QMainWindow):
    def __init__(self, word_type, screen_dim, mode):
        super().__init__()
        self.setWindowTitle(config.QUIZ + " : {}".format(mode))
        self.setGeometry(200,200,635,320)
        
        # enable switch between translation
        self.fr2bra = True
        self.mode = mode

        # load data
        with open('database.json', 'r') as f:
            self.data = json.load(f)

        self.random_word_list = list(self.data.items())
        if word_type == config.NOUN:
            self.random_word_list = [self.random_word_list[i] for i in range(len(self.random_word_list)) if self.random_word_list[i][1]["type"] == "mn" or self.random_word_list[i][1]["type"] == "fn"]
        elif word_type != config.ALL:
            self.random_word_list = [self.random_word_list[i] for i in range(len(self.random_word_list)) if self.random_word_list[i][1]["type"] == word_type]
        self.type = word_type
        self.scores = np.array([self.random_word_list[k][1]['score'] for k in range(len(self.random_word_list))])
        
        # random indexes for sequential test
        self.rand_indexes = np.random.permutation(range(len(self.random_word_list)))
        self.cur_idx = 0
        self.success = 0

        # select a word
        self.select_random_word()

        # head label
        head = QLabel("Traduire " + '(' + self.type + ')', self)  
        font = QFont('Times', 20)
        font.setBold(True)
        font.setUnderline(True)
        head.setFont(font)
        head.setAlignment(Qt.AlignCenter)

        # test label
        if mode == "test":
            self.success_rate = QLabel("Taux de Réussite : 100.0 %")
            self.word_count = QLabel("Mot : "+str(self.cur_idx+1)+'/'+str(len(self.random_word_list)))

        # label to show word and note
        word_fr = self.random_word_fr.split('_')[random.randint(0,len(self.random_word_fr.split('_'))-1)]
        if self.type == 'tous':
            self.word = QLabel(word_fr, self)
        else:
            self.word = QLabel(word_fr, self)
        self.word.setAlignment(Qt.AlignCenter)
        self.word.setFont(QFont('Times', 30))

        self.note = QPushButton('Notes', self)
        self.note.clicked.connect(self.display_notes)
        self.note.adjustSize()
  
        # line edit
        self.input_text = QLineEdit(self)
        self.input_text.setFont(QFont('Arial', 14))
        self.input_text.returnPressed.connect(self.input_action)

        # reset knowledge button
        self.b1 = QPushButton("Reset Weights", self)
        self.b1.clicked.connect(self.reset_knowledge)
        self.b1.adjustSize()

        # switch translation button
        self.b2 = QPushButton(config.LEARNED_LANGUAGED, self)
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
        layout.addWidget(self.b1, 6, 0, Qt.AlignLeft | Qt.AlignBottom)
        layout.addWidget(self.b2, 6, 2, Qt.AlignRight | Qt.AlignBottom)
        if mode == "test":
            layout.addWidget(self.word_count, 4, 1)
            layout.addWidget(self.success_rate, 5, 1)

    def update_success_rate(self, score):
        self.success += score
        self.cur_idx += 1
        if self.mode == 'test':
            self.success_rate.setText("Taux de réussite : "+str(np.round(self.success/self.cur_idx*100, 1))+' %')
            if self.cur_idx != len(self.random_word_list):
                self.word_count.setText("Mot : "+str(self.cur_idx+1)+'/'+str(len(self.random_word_list)))
    
    def select_random_word(self):
        if self.mode == "weighted":
            self.weights = np.exp(-self.scores)/np.sum(np.exp(-self.scores))
            idx = np.random.choice(len(self.random_word_list), p=self.weights)
        elif self.mode == config.RANDOM:
            idx = np.random.choice(len(self.random_word_list))
        elif self.mode == "test":
            idx = self.rand_indexes[self.cur_idx]
        dict = self.random_word_list[idx][1]
        self.word_id = self.random_word_list[idx][0]
        self.translation, self.random_word_fr, self.cur_type = dict["unknown"], dict["known"], dict["type"]
        self.definition = dict["notes"]
        self.synonymes = [i[1]["unknown"] for i in self.random_word_list if i[1]["known"] == self.random_word_fr and i[1]["notes"] == self.definition]

    def reset_knowledge(self):
        self.show_popup()
    
    def show_popup(self):
        msg = QMessageBox()
        msg.setText("Reset weights ?")
        msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Yes)
        msg.buttonClicked.connect(self.popup_button)
        msg.exec_()

    def display_notes(self):
        msg = QMessageBox()
        msg.setInformativeText(self.cur_type)
        if len(self.definition) != 0:
            msg.setText(self.definition)
        else:
            msg.setText("Aucune notes...")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def popup_button(self, i):
        if i.text() == "&Oui":
            for key in self.data.keys():
                if self.type == config.NOUN:
                    if self.data[key]["type"] == 'fn' or self.data[key]["type"] == 'mn':
                        self.data[key]["score"] = 0
                elif self.type == config.ALL:
                    self.data[key]["score"] = 0
                elif self.data[key]["type"] == self.type:
                    self.data[key]["score"] = 0
            with open('database.json', 'w') as f:
                json.dump(self.data, f)
            self.scores = np.zeros(len(self.random_word_list))
            self.display_new_word()

    def input_action(self):
        text = self.input_text.text().strip().lower()
        words_fr = self.random_word_fr.split('_')
        if text != "" and self.fr2bra:
            if text == self.translation or text in self.synonymes:
                self.update_score(self.word_id, 1)
                self.update_success_rate(1)
            else:
                self.update_success_rate(0)
                self.update_score(self.word_id, -1)
                self.display_correction(', '.join(words_fr) +  " : " + self.translation)
            self.display_new_word()
        elif text != "" and not self.fr2bra:
            if text in words_fr:
                self.update_score(self.word_id, 1)
                self.update_success_rate(1)
            else:
                self.update_success_rate(0)
                self.update_score(self.word_id, -1)
                self.display_correction(self.translation +  " : " + ', '.join(words_fr))
            self.display_new_word()

    def update_score(self, key, i):
        self.data[key]["score"] = max(0, self.data[key]["score"] + i)
        self.scores = np.array([self.random_word_list[k][1]['score'] for k in range(len(self.random_word_list))])
        with open('database.json', 'w') as f:
            json.dump(self.data, f) 

    def display_new_word(self):
        if self.cur_idx == len(self.random_word_list) and self.mode == "test":
            msg = QMessageBox()
            if self.success > 1 and (len(self.random_word_list)-self.success) > 1:
                msg.setText("Test terminé\n\n{} traductions correctes \n{} traductions incorrectes".format(self.success, len(self.random_word_list)-self.success))
            elif self.success <= 1 and (len(self.random_word_list)-self.success) > 1:
                msg.setText("Test terminé\n\n{} traduction correcte \n{} traductions incorrectes".format(self.success, len(self.random_word_list)-self.success))
            elif self.success > 1 and (len(self.random_word_list)-self.success) <= 1:
                msg.setText("Test terminé\n\n{} traductions correctes \n{} traduction incorrecte".format(self.success, len(self.random_word_list)-self.success))
            else:
                msg.setText("Test terminé\n\n{} traduction correcte \n{} traduction incorrecte".format(self.success, len(self.random_word_list)-self.success))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.close()
        else:
            self.input_text.clear()
            self.select_random_word()
            word_fr = self.random_word_fr.split('_')[random.randint(0,len(self.random_word_fr.split('_'))-1)]
            if self.fr2bra:
                if self.type == 'tous':
                    self.word.setText(word_fr)
                else:
                    self.word.setText(word_fr)
            else:
                if self.type == 'tous':
                    self.word.setText(self.translation)
                else:
                    self.word.setText(self.translation)

    def switch_translation(self):
        if self.fr2bra:
            self.b2.setText(config.KNOWN_LANGUAGED)
        else:
            self.b2.setText(config.LEARNED_LANGUAGED)
        self.fr2bra = not self.fr2bra
        self.display_new_word()

    def display_correction(self, correction):
        msg = QMessageBox()
        msg.setText("Correction\n")
        msg.setInformativeText(correction + "\n")
        msg.exec_()