import pandas as pd
from flask import Flask, jsonify, render_template, request, redirect, session, url_for, flash
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = '123'  # For flash messages and session management
# MySQL database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='W7301@jqir#',
        database='PharmacyManagement'
    )
    return connection

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query to validate pharmacist credentials
        query = """
            SELECT * 
            FROM Pharmacist 
            WHERE Username = %s AND Password = %s
        """
        cursor.execute(query, (username, password))
        pharmacist = cursor.fetchone()

        if pharmacist:
            # Store PharmacistID in session after successful login
            session['pharmacist_id'] = pharmacist['PharmacistID']
            return redirect(url_for('dashboard'))  # Redirect to a dashboard (create this route)
        else:
            return redirect(url_for('home'))

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return redirect(url_for('home'))

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()


@app.route('/dashboard')
def dashboard():
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to count total customers
        cursor.execute("SELECT COUNT(*) FROM customer") 
        total_customers = cursor.fetchone()[0]

        # Close connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        total_customers = "Error fetching data"
    
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to count total customers
        cursor.execute("SELECT COUNT(*) FROM pharmacist where Role = 'Pharmacist'") 
        total_pharmacist = cursor.fetchone()[0]

        # Close connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        total_pharmacist = "Error fetching data"

    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        current_date = datetime.now().strftime("%Y-%m-%d")

        query="""
                SELECT SUM(p.Price * s.Quantity) AS TotalRevenue 
                FROM  product p ,  Sales s
                where s.date = %s and p.ProductID = s.productid
              """
        cursor.execute(query, (current_date,))
        TotalRevenue = cursor.fetchone()[0]
        if (TotalRevenue == None):
            TotalRevenue =0

        # Close connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        TotalRevenue = "Error fetching data"

    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("select SUM(p.Price * p.Quantity) AS TotalStockValue  FROM Product p") 
        TotalStockValue = cursor.fetchone()[0]

        # Close connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        TotalStockValue = "Error fetching data"
    
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        current_date = datetime.now().strftime("%Y-%m-%d")

        query = """
        SELECT SUM(S.Quantity) AS TotalQuantitySold
        FROM Sales S
        WHERE S.Date = %s
        """

        cursor.execute(query, (current_date,))
        Quantity_of_sales = cursor.fetchone()[0]
        if (Quantity_of_sales == None):
            Quantity_of_sales =0

        # Close connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        Quantity_of_sales = "Error fetching data"
    
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        WITH Revenue AS (
            SELECT 
                SUM(s.Quantity * p.Price) AS TotalRevenue
            FROM 
                Sales s
            JOIN 
                Product p ON s.ProductID = p.ProductID
            WHERE 
                DATE(s.Date) = %s
        ),
        Cost AS (
            SELECT 
                SUM(o.Quantity * (p.Price * 0.9)) AS TotalCost
            FROM 
                Orders o
            JOIN 
                Product p ON o.ProductID = p.ProductID
            WHERE 
                DATE(o.orderDate) = %s
        )
        SELECT 
            COALESCE(r.TotalRevenue, 0) - COALESCE(c.TotalCost, 0) AS Profit
        FROM 
            Revenue r
        CROSS JOIN 
            Cost c
        """
        cursor.execute(query, (current_date,current_date))
        TotalRevenueInDay = cursor.fetchone()[0]
        if (TotalRevenueInDay == None):
            TotalRevenueInDay =0

        # Close connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        TotalRevenueInDay = "Error fetching data"

    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        current_date = datetime.now().strftime("%Y-%m-%d")

        query = """
        SELECT SUM(o.Quantity * (p.Price * 0.9)) AS TotalOrderPrice
        FROM Orders o
        JOIN Product p ON o.ProductID = p.ProductID
        where o.orderdate = %s
        """

        cursor.execute(query, (current_date,))
        TotalOrderPrice = cursor.fetchone()[0]
        if (TotalOrderPrice == None):
            TotalOrderPrice =0

        # Close connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        TotalOrderPrice = "Error fetching data"
    
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        current_date = datetime.now().strftime("%Y-%m-%d")

        query = """
        select count(*) from orders where orderdate = %s
        """

        cursor.execute(query, (current_date,))
        NumnerofOrder = cursor.fetchone()[0]
        if (NumnerofOrder == None):
            NumnerofOrder =0

        # Close connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        NumnerofOrder = "Error fetching data"

    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        query = 'SELECT P.Name, o.Quantity,  (o.Quantity * (p.Price * 0.9)) AS TotalPrice FROM Orders o JOIN Product p ON o.ProductID = p.ProductID where o.orderdate = %s'
        cursor.execute(query, (current_date,))
        orders = cursor.fetchall()
        # Close connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        orders = "Error fetching data"

    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
                SELECT 
                p.name AS pharmacist_name, 
                c.name AS customer_name, 
                SUM(d.Price * s.Quantity) AS total_price, 
                s.paymentmethod
                FROM 
                    customer c
                JOIN 
                    sales s ON c.CustomerID = s.CustomerID
                JOIN 
                    pharmacist p ON p.PharmacistID = s.PharmacistID
                
                JOIN 
                    product d ON d.ProductID = s.ProductID
                WHERE 
                    s.Date = %s
                GROUP BY 
                    p.name, c.name, s.paymentmethod;
                """
        cursor.execute(query, (current_date,))
        sales = cursor.fetchall()
        # Close connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sales = "Error fetching data"


    return render_template('dashboard.html',sales=sales,orders=orders ,NumnerofOrder=NumnerofOrder,TotalOrderPrice=TotalOrderPrice,TotalStockValue=TotalStockValue,total_customers=total_customers ,total_pharmacist=total_pharmacist,Quantity_of_sales=Quantity_of_sales,TotalRevenue=TotalRevenue,TotalRevenueInDay=TotalRevenueInDay)
    
@app.route('/medicien', methods=['GET'])
def medicien():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get the search query from the request
    search_query = request.args.get('search', default='', type=str)

    if search_query.isdigit():  # If the search query is numeric, search by ID
        cursor.execute("SELECT * FROM product p WHERE p.ProductID = %s", (search_query,))
    elif search_query:  # Otherwise, search by name
        cursor.execute("SELECT * FROM product p WHERE p.Name LIKE %s ORDER BY p.Quantity", 
                       (f"%{search_query}%",))
    else:  # Default case, no search query
        cursor.execute("SELECT * FROM product p ORDER BY p.Quantity")

    rows = cursor.fetchall()

    # Fetch products with low stock (Quantity <= 5)
    cursor.execute("SELECT p.name FROM product p WHERE p.Quantity <= 5")
    low_stock_products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('medicen.html', rows=rows, low_stock_products=low_stock_products)



@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        Price = request.form['Price']
        ExpirationDate = request.form['ExpirationDate']
        ProductType = request.form['ProductType']
        Description = request.form['Description']
        LastUpdatedDate = datetime.now().strftime("%Y-%m-%d")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Product (Name, Price, ExpirationDate, ProductType, Description,LastUpdatedDate) VALUES (%s, %s, %s, %s, %s,%s)', 
                       (name, Price, ExpirationDate, ProductType, Description,LastUpdatedDate))
        conn.commit()
        conn.close()

        return redirect(url_for('medicien'))
    return render_template('add_product.html')

@app.route('/edit_product/<string:name>', methods=['GET', 'POST'])
def edit_product(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the product by name
    print(f"Fetching product with name: {name}")
    cursor.execute('SELECT * FROM Product WHERE name = %s', (name,))
    product = cursor.fetchone()

    if not product:
        conn.close()
        print("Product not found!")
        return redirect(url_for('medicien'))

    if request.method == 'POST':
        print("Form submitted!")
        new_name = request.form['name']
        Price = request.form['Price']
        ExpirationDate = request.form['ExpirationDate']
        ProductType = request.form['ProductType']
        Description = request.form['Description']
        LastUpdatedDate = datetime.now().strftime("%Y-%m-%d")
        Quantity=request.form['Quantity']
        # Update the product
        print(f"Updating product: {name}")
        cursor.execute('''
            UPDATE Product 
            SET name = %s, Price = %s, ProductType = %s, ExpirationDate = %s, LastUpdatedDate = %s, Description = %s,Quantity= %s
            WHERE name = %s
        ''', (new_name, Price, ProductType, ExpirationDate, LastUpdatedDate, Description,Quantity, name))
        conn.commit()
        conn.close()
        print("Product updated successfully!")
        return redirect(url_for('medicien'))

    conn.close()
    return render_template('edit_product.html', product=product)


@app.route('/delete_product/<string:name>', methods=['GET', 'POST'])
def delete_product(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM product WHERE Name = %s', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('medicien'))

@app.route("/users", methods=['GET'])
def users():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
  # Get the search query from the request
    search_query = request.args.get('search', default='', type=str)

    if search_query.isdigit():  # If the search query is numeric, search by ID
        cursor.execute("SELECT * FROM pharmacist p WHERE p.PharmacistID = %s", (search_query,))
    elif search_query:  # Otherwise, search by name
        cursor.execute("SELECT * FROM pharmacist p WHERE p.Name LIKE %s", 
                       (f"%{search_query}%",))
    else:  # Default case, no search query
         cursor.execute("SELECT Name, ContactInfo, Role, Wage FROM Pharmacist")
    # Fetch pharmacist details
   
    rows = cursor.fetchall()

    # Calculate the first day of the current month in Python
    first_day_of_month = datetime.now().replace(month=1, day=1).strftime("%Y-%m-%d")

    # Query to get the top pharmacist by total sales
    query = """
        SELECT 
            p.Name,
            COUNT(s.SalesID) AS TotalSales
        FROM 
            Pharmacist p
        JOIN 
            Sales s ON p.PharmacistID = s.PharmacistID
        WHERE 
            s.Date >= %s
        GROUP BY 
            p.PharmacistID, p.Name
        ORDER BY 
            TotalSales DESC
        LIMIT 1
    """
    cursor.execute(query, (first_day_of_month,))
    topUser = cursor.fetchone()  # Use fetchone() since LIMIT 1 guarantees a single row

    # Close connection
    cursor.close()
    connection.close()

    # Render template with the fetched data
    return render_template('users.html', rows=rows, topUser=topUser)

@app.route('/addusers', methods=['GET', 'POST'])
def add_users():
    if request.method == 'POST':
        Name = request.form['Name']
        ContactInfo = request.form['ContactInfo']
        Role = request.form['Role']
        Username = request.form['Username']
        Password = request.form['Password']
        Wage = request.form['Wage']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Pharmacist (Name, ContactInfo, Role, Username, Password, Wage) VALUES (%s, %s, %s, %s, %s,%s)', 
                       (Name, ContactInfo, Role, Username, Password,Wage))
        conn.commit()
        conn.close()

        return redirect(url_for('users'))
    return render_template('add_users.html')
@app.route('/edit_users/<string:name>', methods=['GET', 'POST'])
def edit_users(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the product by name
    print(f"Fetching product with Name: {name}")
    cursor.execute('SELECT * FROM pharmacist WHERE Name = %s', (name,))
    users = cursor.fetchone()

    if not users:
        conn.close()
        print("user not found!")
        return redirect(url_for('users'))

    if request.method == 'POST':
        print("Form submitted!")
        new_name = request.form['name']
        ContactInfo = request.form['ContactInfo']
        Role = request.form['Role']
        Wage = request.form['Wage']
        print(f"Updating user: {name}")
        cursor.execute('''
            UPDATE pharmacist 
            SET Name = %s, ContactInfo = %s, Role = %s, Wage = %s
            WHERE Name = %s
        ''', (new_name, ContactInfo, Role, Wage, name))
        conn.commit()
        conn.close()
        print("user updated successfully!")
        return redirect(url_for('users'))

    conn.close()
    return render_template('edit_users.html', users=users)
@app.route('/delete_users/<string:name>', methods=['GET', 'POST'])
def delete_users(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pharmacist WHERE Name = %s', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))

@app.route("/customer", methods=['GET'])
def customers():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
# Get the search query from the request
    search_query = request.args.get('search', default='', type=str)

    if search_query.isdigit():  # If the search query is numeric, search by ID
        cursor.execute("SELECT * FROM customer  WHERE CustomerID = %s", (search_query,))
    elif search_query:  # Otherwise, search by name
        cursor.execute("SELECT * FROM customer  WHERE Name LIKE %s", 
                       (f"%{search_query}%",))
    else:  # Default case, no search query
        cursor.execute("SELECT Name, city, street, DateOfBirth, Email, Phonenum FROM customer")
    # Fetch pharmacist details
    
    rows = cursor.fetchall()

    # Calculate the first day of the current month in Python
    first_day_of_month = datetime.now().replace(month=1, day=1).strftime("%Y-%m-%d")

    # Query to get the top pharmacist by total sales
    query = """
        SELECT 
            c.Name,
            COUNT(s.SalesID) AS TotalSales
        FROM 
            customer c
        JOIN 
            Sales s ON c.CustomerID = s.CustomerID
        WHERE 
            s.Date >= %s
        GROUP BY 
            c.CustomerID, c.Name
        ORDER BY 
            TotalSales DESC
        LIMIT 1
    """
    cursor.execute(query, (first_day_of_month,))
    topCustomer = cursor.fetchone()  # Use fetchone() since LIMIT 1 guarantees a single row

    # Close connection
    cursor.close()
    connection.close()

    # Render template with the fetched data
    return render_template('customers.html', rows=rows, topCustomer=topCustomer)

@app.route('/add_customers', methods=['GET', 'POST'])
def add_customers():
    if request.method == 'POST':
        Name = request.form['Name']
        city = request.form['city']
        street = request.form['street']
        DateOfBirth = request.form['DateOfBirth']
        Email = request.form['Email']
        Phonenum = request.form['Phonenum']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO customer (Name, city, street, DateOfBirth, Email, Phonenum) VALUES (%s, %s, %s, %s, %s,%s)', 
                       (Name, city, street, DateOfBirth, Email, Phonenum))
        conn.commit()
        conn.close()

        return redirect(url_for('customers'))
    return render_template('add_customer.html')
@app.route('/edit_customers/<string:name>', methods=['GET', 'POST'])
def edit_customers(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the product by name
    print(f"Fetching Customer with Name: {name}")
    cursor.execute('SELECT * FROM customer WHERE Name = %s', (name,))
    customers = cursor.fetchone()

    if not customers:
        conn.close()
        print("customer not found!")
        return redirect(url_for('customers'))

    if request.method == 'POST':
        print("Form submitted!")
        new_name = request.form['name']
        city = request.form['city']
        street = request.form['street']
        DateOfBirth = request.form['DateOfBirth']
        Email = request.form['Email']
        Phonenum = request.form['Phonenum']
        print(f"Updating customer: {name}")
        cursor.execute('''
            UPDATE customer 
            SET Name = %s, city = %s, street = %s, DateOfBirth = %s,Email = %s ,Phonenum=%s
            WHERE Name = %s
        ''', (new_name, city, street, DateOfBirth, Email, Phonenum,name))
        conn.commit()
        conn.close()
        print("customers updated successfully!")
        return redirect(url_for('customers'))

    conn.close()
    return render_template('edit_customers.html', customers=customers)
@app.route('/delete_customers/<string:name>', methods=['GET', 'POST'])
def delete_customers(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM customer WHERE Name = %s', (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('customers'))

@app.route("/orders", methods=['GET'])
def orders():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
# Get the search query from the request
    search_query = request.args.get('search', default='', type=str)

    if search_query.isdigit():  # If the search query is numeric, search by ID
        cursor.execute("select o.OrderID,ph.Name as PharmsticName , p.Name As ProductName, o.OrderDate ,o.Quantity from product p , pharmacist ph , orders o   WHERE o.OrderID = %s and p.ProductID = o.ProductID and o.PharmacistID = ph.PharmacistID order by o.OrderDate desc", (search_query,))
    
    elif search_query:  # Otherwise, search by name
        cursor.execute("""select o.OrderID,ph.Name as PharmsticName , p.Name As ProductName, o.OrderDate ,o.Quantity
            from product p , pharmacist ph , orders o
            where p.ProductID = o.ProductID and o.PharmacistID = ph.PharmacistID and o.OrderDate = %s
                    order by o.OrderDate desc """, 
                       (f"{search_query}",))
    else:  # Default case, no search query
    # Fetch pharmacist details
        cursor.execute('''
            select o.OrderID,ph.Name as PharmsticName , p.Name As ProductName, o.OrderDate ,o.Quantity
            from product p , pharmacist ph , orders o
            where p.ProductID = o.ProductID and o.PharmacistID = ph.PharmacistID
                    order by o.OrderDate desc;
                    ''')
    rows = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Render template with the fetched data
    return render_template('order.html', rows=rows)

@app.route('/add_orders', methods=['GET', 'POST'])
def add_orders():
    if request.method == 'POST':
        if 'pharmacist_id' not in session:
            return redirect(url_for('login'))  # Redirect to login if not authenticated
    
    # Get logged-in pharmacist ID from session
        PharmacistID = session['pharmacist_id']
        ProductID = request.form['ProductID']
        OrderDate = datetime.now().strftime("%Y-%m-%d")
        Quantity = request.form['Quantity']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (PharmacistID, ProductID, OrderDate, Quantity) VALUES (%s, %s, %s, %s)', 
                       (PharmacistID, ProductID, OrderDate, Quantity))
        cursor.execute('''Update product 
                    set Quantity = Quantity + %s
                    where productID = %s
                   ''',(Quantity,ProductID))
        conn.commit()
        conn.close()

        return redirect(url_for('orders'))
    return render_template('add_order.html')
@app.route('/edit_orders/<int:id>', methods=['GET', 'POST'])
def edit_orders(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the product by name
    print(f"Fetching orders with ID: {id}")
    cursor.execute('select * from orders o WHERE OrderID = %s', (id,))
    orders = cursor.fetchone()
    if not orders:
        conn.close()
        print("orders not found!")
        return redirect(url_for('orders'))

    if request.method == 'POST':
        print("Form submitted!")
        
        PharmacistID = session['pharmacist_id']
        ProductID = request.form['ProductID']
        OrderDate = datetime.now().strftime("%Y-%m-%d")
        Quantity = request.form['Quantity']
        print(f"Updating orders: {id}")
        cursor.execute('''
            UPDATE orders 
            SET  PharmacistID = %s, ProductID = %s, OrderDate = %s, Quantity= %s
            WHERE OrderID = %s
        ''', (PharmacistID, ProductID, OrderDate, Quantity,id))
        
        conn.commit()
        conn.close()
        print("orders updated successfully!")
        return redirect(url_for('orders'))

    conn.close()
    return render_template('edit_order.html', orders=orders)
@app.route('/delete_orders/<int:id>', methods=['GET', 'POST'])
def delete_orders(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM orders WHERE OrderID = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('orders'))

@app.route("/sales")
def sales():
    return render_template('question_sale.html')

@app.route("/new_sale")
def new_sale():
    return render_template('new_sale.html')

# Route to process form submission
from flask import render_template

@app.route('/submit', methods=['POST'])
def submit_sales():
    # Ensure that the pharmacist is logged in
    if 'pharmacist_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    # Get logged-in pharmacist ID from session
    pharmacist_id = session['pharmacist_id']
    data = request.form
    date = datetime.now().strftime("%Y-%m-%d")
    payment_method = data['payment_method']
    customer_id = data['customer_id']
    product_ids = data.getlist('product_id')
    quantities = data.getlist('quantity')

    with get_db_connection() as conn:
        cursor = conn.cursor()

        for product_id, quantity in zip(product_ids, quantities):
            product_id = int(product_id)
            quantity = int(quantity)

            # Fetch the current stock of the product
            cursor.execute('''
                SELECT Quantity, Description 
                FROM Product 
                WHERE ProductID = %s
            ''', (product_id,))
            result = cursor.fetchone()

            if not result:
                return render_template('out_of_stock.html', message=f"Product ID {product_id} does not exist.")

            current_stock, description = result

            # Check if stock is sufficient
            if current_stock == 0:
                # Find an alternative product with the same description
                cursor.execute('''
                    SELECT ProductID, Name 
                    FROM Product 
                    WHERE Description = %s AND Quantity > 0 AND ProductID != %s
                    LIMIT 1
                ''', (description, product_id))
                alternative = cursor.fetchone()

                if alternative:
                    alternative_id, alternative_name = alternative
                    return render_template(
                        'out_of_stock.html', 
                        message=f"Product ID {product_id} is out of stock. Consider Product ID {alternative_id} ({alternative_name}) instead."
                    )
                else:
                    return render_template(
                        'out_of_stock.html', 
                        message=f"Product ID {product_id} is out of stock, and no alternatives are available."
                    )

            elif quantity > current_stock:
                return render_template(
                    'out_of_stock.html', 
                    message=f"Requested quantity for Product ID {product_id} exceeds available stock ({current_stock})."
                )

            # Insert the sale record
            cursor.execute('''
                INSERT INTO Sales (ProductID, Quantity, Date, PaymentMethod, CustomerID, PharmacistID)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (product_id, quantity, date, payment_method, customer_id, pharmacist_id))

            # Update the product quantity
            cursor.execute('''
                UPDATE Product 
                SET Quantity = Quantity - %s 
                WHERE ProductID = %s
            ''', (quantity, product_id))

        conn.commit()

    return redirect(url_for('sales'))

@app.route("/sale_archive", methods=['GET'])
def sale_archive():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
# Get the search query from the request
    search_query = request.args.get('search', default='', type=str)

    if search_query.isdigit():  # If the search query is numeric, search by ID
        cursor.execute("""select s.SalesID ,ph.Name as PharmsticName , p.Name As ProductName, s.Date ,s.Quantity,s.PaymentMethod,c.Name As CustomerName
        from product p , pharmacist ph , sales s, customer c
        where p.ProductID = s.ProductID and s.PharmacistID = ph.PharmacistID and c.CustomerID= s.CustomerID
        and s.SalesID = %s
        order by s.Date desc """, (search_query,))
    elif search_query:  # Otherwise, search by name
        cursor.execute("""select s.SalesID ,ph.Name as PharmsticName , p.Name As ProductName, s.Date ,s.Quantity,s.PaymentMethod,c.Name As CustomerName
        from product p , pharmacist ph , sales s, customer c
        where p.ProductID = s.ProductID and s.PharmacistID = ph.PharmacistID and c.CustomerID= s.CustomerID
        and s.Date = %s
        order by s.Date desc""", 
                       (f"{search_query}",))
    else:  # Default case, no search query
    # Fetch pharmacist details
        cursor.execute('''
            select s.SalesID ,ph.Name as PharmsticName , p.Name As ProductName, s.Date ,s.Quantity,s.PaymentMethod,c.Name As CustomerName
            from product p , pharmacist ph , sales s, customer c
            where p.ProductID = s.ProductID and s.PharmacistID = ph.PharmacistID and c.CustomerID= s.CustomerID
                    order by s.Date desc;
                    ''')
    rows = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Render template with the fetched data
    return render_template('sale_archive.html', rows=rows)

@app.route('/edit_sales/<int:id>', methods=['GET', 'POST'])
def edit_sales(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the product by name
    print(f"Fetching sales with ID: {id}")
    cursor.execute('select * from sales s WHERE SalesID = %s', (id,))
    sales = cursor.fetchone()
    if not sales:
        conn.close()
        print("sales not found!")
        return redirect(url_for('sale_archive'))

    if request.method == 'POST':
        print("Form submitted!")
        ProductID = request.form['ProductID']
        CustomerID = request.form['CustomerID']
        Date = datetime.now().strftime("%Y-%m-%d")
        Quantity = request.form['Quantity']
        PharmacistID=session['pharmacist_id']
        PaymentMethod=request.form['PaymentMethod']
        cursor.execute('''
            UPDATE sales 
            SET  ProductID = %s, Date = %s, Quantity= %s, CustomerID= %s , PaymentMethod=%s , PharmacistID= %s
            WHERE SalesID = %s
        ''', (ProductID, Date, Quantity, CustomerID,PaymentMethod ,PharmacistID,id))
        conn.commit()
        conn.close()
        print("sales updated successfully!")
        return redirect(url_for('sale_archive'))

    conn.close()
    return render_template('edit_sale.html', sales=sales)
@app.route('/delete_sales/<int:id>', methods=['GET', 'POST'])
def delete_sales(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sales WHERE SalesID = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('sale_archive'))

@app.route('/get_chart')
def get_chart_data():
    connection = get_db_connection()
    # Query execution
    query = """
    SELECT 
        P.Name AS ProductName, 
        SUM(S.Quantity * P.Price) AS TotalRevenue
    FROM 
        Sales S
    JOIN 
        Product P ON S.ProductID = P.ProductID
    GROUP BY 
        P.Name
    HAVING 
        SUM(S.Quantity * P.Price) > 500;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert result to JSON
    data = {"productNames": [], "totalRevenue": []}
    for row in result:
        data["productNames"].append(row[0])  # ProductName
        data["totalRevenue"].append(row[1])  # TotalRevenue

    return jsonify(data)

@app.route('/get_chart1')
def get_chart_data1():
    connection = get_db_connection()

    # Query execution
    query = """
    SELECT 
        PH.Name AS PharmacistName, 
        SUM(S.Quantity * P.Price) AS TotalRevenue
    FROM 
        Pharmacist PH
    LEFT JOIN 
        Sales S ON PH.PharmacistID = S.PharmacistID
    LEFT JOIN 
        Product P ON S.ProductID = P.ProductID
    GROUP BY 
        PH.Name
    ORDER BY 
        TotalRevenue DESC;
    """
    
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert result to JSON
    data = {"pharmacistNames": [], "totalRevenue": []}
    for row in result:
        data["pharmacistNames"].append(row[0])  # PharmacistName
        data["totalRevenue"].append(row[1])    # TotalRevenue

    return jsonify(data)

@app.route('/report2')
def report2():
    return render_template ('report2.html')

@app.route('/get_chart3')
def get_chart_data3():
    connection = get_db_connection()
    # Query execution
    query = """
    SELECT 
        C.Name AS CustomerName, 
        SUM(S.Quantity * P.Price) AS TotalSpent
    FROM 
        Customer C
    JOIN 
        Sales S ON C.CustomerID = S.CustomerID
    JOIN 
        Product P ON S.ProductID = P.ProductID
    GROUP BY 
        C.Name
    ORDER BY 
        TotalSpent DESC
    LIMIT 3;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Check if results exist
    if not result:
        return jsonify({"error": "No data available"})

    # Convert result to JSON
    data = {"customerNames": [], "totalSpent": []}
    for row in result:
        data["customerNames"].append(row[0])  # CustomerName
        data["totalSpent"].append(row[1])  # TotalSpent

    return jsonify(data)
@app.route('/report3')
def report3():
    # Serve the HTML file
    return  render_template('report3.html')

@app.route('/get_chart_data5')
def get_chart_data5():
    connection = get_db_connection()
    
    query = """
    SELECT 
        P.ProductType, 
        SUM(S.Quantity) AS TotalQuantitySold
    FROM 
        Sales S
    JOIN 
        Product P ON S.ProductID = P.ProductID
    GROUP BY 
        P.ProductType;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert results to JSON format
    data = {"productTypes": [], "totalQuantities": []}
    for row in result:
        data["productTypes"].append(row[0])  # ProductType
        data["totalQuantities"].append(row[1])  # TotalQuantitySold

    return jsonify(data)

@app.route('/report5')
def index():
    return render_template('report5.html')  # Render HTML template

@app.route('/get_chart7')
def get_chart_data7():
    connection = get_db_connection()
    
    # Updated query execution
    query = """
    SELECT 
        P.Name AS ProductName, 
        SUM(S.Quantity) AS TotalPurchased
    FROM 
        Sales S
    JOIN 
        Product P ON S.ProductID = P.ProductID
    GROUP BY 
        P.ProductID
    ORDER BY 
        TotalPurchased DESC
    ;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert result to JSON
    data = {"productName": "", "totalPurchased": 0}
    if result:
        row = result[0]
        data["productName"] = row[0]  # ProductName
        data["totalPurchased"] = row[1]  # TotalPurchased

    return jsonify(data)

@app.route('/report7')
def report7():
    # Serve the HTML file
    return  render_template('report7.html')

@app.route('/get_chart8')
def get_chart_data8():
    connection = get_db_connection()
    
    # Updated query execution
    query = """
    SELECT 
        PH.Name AS PharmacistName, 
        SUM(O.Quantity) AS TotalQuantityOrdered
    FROM 
        Pharmacist PH
    JOIN 
        Orders O ON PH.PharmacistID = O.PharmacistID
    GROUP BY 
        PH.Name;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert result to JSON
    data = {"pharmacistNames": [], "totalQuantitiesOrdered": []}
    for row in result:
        data["pharmacistNames"].append(row[0])  # PharmacistName
        data["totalQuantitiesOrdered"].append(row[1])  # TotalQuantityOrdered

    return jsonify(data)

@app.route('/report8')
def report8():
    # Serve the HTML file
    return  render_template('report8.html')
@app.route('/get_chart11')
def get_chart_data11():
    connection = get_db_connection()
    query = """
    SELECT 
        PaymentMethod, 
        SUM(S.Quantity * P.Price) AS TotalRevenue
    FROM 
        Sales S
    JOIN 
        Product P ON S.ProductID = P.ProductID
    GROUP BY 
        PaymentMethod
    ORDER BY 
        TotalRevenue DESC
    LIMIT 1;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    # Convert result to JSON
    data = {"paymentMethods": [], "totalRevenue": []}
    for row in result:
        data["paymentMethods"].append(row[0])  # PaymentMethod
        data["totalRevenue"].append(row[1])  # TotalRevenue

    return jsonify(data)

@app.route('/report11')
def report11():
    # Serve the HTML file
    return  render_template('report11.html')
@app.route('/reports')
def home1():
    # Serve the HTML file
    return  render_template('report.html')

@app.route("/report4")
def report4():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # SQL query to fetch the data
    query = '''
        SELECT 
            Name AS ProductName, 
            ExpirationDate, 
            Quantity
        FROM 
            Product
        WHERE 
            ExpirationDate BETWEEN %s AND DATE_ADD(%s, INTERVAL 90 DAY)
            AND Quantity < 50;
    '''
    cursor.execute(query, (current_date, current_date))
    rows = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Render template with the fetched data
    return render_template('report4.html', rows=rows)
@app.route("/report10")
def report10():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    
    # SQL query to fetch the data
    query = '''
        SELECT 
        P.Name AS ProductName, 
        P.Quantity AS CurrentStock, 
        COALESCE(SUM(O.Quantity), 0) AS TotalOrdered
    FROM 
        Product P
    LEFT JOIN 
        Orders O ON P.ProductID = O.ProductID
    WHERE 
        P.Quantity < 30
    GROUP BY 
        P.Name, P.Quantity;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Render template with the fetched data
    return render_template('report10.html', rows=rows)

@app.route("/report6")
def report6():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # SQL query to fetch the data
    query = '''
        SELECT 
            Role, 
            AVG(Wage) AS AvgWage, 
            MAX(Wage) AS MaxWage
        FROM 
            Pharmacist
        GROUP BY 
            Role;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Render template with the fetched data
    return render_template('report6.html', rows=rows)

@app.route("/report12")
def report12():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # SQL query to fetch the data
    query = '''
        SELECT 
        P.Name AS ProductName
    FROM 
        Product P
    LEFT JOIN 
        Sales S ON P.ProductID = S.ProductID
    WHERE 
        S.ProductID IS NULL;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Render template with the fetched data
    return render_template('report12.html', rows=rows)
@app.route('/')
def home():
    return render_template('login.html')  # Render the login page

@app.route('/report9')
def customer_spending_by_city():
    # SQL query
    query = """
        SELECT 
            C.city AS City, 
            C.Name AS CustomerName, 
            SUM(P.Price * S.Quantity) AS TotalSpent
        FROM 
            Customer C
        JOIN 
            Sales S ON C.CustomerID = S.CustomerID
        JOIN 
            Product P ON S.ProductID = P.ProductID
        WHERE 
            P.Price > 50
        GROUP BY 
            C.city, C.Name
        ORDER BY 
            TotalSpent DESC;
    """

    # Fetch data from the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query)
    rows = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()
    # Render results in the HTML template
    return render_template('report9.html', rows=rows)
if __name__ == '__main__':
    app.run(debug=True)
