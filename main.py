from flask import Flask, render_template, redirect, url_for, request
import sqlite3
from random import choice, randint, shuffle

app = Flask(__name__)


def generate_id():
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    rn_numbers = [choice(numbers) for char in range(randint(4, 8))]
    password_list = rn_numbers
    shuffle(password_list)
    gen_id = "".join(password_list)
    return gen_id

# creating and adding the data in the database
# data
# name = "Sachin Rajput"
# acc_num = "8452 0943 1294"
# email = "sachin@outlook.com"

# database
# db = sqlite3.connect("customer_data.db")
# db.row_factory = sqlite3.Row
# cur = db.cursor()
# cur.execute("select * from customers")
# data = cur.fetchall()
# cur.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, customer_id varchar(250) NOT NULL UNIQUE, "
#             "name varchar(250) NOT NULL UNIQUE, "
#             "account INTEGER NOT NULL UNIQUE, email varchar(250) NOT NULL UNIQUE)")
# cur.execute(f"INSERT INTO customers VALUES('{len(data) + 1}', '{generate_id()}', '{name}', '{acc_num}', '{email}')")
# db.commit()


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html", place="home")


@app.route("/pay", methods=['GET', 'POST'])
def pay():
    if request.method == 'POST':
        if request.form.get('account') and request.form.get('name') and not request.form.get('amount') == '':
            print("send")
            print(request.form.get('account').split())
            # if len(request.form.get('account')) ==
            return render_template("pay.html", place="pay", send='yes')
        if request.form.get('account') and not request.form.get('name') and not request.form.get('amount') == '':
            print("name missing")
            print(request.form.get('amount'))
            acc = request.form.get('account')
            amm = request.form.get('amount')
            return render_template("pay.html", place="pay", send='name', account=acc, amount=amm)
        if not request.form.get('account') and request.form.get('name') and not request.form.get('amount') == '':
            print("name missing")
            print(request.form.get('amount'))
            name = request.form.get('name')
            amm = request.form.get('amount')
            return render_template("pay.html", place="pay", send='account', name=name, amount=amm)
        if request.form.get('account') and request.form.get('name') and request.form.get('amount') == '':
            print("amount not given!")
            print(request.form.get('amount'))
            name = request.form.get('name')
            acc = request.form.get('account')
            return render_template("pay.html", place="pay", send='amount', name=name, account=acc)
        if request.form.get('account') and not request.form.get('name') and request.form.get('amount') == '':
            print("amount not given!")
            print(request.form.get('amount'))
            acc = request.form.get('account')
            return render_template("pay.html", place="pay", send='no', account=acc)
        if not request.form.get('account') and request.form.get('name') and request.form.get('amount') == '':
            print("amount not given!")
            print(request.form.get('amount'))
            name = request.form.get('name')
            return render_template("pay.html", place="pay", send='no', name=name)
        if request.form.get('amount') == '':
            print("none")
            return render_template("pay.html", place="pay", send='no')
        if request.form.get('account') == '' and request.form.get('account') == '' and not request.form.get('amount') == '':
            print("none")
            return render_template("pay.html", place="pay", send='no')
    return render_template("pay.html", place="pay")


@app.route("/pay/<int:customer_id>", methods=['GET', 'POST'])
def payment(customer_id):
    print(customer_id)
    db = sqlite3.connect("customer_data.db")
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from customers where customer_id = (?)", [str(customer_id)])
    data = cur.fetchone()
    name = data['name']
    acc_no = data['account']
    email = data['email']
    print(name, acc_no, email)
    return render_template("pay.html", place="pay", account=acc_no, name=name)


@app.route("/customers", methods=['GET', 'POST'])
def customers():
    customers_list = []
    db = sqlite3.connect("customer_data.db")
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("select * from customers")
    data_list = cur.fetchall()
    for customer in data_list:
        entry = {
            'id': customer['customer_id'],
            'name': customer['name'],
            'acc_no': customer['account'],
            'email': customer['email'],
        }
        customers_list.append(entry)
    # print(customers_list)
    return render_template("customer.html", place="customer", c_list=customers_list)


if __name__ == "__main__":
    app.run(debug=True)
