-- Insert test data into the product table
INSERT INTO product (name, description, price, stock) VALUES
('Laptop', 'High-performance laptop', 1200.99, 10),
('Smartphone', 'Latest model smartphone', 799.49, 25),
('Headphones', 'Noise-cancelling headphones', 199.99, 50),
('Monitor', '4K Ultra HD monitor', 349.99, 15),
('Keyboard', 'Mechanical keyboard', 89.99, 30);

-- Insert test data into the customer table
INSERT INTO customer (first_name, last_name, email, phone) VALUES
('John', 'Doe', 'john.doe@example.com', '123-456-7890'),
('Jane', 'Smith', 'jane.smith@example.com', '987-654-3210'),
('Alice', 'Johnson', 'alice.johnson@example.com', '555-123-4567'),
('Bob', 'Brown', 'bob.brown@example.com', '444-555-6666'),
('Charlie', 'Davis', 'charlie.davis@example.com', '333-222-1111');

-- Insert test data into the orders table
INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
(1, 1, 1, '2025-05-01'),
(2, 2, 2, '2025-05-02'),
(3, 3, 1, '2025-05-03'),
(4, 4, 1, '2025-05-04'),
(5, 5, 3, '2025-05-05'),
(1, 2, 1, '2025-04-02'),
(2, 5, 2, '2025-04-02'),
(3, 2, 1, '2025-04-02'),
(4, 3, 1, '2025-04-02'),
(5, 3, 3, '2025-04-02');