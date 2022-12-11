from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

import json

class ModifyDictionary(QMainWindow):
    def __init__(self, word, parent):
        super().__init__()
        self.setWindowTitle("Modifier")
        self.setGeometry(200,200,500,300)
        
        self.parent = parent

        with open('database.json', 'r') as f:
            self.data = json.load(f)

        # data input
        self.word = word.text()
        self.word_id = word.data(Qt.UserRole)
        self.fr_trad = self.data[self.word_id]["fr"]
        self.eng_trad = self.data[self.word_id]["eng"]
        self.definition = self.data[self.word_id]["def"]
        self.type = self.data[self.word_id]["type"]
        self.conj = self.data[self.word_id]["conj"]
        self.conj_pp = self.data[self.word_id]["conj_pp"]
        self.word_input, self.fr_trad_input, self.eng_trad_input, self.definition_input = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
        self.type_input = QComboBox()
        self.type_input.addItems(["fn", "mn", "verb", "adj", "other"])

        self.word_input.setText(self.word)
        self.fr_trad_input.setText(self.fr_trad)
        self.eng_trad_input.setText(self.eng_trad)
        self.definition_input.setText(self.definition)
        self.type_input.setCurrentText(self.type)

        # form
        self.form_1 = QFormLayout()
        self.form_1.addRow(QLabel("Português"), self.word_input)
        self.form_1.addRow(QLabel("Francês"), self.fr_trad_input)
        self.form_1.addRow(QLabel("Inglês"), self.eng_trad_input)
        self.form_1.addRow(QLabel("Definição"), self.definition_input)
        self.form_1.addRow(QLabel("Tipo"), self.type_input)

        self.type_input.currentIndexChanged.connect(self.display_conj)

        if self.type == "verb":
            self.conj1, self.conj2, self.conj3 = QLineEdit(), QLineEdit(), QLineEdit()
            self.conj4, self.conj5, self.conj6 = QLineEdit(), QLineEdit(), QLineEdit()

            self.widget0 = QWidget()
            layout_h0 = QHBoxLayout(self.widget0)
            layout_h0.addWidget(QLabel("Presente                     "))
            layout_h0.addWidget(QLabel("Pretérito Perfeito"))
            self.widget1 = QWidget()
            layout_h1 = QHBoxLayout(self.widget1)
            layout_h1.addWidget(self.conj1)
            layout_h1.addWidget(self.conj4)
            self.widget2 = QWidget()
            layout_h2 = QHBoxLayout(self.widget2)
            layout_h2.addWidget(self.conj2)
            layout_h2.addWidget(self.conj5)
            self.widget3 = QWidget()
            layout_h3 = QHBoxLayout(self.widget3)
            layout_h3.addWidget(self.conj3)
            layout_h3.addWidget(self.conj6)

            if self.conj != "":
                self.t1, self.t2, self.t3 = self.conj.split('_')
                self.conj1.setText(self.t1)
                self.conj2.setText(self.t2)
                self.conj3.setText(self.t3)
            if self.conj_pp != "":
                self.t4, self.t5, self.t6 = self.conj_pp.split('_')
                self.conj4.setText(self.t4)
                self.conj5.setText(self.t5)
                self.conj6.setText(self.t6)

            self.form_1.addRow(QLabel("Conjugation :"))
            self.form_1.addRow(QLabel(""), self.widget0)
            self.form_1.addRow(QLabel("Eu"), self.widget1)
            self.form_1.addRow(QLabel("Ele"), self.widget2)
            self.form_1.addRow(QLabel("Eles"), self.widget3)

        # buttons
        self.b1 = QPushButton("Modifier")
        self.b1.clicked.connect(self.modify_word)
        self.b2 = QPushButton("Delete")
        self.b2.clicked.connect(self.delete_word)
        self.b3 = QPushButton("Cancel")
        self.b3.clicked.connect(self.close_window)

        # form
        self.form_2 = QFormLayout()
        self.form_2.addRow(self.b1)
        self.form_2.addRow(self.b2)
        self.form_2.addRow(self.b3)

        # layout
        layout = QGridLayout()

        layout.addLayout(self.form_1, 0, 0)
        widget_1 = QWidget()
        widget_1.setLayout(layout)
        self.setCentralWidget(widget_1)

        layout.addLayout(self.form_2, 0, 2)
        widget_3 = QWidget()
        widget_3.setLayout(layout)
        self.setCentralWidget(widget_3)

    def modify_word(self):
        if self.word_input.text() == "":
            self.raise_error("Enter a Word")
        else:
            if self.word_input.text() != self.word:
                s = self.data[self.word_id]["score"]
                del self.data[self.word_id]
                item = self.parent.word_list.findItems(self.word, Qt.MatchExactly)
                r = self.parent.word_list.row(item[0])
                self.parent.word_list.takeItem(r)
                item_to_add = QListWidgetItem()
                item_to_add.setText(self.word_input.text())   
                item_to_add.setData(Qt.UserRole, self.word_id) 
                self.parent.word_list.addItem(item_to_add)
                self.parent.word_list.sortItems()
                if self.type_input.currentText() == "verb":
                    conj = self.conj1.text() +"_"+ self.conj2.text() +"_"+ self.conj3.text()
                else:
                    conj = ""
                self.data[self.word_id] = {"bra": self.word_input.text(),
                                            "fr": self.fr_trad_input.text(), 
                                            "eng": self.eng_trad_input.text(), 
                                            "def": self.definition_input.text(), 
                                            "type": self.type_input.currentText(),
                                            "score" : s,
                                            "conj": conj}
            else:
                self.data[self.word_id]["fr"] = self.fr_trad_input.text()
                self.data[self.word_id]["eng"] = self.eng_trad_input.text()
                self.data[self.word_id]["def"] = self.definition_input.text()
                self.data[self.word_id]["type"] = self.type_input.currentText()
                if self.type_input.currentText() == "verb":
                    self.data[self.word_id]["conj"] = self.conj1.text() +"_"+ self.conj2.text() +"_"+ self.conj3.text()
                else:
                    self.data[self.word_id]["conj"] = ""
            
            with open('database.json', 'w') as f:
                json.dump(self.data, f)
            self.close()

    def delete_word(self):
        del self.data[self.word_id]
        self.parent.title_3.setText("Palavras ({}) :".format(len(self.data)))
        item = self.parent.word_list.currentItem()
        r = self.parent.word_list.row(item)
        self.parent.word_list.takeItem(r)
        with open('database.json', 'w') as f:
            json.dump(self.data, f)
        self.close()

    def close_window(self):
        self.close()

    def raise_error(self, error):
        msg = QMessageBox()
        msg.setText(error)
        msg.exec_()

    def display_conj(self):
        sender = self.sender()
        idx, _ = self.form_1.getWidgetPosition(sender)
        if self.type_input.currentText() == "verb":
            
            self.conj1, self.conj2, self.conj3 = QLineEdit(), QLineEdit(), QLineEdit()
            self.conj4, self.conj5, self.conj6 = QLineEdit(), QLineEdit(), QLineEdit()

            self.widget0 = QWidget()
            layout_h0 = QHBoxLayout(self.widget0)
            layout_h0.addWidget(QLabel("Presente                     "))
            layout_h0.addWidget(QLabel("Pretérito Perfeito"))
            self.widget1 = QWidget()
            layout_h1 = QHBoxLayout(self.widget1)
            layout_h1.addWidget(self.conj1)
            layout_h1.addWidget(self.conj4)
            self.widget2 = QWidget()
            layout_h2 = QHBoxLayout(self.widget2)
            layout_h2.addWidget(self.conj2)
            layout_h2.addWidget(self.conj5)
            self.widget3 = QWidget()
            layout_h3 = QHBoxLayout(self.widget3)
            layout_h3.addWidget(self.conj3)
            layout_h3.addWidget(self.conj6)

            self.form_1.insertRow(idx+1, QLabel("Conjugation :"))
            self.form_1.insertRow(idx+2, QLabel(""), self.widget0)
            self.form_1.insertRow(idx+3, QLabel("Eu"), self.widget1)
            self.form_1.insertRow(idx+4, QLabel("Ele"), self.widget2)
            self.form_1.insertRow(idx+5, QLabel("Eles"), self.widget3)
            self.flag = 1
        else:
            if self.flag:
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.flag = 0