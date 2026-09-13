CREATE database pizza_hut;
use pizza_hut;

-- create tables
SELECT * FROM pizza_hut.pizza;
SELECT * FROM pizza_hut.pizza_type;

-- create tables
DROP TABLE IF EXISTS order_details;

CREATE TABLE order_details (
    order_details_id INT,
    order_id INT,
    pizza_id VARCHAR(50),
    quantity INT
);




