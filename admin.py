from PyQt5.QtWidgets import (QMainWindow,QAction,QApplication,QDesktopWidget,QComboBox,QTextEdit,QLineEdit,QPushButton,QMessageBox,QToolTip)
from PyQt5.QtGui import QFont
import sys
import pymysql


class UI_admin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)

        #选择表

        self.option_table = QComboBox(self)  #下拉选项
        self.option_table.move(50,50)
        cur_option_table = db.cursor()
        cur_option_table.execute('SHOW TABLES')
        table_name = cur_option_table.fetchall()
        for i in table_name:
            self.option_table.addItem("{}".format(i[0]))
        cur_option_table.close()

        #选表控件
        self.option_table.activated[str].connect(self.showtable)
        
        #三个提示标签
        QToolTip.setFont(QFont('SansSerif', 10))

        #增加按钮
        btn_add = QPushButton('添加',self)
        btn_add.move(50,625)
        btn_add.clicked.connect(self.ADD)
        btn_add.setToolTip('注意属性个数，类型')


        
        #删除按钮
        btn_del = QPushButton('删除',self)
        btn_del.move(50,675)
        btn_del.clicked.connect(self.DEL)
        btn_del.setToolTip('写入删除条件即可！')

        #修改按钮
        btn_upd = QPushButton('修改',self)
        btn_upd.move(50,725)
        btn_upd.clicked.connect(self.UPD)
        btn_upd.setToolTip('第一个框写where条件，第二个框写修改内容')

        #显示属性的文本框 
        self.showdesc = QTextEdit(self)
        self.showdesc.move(200,10)
        self.showdesc.resize(1000,45)     
        self.showdesc.setFont(QFont('SansSerif', 18))
        #文本框
        self.showtext = QTextEdit(self)
        self.showtext.move(200,50)
        self.showtext.resize(1000,550)
        self.showtext.setFont(QFont('SansSerif', 18))
        #增加，和删除的框
        self.another = QLineEdit('请严格按照格式填写！',self)
        self.another.move(200,620)
        self.another.resize(1000,45)
        self.another.setFont(QFont('SansSerif', 18))
        #修改
        self.update = QLineEdit('修改内容',self)
        self.update.move(200,700)
        self.update.resize(1000,45)
        self.update.setFont(QFont('SansSerif',18))


        #window
        self.resize(1200, 800)
        self.center()
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('管理员')
 #       self.show()

    def showtable(self,tab_name):
        #查询内容
        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)

        cur_showtext = db.cursor()      
        cur_showtext.execute('SELECT * FROM {}'.format(tab_name))
        desc = [tuple[0] for tuple in cur_showtext.description]     #属性

        text = cur_showtext.fetchall()
        
        self.showdesc.clear()       #清
        self.showdesc.setPlainText('      '.join(desc))   #属性

        self.showtext.clear()       
        #内容
        list_text=[]
        for i in text:      #一行
            for j in range(len(desc)):      #一个    
                list_text.append(str(i[j])+'      ')           #每行的每个
            list_text.append('\n')                      #显示一行后换行，一行的值之后加一个'\n'
        self.showtext.setPlainText(''.join(list_text))  #.join方法连接
        
        cur_showtext.close()
        db.close()




    def ADD(self):

        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)

        tab_name = self.option_table.currentText()  #获取当前的表名
        
        text = self.another.text()    #获取需要增加的文本
        
        cur = db.cursor()
        cur.execute('SELECT * FROM {}'.format(tab_name))
        data = cur.fetchall()
        cur.close()
        db.close()

        if text in data:
            QMessageBox().information(self, "提示", "已存在！", QMessageBox.Yes)
        elif text == '' or text == '请严格按照格式填写！':
            pass
        else:
            try:        
                db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
                cur_add = db.cursor()
                cur_add.execute('INSERT INTO {} VALUES({})'.format(tab_name,text))
                db.commit()
                cur_add.close()
                db.close()

                self.showtable(self.option_table.currentText())     #刷新文本框
                self.another.clear()
            except Exception as e:
                QMessageBox().information(self, "提示",str(e), QMessageBox.Yes)
                cur_add.close()
                db.close()
            finally:
                
                print(tab_name)
                print(text)

    def DEL(self):

    #    db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)

        tab_name = self.option_table.currentText()  #获取当前的表名
        
        text = self.another.text()    #获取需要删除的内容
    #    
    #    cur = db.cursor()
    #    cur.execute('SELECT * FROM {}'.format(tab_name))
    #    data = cur.fetchall()
    #    cur.close()
    #    db.close()

    #    if text in data:
    #        QMessageBox().information(self, "提示", "已存在！", QMessageBox.Yes)
        if text == '' or text == '请严格按照格式填写！':
            pass
        else:
            try:        
                db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
                cur_del = db.cursor()
                cur_del.execute('DELETE FROM {} WHERE {}'.format(tab_name,text))
                db.commit()
                cur_del.close()
                db.close()

                self.showtable(self.option_table.currentText())     #刷新文本框
                self.another.clear()
            except Exception as e:
                QMessageBox().information(self, "提示",str(e), QMessageBox.Yes)
                cur_add.close()
                db.close()
            finally:
                
                print(tab_name)
                print(text)
    def UPD(self):

    #    db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)

        tab_name = self.option_table.currentText()  #获取当前的表名
        
        text = self.another.text()    #获取需要修改的where条件
        update = self.update.text()   #获取修改内容
    #    
    #    cur = db.cursor()
    #    cur.execute('SELECT * FROM {}'.format(tab_name))
    #    data = cur.fetchall()
    #    cur.close()
    #    db.close()

    #    if text in data:
    #        QMessageBox().information(self, "提示", "已存在！", QMessageBox.Yes)
        if text == '' or text == '请严格按照格式填写！':
            pass
        else:
            try:        
                db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
                cur_upd = db.cursor()
                cur_upd.execute('UPDATE {} SET {} WHERE {}'.format(tab_name,update,text))
                db.commit()
                cur_upd.close()
                db.close()

                self.showtable(self.option_table.currentText())     #刷新文本框
                self.another.clear()
                self.update.clear()
            except Exception as e:
                QMessageBox().information(self, "提示",str(e), QMessageBox.Yes)
                cur_upd.close()
                db.close()
            finally:
                
                print(tab_name)
                print(text)



    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
#if __name__=='__main__':
#        app = QApplication(sys.argv)
#        ex = UI_admin()
#        sys.exit(app.exec_()) 
