CREATE DATABASE ecom;
use ecom;

CREATE TABLE Orders (
OrderID int,
CustomerName varchar(50),
Product varchar(50),
Category varchar(50),
Quantity int,
Price int,
City varchar(50),
OrderDate date
);

-- Insert Data
INSERT INTO Orders VALUES
(101,'Amit','Laptop','Electronics',1,50000,'Delhi','2025-01-05'),
(102,'Priya','Mobile','Electronics',2,20000,'Mumbai','2025-01-06'),
(103,'Rahul','Shoes','Fashion',3,3000,'Delhi','2025-01-07'),
(104,'Neha','Watch','Fashion',1,5000,'Pune','2025-01-08'),
(105,'Arjun','Laptop','Electronics',1,50000,'Mumbai','2025-01-09'),
(106,'Kavya','Bag','Fashion',2,2500,'Delhi','2025-01-10'),
(107,'Rohit','Mobile','Electronics',1,20000,'Pune','2025-01-11'),
(108,'Ananya','Shoes','Fashion',2,3000,'Mumbai','2025-01-12');

-- Now check the data which is inserted or not
select *
from orders;

-- Now we need to use where to apply condition
select *
from orders
WHERE City = 'Mumbai'; 

-- Now calculate the things

Select *,
Quantity * Price AS Sales
From Orders;

-- AGGREGATIONS 
-- Now calculate the Revenue
Select Sum(Quantity * Price) AS Revenue
From Orders;

-- Average Revenue
Select AVG(Quantity * Price)
From Orders;

--  GROUP BY 

Select Category,
        Sum(Quantity * Price) AS Revenue
From Orders
GROUP BY Category;

-- Sales By City
Select City,
       sum(Quantity * Price) AS Revenue
       From Orders
       Group By City;
       
       
-- ORDERS BY CATEGORY
Select Category,
Count(OrderID)
From Orders
Group By Category;
 
 
 -- Avg price by product
Select Product,
AVG(Price)
from Orders
Group By Product;

-- Top Selling Product
Select Product,
Sum(Quantity) As UnitsSold
From Orders
Group By Product
Order By UnitsSold Desc;

-- CITY WITH HIGHEST REVENUE
Select City,
sum(Quantity * Price) As Revenue
From Orders
Group By City
Order By Revenue Desc;







