import sqlite3


def create_tables(connection):
    cursor = connection.cursor()

    clients_create_script = """CREATE TABLE IF NOT EXISTS clients (
        id integer PRIMARY KEY,
        personal_code text NOT NULL,
        name text NOT NULL,
        surname text NOT NULL        
    )
    """

    products_create_script = """CREATE TABLE IF NOT EXISTS products (
        id integer PRIMARY KEY,
        name text NOT NULL,
        price real NOT NULL,
        amount integer DEFAULT(0)
    )
    """

    orders_create_script = """CREATE TABLE IF NOT EXISTS orders (
        id integer PRIMARY KEY,
        client_id integer NOT NULL,
        number text NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE
    )
    """

    order_details_create_script = """CREATE TABLE IF NOT EXISTS order_details (
        id integer PRIMARY KEY,
        order_id integer NOT NULL,
        product_id integer NOT NULL,
        amount integer default(1),
        FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
    )
    """

    cursor.execute(clients_create_script)
    cursor.execute(products_create_script)
    cursor.execute(orders_create_script)
    cursor.execute(order_details_create_script)

    connection.commit()


def main():
    connection = sqlite3.connect("db.sqlite")

    create_tables(connection)

    connection.close()


if __name__ == "__main__":
    main()
