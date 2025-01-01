from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime


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
            # Welcome message for the authenticated pharmacist
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
    
@app.route('/medicien')
def medicien():
        # Establish database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("select p.name , p.Price , p.ExpirationDate,p.ProductType,p.Quantity,p.LastUpdatedDate from product p order by p.Quantity ") 
    rows = cursor.fetchall()

    # Fetch products with low stock (Quantity <= 5)
    cursor.execute("SELECT p.name FROM product p WHERE p.Quantity <= 5")
    low_stock_products = cursor.fetchall()  # This will return a list of dictionaries
        # Close connection
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

@app.route("/users")
def users():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch pharmacist details
    cursor.execute("SELECT Name, ContactInfo, Role, Wage FROM Pharmacist")
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

@app.route("/customer")
def customers():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch pharmacist details
    cursor.execute("SELECT Name, city, street, DateOfBirth, Email, Phonenum FROM customer")
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

@app.route("/orders")
def orders():
    # Get database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch pharmacist details
    cursor.execute('''
        select o.OrderID,ph.Name as PharmsticName , p.Name As ProductName, o.OrderDate ,o.Quantity
        from product p , pharmacist ph , orders o
        where p.ProductID = o.ProductID and o.PharmacistID = ph.PharmacistID;
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
        PharmacistID = request.form['PharmacistID']
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
    cursor.execute('select * from orders o WHERE OrderID = %s ', (id,))
    orders = cursor.fetchone()
    if not orders:
        conn.close()
        print("orders not found!")
        return redirect(url_for('orders'))

    if request.method == 'POST':
        print("Form submitted!")
        PharmacistID = request.form['PharmacistID']
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
@app.route('/')
def home():
    return render_template('login.html')  # Render the login page

if __name__ == '__main__':
    app.run(debug=True)
