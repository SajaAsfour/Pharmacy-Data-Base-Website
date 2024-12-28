from flask import Flask, render_template, request, redirect, url_for, flash
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

@app.route('/')
def home():
    return render_template('login.html')  # Render the login page

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

        cursor.execute("select SUM(p.Price * i.Quantity) AS TotalStockValue  FROM Product p , inventory i where p.productID = i.ProductID") 
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
    

if __name__ == '__main__':
    app.run(debug=True)
