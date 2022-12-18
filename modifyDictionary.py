from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from input_form import InputForm

import json

class ModifyDictionary(QMainWindow):
    def __init__(self, word, parent):
        super().__init__()
        self.setWindowTitle("Modifier")
        self.setGeometry(200,200,500,300)
        
        self.p = parent

        with open('database.json', 'r') as f:
            self.data = json.load(f)

        # data input
        self.word = word.text()
        self.word_id = word.data(Qt.UserRole)
        self.fr_trad = self.data[self.word_id]["fr"].split('_')
        self.eng_trad = self.data[self.word_id]["eng"].split('_')
        self.definition = self.data[self.word_id]["def"]
        self.type = self.data[self.word_id]["type"]
        self.conj = self.data[self.word_id]["conj"]
        self.conj_pp = self.data[self.word_id]["conj_pp"]

        self.form_1 = QFormLayout()
        self.input_form = InputForm(self, self.form_1)

        self.input_form.word.setText(self.word)
        self.input_form.fr_trad.setText(self.fr_trad[0])
        self.input_form.eng_trad.setText(self.eng_trad[0])
        self.input_form.definition_input.setText(self.definition)
        self.input_form.type.setCurrentText(self.type)

        # form
        for i in range(len(self.fr_trad[1:])):
            b_rm = QPushButton("-")
            b_rm.metadata = 0
            b_rm.clicked.connect(self.rm_translation_row)
            tr_input = QLineEdit()
            tr_input.setText(self.fr_trad[i+1])
            widget_tr = QWidget()
            layout_h_tr = QHBoxLayout(widget_tr)
            layout_h_tr.addWidget(tr_input)
            layout_h_tr.addWidget(b_rm)
            idx, _ = self.form_1.getWidgetPosition(self.input_form.widget_fr)
            self.form_1.insertRow(idx + self.input_form.counter[0] + 1, widget_tr)
            self.input_form.counter[0] += 1

        for i in range(len(self.eng_trad[1:])):
            b_rm = QPushButton("-")
            b_rm.metadata = 1
            b_rm.clicked.connect(self.rm_translation_row)
            tr_input = QLineEdit()
            tr_input.setText(self.eng_trad[i+1])
            widget_tr = QWidget()
            layout_h_tr = QHBoxLayout(widget_tr)
            layout_h_tr.addWidget(tr_input)
            layout_h_tr.addWidget(b_rm)
            idx, _ = self.form_1.getWidgetPosition(self.input_form.widget_eng)
            self.form_1.insertRow(idx + self.input_form.counter[1] + 1, widget_tr)
            self.input_form.counter[1] += 1

        self.input_form.type.currentIndexChanged.connect(self.display_conj)

        if self.type == "verb":
            if self.conj != "":
                self.t1, self.t2, self.t3 = self.conj.split('_')
                self.input_form.conj1.setText(self.t1)
                self.input_form.conj2.setText(self.t2)
                self.input_form.conj3.setText(self.t3)
            if self.conj_pp != "":
                self.t4, self.t5, self.t6 = self.conj_pp.split('_')
                self.input_form.conj4.setText(self.t4)
                self.input_form.conj5.setText(self.t5)
                self.input_form.conj6.setText(self.t6)

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
        
        self.init_length = self.form_1.rowCount()

    def modify_word(self):
        if self.input_form.word.text() == "":
            self.raise_error("Enter a Word")
        else:            
            fr = ""
            eng = ""
            for i in range(self.init_length, self.form_1.rowCount(), 1):
                widget = self.form_1.itemAt(i).widget()
                if type(widget) is QWidget and widget.metadata == 3:
                    metadata = widget.children()[2].metadata
                    if metadata == 0:
                        fr += '_' + widget.children()[1].text()
                    elif metadata == 1:
                        eng += '_' + widget.children()[1].text()
            if self.input_form.word.text() != self.word:
                self.data[self.word_id]["bra"] = self.input_form.word.text()
                items = self.p.word_list.findItems(self.word, Qt.MatchExactly)
                for item in items:
                    if item.data(Qt.UserRole) == self.word_id:
                        r = self.p.word_list.row(item)
                        self.p.word_list.takeItem(r)
                        item_to_add = QListWidgetItem()
                        item_to_add.setText(self.input_form.word.text())   
                        item_to_add.setData(Qt.UserRole, self.word_id) 
                        self.p.word_list.addItem(item_to_add)
                        self.p.word_list.sortItems()
            self.data[self.word_id]["fr"] = self.input_form.fr_trad.text()+fr
            self.data[self.word_id]["eng"] = self.input_form.eng_trad.text()+eng
            self.data[self.word_id]["def"] = self.input_form.definition_input.text()
            self.data[self.word_id]["type"] = self.input_form.type.currentText()
            if self.input_form.type.currentText() == "verb":
                self.data[self.word_id]["conj"] = self.input_form.conj1.text() +"_"+ self.input_form.conj2.text() +"_"+ self.input_form.conj3.text()
                self.data[self.word_id]["conj_pp"] = self.input_form.conj4.text() +"_"+ self.input_form.conj5.text() +"_"+ self.input_form.conj6.text()
            else:
                self.data[self.word_id]["conj"] = ""
                self.data[self.word_id]["conj_pp"] = ""

            with open('database.json', 'w') as f:
                json.dump(self.data, f)
            self.close()

    def delete_word(self):
        self.show_popup()
    
    def show_popup(self):
        msg = QMessageBox()
        msg.setText("Delete Word ?")
        msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Yes)
        msg.buttonClicked.connect(self.popup_button)
        msg.exec_()

    def popup_button(self, i):
        if i.text() == "&Yes":
            del self.data[self.word_id]
            self.p.title_3.setText("Palavras ({}) :".format(len(self.data)))
            item = self.p.word_list.currentItem()
            r = self.p.word_list.row(item)
            self.p.word_list.takeItem(r)
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
        sender = self.p.sender()
        idx, _ = self.form_1.getWidgetPosition(sender.parent())
        if self.input_form.type.currentText() == "verb":
            if self.conj != "":
                self.t1, self.t2, self.t3 = self.conj.split('_')
                self.input_form.conj1.setText(self.t1)
                self.input_form.conj2.setText(self.t2)
                self.input_form.conj3.setText(self.t3)
            if self.conj_pp != "":
                self.t4, self.t5, self.t6 = self.conj_pp.split('_')
                self.input_form.conj4.setText(self.t4)
                self.input_form.conj5.setText(self.t5)
                self.input_form.conj6.setText(self.t6)

            self.input_form.flag = 1
        else:
            if self.input_form.flag:
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.form_1.removeRow(idx+1)
                self.input_form.flag = 0

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
        if self.input_form.counter[i] < self.input_form.number_of_translations:
            idx, _ = self.form_1.getWidgetPosition(sender.parent())
            self.form_1.insertRow(idx + self.input_form.counter[i] + 1, widget_tr)
            self.input_form.counter[i] += 1

    def rm_translation_row(self):
        sender = self.sender()
        i = sender.metadata
        idx, _ = self.form_1.getWidgetPosition(sender.parent())
        self.form_1.removeRow(idx)
        self.input_form.counter[i] -= 1