CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(40) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    admin INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    amount INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS shopping_cart (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    total_price DECIMAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users,
    FOREIGN KEY (product_id) REFERENCES products
);
CREATE TABLE IF NOT EXISTS completed_orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    date_created TIMESTAMP DEFAULT now(),
    address TEXT NOT NULL,
    total_price DECIMAL NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users,
    FOREIGN KEY (product_id) REFERENCES products
);
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    rating INTEGER NOT NULL DEFAULT 0,
    description TEXT NOT NULL,
    date_created TIMESTAMP DEFAULT now(),
    FOREIGN KEY (user_id) REFERENCES users,
    FOREIGN KEY (product_id) REFERENCES products
);