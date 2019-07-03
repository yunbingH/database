# database
数据库课设
 



设计内容

选课系统主要满足三类用户的要求，这三类用户分别是教务处的系统管理员、教师和学生，他们所具有的操作权限以及操作内容是不同的。具体要求如下：

系统管理员:实现对学生、教师、课程、授课信息的增加、删除、查询、修改等。 

学生:只能查看和修改自己个人信息、已选课程成绩及总学分；修改自己密码；可以查看课程信息、授课及教师信息；可以进行选课操作。

教师:只能查看和修改自己个人信息；修改自己的密码；只能录入自己所授课程的学生成绩，一旦提交将不能修改，否则必须通过管理员授权才可修改学生成绩。能够输出所授课程的成绩单。

 



主要功能：

教师和学生登陆系统的帐号和密码，初始都分别为教师工号和学号，登陆后密码可以修改。其中教师的职位可以是管理员。管理员和非管理员的老师及学生对系统的操作具有不同的权限。管理员登陆系统，对学生选课情况进行管理，包括发布选课信息，对学生的选课情况进行查看。管理员还可以对授课老师的信息进行增加、删除、修改、查询。教师登陆系统，能查看自己的个人信息，及所授课的班级的所有学生的本门课程的成绩信息，并能进行增加和修改。学生登陆系统，能进行选课，查看管理员发布的选课信息，自己的选课情况，本人的基本信息，以及课程的成绩。



数据需求

学生的信息包括学号，姓名，性别，出生日期，专业，电话，EMAIL地址等。

教师的信息包括教师号，姓名，性别，职称，电话，EMAIL地址等。

课程信息包括课程号，课程名，学分等。




本系统共设计5个关系，详细信息如下所示：

账户（账号，密码，身份）

学生（学号，姓名，性别，生日，专业，电话，邮箱）

教师（工号，姓名，性别，职称，电话，邮箱）

课程（课程号，课程名，学分，任课教师）

选课（学号，教师号，课程号，成绩，课程名）


经过数据库系统分析和逻辑设计后，数据库的结果已经非常清晰，剩下的就是用数据库软件实现这样的结构。本章节主要是对表等一系列数据库内容的建立以及实施。本系统中的数据库采用MySql作为数据库。首先创建一个名为“STU”的数据库。

在数据库中创建ACCOUNT账户表：

CREATE TABLE ACCOUNT(

​    a_no char(20) NOT NULL PRIMARY KEY,

​    a_pw char(20) NOT NULL,

​    state char(20) NOT NULL

);

State属性用来区别身份，进一步区分权限。


 

创建STUDENT学生表：

CREATE TABLE STUDENT(

​    s_id char(20) NOT NULL PRINARY KEY,

​    s_name char(20) NOT NULL,

​    s_sex char(5) CHECK(s_sex IN (‘男’,‘女’)),

​    s_birthday data NOT NULL,

​    s_special char(20) NOT NULL,

​    s_tel char(20),

​    s_email char(20)

);



 

创建TEACHER老师表：

CREATE TABLE TEACHER(

​    t_id char(20) NOT NULL PRIMARY KEY,

​    t_name char(20) NOT NULL,

​    t_sex char(20)CHECK(t_sex IN(‘男’,’女’)),

​    t_title char(20) NOT NULL,

​    t_tel char(20)，

​    t_email char(20)

);


 

创建SC选课表：

CREATE TABLE SC(

​    s_id char(20) NOT NULL,

​    t_id char(20) NOT NULL,

​    c_id char(20) NOT NULL,

​    grade smallint CHECK(grade>=0 AND grade<=100),

​    course char(20),

​    PRIMARY KEY(s_id,t_id,c_id),

​    FOREIGN KEY(s_id) REFERENCES STUDENT(s_id),

​    FOREIGN KEY(t_id) REFERENCES TEACHER(t_id),

​    FOREIGN KEY(c_id) REFERENCES COURSE(c_id)

);



 

创建COURSE课程表：

CREATE TABLE COURSE(

​    c_id char(20) NOT NULL PRIMARY KEY,

​    c_name char(20) NOT NULL,

​    c_score char(20) NOT NULL,

​    c_teacher char(20) NOT NULL

);




 

 

 

 

 

 

 

 
