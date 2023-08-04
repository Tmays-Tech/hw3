#Treyvon Mays
#CIS3325
#7/27/23

#Flask
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

#------------
# google cloud
#------------
host='34.16.22.143'
db = 'hw3_db'
user = 'root'
pasw = '9BqpDxo374xog;Fn'


#Database configs
db_config = {
    'user': user,
    'password': pasw,
    'host': host,
    'database': db,
}


#Payment class
class Payment:
    def __init__(self, phone_number, payment_type, amount):
        self.phone_number = phone_number
        self.payment_type = payment_type
        self.amount = amount


    def save_to_database(self):
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        insert_query = "INSERT INTO payments (phone_number, payment_type, amount) VALUES (%s, %s, %s)"
        data = (self.phone_number, self.payment_type, self.amount)
        cursor.execute(insert_query, data)
        connection.commit()
        connection.close()

#Route/fourms
@app.route('/', methods=['GET', 'POST'])
def opening_page():
    if request.method == 'POST':
        first_name = "first"
        last_name = "last"
        phone_number = request.form['phone_number']
        payment_type = request.form['payment_type']
        amount = request.form['amount']

        payment = Payment(phone_number, payment_type, amount)
        payment.save_to_database()

        return redirect(url_for('second_page', phone_number=phone_number, payment_type=payment_type, amount=amount))

    return render_template('opening_page.html')

#Route second page
@app.route('/second-page/<phone_number>/<payment_type>/<amount>')
def second_page(phone_number, payment_type, amount):
    return render_template('second_page.html', phone_number=phone_number, payment_type=payment_type, amount=amount)

if __name__ == '__main__':
    app.run(debug=True)
