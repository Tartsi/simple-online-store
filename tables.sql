CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    admin INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    amount INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS shopping_cart (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE
    SET NULL,
        product_id INTEGER REFERENCES products ON DELETE
    SET NULL,
        quantity INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS completed_orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE
    SET NULL,
        cart_id INTEGER REFERENCES shopping_cart ON DELETE
    SET NULL,
        address TEXT NOT NULL,
        total_price DECIMAL NOT NULL DEFAULT 0,
        date_created TIMESTAMP DEFAULT now()
);
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE
    SET NULL,
        product_id INTEGER REFERENCES products ON DELETE CASCADE,
        rating INTEGER NOT NULL DEFAULT 0,
        description TEXT NOT NULL,
        date_created TIMESTAMP DEFAULT now()
);