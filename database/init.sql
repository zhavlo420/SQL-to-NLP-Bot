CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    age INT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INT REFERENCES categories(id),
    price NUMERIC(12,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL,
    total_amount NUMERIC(12,2) NOT NULL,
    order_date DATE NOT NULL
);

INSERT INTO categories (name) VALUES
('Laptops'), ('Phones'), ('Audio'), ('Accessories')
ON CONFLICT DO NOTHING;

INSERT INTO customers (name, city, country, age) VALUES
('Aarav','Mumbai','India',27),
('Diya','Delhi','India',31),
('Kabir','Bengaluru','India',24),
('Maya','Pune','India',29),
('Arjun','Hyderabad','India',35),
('Noah','London','UK',30)
ON CONFLICT DO NOTHING;

INSERT INTO products (name, category_id, price)
SELECT 'Pro Laptop', id, 120000 FROM categories WHERE name='Laptops'
ON CONFLICT DO NOTHING;

INSERT INTO products (name, category_id, price)
SELECT 'Smart Phone X', id, 70000 FROM categories WHERE name='Phones'
ON CONFLICT DO NOTHING;

INSERT INTO products (name, category_id, price)
SELECT 'Studio Headphones', id, 18000 FROM categories WHERE name='Audio'
ON CONFLICT DO NOTHING;

INSERT INTO products (name, category_id, price)
SELECT 'Mechanical Keyboard', id, 9000 FROM categories WHERE name='Accessories'
ON CONFLICT DO NOTHING;

INSERT INTO orders (customer_id, product_id, quantity, total_amount, order_date)
SELECT c.id, p.id, 1, p.price, CURRENT_DATE - INTERVAL '10 days'
FROM customers c CROSS JOIN products p
WHERE c.country='India'
LIMIT 8;

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'querymind_ro') THEN
    CREATE ROLE querymind_ro LOGIN PASSWORD 'querymind_ro';
  END IF;
END $$;

GRANT CONNECT ON DATABASE querymind TO querymind_ro;
GRANT USAGE ON SCHEMA public TO querymind_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO querymind_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO querymind_ro;
