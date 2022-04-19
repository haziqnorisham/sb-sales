from datetime import date

from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect
import database_handler

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/customer')
def customer():    
    all_customer = database_handler.get_all_customer()        
    return render_template('customer.html', all_customer = all_customer)

@app.route('/customer/add_customer', methods=['POST'])
def add_customer():    
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_phone = request.form['customer_phone']
        try:
            database_handler.add_customer(customer_name, customer_phone)
            flash('Added New '+ customer_name +'!', 'success')
        except Exception as e:
            flash(str(e)+ " " +str(e.with_traceback), 'warning')
    
    
    return redirect("/customer")

@app.route('/customer/edit_customer', methods=['POST'])
def edit_customer():    
    if request.method == 'POST':
        
        customer_id = request.form['modal_customer_id']
        customer_name = request.form['modal_customer_name']
        customer_phone = request.form['modal_customer_phone']

        if (request.form['modal_submit'] == "delete"):
            try:
                database_handler.delete_customer(customer_id)
                flash('Deleted user ' + customer_name, 'success')
            except Exception as e:
                flash(str(e)+ " " +str(e.with_traceback), 'warning')
        elif (request.form['modal_submit'] == "save"):
            try:
                database_handler.edit_customer(customer_id, customer_name, customer_phone)
                flash('Edited User ' + customer_name + "!", 'success')
            except Exception as e:
                flash(str(e)+ " " +str(e.with_traceback), 'warning')
    
    return redirect("/customer")

@app.route('/stock')
def stock():    
    all_stock = database_handler.get_all_stock()        
    return render_template('stock.html', all_stock = all_stock)

@app.route('/stock/add_stock', methods=['POST'])
def add_stock():
    if request.method == 'POST':
        stock_name = request.form['StockName']
        stock_price = request.form['StockPrice']
        stock_amount = request.form['StockAmount']
        try:
            database_handler.add_stock(stock_name, stock_price, stock_amount)
            flash('Added New Stock ' + stock_name + "!", 'success')
        except Exception as e:
            flash(str(e) + " " + str(e.with_traceback), 'warning')

    return redirect('/stock')

@app.route('/stock/edit_stock', methods=['POST'])
def edit_stock(): 
    
    if request.method == 'POST':        
        
        stock_id = request.form['modal_StockID']
        stock_name = request.form['modal_StockName']
        stock_price = request.form['modal_StockPrice']
        stock_amount = request.form['modal_StockAmount']
        
        if (request.form['modal_submit'] == "delete"):
            try:
                database_handler.delete_stock(stock_id)
                flash('Deleted stock ' + stock_name, 'success')
            except Exception as e:
                flash(str(e)+ " " +str(e.with_traceback), 'warning')
        elif (request.form['modal_submit'] == "save"):
            try:
                database_handler.edit_stock(stock_id, stock_name, stock_price, stock_amount)
                flash('Edited Stock ' + stock_name + "!", 'success')
            except Exception as e:
                flash(str(e)+ " " +str(e.with_traceback), 'warning')
        
    return redirect("/stock")

@app.route('/new_order')
def new_order():
    all_customer = database_handler.get_all_customer() 
    all_stocks = database_handler.get_all_stock()
    return render_template('new_order.html', all_customer=all_customer, all_stocks=all_stocks)

@app.route('/new_order/add_order', methods=['POST'])
def add_order():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        order_date = request.form['order_date']
        delivery_address = request.form['order_delivery_location']
        total_price = request.form['total_order_price']
        stock_id = request.form.getlist('stock_id')
        delivery_charge = request.form['delivery_charge']
        amount = request.form.getlist('amount')        

        try:
            database_handler.add_order(customer_id, order_date, total_price, delivery_address, stock_id, amount, delivery_charge)   
            flash('Created order for ' + order_date, 'success')
        except Exception as e:
            flash(str(e)+ " " +str(e.with_traceback), 'warning')  

    return redirect('/new_order')

@app.route('/summary')
def summary():

    try:
        from_date = request.args['from_date']
        to_date = request.args['to_date']
    except Exception as e:
        today = date.today()
        from_date = today
        to_date = today    

    
    order_list = database_handler.get_order_range(from_date, to_date)

    stock_list_range = database_handler.get_stock_list_range(from_date, to_date)
    ordered_item_range = database_handler.get_ordered_items_range(from_date, to_date)

    total_price_cash = database_handler.get_total_cash_range(from_date, to_date)
    if total_price_cash == None:
        total_price_cash = 0
    total_price_transfer = database_handler.get_total_transfer_range(from_date, to_date)
    if total_price_transfer == None:
        total_price_transfer = 0
    total_price_overall = total_price_cash + total_price_transfer  

    total_delivery = database_handler.get_total_delivery_range(from_date, to_date)  

    return render_template('summary.html', ordered_item_range = ordered_item_range, total_delivery = total_delivery, stock_list_range=stock_list_range, from_date=from_date, to_date=to_date, order_list=order_list, total_price_cash=total_price_cash, total_price_transfer=total_price_transfer, total_price_overall=total_price_overall)

@app.route('/hidden_summary')
def hidden_summary():
    try:
        from_date = request.args['from_date']
        to_date = request.args['to_date']
    except Exception as e:
        today = date.today()
        from_date = today
        to_date = today    

    
    order_list = database_handler.get_order_range(from_date, to_date)

    stock_list_range = database_handler.get_stock_list_range(from_date, to_date)
    ordered_item_range = database_handler.get_ordered_items_range(from_date, to_date)

    total_price_cash = database_handler.get_total_cash_range(from_date, to_date)
    if total_price_cash == None:
        total_price_cash = 0
    total_price_transfer = database_handler.get_total_transfer_range(from_date, to_date)
    if total_price_transfer == None:
        total_price_transfer = 0
    total_price_overall = total_price_cash + total_price_transfer  

    total_delivery = database_handler.get_total_delivery_range(from_date, to_date)  

    return render_template('hidden_summary.html', ordered_item_range = ordered_item_range, total_delivery = total_delivery, stock_list_range=stock_list_range, from_date=from_date, to_date=to_date, order_list=order_list, total_price_cash=total_price_cash, total_price_transfer=total_price_transfer, total_price_overall=total_price_overall)

@app.route("/order_details")
def order_details():
    if request.method == 'GET':
        order_id = request.args.get("order_id")
        order_details, ordered_item = database_handler.get_order_details(order_id)
        all_stocks = database_handler.get_all_stock()
    return render_template('order_details.html', all_stocks=all_stocks, order_details=order_details, ordered_item=ordered_item)

@app.route("/hidden_order_details")
def hidden_order_details():
    if request.method == 'GET':
        order_id = request.args.get("order_id")
        order_details, ordered_item = database_handler.get_order_details(order_id)
        all_stocks = database_handler.get_all_stock()
    return render_template('hidden_order_details.html', all_stocks=all_stocks, order_details=order_details, ordered_item=ordered_item)

@app.route('/hidden_order_details/update_order_status', methods=['POST'])
def hidden_update_order_status():
    if request.method == 'POST':
        status = request.form['order_status']
        payment_type = request.form['payment_type']
        order_id = request.form['order_id']        

        if status == '1':
            database_handler.update_order_status(order_id, status, payment_type)
        else:
            database_handler.update_order_status(order_id, status, payment_type)

    return redirect('/hidden_summary')

@app.route('/order_details/update_order_status', methods=['POST'])
def update_order_status():
    if request.method == 'POST':
        status = request.form['order_status']
        payment_type = request.form['payment_type']
        order_id = request.form['order_id']        

        if status == '1':
            database_handler.update_order_status(order_id, status, payment_type)
        else:
            database_handler.update_order_status(order_id, status, payment_type)

    return redirect('/summary')

@app.route('/order_details/update_order_details', methods=['POST'])
def update_order_details():
    if request.method == 'POST':
        button = request.form['button']
        if button == "update":
            order_id = request.form['order_id']
            order_date = request.form['order_date']
            delivery_address = request.form['order_delivery_location']
            total_price = request.form['total_order_price']
            stock_id = request.form.getlist('stock_id')
            delivery_charge = request.form['delivery_charge']
            amount = request.form.getlist('amount')        
            try:
                database_handler.update_order_details(order_id, order_date, total_price, delivery_address, stock_id, amount, delivery_charge)   
                flash('Updated order for ' + order_date , 'success')
            except Exception as e:
                flash(str(e)+ " " +str(e.with_traceback), 'warning')
            
            return redirect('/order_details?order_id='+ order_id)
        else:
            order_id = request.form['order_id']
            try:
                database_handler.delete_order(order_id)
                flash('Deleted order ' + str(order_id) , 'success')
            except Exception as e:
                flash(str(e)+ " " +str(e.with_traceback), 'warning')

            return redirect('/summary')

if __name__=='__main__':    
    app.run(host='0.0.0.0',port='8080', debug=True)
