import sys
import requests
import json
from PyQt5 import QtWidgets
# print('\n'.join(dir(requests)))
endpoint = "https://vr-61-p1-4/suite-api/api/adapterkinds"
response = requests.get(endpoint, auth=("admin", "P@ssw0rd1"), verify=False, headers={"Accept": "application/json"})
keys = list()

for thing in response.json()['adapter-kind']:
    keys.append((thing['key'], thing['name']))

keys.sort(key=lambda name: name[1])

app = QtWidgets.QApplication(sys.argv)

vbox = QtWidgets.QVBoxLayout()
hbox = QtWidgets.QHBoxLayout()
vbox.addLayout(hbox)
label = QtWidgets.QLabel("Adapter Type: ")
combo = QtWidgets.QComboBox()
hbox.addWidget(label)
hbox.addWidget(combo)
for key, name in keys:
    combo.addItem(name, key)

combo.setFixedSize(500,25)

# create table view
table = QtWidgets.QTableWidget()
item1 = QtWidgets.QTableWidgetItem("hallo.")
item1.setData(0, "hello!")
table.insertRow(0)
table.insertColumn(0)
table.setItem(0, 0, item1)

vbox.addWidget(table)

# create application window
window = QtWidgets.QWidget()
window.setLayout(vbox)
window.show()

app.exec_()
