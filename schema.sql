CREATE TABLE 'Customer' (
    'CustomerID' int  NOT NULL ,
    'Name' varchar(200)   NOT NULL ,
    'Phone' varchar(200)   NOT NULL ,
    PRIMARY KEY (
        'CustomerID'
    )
);

CREATE TABLE 'Order' (
    'OrderID' int  NOT NULL ,
    'CustomerID' int  NOT NULL ,
    'OrderDate' date  NOT NULL ,
    'TotalAmount' float  NOT NULL ,
    'ShipmentAddress' varchar(200)   NOT NULL ,
    'OrderStatusID' int  NOT NULL ,
    PRIMARY KEY (
        'OrderID'
    )
);

CREATE TABLE 'OrderLine' (
    'OrderLineID' int  NOT NULL ,
    'OrderID' int  NOT NULL ,
    'ProductID' int  NOT NULL ,
    'Quantity' int  NOT NULL ,
    PRIMARY KEY (
        'OrderLineID'
    )
);

CREATE TABLE 'Product' (
    'ProductID' int  NOT NULL ,
    'Name' varchar(200)  NOT NULL ,
    'Price' money  NOT NULL ,
    PRIMARY KEY (
        'ProductID'
    ),
    CONSTRAINT 'uc_Product_Name' UNIQUE (
        'Name'
    )
);

CREATE TABLE 'OrderStatus' (
    'OrderStatusID' int  NOT NULL ,
    'Name' varchar(200)   NOT NULL ,
    PRIMARY KEY (
        'OrderStatusID'
    ),
    CONSTRAINT 'uc_OrderStatus_Name' UNIQUE (
        'Name'
    )
);

CREATE TABLE 'Expenses' (
    'ExpenseID' int  NOT NULL ,
    'SpendingDate' date  NOT NULL ,
    'TotalAmount' float  NOT NULL ,
    'Note' varchar(200)   NOT NULL ,
    PRIMARY KEY (
        'ExpenseID'
    )
);

ALTER TABLE 'Order' ADD CONSTRAINT 'fk_Order_CustomerID' FOREIGN KEY('CustomerID')
REFERENCES 'Customer' ('CustomerID');

ALTER TABLE 'Order' ADD CONSTRAINT 'fk_Order_OrderStatusID' FOREIGN KEY('OrderStatusID')
REFERENCES 'OrderStatus' ('OrderStatusID');

ALTER TABLE 'OrderLine' ADD CONSTRAINT 'fk_OrderLine_OrderID' FOREIGN KEY('OrderID')
REFERENCES 'Order' ('OrderID');

ALTER TABLE 'OrderLine' ADD CONSTRAINT 'fk_OrderLine_ProductID' FOREIGN KEY('ProductID')
REFERENCES 'Product' ('ProductID');

CREATE INDEX 'idx_Customer_Name'
ON 'Customer' ('Name');

