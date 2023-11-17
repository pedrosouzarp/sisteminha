import mysql.connector

def create_connection():
    # Database information
    database_config = {
        'host': 'db5014788667.hosting-data.io',
        'port': 3306,
        'user': 'dbu2452243',
        'password': '|-|(@r#2021',
        'database': 'dbs12287544'
    }

    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(**database_config)

        if connection.is_connected():
            print("Connected to the database!")

            # Test the connection with a simple query
            test_query = "SELECT 1"
            cursor = connection.cursor()
            cursor.execute(test_query)
            result = cursor.fetchone()

            if result:
                print("Connection test successful!")
            else:
                print("Connection test failed.")

            cursor.close()

        return connection

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
