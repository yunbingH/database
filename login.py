from PyQt5.QtWidgets import (QWidget,QMainWindow,QDesktopWidget, QLabel, QPushButton, QApplication,QTextEdit,QLineEdit,QMessageBox,QInputDialog)
from PyQt5.QtGui import QFont
import sys
import pymysql
from admin import UI_admin
#from student import UI_student

yourid='001'

db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
class UI_login(QWidget):
    yourid=0
    def __init__(self):
        super().__init__()
        self.initUI()
 #       self.admin = UI_admin()
    def initUI(self):
        lab1 = QLabel('账号:',self)
        #lab1.resize(70,25)
        lab1.move(40,40)
        lab1.setFont(QFont('SansSerif', 20))

        lab2 = QLabel('密码:',self)
        #lab2.resize(70,25)
        lab2.move(40,100)
        lab2.setFont(QFont('SansSerif', 20))

        self.IDEdit = QLineEdit(self)
        self.IDEdit.move(120,40)
        self.IDEdit.resize(200,35) 

        self.PWDEdit = QLineEdit(self)
        self.PWDEdit.move(120,100)
        self.PWDEdit.resize(200,35) 
        self.PWDEdit.setEchoMode(QLineEdit.Password)
  
        btn = QPushButton('登录', self)
        btn.resize(80,40)
        btn.move(80, 200)
        btn.clicked.connect(self.login) 
        
        #btn = QPushButton('Button', self)
        #btn.resize(80,40)
        #btn.move(220, 200)       
       





       #window
        self.resize(400, 300)
        self.center()
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('登录')
        self.show()



    def login(self):
        global yourid
        ID = self.IDEdit.text()
        yourid = ID
        PWD = self.PWDEdit.text()
        cur = db.cursor()
        cur.execute("SELECT * FROM ACCOUNT ;")
        data = cur.fetchall()
        cur.close()
        db.close()


  #      print(str(ID),str(yourid))

        #判断
        flag = 0
        for i in data:
            if ID == i[0] and PWD == i[1] and i[2] == 'admin':

                self.admin = UI_admin()
                self.close()
                self.admin.show()
   #             cur.close()
   #             db.close()
                flag = 1
                break
            elif ID == i[0] and PWD == i[1] and i[2] == 'student':
                       
                self.student = UI_student()
  #              print('aa',ID,yourid)
                self.student.show()
                self.close()
    #            cur.close()
    #            db.close()
                flag = 1
                break
            elif ID == i[0] and PWD == i[1] and i[2] == 'teacher':
                self.teacher = UI_teacher()
                self.close()
                self.teacher.show()
     #           cur.close()
     #           db.close()
                flag = 1
                break
            #else:
        if flag==0:

            QMessageBox().information(self, "提示", "账号或密码错误！", QMessageBox.Yes)
       #     break

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

#    print('out',yourid)







class UI_student(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):

        ID = yourid
     #   ID = '001'
        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
        cur_info = db.cursor()
        cur_info.execute("SELECT * FROM STUDENT WHERE s_id='{}'".format(ID))
        data = cur_info.fetchall()
        cur_info.close()
  #      db.close()

        #欢迎
        lab_welcome = QLabel('Hi,{}'.format(data[0][1]),self)

        lab_welcome.move(10,10)
        lab_welcome.setFont(QFont('SansSerif', 20))

        #个人信息
        self.lab_self_info = QLabel(self)
 #       print('new',ID)
        self.lab_self_info.setText("学号：{0}\n性别：{2}\n出生日期：{3}\n专业：{4}\n电话：{5}\n邮箱：{6}\n".format(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5],data[0][6]))
        self.lab_self_info.move(10,50)
        self.lab_self_info.resize(300,300)
        self.lab_self_info.setFont(QFont('SansSerif',20))

        #选课
        lab_desc_course = QLabel(self)
        lab_desc_course.setText("课程号\t课程名\t\t学分\t任课教师")
        lab_desc_course.move(600,10)
        lab_desc_course.resize(550,40)
        lab_desc_course.setFont(QFont('SansSerif',20))

        self.showcourse = QTextEdit(self) 
        self.showcourse.move(600,50)
        self.showcourse.resize(560,550)
        self.showcourse.setFont(QFont('SansSerif', 18))

        cur_course = db.cursor()
        cur_course.execute("SELECT * FROM COURSE")
        course = cur_course.fetchall()
        cur_course.close()

        list_course=[]
        for i in course:      #一行
            for j in range(4):      #一个
                list_course.append(str(i[j])+'\t\t')           #每行的每个
            list_course.append('\n')                      #显示一行后换行，一行的值之后加一个'\n'
        self.showcourse.setPlainText(''.join(list_course))  #.join方法连接
        
        ##选课文本框
        self.c_id = QLineEdit('请输入课程号进行选课',self)
        self.c_id.move(600,620)
        self.c_id.resize(200,40)
        ##选课按钮
        self.btn_choice = QPushButton('选课',self)
        self.btn_choice.move(820,620)
        self.btn_choice.resize(80,40)
        self.btn_choice.clicked.connect(self.choice)
        

        #总学分
        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
        cur_score = db.cursor()
        cur_score.execute("SELECT c_score FROM COURSE,SC WHERE COURSE.c_id=SC.c_id AND SC.grade IS NOT NULL AND s_id={}".format(ID))
        score = [int[0] for int in cur_score.fetchall()]
        cur_score.close()
        db.close()

        sum_score = sum(score)   #求和

        lab_score = QLabel(self)
        lab_score.setText('总学分：{}'.format(str(sum_score)))
        lab_score.move(10,320)
        lab_score.resize(160,40)
        lab_score.setFont(QFont('SansSerif',20))

        #成绩
        self.showgrade = QTextEdit(self)
        self.showgrade.move(10,360)
        self.showgrade.resize(500,400)
        self.showgrade.setFont(QFont('SansSerif',20))

        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
        cur_grade = db.cursor()
        cur_grade.execute("SELECT course,grade FROM SC WHERE s_id='{}'".format(ID))
        grade = cur_grade.fetchall()
        cur_grade.close()
        db.close()

        list_grade=[]
        for i in grade:      #一行
            for j in range(2):      #一个
                list_grade.append(str(i[j])+'      ')           #每行的每个
            list_grade.append('\n')                      #显示一行后换行，一行的值之后加一个'\n'
        self.showgrade.setPlainText(''.join(list_grade))  #.join方法连接


        #修改按钮
        btn_update = QPushButton('修改',self) 
        btn_update.move(300,230)
        btn_update.clicked.connect(self.updateDialog_tel)
        btn_update = QPushButton('修改',self) 
        btn_update.move(300,270)
        btn_update.clicked.connect(self.updateDialog_email)
           
                    
            
            
            
            
  #      db.close()
            
            
            
        #window
        self.resize(1200, 800)
        self.center()
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('学生')
#        self.show()

    def choice(self):
        #ID = '001'
        ID = yourid

        choice_id = self.c_id.text()

        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
        cur_choice = db.cursor()
        cur_choice.execute("INSERT INTO SC(s_id,t_id,c_id,course) SELECT s_id,t_id,c_id,c_name FROM TEACHER,COURSE,STUDENT WHERE s_id={} AND c_teacher=t_name AND c_id='{}'".format(ID,choice_id))
        db.commit()
        cur_choice.close()

        cur_newgrade = db.cursor()
        cur_newgrade.execute("SELECT course,grade FROM SC WHERE s_id='{}'".format(ID))
        newgrade = cur_newgrade.fetchall()

        list_grade=[]
        for i in newgrade:      #一行
            for j in range(2):      #一个
                list_grade.append(str(i[j])+'      ')           #每行的每个
            list_grade.append('\n')                      #显示一行后换行，一行的值之后加一个'\n'
        self.showgrade.setPlainText(''.join(list_grade))  #.join方法连接

        db.close()


    def updateDialog_tel(self):

        ID = yourid
        #ID = '001'
  #      db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
  #      cur_info = db.cursor()
  #      cur_info.execute("SELECT * FROM STUDENT WHERE s_id='{}'".format(ID))
  #      data = cur_info.fetchall()
  #      cur_info.close()
  #      db.close()

        newtel, ok = QInputDialog.getText(self, 'Update Dialog','请输入新的电话')
        if ok:
            #更新数据库
            db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
            cur_update = db.cursor()
            cur_update.execute("UPDATE STUDENT SET s_tel='{}' WHERE s_id='{}'".format(newtel,ID))
            db.commit()
            cur_update.close()
            db.close()

            #获取更新后的内容
            db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
            cur_info2 = db.cursor()
            cur_info2.execute("SELECT * FROM STUDENT WHERE s_id='{}'".format(ID))
            data2 = cur_info2.fetchall()
            cur_info2.close()
            db.close()

            #重置label
            self.lab_self_info.setText("学号：{0}\n性别：{2}\n出生日期：{3}\n专业：{4}\n电话：{5}\n邮箱：{6}\n".format(data2[0][0],data2[0][1],data2[0][2],data2[0][3],data2[0][4],data2[0][5],data2[0][6]))
           
#            print(data[0][5])
#            print(newtel)
    def updateDialog_email(self):

        ID = yourid
        #ID = '001'
#        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
#        cur_info = db.cursor()
#        cur_info.execute("SELECT * FROM STUDENT WHERE s_id='{}'".format(ID))
#        data = cur_info.fetchall()
#        cur_info.close()
#        db.close()
#        
        newemail, ok = QInputDialog.getText(self, 'Update Dialog','请输入新的邮箱')
        if ok:
                
            db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
            cur_update = db.cursor()
            cur_update.execute("UPDATE STUDENT SET s_email='{}' WHERE s_id='{}'".format(newemail,ID))
            db.commit()
            cur_update.close()
            db.close()

            db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
            cur_info2 = db.cursor()
            cur_info2.execute("SELECT * FROM STUDENT WHERE s_id='{}'".format(ID))
            data2 = cur_info2.fetchall()
            cur_info2.close()
            db.close()


            self.lab_self_info.setText("学号：{0}\n性别：{2}\n出生日期：{3}\n专业：{4}\n电话：{5}\n邮箱：{6}\n".format(data2[0][0],data2[0][1],data2[0][2],data2[0][3],data2[0][4],data2[0][5],data2[0][6]))
    


    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class UI_teacher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):

        ID = yourid
        #ID = 'T001'
        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
        cur_info = db.cursor()
        cur_info.execute("SELECT * FROM TEACHER WHERE t_id='{}'".format(ID))
        data = cur_info.fetchall()
        cur_info.close()
    #    db.close()

        #欢迎
        lab_welcome = QLabel('Hi,{}'.format(data[0][1]),self)

        lab_welcome.move(10,10)
        lab_welcome.setFont(QFont('SansSerif', 20))

        #个人信息
        self.lab_self_info = QLabel(self)
        self.lab_self_info.setText("工号：{0}\n性别：{2}\n职称：{3}\n电话：{4}\n邮箱：{5}\n".format(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5]))
        self.lab_self_info.move(10,50)
        self.lab_self_info.resize(300,300)
        self.lab_self_info.setFont(QFont('SansSerif',20))

        #成绩单
        lab_desc_gradelist = QLabel(self)
        lab_desc_gradelist.setText("学号\t姓名\t\t课程名\t成绩")
        lab_desc_gradelist.move(600,10)
        lab_desc_gradelist.resize(550,40)
        lab_desc_gradelist.setFont(QFont('SansSerif',20))

        self.gradelist= QTextEdit(self) 
        self.gradelist.move(600,50)
        self.gradelist.resize(560,550)
        self.gradelist.setFont(QFont('SansSerif', 18))

        cur_grade = db.cursor()
        cur_grade.execute("SELECT DISTINCT SC.s_id,STUDENT.s_name,COURSE.c_name,SC.grade FROM SC,STUDENT,TEACHER,COURSE WHERE SC.s_id=STUDENT.s_id AND SC.c_id=COURSE.c_id AND grade IS NULL AND SC.t_id='{}'".format(ID))
        grade = cur_grade.fetchall()
        cur_grade.close()

        list_grade=[]
        for i in grade:      #一行
            for j in range(4):      #一个
                list_grade.append(str(i[j])+'\t\t')           #每行的每个
            list_grade.append('\n')                      #显示一行后换行，一行的值之后加一个'\n'
        self.gradelist.setPlainText(''.join(list_grade))  #.join方法连接
        
        ##录入成绩
        self.c_id = QLineEdit('请输入学生学号',self)
        self.c_id.move(600,620)
        self.c_id.resize(200,40)
        self.grade = QLineEdit('请输入成绩',self)
        self.grade.move(810,620)
        self.grade.resize(200,40)
        ##录入按钮
        self.btn_entering  = QPushButton('录入成绩',self)
        self.btn_entering.move(1030,620)
        self.btn_entering.resize(80,40)
        self.btn_entering.clicked.connect(self.entering)
        ##查看成绩按钮
        self.btn_scangrade = QPushButton('已录入的成绩',self)
        self.btn_scangrade.move(600,700)
        self.btn_scangrade.resize(200,40)
        self.btn_scangrade.clicked.connect(self.scan_grade)
        self.btn_scangrade2 = QPushButton('未录入的成绩',self)
        self.btn_scangrade2.move(900,700)
        self.btn_scangrade2.resize(200,40)
        self.btn_scangrade2.clicked.connect(self.scan_grade2)




        #修改按钮
        btn_update = QPushButton('修改',self) 
        btn_update.move(300,205)
        btn_update.clicked.connect(self.updateDialog_tel)
        btn_update = QPushButton('修改',self) 
        btn_update.move(300,245)
        btn_update.clicked.connect(self.updateDialog_email)
           
                    
            
            
            
            
  #      db.close()
            
            
            
        #window
        self.resize(1200, 800)
        self.center()
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('学生')
  #      self.show()

    def scan_grade(self):
        ID = yourid
        #ID = 'T001'        

        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
        cur_newgrade = db.cursor()
        cur_newgrade.execute("SELECT DISTINCT SC.s_id,STUDENT.s_name,COURSE.c_name,SC.grade FROM SC,STUDENT,TEACHER,COURSE WHERE SC.s_id=STUDENT    .s_id AND SC.c_id=COURSE.c_id AND grade IS NOT NULL AND SC.t_id='{}'".format(ID))
        newgrade = cur_newgrade.fetchall()

        list_grade=[]
        for i in newgrade:      #一行
            for j in range(4):      #一个
                list_grade.append(str(i[j])+'\t\t')           #每行的每个
            list_grade.append('\n')                      #显示一行后换行，一行的值之后加一个'\n'
        self.gradelist.setPlainText(''.join(list_grade))  #.join方法连接

        db.close()


    def scan_grade2(self):
        ID = yourid
        #ID = 'T001'        

        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
        cur_newgrade = db.cursor()
        cur_newgrade.execute("SELECT DISTINCT SC.s_id,STUDENT.s_name,COURSE.c_name,SC.grade FROM SC,STUDENT,TEACHER,COURSE WHERE SC.s_id=STUDENT    .s_id AND SC.c_id=COURSE.c_id AND grade IS NULL AND SC.t_id='{}'".format(ID))
        newgrade = cur_newgrade.fetchall()

        list_grade=[]
        for i in newgrade:      #一行
            for j in range(4):      #一个
                list_grade.append(str(i[j])+'\t\t')           #每行的每个
            list_grade.append('\n')                      #显示一行后换行，一行的值之后加一个'\n'
        self.gradelist.setPlainText(''.join(list_grade))  #.join方法连接

        db.close()




    def entering(self):
        #ID = 'T001'
        ID = yourid

        student_id = self.c_id.text()
        student_grade = self.grade.text()
    
        db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
        try:
            cur_grade = db.cursor()
            cur_grade.execute("UPDATE SC SET grade={} WHERE s_id='{}'".format(student_grade,student_id))
            db.commit()
            cur_grade.close()

            cur_newgrade = db.cursor()
            cur_newgrade.execute("SELECT DISTINCT SC.s_id,STUDENT.s_name,COURSE.c_name,SC.grade FROM SC,STUDENT,TEACHER,COURSE WHERE SC.s_id=STUDENT.s_id AND SC.c_id=COURSE.c_id AND grade IS NULL AND SC.t_id='{}'".format(ID))
            newgrade = cur_newgrade.fetchall()

            list_grade=[]
            for i in newgrade:      #一行
                for j in range(2):      #一个
                    list_grade.append(str(i[j])+'\t\t')           #每行的每个
                list_grade.append('\n')                      #显示一行后换行，一行的值之后加一个'\n'
            self.gradelist.setPlainText(''.join(list_grade))  #.join方法连接
        except Exception as e:
            QMessageBox().information(self, "提示",str(e), QMessageBox.Yes)
        
        
        finally:
            db.close()


    def updateDialog_tel(self):

        ID = yourid
        #ID = '001'

        newtel, ok = QInputDialog.getText(self, 'Update Dialog','请输入新的电话')
        if ok:
            #更新数据库
            db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
            cur_update = db.cursor()
            cur_update.execute("UPDATE STUDENT SET s_tel='{}' WHERE s_id='{}'".format(newtel,ID))
            db.commit()
            cur_update.close()
            db.close()

            #获取更新后的内容
            db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
            cur_info2 = db.cursor()
            cur_info2.execute("SELECT * FROM STUDENT WHERE s_id='{}'".format(ID))
            data2 = cur_info2.fetchall()
            cur_info2.close()
            db.close()

            #重置label
            self.lab_self_info.setText("工号：{0}\n性别：{2}\n职称：{3}\n电话：{4}\n邮箱：{5}\n".format(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5]))
           
    def updateDialog_email(self):

        ID = yourid
        #ID = '001'
        
        newemail, ok = QInputDialog.getText(self, 'Update Dialog','请输入新的邮箱')
        if ok:
                
            db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
            cur_update = db.cursor()
            cur_update.execute("UPDATE STUDENT SET s_email='{}' WHERE s_id='{}'".format(newemail,ID))
            db.commit()
            cur_update.close()
            db.close()
      #      self.lab_self_info.hide()

            db = pymysql.connect( host='localhost', user='root', passwd='ie6lan7', db='STU', port=3306)
            cur_info2 = db.cursor()
            cur_info2.execute("SELECT * FROM STUDENT WHERE s_id='{}'".format(ID))
            data2 = cur_info2.fetchall()
            cur_info2.close()
            db.close()


            self.lab_self_info.setText("工号：{0}\n性别：{2}\n职称：{3}\n电话：{4}\n邮箱：{5}\n".format(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5]))
    




    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())





if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = UI_login()
    sys.exit(app.exec_())
