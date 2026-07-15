import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    name = request.form['name']

    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM sales WHERE name = ?",
        (name,)
    )

    row = cursor.fetchone()

    if row:
        return f'名前：{row[1]}<br>売上：{row[2]}円<br><a href="/">戻る</a>'
    else:
        return '見つかりませんでした<br><a href="/">戻る</a>'

@app.route('/list')
def list_sales():
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()

    conn.close()

    return render_template('list.html', rows=rows)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        sale = request.form['sale']

        conn = sqlite3.connect('sales.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO sales (name, sale) VALUES (?, ?)",
            (name, sale)
        )

        conn.commit()
        conn.close()

        return '追加しました<br><a href="/list">一覧を見る</a>'

    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM sales WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return '<p>削除しました</p><a href="/list">一覧に戻る</a>'


@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM sales WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()

    conn.close()

    return render_template('edit.html', row=row)


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    sale = request.form['sale']

    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE sales SET name = ?, sale = ? WHERE id = ?",
        (name, sale, id)
    )

    conn.commit()
    conn.close()

    return '<p>更新しました</p><a href="/list">一覧に戻る</a>'

# app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)