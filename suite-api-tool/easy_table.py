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
            last_column_index = self.columnCount() - 1

            clipboard_content = list()
            row = list()
            column_headers = list()

            for i in range(0,last_column_index):
                column_headers.append(str(self.horizontalHeaderItem(i).text()))
            clipboard_content.append('\t'.join(column_headers))
            clipboard_content.append('\n')

            for item in self.selectedItems():
                row.append(str(item.text()))
                if item.column() == last_column_index:
                    clipboard_content.append('\t'.join(row))
                    clipboard_content.append('\n')
                    row.clear()
            self.clipboard.setText(''.join(clipboard_content))
