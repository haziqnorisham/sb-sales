import os
import sqlite3

import config_handler

print(os.getcwd())
conn = sqlite3.connect(os.getcwd()+config_handler.get_sqlite_path(), check_same_thread=False)
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON", ())   

def get_all_customer():
    
    customer_list = []
    
    for row in c.execute('SELECT Customer.CustomerID , Customer.Name, Customer.Phone FROM Customer'):
        customer_list.append( {'id': row[0], 'name': row[1], 'phone': row[2]} )
    
    return customer_list

def add_customer(customer_name, customer_phone):
    
    stmt = 'INSERT INTO Customer (Name, Phone) VALUES(?, ?)'
    c.execute(stmt, (customer_name, customer_phone))

    conn.commit()
    return None

def edit_customer(customer_id, customer_name, customer_phone):
    stmt = 'UPDATE Customer SET Name = ? , Phone = ? WHERE CustomerID = ?'
    c.execute(stmt, (customer_name, customer_phone, customer_id))
    conn.commit()
    return None

def delete_customer(customer_id):
    stmt = 'DELETE FROM Customer where CustomerID = ?'
    c.execute(stmt, (customer_id,))
    conn.commit()
    return None

def get_all_stock():
    
    stock_list = []
    
    for row in c.execute('SELECT Stock.StockID , Stock.StockName, Stock.StockPrice, Stock.StockAmount FROM Stock WHERE StockName NOT LIKE \'<DELETED>%\''):
        stock_list.append( {'StockID': row[0], 'StockName': row[1], 'StockPrice': row[2], 'StockAmount': row[3]} )
    
    return stock_list

def add_stock(stock_name, stock_price, stock_amount):
    stmt = 'INSERT INTO Stock (StockName, StockPrice, StockAmount) VALUES (?, ?, ?)'
    c.execute(stmt, (stock_name, stock_price, stock_amount))

    conn.commit()
    return None

def edit_stock(stock_id, stock_name, stock_price, stock_amount):
    stmt = 'UPDATE Stock SET StockName=?, StockPrice=?, StockAmount=? WHERE StockID=?'
    c.execute(stmt, (stock_name, stock_price, stock_amount, stock_id))
    conn.commit()
    return None

def delete_stock(stock_id):
    stmt = 'UPDATE Stock SET StockName = \'<DELETED> \' || StockName WHERE StockID = ?'
    c.execute(stmt, (stock_id,))

    conn.commit()
    return None

def add_order(customer_id, order_date, total_amount, shipment_address, stock_id, amount, delivery_charge):
    
    stmt='INSERT INTO OrderTable (CustomerID, OrderDate, TotalAmount, ShipmentAddress, OrderStatusID, DeliveryCharge) VALUES (?, datetime(?), ?, ?, ?, ?)'
    c.execute(stmt, (customer_id, order_date, total_amount, shipment_address, 0, delivery_charge))
    conn.commit()

    stmt='SELECT max(OrderID) FROM OrderTable'
    rows = c.execute(stmt,())

    order_id = rows.fetchall()[0][0]
    
    i=0
    for id in stock_id:
        stmt='INSERT INTO OrderLine (OrderID, StockID, Amount) VALUES (?, ?, ?)'
        c.execute(stmt, (order_id, id, amount[i]))
        conn.commit()
        i+=1

    return None

def update_order_details(order_id, order_date, total_amount, shipment_address, stock_id, amount, delivery_charge):
    stmt = 'DELETE FROM OrderLine WHERE OrderLine.OrderID = ?'
    param = (order_id,)
    c.execute(stmt, param)
    conn.commit()

    stmt = 'UPDATE OrderTable SET OrderDate = datetime(?), TotalAmount = ?, ShipmentAddress = ?, DeliveryCharge = ? WHERE OrderID = ?'
    param = (order_date, total_amount, shipment_address, delivery_charge, order_id)
    c.execute(stmt, param)
    conn.commit()

    i=0
    for id in stock_id:
        stmt='INSERT INTO OrderLine (OrderID, StockID, Amount) VALUES (?, ?, ?)'
        c.execute(stmt, (order_id, id, amount[i]))
        conn.commit()
        i+=1
    
    return None

def get_order_range(from_date, to_date):

    order_list = []

    stmt = '''
            SELECT 
            OrderTable.OrderID, 
            OrderTable.CustomerID, 
            Customer.Name, 
            Customer.Phone,
            datetime(OrderTable.OrderDate), 
            OrderTable.TotalAmount, 
            OrderTable.ShipmentAddress, 
            OrderTable.OrderStatusID, 
            OrderTable.PaymentType
            FROM
                OrderTable
            LEFT JOIN
                Customer
            ON
                OrderTable.CustomerID = Customer.CustomerID
            WHERE
                date(OrderTable.OrderDate) BETWEEN date(?) AND date(?)
            ORDER BY
	            datetime(OrderTable.OrderDate)
            ASC'''    

    rows = c.execute(stmt, (from_date, to_date)).fetchall()

    for row in rows:

        ordered_items = get_ordered_item(row[0])
        order_string = ''

        for item in ordered_items:
            order_string = order_string + str(item['stock_amount']) + " " + item['stock_name'] + " + "

        order_list.append( {'order_id': row[0], 'customer_id': row[1], 'customer_name': row[2], 'customer_phone': row[3], 'order_datetime': row[4], 'total_amount': row[5], 'delivery_address': row[6], 'order_status': row[7], 'payment_type': row[8], 'ordered_items' : order_string} )

    return order_list

def get_ordered_item(order_id):
    
    ordered_items = []
    
    stmt= '''
        SELECT
            Stock.StockName,
            Stock.StockPrice,
            OrderLine.Amount,
            Stock.StockID
        FROM
            OrderLine
        LEFT JOIN
            Stock
        ON
            OrderLine.StockID = Stock.StockID
        WHERE
            OrderLine.OrderID = ?'''
    
    for row in c.execute(stmt, (order_id,)):
        ordered_items.append( {'stock_name': row[0], 'stock_price': row[1], 'stock_amount': row[2], 'stock_id': row[3]} )
    
    return ordered_items

def get_order_details(order_id):
    
    ordered_items = []

    stmt = '''
            SELECT 
            OrderTable.OrderID, 
            OrderTable.CustomerID, 
            Customer.Name, 
            Customer.Phone,
            datetime(OrderTable.OrderDate), 
            OrderTable.TotalAmount, 
            OrderTable.ShipmentAddress, 
            OrderTable.OrderStatusID, 
            OrderTable.PaymentType,
            OrderTable.DeliveryCharge
            FROM
                OrderTable
            LEFT JOIN
                Customer
            ON
                OrderTable.CustomerID = Customer.CustomerID
            WHERE
                OrderTable.OrderID = ?''' 
    
    rows = c.execute(stmt, (order_id,))
    row = rows.fetchall()[0]    
    
    order_details = {'order_id': row[0], 'customer_id': row[1], 'customer_name': row[2], 'customer_phone': row[3], 'order_datetime': row[4], 'total_amount': row[5], 'delivery_address': row[6], 'order_status': row[7], 'payment_type': [8], 'delivery_charge': row[9]}

    stmt= '''
        SELECT
            Stock.StockName,
            Stock.StockPrice,
            OrderLine.Amount,
            Stock.StockID
        FROM
            OrderLine
        LEFT JOIN
            Stock
        ON
            OrderLine.StockID = Stock.StockID
        WHERE
            OrderLine.OrderID = ?'''
    
    for row in c.execute(stmt, (order_id,)):
        ordered_items.append( {'stock_name': row[0], 'stock_price': row[1], 'stock_amount': row[2], 'stock_id': row[3]} )

    return(order_details, ordered_items)

def update_order_status(order_id, order_status, payment_type):

    stmt = 'UPDATE OrderTable SET OrderStatusID = ?, PaymentType = ? WHERE OrderID = ?'

    c.execute(stmt, (order_status, payment_type, order_id))
    conn.commit()

    return None

def get_total_cash_range(from_date, to_date):

    stmt = "SELECT sum(TotalAmount) FROM OrderTable WHERE OrderStatusID = 1 AND PaymentType = 0 AND date(OrderDate) BETWEEN date(?) AND date(?)"
    total_price = c.execute(stmt, (from_date, to_date))
    total_price = total_price.fetchall()
    total_price = total_price[0][0]

    return total_price

def get_total_transfer_range(from_date, to_date):

    stmt = "SELECT sum(TotalAmount) FROM OrderTable WHERE OrderStatusID = 1 AND PaymentType = 1 AND date(OrderDate) BETWEEN date(?) AND date(?)"
    total_price = c.execute(stmt, (from_date, to_date))
    total_price = total_price.fetchall()
    total_price = total_price[0][0]

    return total_price

def get_stock_list_range(from_date, to_date):

    stock_list_range = []

    stmt = 'SELECT DISTINCT OrderLine.StockID FROM OrderLine WHERE OrderLine.OrderID IN (SELECT OrderID FROM OrderTable WHERE OrderStatusID = 1 AND date(OrderDate) BETWEEN date(?) AND date(?)) '
    rows = c.execute(stmt, (from_date, to_date)).fetchall()
    
    for row in rows:
        print(row[0])
        stmt2 = 'SELECT Stock.StockName, stock.StockPrice, total(OrderLine.Amount), (stock.StockPrice * total(OrderLine.Amount)) FROM OrderLine LEFT JOIN Stock ON OrderLine.StockID = Stock.StockID  WHERE OrderLine.StockID = ? AND OrderLine.OrderID IN (SELECT OrderID FROM OrderTable WHERE OrderStatusID = 1 AND date(OrderDate) BETWEEN date(?) AND date(?)) '
        for row_in in c.execute(stmt2, (row[0], from_date, to_date)):
            stock_list_range.append({'stock_name' : row_in[0], 'stock_price' : row_in[1], 'stock_total_amount': int(row_in[2]), 'stock_total_price': row_in[3]})

    return stock_list_range

def get_ordered_items_range(from_date, to_date):

    stock_list_range = []

    stmt = 'SELECT DISTINCT OrderLine.StockID FROM OrderLine WHERE OrderLine.OrderID IN (SELECT OrderID FROM OrderTable WHERE date(OrderDate) BETWEEN date(?) AND date(?)) '
    rows = c.execute(stmt, (from_date, to_date)).fetchall()
    
    for row in rows:
        print(row[0])
        stmt2 = 'SELECT Stock.StockName, stock.StockPrice, total(OrderLine.Amount), (stock.StockPrice * total(OrderLine.Amount)) FROM OrderLine LEFT JOIN Stock ON OrderLine.StockID = Stock.StockID  WHERE OrderLine.StockID = ? AND OrderLine.OrderID IN (SELECT OrderID FROM OrderTable WHERE date(OrderDate) BETWEEN date(?) AND date(?)) '
        for row_in in c.execute(stmt2, (row[0], from_date, to_date)):
            stock_list_range.append({'stock_name' : row_in[0], 'stock_price' : row_in[1], 'stock_total_amount': int(row_in[2]), 'stock_total_price': row_in[3]})

    return stock_list_range

def get_total_delivery_range(from_date, to_date):

    total_delivery = 0

    stmt = "SELECT total(OrderTable.DeliveryCharge) FROM OrderTable WHERE OrderTable.OrderStatusID = 1 AND date(OrderTable.OrderDate) BETWEEN date(?) AND date(?)"
    for row in c.execute(stmt, (from_date, to_date)):
        total_delivery = row[0]
    
    return total_delivery

def delete_order(order_id):
    stmt = "DELETE FROM OrderLine WHERE OrderID = ?"
    param = (order_id,)

    c.execute(stmt, param)
    conn.commit()

    stmt = "DELETE FROM OrderTable WHERE OrderID = ?"
    
    c.execute(stmt, param)
    conn.commit()

    return None
