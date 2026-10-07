-- ============================================================
-- FactoryFlow Sample Data
-- ============================================================

-- EMPLOYEES
INSERT INTO employees
(employee_code, name, department, job_role, phone, email, hire_date)
VALUES
('EMP001', 'Arun Kumar', 'Production', 'Production Manager', '9876543210', 'arun@factoryflow.com', '2023-06-15'),
('EMP002', 'Priya S', 'Maintenance', 'Maintenance Engineer', '9876543211', 'priya@factoryflow.com', '2024-01-10'),
('EMP003', 'Rahul M', 'Quality', 'Quality Inspector', '9876543212', 'rahul@factoryflow.com', '2024-03-20'),
('EMP004', 'Kavin R', 'Production', 'Machine Operator', '9876543213', 'kavin@factoryflow.com', '2024-07-05');


-- MACHINE TYPES
INSERT INTO machine_types
(type_name, description)
VALUES
('CNC Machine', 'Computer controlled precision machining'),
('Assembly Machine', 'Automated product assembly'),
('Injection Molding', 'Plastic injection molding machine'),
('Packaging Machine', 'Automated product packaging');


-- MACHINES
INSERT INTO machines
(machine_code, machine_name, machine_type_id, manufacturer, model_number,
 purchase_date, installation_date, status, location, operating_hours)
VALUES
('MCH001', 'CNC Alpha', 1, 'Siemens', 'CNC-500', '2022-04-10', '2022-05-01', 'Operational', 'Plant A', 5420.50),
('MCH002', 'Assembly Pro', 2, 'ABB', 'ASM-200', '2023-01-15', '2023-02-05', 'Operational', 'Plant A', 3210.25),
('MCH003', 'Mold Master', 3, 'Husky', 'HM-300', '2021-08-20', '2021-09-10', 'Maintenance', 'Plant B', 6780.75),
('MCH004', 'Pack Fast', 4, 'Bosch', 'PKG-100', '2024-02-12', '2024-03-01', 'Operational', 'Plant B', 1850.40);


-- PRODUCTS
INSERT INTO products
(product_code, product_name, description, category, unit_price, target_quantity)
VALUES
('PRD001', 'Industrial Gear', 'Precision manufactured gear', 'Mechanical', 1250.00, 500),
('PRD002', 'Motor Housing', 'Protective motor housing', 'Mechanical', 850.00, 300),
('PRD003', 'Control Panel', 'Industrial machine control panel', 'Electrical', 2200.00, 200),
('PRD004', 'Pump Assembly', 'Industrial pump assembly', 'Mechanical', 1750.00, 250);


-- SUPPLIERS
INSERT INTO suppliers
(supplier_code, supplier_name, contact_person, phone, email, address, city)
VALUES
('SUP001', 'SteelWorks Ltd', 'Ramesh Kumar', '9000000001', 'sales@steelworks.com', 'Industrial Estate', 'Coimbatore'),
('SUP002', 'TechMaterials Pvt Ltd', 'Suresh B', '9000000002', 'contact@techmaterials.com', 'SIDCO Industrial Park', 'Chennai'),
('SUP003', 'PowerParts Industries', 'Vijay Kumar', '9000000003', 'sales@powerparts.com', 'Industrial Road', 'Bangalore');


-- RAW MATERIALS
INSERT INTO raw_materials
(material_code, material_name, supplier_id, unit, unit_cost, reorder_level)
VALUES
('MAT001', 'Steel Rod', 1, 'Kg', 180.00, 500),
('MAT002', 'Aluminium Sheet', 2, 'Kg', 320.00, 300),
('MAT003', 'Copper Wire', 2, 'Meter', 75.00, 1000),
('MAT004', 'Motor Component', 3, 'Piece', 450.00, 100),
('MAT005', 'Plastic Granules', 3, 'Kg', 150.00, 400);


-- INVENTORY
INSERT INTO inventory
(material_id, quantity, warehouse_location)
VALUES
(1, 1250, 'Warehouse A'),
(2, 650, 'Warehouse A'),
(3, 2400, 'Warehouse B'),
(4, 180, 'Warehouse B'),
(5, 900, 'Warehouse C');


-- INVENTORY TRANSACTIONS
INSERT INTO inventory_transactions
(material_id, transaction_type, quantity, reference_type, notes)
VALUES
(1, 'IN', 1000, 'Purchase', 'Initial stock'),
(2, 'IN', 500, 'Purchase', 'Initial stock'),
(3, 'IN', 2000, 'Purchase', 'Initial stock'),
(4, 'IN', 200, 'Purchase', 'Initial stock'),
(5, 'IN', 800, 'Purchase', 'Initial stock'),
(1, 'OUT', 250, 'Production', 'Material issued for production'),
(2, 'OUT', 100, 'Production', 'Material issued for production');


-- PRODUCTION ORDERS
INSERT INTO production_orders
(order_number, product_id, machine_id, employee_id,
 planned_quantity, produced_quantity, start_time, status)
VALUES
('PO001', 1, 1, 4, 500, 420, '2026-10-01 08:00:00', 'In Progress'),
('PO002', 2, 2, 4, 300, 300, '2026-09-28 08:00:00', 'Completed'),
('PO003', 3, 3, 1, 200, 120, '2026-10-02 09:00:00', 'In Progress'),
('PO004', 4, 4, 1, 250, 0, '2026-10-07 08:00:00', 'Planned');


-- PRODUCTION MATERIALS
INSERT INTO production_materials
(production_id, material_id, quantity_used)
VALUES
(1, 1, 450),
(1, 2, 120),
(2, 1, 300),
(2, 4, 100),
(3, 3, 800),
(3, 4, 80),
(4, 5, 350);


-- MAINTENANCE
INSERT INTO maintenance
(machine_id, employee_id, maintenance_type, description,
 scheduled_date, completed_date, cost, status)
VALUES
(1, 2, 'Preventive', 'Routine CNC inspection and lubrication',
 '2026-09-25', '2026-09-25', 4500.00, 'Completed'),

(2, 2, 'Preventive', 'Assembly machine service',
 '2026-10-10', NULL, 3000.00, 'Scheduled'),

(3, 2, 'Corrective', 'Hydraulic system maintenance',
 '2026-10-03', NULL, 7500.00, 'In Progress'),

(4, 2, 'Preventive', 'Packaging machine inspection',
 '2026-10-15', NULL, 2500.00, 'Scheduled');


-- MAINTENANCE PARTS
INSERT INTO maintenance_parts
(maintenance_id, material_id, quantity_used, cost)
VALUES
(1, 1, 20, 3600.00),
(3, 4, 5, 2250.00),
(4, 5, 10, 1500.00);


-- QUALITY CHECKS
INSERT INTO quality_checks
(production_id, product_id, employee_id,
 quantity_inspected, quantity_passed, quantity_failed,
 quality_status, defect_description, remarks)
VALUES
(1, 1, 3, 100, 94, 6, 'Completed',
 'Minor dimensional defects', 'Within acceptable limits'),

(2, 2, 3, 100, 98, 2, 'Completed',
 'Surface defects', 'Good quality'),

(3, 3, 3, 50, 47, 3, 'Completed',
 'Wiring defects', 'Requires minor improvement');


-- USERS
INSERT INTO users
(employee_id, username, password_hash, role)
VALUES
(1, 'admin', 'factoryflow_admin', 'Admin'),
(2, 'maintenance', 'factoryflow_maintenance', 'Maintenance'),
(3, 'quality', 'factoryflow_quality', 'Quality'),
(4, 'operator', 'factoryflow_operator', 'Employee');