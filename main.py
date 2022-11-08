from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

from wordTraining import TrainingWindow
from conjugationTraining import TrainingVerbWindow
from modifier import ModifierWindow

import sys
import json
  
# key : word portuguese / value : word french, word english, definition, type (feminin word, masculin word, adj, verb ...)
# {"comer": {"fr": "manger", "eng": "eat", "def": "", "type": "verb"}, "pequeno": {"fr": "petit", "eng": "small", "def": "", "type": "adj"}}

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200,200,1000,800)
        self.setWindowTitle('🇧🇷')

        self.initUI()

    def initUI(self):
        """add a new word to the database"""
        ## Add New Word to Database
        self.form_1 = QFormLayout()
        
        self.word, self.fr_trad, self.eng_trad, self.definition_input = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
        self.type = QComboBox()
        self.type.addItems(["fn", "mn", "verb", "adj", "other"])
        self.type.currentIndexChanged.connect(self.display_input)
        self.b1 = QPushButton("Adicionar uma Nova Palavra")
        self.title_1 = QLabel("Adicionar uma Nova Palavra :")
        self.title_1.setFont(QFont("Helvetica", 20, QFont.Bold))

        self.form_1.addRow(self.title_1)
        self.form_1.addRow(QLabel("Português"), self.word)
        self.form_1.addRow(QLabel("Francês"), self.fr_trad)
        self.form_1.addRow(QLabel("Inglês"), self.eng_trad)
        self.form_1.addRow(QLabel("Definição"), self.definition_input)
        self.form_1.addRow(QLabel("Tipo"), self.type)
        self.form_1.addRow(self.b1)

        # Word List
        form_3 = QFormLayout()
        
        self.word_list = QListWidget()
        with open('database.json', 'r+') as f:
            database = json.load(f)
        for key in database.keys():
            self.word_list.addItem(key)
        self.word_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.word_list.resetHorizontalScrollMode()
        self.word_list.sortItems()
        self.word_list.setCurrentRow(0)
        self.word_list.itemSelectionChanged.connect(self.selectionChanged)
        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.search_word)
        self.selected_word = QLabel(self.word_list.currentItem().text())
        self.traduction_fr = QLabel(database[self.selected_word.text()]["fr"])
        self.traduction_eng = QLabel(database[self.selected_word.text()]["eng"])
        self.definition = QLabel(database[self.selected_word.text()]["def"])
        self.definition.setMaximumSize(int(self.width()*0.4), int(self.height()*0.15))
        self.title_3 = QLabel("Palavras ({}) :".format(len(database)))
        self.title_3.setFont(QFont("Helvetica", 20, QFont.Bold))
        self.b5 = QPushButton("Modifier/Supprimer")

        form_3.addRow(self.title_3)
        form_3.addRow(QLabel("Search Word :"), self.search_bar)
        form_3.addRow(self.word_list)
        form_3.addRow(QLabel("Tradução Francesa :"), self.traduction_fr)
        form_3.addRow(QLabel("Tradução Inglesa :"), self.traduction_eng)
        form_3.addRow(QLabel("Definição :"), self.definition)
        form_3.addRow(self.b5)
        self.b5.clicked.connect(self.b5Action)
        
        # Test Knowledge
        form_4 = QFormLayout()

        self.select_training_1 = QComboBox()
        self.select_training_1.addItems(["all", "verb", "adj", "noun", "other"])

        self.b3 = QPushButton("Ensaio (palavras)")
        form_4.addRow(self.b3, self.select_training_1)
        
        self.select_training_2 = QComboBox()
        self.select_training_2.addItems(["all", "regular", "irregular"])

        self.b4 = QPushButton("Ensaio (verbos)")
        form_4.addRow(self.b4, self.select_training_2)

        # Layout Grid
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

        # Button to Add New Word 
        self.b1.clicked.connect(self.b1Action)

        # Training Button
        self.b3.clicked.connect(self.b3Action)
        self.b4.clicked.connect(self.b4Action)

    def search_word(self):
        model = self.word_list.model()
        match = model.match(
            model.index(0, self.word_list.modelColumn()), 
            Qt.DisplayRole, 
            self.search_bar.text(), 
            hits=1, 
            flags=Qt.MatchStartsWith)
        if match:
            self.word_list.setCurrentIndex(match[0])
    
    def b1Action(self):
        """add word to dictionary"""
        with open('database.json', 'r+') as f:
            database = json.load(f)

        if len(self.word.text()) == 0:
            self.raiseError("Enter a word")
        if self.type.currentText() == "verb" and (self.conj1.text() == "" or self.conj2.text() == "" or self.conj3.text() == ""):
            self.raiseError("Enter conjugaison")
        elif self.word.text() not in database:
            if self.form_1.rowCount() == 11:
                conj = self.conj1.text() +"_"+ self.conj2.text() +"_"+ self.conj3.text()
            else:
                conj = ""
            database[self.word.text()] = {"fr": self.fr_trad.text(), 
                                          "eng": self.eng_trad.text(), 
                                          "def": self.definition_input.text(), 
                                          "type": self.type.currentText(),
                                          "score" : 0,
                                          "conj": conj}
            self.new_words.addItems([self.word.text()])
            self.word_list.addItem(self.word.text())
        else:
            self.raiseError("Você já sabe essa palavra")
        
        with open('database.json', 'w') as f:
            json.dump(database, f)   
    
    def b3Action(self):
        self.w1 = TrainingWindow(self.select_training_1.currentText())
        self.w1.show()

    def b4Action(self):
        self.w2 = TrainingVerbWindow(self.select_training_2.currentText())
        self.w2.show()

    def b5Action(self):
        self.w3 = ModifierWindow(self.word_list.currentItem().text())
        self.w3.show()

    def raiseError(self, error):
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

    def selectionChanged(self):
        with open('database.json', 'r+') as f:
                database = json.load(f)
        self.selected_word.setText(self.word_list.currentItem().text())
        self.traduction_fr.setText(database[self.word_list.currentItem().text()]["fr"])
        self.traduction_eng.setText(database[self.word_list.currentItem().text()]["eng"])
        self.definition.setText(database[self.selected_word.text()]["def"])

def window():
    app = QApplication(sys.argv)

    win = MainWindow()

    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()