from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from input_form import InputForm
import config 
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
        self.fr_trad = self.data[self.word_id]["known"].split('_')
        self.definition = self.data[self.word_id]["notes"]
        self.type = self.data[self.word_id]["type"]

        self.form_1 = QFormLayout()
        self.input_form = InputForm(self, self.form_1)

        self.input_form.word.setText(self.word)
        self.input_form.fr_trad.setText(self.fr_trad[0])
        self.input_form.notes_input.insertPlainText(self.definition)
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

        # buttons
        self.b1 = QPushButton("Modifier")
        self.b1.clicked.connect(self.modify_word)
        self.b2 = QPushButton("Supprimer")
        self.b2.clicked.connect(self.delete_word)
        self.b3 = QPushButton("Annuler")
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
        if len(self.input_form.word.text().strip().lower()) == 0 and len(self.input_form.fr_trad.text().strip().lower()) == 0:
            self.raise_error("Entrer un mot et au moins une traduction")
        elif len(self.input_form.fr_trad.text().strip().lower()) == 0:
            self.raise_error("Entrer une traduction")
        elif len(self.input_form.word.text().strip().lower()) == 0:
            self.raise_error("Entrer un mot")
        else:            
            fr = ""
            for i in range(self.init_length, self.form_1.rowCount(), 1):
                widget = self.form_1.itemAt(i).widget()
                if type(widget) is QWidget and widget.metadata == 3:
                    metadata = widget.children()[2].metadata
                    if metadata == 0:
                        fr += '_' + widget.children()[1].text()
            if self.input_form.word.text().strip().lower() != self.word:
                self.data[self.word_id]["unknown"] = self.input_form.word.text().strip().lower()
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
                        self.p.word_list.setCurrentItem(item_to_add)        
            self.data[self.word_id]["known"] = self.input_form.fr_trad.text().strip().lower()+fr
            self.data[self.word_id]["notes"] = self.input_form.notes_input.toPlainText()
            self.data[self.word_id]["type"] = self.input_form.type.currentText()
            self.p.traduction_fr.setText(self.data[self.word_id]["known"])
            self.p.notes.setPlainText(self.data[self.word_id]["notes"])

            with open('database.json', 'w') as f:
                json.dump(self.data, f)
            self.close()

    def delete_word(self):
        self.show_popup()
    
    def show_popup(self):
        msg = QMessageBox()
        msg.setText("Supprimer le Mot ?")
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