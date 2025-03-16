import mysql.connector

def create_db():
    try:
        # Connect to MySQL Server
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jaydip@1234"
        )
        cur = con.cursor()

        # Create database if not exists
        cur.execute("CREATE DATABASE IF NOT EXISTS ims")
        con.commit()

        # Connect to the 'ims' database
        con.database = "ims"

        # Create employee table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                eid INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                gender VARCHAR(10),
                contact VARCHAR(20),
                dob VARCHAR(20),
                doj VARCHAR(20),
                pass VARCHAR(255),
                utype VARCHAR(50),
                address TEXT,
                salary DECIMAL(10,2)
            )
        """)
        con.commit()

        # Create supplier table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS supplier (
                invoice INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                contact VARCHAR(50),
                description TEXT
            )
        """)
        con.commit()

        # Create category table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS category (
                cid INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255)
            )
        """)
        con.commit()

        # Create product table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS product (
                pid INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(255),
                supplier VARCHAR(255),
                name VARCHAR(255),
                price DECIMAL(10,2),
                qty INT,
                status VARCHAR(50)
            )
        """)
        con.commit()

        print("Database and tables created successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cur.close()
        con.close()

# Run the function
create_db()
