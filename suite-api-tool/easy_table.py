from PyQt5.QtWidgets import QTableWidget
from PyQt5 import QtCore
class EasyTable(QTableWidget):


    def __init__(self, clipboard):
        super(EasyTable, self).__init__()
        self.clipboard = clipboard

    def keyPressEvent(self, key_event):
        if key_event.key() == QtCore.Qt.Key_C and key_event.modifiers().__eq__(QtCore.Qt.ControlModifier):
            self.copySelectedCellsToClipboard()
        if key_event.key() == QtCore.Qt.Key_A and key_event.modifiers().__eq__(QtCore.Qt.ControlModifier):
            self.selectAll()
        if key_event.key() == QtCore.Qt.Key_Up:
            if(self.currentRow() > 0):
                self.selectRow(self.currentRow() - 1)
        if key_event.key() == QtCore.Qt.Key_Down:
            if(self.currentRow() < self.rowCount() - 1):
                self.selectRow(self.currentRow() + 1)


    def copySelectedCellsToClipboard(self):
        if len(self.selectedItems()) > 0:
            strings = list()
            row = list()
            last_row = None
            got_columns = False
            columns = list()
            for item in self.selectedItems():
                current_row = item.row()
                if(last_row is not None and last_row < current_row):
                    if(not got_columns):
                        strings.append('\t'.join(columns))
                        strings.append('\n')
                        got_columns = True
                    strings.append('\t'.join(row))
                    strings.append('\n')
                    row.clear()
                if(not got_columns):
                    str(self.horizontalHeaderItem(item.column()))
                    columns.append(str(self.horizontalHeaderItem(item.column()).text()))
                row.append(str(item.text()))
                last_row = item.row()
            self.clipboard.setText(''.join(strings))
