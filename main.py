from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

from wordTraining import WordTraining
from conjugationTraining import ConjugationTraining
from modifyDictionary import ModifyDictionary

import sys
import json
  
# {"comer": {"fr": "manger", "eng": "eat", "def": "", "type": "verb", "score": 4, "conj": "como_come_comem"}

class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super(MainWindow, self).__init__()
        self.screen_dim = (width, height)

        self.setGeometry(200,200,1000,800)
        self.setWindowTitle('🇧🇷')

        ### layouts ###

        ## add word to dictionary
        # add multiple translations
        self.number_of_translations = 3
        self.counter = [0, 0]
        # inputs
        self.title_1 = QLabel("Adicionar uma Nova Palavra :")
        self.title_1.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.word, self.fr_trad, self.eng_trad, self.definition_input = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
        self.type = QComboBox()
        self.type.addItems(["fn", "mn", "verb", "adj", "other"])
        self.type.currentIndexChanged.connect(self.display_input)
        self.b1 = QPushButton("Adicionar uma Nova Palavra")
        self.b1.clicked.connect(self.fill_dictionary)

        self.b_add_fr = QPushButton("+")
        self.b_add_fr.metadata = 0
        self.b_add_fr.clicked.connect(self.add_translation_row)
        self.widget_fr = QWidget()
        layout_h_fr = QHBoxLayout(self.widget_fr)
        layout_h_fr.addWidget(self.fr_trad)
        layout_h_fr.addWidget(self.b_add_fr)

        self.b_add_eng = QPushButton("+")
        self.b_add_eng.metadata = 1
        self.b_add_eng.clicked.connect(self.add_translation_row)
        self.widget_eng = QWidget()
        layout_h_eng = QHBoxLayout(self.widget_eng)
        layout_h_eng.addWidget(self.eng_trad)
        layout_h_eng.addWidget(self.b_add_eng)
        # form
        self.form_1 = QFormLayout()
        self.form_1.addRow(self.title_1)
        self.form_1.addRow(QLabel("Português"), self.word)
        self.form_1.addRow(QLabel("Francês"), self.widget_fr)
        self.form_1.addRow(QLabel("Inglês"), self.widget_eng)
        self.form_1.addRow(QLabel("Definição"), self.definition_input)
        self.form_1.addRow(QLabel("Tipo"), self.type)
        self.form_1.addRow(self.b1)
        ## data interface
        # word list
        self.word_list = QListWidget()
        with open('database.json', 'r+') as f:
            database = json.load(f)
        for key in database.keys():
            item_to_add = QListWidgetItem()
            item_to_add.setText(database[key]["bra"])   
            item_to_add.setData(Qt.UserRole, key) 
            self.word_list.addItem(item_to_add)
        self.word_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.word_list.resetHorizontalScrollMode()
        self.word_list.sortItems()
        self.word_list.setCurrentRow(0)
        self.word_list.itemSelectionChanged.connect(self.selection_changed)

        # search bar
        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.search_word)

        # display/modify word info
        self.selected_word = QLabel(self.word_list.currentItem().text())
        self.word_id = self.word_list.currentItem().data(Qt.UserRole)
        self.traduction_fr = QLabel(database[self.word_id]["fr"])
        self.traduction_eng = QLabel(database[self.word_id]["eng"])
        self.definition = QLabel(database[self.word_id]["def"])
        self.definition.setMaximumSize(int(self.width()*0.4), int(self.height()*0.15))
        self.title_3 = QLabel("Palavras ({}) :".format(len(database)))
        self.title_3.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.b5 = QPushButton("Modifier/Supprimer")
        self.b5.clicked.connect(self.modify_dictionary)

        # form
        form_3 = QFormLayout()
        form_3.addRow(self.title_3)
        form_3.addRow(QLabel("Search Word :"), self.search_bar)
        form_3.addRow(self.word_list)
        form_3.addRow(QLabel("Tradução Francesa :"), self.traduction_fr)
        form_3.addRow(QLabel("Tradução Inglesa :"), self.traduction_eng)
        form_3.addRow(QLabel("Definição :"), self.definition)
        form_3.addRow(self.b5)
        
        ## test knowledge
        # words
        self.select_training_1 = QComboBox()
        self.select_training_1.addItems(["all", "verb", "adj", "noun", "other"])
        self.b3 = QPushButton("Ensaio (palavras)")
        self.b3.clicked.connect(self.train_word)
        
        # conjugation
        self.select_training_2 = QComboBox()
        self.select_training_2.addItems(["all", "regular", "irregular"])
        self.b4 = QPushButton("Ensaio (verbos)")
        self.b4.clicked.connect(self.train_conjugation)

        # form
        form_4 = QFormLayout()
        form_4.addRow(self.b3, self.select_training_1)
        form_4.addRow(self.b4, self.select_training_2)

        ### layout grid ###

        layout = QGridLayout()

        layout.addLayout(self.form_1, 0, 0)
        widget_1 = QWidget()
        widget_1.setLayout(layout)
        self.setCentralWidget(widget_1)

        layout.addLayout(form_3, 0, 1)
        widget_3 = QWidget()
        widget_3.setLayout(layout)
        self.setCentralWidget(widget_3)

        layout.addLayout(form_4, 1, 0)
        widget_4 = QWidget()
        widget_4.setLayout(layout)
        self.setCentralWidget(widget_4)

    def search_word(self):
        with open('database.json', 'r+') as f:
            database = json.load(f)
        bra_words = []
        fr_words = []
        eng_words = []
        for k in database.keys():
            bra_words.append(database[k]["bra"])
            fr_words.append(database[k]["fr"])
            eng_words.append(database[k]["eng"])
        word = self.search_bar.text()
        if word in fr_words:
            idx = fr_words.index(word)
            word = bra_words[idx]
        elif word in eng_words:
            idx = eng_words.index(word)
            word = bra_words[idx]
        model = self.word_list.model()
        match = model.match(
            model.index(0, self.word_list.modelColumn()), 
            Qt.DisplayRole, 
            word, 
            hits=1, 
            flags=Qt.MatchExactly)
        if match:
            self.word_list.setCurrentIndex(match[0])
    
    def check(self, word, data, i):
        words = []
        for d in data:
            if d[i] == word:
                words.append(d[2])
        return words

    def fill_dictionary(self):
        with open('database.json', 'r+') as f:
            database = json.load(f)

        data = [(key, value["bra"], value["type"]) for key, value in database.items()]

        if len(self.word.text()) == 0:
            self.raise_error("Enter a word")
        elif self.type.currentText() == "verb" and (self.conj1.text() == "" or self.conj2.text() == "" or self.conj3.text() == ""):
            self.raise_error("Enter conjugaison")
        elif not self.check(self.word.text(), data, 1) or self.type.currentText() not in self.check(self.word.text(), data, 1):
            if self.form_1.rowCount() == 11:
                conj = self.conj1.text() +"_"+ self.conj2.text() +"_"+ self.conj3.text()
            else:
                conj = ""
            key = str(int(list(database)[-1])+1)
            database[key] = {"bra": self.word.text(),
                            "fr": self.fr_trad.text(), 
                            "eng": self.eng_trad.text(), 
                            "def": self.definition_input.text(), 
                            "type": self.type.currentText(),
                            "score" : 0,
                            "conj": conj}
            item_to_add = QListWidgetItem()
            item_to_add.setText(self.word.text())   
            item_to_add.setData(Qt.UserRole, key) 
            self.word_list.addItem(item_to_add)
            self.word_list.sortItems()
            self.title_3.setText("Palavras ({}) :".format(len(database)))
            with open('database.json', 'w') as f:
                json.dump(database, f)
        else:
            self.raise_error("Você já sabe essa palavra")   
    
    def train_word(self):
        self.w1 = WordTraining(self.select_training_1.currentText(), self.screen_dim)
        self.w1.show()

    def train_conjugation(self):
        self.w2 = ConjugationTraining(self.select_training_2.currentText())
        self.w2.show()

    def modify_dictionary(self):
        self.w3 = ModifyDictionary(self.word_list.currentItem(), parent=self)
        self.w3.show()

    def raise_error(self, error):
        msg = QMessageBox()
        msg.setText(error)
        msg.exec_()

    def display_input(self):
        if self.type.currentText() == "verb":
            self.conj1, self.conj2, self.conj3 = QLineEdit(), QLineEdit(), QLineEdit()
            self.form_1.insertRow(6, QLabel("Conjugation :"))
            self.form_1.insertRow(7, QLabel("Eu"), self.conj1)
            self.form_1.insertRow(8, QLabel("Ele"), self.conj2)
            self.form_1.insertRow(9, QLabel("Eles"), self.conj3)
        else:
            if self.form_1.rowCount() == 11:
                self.form_1.removeRow(6)
                self.form_1.removeRow(6)
                self.form_1.removeRow(6)
                self.form_1.removeRow(6)

    def selection_changed(self):
        with open('database.json', 'r+') as f:
            database = json.load(f)
        self.selected_word.setText(self.word_list.currentItem().text())
        self.word_id = self.word_list.currentItem().data(Qt.UserRole)
        self.traduction_fr.setText(database[self.word_id]["fr"])
        self.traduction_eng.setText(database[self.word_id]["eng"])
        self.definition.setText(database[self.word_id]["def"])

    def add_translation_row(self):
        sender = self.sender()
        i = sender.metadata
        b_rm = QPushButton("-")
        b_rm.metadata = i
        b_rm.clicked.connect(self.rm_translation_row)
        tr_input = QLineEdit()
        widget_tr = QWidget()
        layout_h_tr = QHBoxLayout(widget_tr)
        layout_h_tr.addWidget(tr_input)
        layout_h_tr.addWidget(b_rm)
        if self.counter[i] < self.number_of_translations:
            idx, _ = self.form_1.getWidgetPosition(sender.parent())
            print(idx+self.counter[i])
            self.form_1.insertRow(idx + self.counter[i] + 1, QLabel(''), widget_tr)
            self.counter[i] += 1

    def rm_translation_row(self):
        sender = self.sender()
        i = sender.metadata
        idx, _ = self.form_1.getWidgetPosition(sender.parent())
        self.form_1.removeRow(idx)
        self.counter[i] -= 1

def window():
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    win = MainWindow(width, height)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()