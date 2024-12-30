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
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select Name , ContactInfo,Role,Wage from pharmacist ") 
    rows = cursor.fetchall()
    # Close connection
    cursor.close()
    connection.close()
    return render_template('users.html', rows=rows)

@app.route('/')
def home():
    return render_template('login.html')  # Render the login page

if __name__ == '__main__':
    app.run(debug=True)
