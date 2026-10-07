-- ============================================================
-- FactoryFlow
-- Smart Manufacturing & Maintenance Database
-- PostgreSQL Database Schema
-- ============================================================


-- ============================================================
-- 1. EMPLOYEES
-- ============================================================

CREATE TABLE employees (
    employee_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    job_role VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    hire_date DATE,
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 2. MACHINE TYPES
-- ============================================================

CREATE TABLE machine_types (
    machine_type_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);


-- ============================================================
-- 3. MACHINES
-- ============================================================

CREATE TABLE machines (
    machine_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    machine_code VARCHAR(20) UNIQUE NOT NULL,
    machine_name VARCHAR(100) NOT NULL,
    machine_type_id INTEGER NOT NULL,
    manufacturer VARCHAR(100),
    model_number VARCHAR(100),
    purchase_date DATE,
    installation_date DATE,
    status VARCHAR(30) DEFAULT 'Operational',
    location VARCHAR(100),
    operating_hours NUMERIC(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_machine_type
        FOREIGN KEY (machine_type_id)
        REFERENCES machine_types(machine_type_id)
);


-- ============================================================
-- 4. PRODUCTS
-- ============================================================

CREATE TABLE products (
    product_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_code VARCHAR(20) UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    unit_price NUMERIC(12,2) CHECK (unit_price >= 0),
    target_quantity INTEGER DEFAULT 0 CHECK (target_quantity >= 0),
    status VARCHAR(30) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 5. SUPPLIERS
-- ============================================================

CREATE TABLE suppliers (
    supplier_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_code VARCHAR(20) UNIQUE NOT NULL,
    supplier_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    address TEXT,
    city VARCHAR(100),
    status VARCHAR(30) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 6. RAW MATERIALS
-- ============================================================

CREATE TABLE raw_materials (
    material_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    material_code VARCHAR(20) UNIQUE NOT NULL,
    material_name VARCHAR(100) NOT NULL,
    supplier_id INTEGER NOT NULL,
    unit VARCHAR(30) NOT NULL,
    unit_cost NUMERIC(12,2) CHECK (unit_cost >= 0),
    reorder_level NUMERIC(12,2) DEFAULT 0 CHECK (reorder_level >= 0),
    status VARCHAR(30) DEFAULT 'Available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_material_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
);


-- ============================================================
-- 7. INVENTORY
-- ============================================================

CREATE TABLE inventory (
    inventory_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    material_id INTEGER NOT NULL,
    quantity NUMERIC(12,2) DEFAULT 0 CHECK (quantity >= 0),
    warehouse_location VARCHAR(100),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_inventory_material
        FOREIGN KEY (material_id)
        REFERENCES raw_materials(material_id),

    CONSTRAINT unique_inventory_material
        UNIQUE (material_id)
);


-- ============================================================
-- 8. INVENTORY TRANSACTIONS
-- ============================================================

CREATE TABLE inventory_transactions (
    transaction_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    material_id INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    quantity NUMERIC(12,2) NOT NULL CHECK (quantity > 0),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reference_type VARCHAR(50),
    reference_id INTEGER,
    notes TEXT,

    CONSTRAINT fk_transaction_material
        FOREIGN KEY (material_id)
        REFERENCES raw_materials(material_id),

    CONSTRAINT check_transaction_type
        CHECK (
            transaction_type IN ('IN', 'OUT', 'ADJUSTMENT')
        )
);


-- ============================================================
-- 9. PRODUCTION ORDERS
-- ============================================================

CREATE TABLE production_orders (
    production_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_number VARCHAR(30) UNIQUE NOT NULL,
    product_id INTEGER NOT NULL,
    machine_id INTEGER NOT NULL,
    employee_id INTEGER,
    planned_quantity INTEGER NOT NULL CHECK (planned_quantity > 0),
    produced_quantity INTEGER DEFAULT 0 CHECK (produced_quantity >= 0),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(30) DEFAULT 'Planned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_production_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_production_machine
        FOREIGN KEY (machine_id)
        REFERENCES machines(machine_id),

    CONSTRAINT fk_production_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);


-- ============================================================
-- 10. PRODUCTION MATERIALS
-- ============================================================

CREATE TABLE production_materials (
    production_material_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    production_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity_used NUMERIC(12,2) NOT NULL CHECK (quantity_used > 0),

    CONSTRAINT fk_pm_production
        FOREIGN KEY (production_id)
        REFERENCES production_orders(production_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_pm_material
        FOREIGN KEY (material_id)
        REFERENCES raw_materials(material_id),

    CONSTRAINT unique_production_material
        UNIQUE (production_id, material_id)
);


-- ============================================================
-- 11. MAINTENANCE
-- ============================================================

CREATE TABLE maintenance (
    maintenance_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    machine_id INTEGER NOT NULL,
    employee_id INTEGER,
    maintenance_type VARCHAR(30) NOT NULL,
    description TEXT,
    scheduled_date DATE,
    completed_date DATE,
    cost NUMERIC(12,2) DEFAULT 0 CHECK (cost >= 0),
    status VARCHAR(30) DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_maintenance_machine
        FOREIGN KEY (machine_id)
        REFERENCES machines(machine_id),

    CONSTRAINT fk_maintenance_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);


-- ============================================================
-- 12. MAINTENANCE PARTS
-- ============================================================

CREATE TABLE maintenance_parts (
    maintenance_part_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    maintenance_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity_used NUMERIC(12,2) NOT NULL CHECK (quantity_used > 0),
    cost NUMERIC(12,2) DEFAULT 0 CHECK (cost >= 0),

    CONSTRAINT fk_mp_maintenance
        FOREIGN KEY (maintenance_id)
        REFERENCES maintenance(maintenance_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_mp_material
        FOREIGN KEY (material_id)
        REFERENCES raw_materials(material_id)
);


-- ============================================================
-- 13. QUALITY CHECKS
-- ============================================================

CREATE TABLE quality_checks (
    quality_check_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    production_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    employee_id INTEGER,
    inspection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity_inspected INTEGER NOT NULL CHECK (quantity_inspected > 0),
    quantity_passed INTEGER DEFAULT 0 CHECK (quantity_passed >= 0),
    quantity_failed INTEGER DEFAULT 0 CHECK (quantity_failed >= 0),
    quality_status VARCHAR(30) DEFAULT 'Pending',
    defect_description TEXT,
    remarks TEXT,

    CONSTRAINT fk_quality_production
        FOREIGN KEY (production_id)
        REFERENCES production_orders(production_id),

    CONSTRAINT fk_quality_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_quality_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),

    CONSTRAINT check_quality_quantity
        CHECK (
            quantity_passed + quantity_failed <= quantity_inspected
        )
);


-- ============================================================
-- 14. USERS
-- ============================================================

CREATE TABLE users (
    user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id INTEGER UNIQUE,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(30) DEFAULT 'Employee',
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);


-- ============================================================
-- 15. INDEXES
-- ============================================================

CREATE INDEX idx_machines_status
    ON machines(status);

CREATE INDEX idx_machines_type
    ON machines(machine_type_id);

CREATE INDEX idx_production_product
    ON production_orders(product_id);

CREATE INDEX idx_production_machine
    ON production_orders(machine_id);

CREATE INDEX idx_production_status
    ON production_orders(status);

CREATE INDEX idx_inventory_material
    ON inventory(material_id);

CREATE INDEX idx_inventory_transactions_material
    ON inventory_transactions(material_id);

CREATE INDEX idx_inventory_transactions_date
    ON inventory_transactions(transaction_date);

CREATE INDEX idx_maintenance_machine
    ON maintenance(machine_id);

CREATE INDEX idx_maintenance_status
    ON maintenance(status);

CREATE INDEX idx_quality_production
    ON quality_checks(production_id);

CREATE INDEX idx_quality_product
    ON quality_checks(product_id);


-- ============================================================
-- END OF FACTORYFLOW SCHEMA
-- ============================================================