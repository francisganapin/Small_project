import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import  QApplication
from pymongo import MongoClient
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from PyQt6 import  QtWidgets
import requests
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QDoubleValidator #SET ONLY NUMERICAL NUMBER INPUT IN YOUR QLINE EDIT

class MyAPP(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi('main.ui',self)
            
            #this will set fixed size base on our loade ui
            self.setFixedSize(self.size())

   
            self.save_bt.clicked.connect(self.input_data_db)
            self.connect_mongodb()
            self.input_data_db()
            self.validator_label.setText('')

        except FileNotFoundError:
            print('Our ui was missing')









     
    
    def input_data_db(self):
        """this will create database and collection on our mongo db"""
        if not self.inputs():
            return  # Stop if inputs are invalid


        self.mongo_link = 'mongodb://localhost:27017'
        self.client = MongoClient(self.mongo_link)



        try:
            self.database_name = self.client['bank_database']
            self.collection_name = self.database_name['bank_details']
            self.collection_name.insert_one({
                "year_creation": {'month': self.month, 'day': self.date, "year": self.year},
                'branch': self.branch,
                'main_bank': self.main_bank,
                'name': {'first_name': self.first_name, 'last_name': self.last_name},
                'location': {'address': self.address, 'city': self.city},
                'bank_account': {'n1#': self.bank_1, 'n2#': self.bank_2, 'n3#': self.bank_3, 'n4#': self.bank_4},
                'debit_type': self.bank_type,
                'email_address': self.email
            })
            
            print('input sucess')
            self.validator_label.setText('sucesss')
            QTimer.singleShot(10000, lambda: self.validator_label.setText(''))
            self.clear_input()
        except Exception as e:
            print('error')

    def connect_mongodb(self):
        """This will connect to our MongoDB"""
        self.mongo_link = 'mongodb://localhost:27017'
        self.client = MongoClient(self.mongo_link)
        self.my_database = self.client['bank_database']
        try:
            # Check if the connection is established
            self.client.admin.command('ismaster')
            dblist = self.client.list_database_names()
            if 'bank_database' in dblist:
                print(f'Database {self.my_database.name} exists.')
            else:
                print('Database does not exist.')
        except Exception as e:
            print(f'Connection failed: {e}')


    def inputs(self):
        """This is our input for our Bank"""
        self.month = self.month_input.currentText()
        self.date = self.date_input.text()
        self.year = self.year_input.currentText()
        self.branch = self.branch_input.currentText()
        self.main_bank = self.main_bank_input.currentText()
        self.first_name = self.first_name_input.text()
        self.last_name = self.last_name_input.text()
        self.address = self.address_input.text()
        self.city = self.city_input.currentText()

        #this will 4 input for our 16 digit number
        self.bank_1 = self.bank_1_input.text()
        self.bank_2 =self.bank_2_input.text()
        self.bank_3 =self.bank_3_input.text()
        self.bank_4 =self.bank_4_input.text()
        
        self.bank_type = self.bank_type_input.currentText()
        self.email = self.email_input.text()

        # Optionally limit the text length for certain QLineEdit inputs
        # Assuming you have these QLineEdit widgets in your .ui file

            
            # Set max length for QLineEdit inputs
        if self.date_input:
            self.date_input.setMaxLength(2)
        if self.bank_1_input:
            self.bank_1_input.setMaxLength(4)
        if self.bank_2_input:
            self.bank_2_input.setMaxLength(4)
        if self.bank_3_input:
            self.bank_3_input.setMaxLength(4)
        if self.bank_4_input:
            self.bank_4_input.setMaxLength(4)

                # Allow only letters and spaces
        self.reg_exp = QRegularExpression("[a-zA-Z ]*")
        self.validator = QRegularExpressionValidator(self.reg_exp)
        self.first_name_input.setValidator(self.validator)
        self.last_name_input.setValidator(self.validator)

        #only accept number
        self.bank_1_input.setValidator(QDoubleValidator(0.0, 9999.99, 2))
        self.bank_2_input.setValidator(QDoubleValidator(0.0, 9999.99, 2))
        self.bank_3_input.setValidator(QDoubleValidator(0.0, 9999.99, 2))
        self.bank_4_input.setValidator(QDoubleValidator(0.0, 9999.99, 2))





        if not all([self.date,self.first_name,self.last_name,self.address,self.bank_1,
                    self.bank_2,self.bank_3,self.bank_4,self.email]):
                    self.validator_label.setText('Please complete all input')
                    QTimer.singleShot(10000,lambda:self.validator_label.setText('Please complete all input'))
                    return False



    def clear_input(self):

        self.month_input.currentText()
        self.date_input.clear()
        self.year_input.currentText()
        self.branch_input.currentText()
        self.main_bank_input.currentText()
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.address_input.clear()
        self.city_input.currentText()

        #this will 4 input for our 16 digit number
        self.bank_1_input.clear()
        self.bank_2_input.clear()
        self.bank_3_input.clear()
        self.bank_4_input.clear()
        
        self.bank_type_input.currentText()
        self.email_input.clear()

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MyAPP()
    main_app.show()
    sys.exit(app.exec())