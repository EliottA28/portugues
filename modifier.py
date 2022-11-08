from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

import json

class ModifierWindow(QMainWindow):
    def __init__(self, word):
        super().__init__()
        self.setWindowTitle("Modifier")
        self.setGeometry(200,200,500,300)
        
        with open('database.json', 'r') as f:
            self.data = json.load(f)

        self.word = word
        self.fr_trad = self.data[word]["fr"]
        self.eng_trad = self.data[word]["eng"]
        self.definition = self.data[word]["def"]
        self.type = self.data[word]["type"]
        self.conj = self.data[word]["conj"]

        self.form_1 = QFormLayout()
        
        self.word_input, self.fr_trad_input, self.eng_trad_input, self.definition_input = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
        self.type_input = QComboBox()
        self.type_input.addItems(["fn", "mn", "verb", "adj", "other"])

        self.word_input.setText(self.word)
        self.fr_trad_input.setText(self.fr_trad)
        self.eng_trad_input.setText(self.eng_trad)
        self.definition_input.setText(self.definition)
        self.type_input.setCurrentText(self.type)

        self.form_1.addRow(QLabel("Português"), self.word_input)
        self.form_1.addRow(QLabel("Francês"), self.fr_trad_input)
        self.form_1.addRow(QLabel("Inglês"), self.eng_trad_input)
        self.form_1.addRow(QLabel("Definição"), self.definition_input)
        self.form_1.addRow(QLabel("Tipo"), self.type_input)

        layout = QGridLayout()

        layout.addLayout(self.form_1, 0, 0)
        widget_1 = QWidget()
        widget_1.setLayout(layout)
        self.setCentralWidget(widget_1)

        if self.type == "verb":
            self.conj1, self.conj2, self.conj3 = QLineEdit(), QLineEdit(), QLineEdit()
            
            if self.conj != "":
                self.t1, self.t2, self.t3 = self.conj.split('_')
                self.conj1.setText(self.t1)
                self.conj2.setText(self.t2)
                self.conj3.setText(self.t3)

            self.form_1.addRow(QLabel("Conjugation :"))
            self.form_1.addRow(QLabel("Eu"), self.conj1)
            self.form_1.addRow(QLabel("Ele"), self.conj2)
            self.form_1.addRow(QLabel("Eles"), self.conj3)

        self.form_3 = QFormLayout()

        self.b1 = QPushButton("Modifier")
        self.b1.clicked.connect(self.b1Action)
        self.form_3.addRow(self.b1)
        self.b2 = QPushButton("Delete")
        self.b2.clicked.connect(self.b2Action)
        self.form_3.addRow(self.b2)
        self.b3 = QPushButton("Cancel")
        self.b3.clicked.connect(self.b3Action)
        self.form_3.addRow(self.b3)

        layout.addLayout(self.form_3, 0, 2)
        widget_3 = QWidget()
        widget_3.setLayout(layout)
        self.setCentralWidget(widget_3)

    def b1Action(self):
        if self.word_input.text() == "":
            self.raiseError("Enter a Word")
        else:
            if self.word_input.text() != self.word:
                s = self.data[self.word]["score"]
                del self.data[self.word]
                if self.type_input.currentText() == "verb":
                    conj = self.conj1.text() +"_"+ self.conj2.text() +"_"+ self.conj3.text()
                else:
                    conj = ""
                self.data[self.word_input.text()] = {"fr": self.fr_trad_input.text(), 
                                                    "eng": self.eng_trad_input.text(), 
                                                    "def": self.definition_input.text(), 
                                                    "type": self.type_input.currentText(),
                                                    "score" : s,
                                                    "conj": conj}

            else:
                self.data[self.word]["fr"] = self.fr_trad_input.text()
                self.data[self.word]["eng"] = self.eng_trad_input.text()
                self.data[self.word]["def"] = self.definition_input.text()
                self.data[self.word]["type"] = self.type_input.currentText()
                if self.type_input.currentText() == "verb":
                    self.data[self.word]["conj"] = self.conj1.text() +"_"+ self.conj2.text() +"_"+ self.conj3.text()
                else:
                    self.data[self.word]["conj"] = ""
            
            with open('database.json', 'w') as f:
                json.dump(self.data, f)
            
            self.close()

    def b2Action(self):
        del self.data[self.word]
        with open('database.json', 'w') as f:
            json.dump(self.data, f)

        self.close()

    def b3Action(self):
        self.close()

    def raiseError(self, error):
        msg = QMessageBox()
        msg.setText(error)
        msg.exec_()