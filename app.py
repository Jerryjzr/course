#from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL连接配置
db_config = {
    'host': 'your·ip',
    'user': 'course_schedule',
    'password': 'course_schedule',
    'database': 'course_schedule'
}

# 显示课程表
@app.get('/')
def show_schedule():
    # 连接MySQL数据库
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 查询所有课程
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    # 渲染网页模板并传递课程数据
    return render_template('schedule.html', courses=courses)


# 添加课程
@app.route('/add', methods=['POST'])
def add_course():
    # 获取表单数据
    name = request.form['name']
    day = request.form['day']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    location = request.form['location']

    # 连接MySQL数据库
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 插入新课程
    cursor.execute('INSERT INTO courses (name, day, start_time, end_time, location) VALUES (%s, %s, %s, %s, %s)',
                   (name, day, start_time, end_time, location))
    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    # 重定向到课程表页面
    return redirect('/')

# 删除课程
@app.route('/delete/<int:id>')
def delete_course(id):
    # 连接MySQL数据库
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 删除指定ID的课程
    cursor.execute('DELETE FROM courses WHERE id = %s', (id,))
    conn.commit()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    # 重定向到课程表页面
    return redirect('/')

if __name__ == '__main__':
    app.run()
