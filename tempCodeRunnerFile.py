select s.SalesID ,ph.Name as PharmsticName , p.Name As ProductName, s.Date ,s.Quantity,s.PaymentMethod,c.Name As CustomerName
        from product p , pharmacist ph , sales s, customer c
        where p.ProductID = s.ProductID and s.PharmacistID = ph.PharmacistID and c.CustomerID= s.CustomerID
                   order by s.Date desc;