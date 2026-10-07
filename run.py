from flask import Flask, render_template, request, redirect, url_for, flash
from config.db import get_connection

app = Flask(__name__)
app.secret_key = "factoryflow-secret-key"


# =========================================================
# DASHBOARD
# =========================================================
@app.route("/")
def home():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM machines")
        machine_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM production_orders")
        production_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM employees")
        employee_count = cursor.fetchone()[0]

        return render_template(
            "index.html",
            machine_count=machine_count,
            product_count=product_count,
            production_count=production_count,
            employee_count=employee_count
        )

    except Exception as e:

        return f"""
        <h2>Dashboard Database Error</h2>
        <p>The Dashboard could not load.</p>
        <pre>{e}</pre>
        """

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# =========================================================
# MACHINES - LIST
# =========================================================

@app.route("/machines")
def machines():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            m.machine_id,
            m.machine_code,
            m.machine_name,
            mt.type_name,
            m.manufacturer,
            m.location,
            m.status,
            m.operating_hours
        FROM machines m
        JOIN machine_types mt
            ON m.machine_type_id = mt.machine_type_id
        ORDER BY m.machine_id
    """)

    machines_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "machines.html",
        machines=machines_data
    )


# =========================================================
# ADD MACHINE
# =========================================================

@app.route("/machines/add", methods=["GET", "POST"])
def add_machine():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        machine_code = request.form["machine_code"].strip()
        machine_name = request.form["machine_name"].strip()
        machine_type_id = request.form["machine_type_id"]
        manufacturer = request.form["manufacturer"].strip()
        location = request.form["location"].strip()
        status = request.form["status"]
        operating_hours = request.form["operating_hours"]

        try:

            cursor.execute("""
                INSERT INTO machines
                (
                    machine_code,
                    machine_name,
                    machine_type_id,
                    manufacturer,
                    location,
                    status,
                    operating_hours
                )
                VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                machine_code,
                machine_name,
                machine_type_id,
                manufacturer,
                location,
                status,
                operating_hours
            ))

            connection.commit()

            flash(
                "Machine added successfully!",
                "success"
            )

        except Exception as e:

            connection.rollback()

            flash(
                f"Error adding machine: {e}",
                "error"
            )

        finally:

            cursor.close()
            connection.close()

        return redirect(url_for("machines"))

    cursor.execute("""
        SELECT
            machine_type_id,
            type_name
        FROM machine_types
        ORDER BY type_name
    """)

    machine_types = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "machine_form.html",
        machine=None,
        machine_types=machine_types
    )


# =========================================================
# EDIT MACHINE
# =========================================================

@app.route("/machines/edit/<int:machine_id>", methods=["GET", "POST"])
def edit_machine(machine_id):

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        machine_code = request.form["machine_code"].strip()
        machine_name = request.form["machine_name"].strip()
        machine_type_id = request.form["machine_type_id"]
        manufacturer = request.form["manufacturer"].strip()
        location = request.form["location"].strip()
        status = request.form["status"]
        operating_hours = request.form["operating_hours"]

        try:

            cursor.execute("""
                UPDATE machines
                SET
                    machine_code = %s,
                    machine_name = %s,
                    machine_type_id = %s,
                    manufacturer = %s,
                    location = %s,
                    status = %s,
                    operating_hours = %s
                WHERE machine_id = %s
            """, (
                machine_code,
                machine_name,
                machine_type_id,
                manufacturer,
                location,
                status,
                operating_hours,
                machine_id
            ))

            connection.commit()

            flash(
                "Machine updated successfully!",
                "success"
            )

        except Exception as e:

            connection.rollback()

            flash(
                f"Error updating machine: {e}",
                "error"
            )

        finally:

            cursor.close()
            connection.close()

        return redirect(url_for("machines"))

    cursor.execute("""
        SELECT
            machine_code,
            machine_name,
            machine_type_id,
            manufacturer,
            location,
            status,
            operating_hours
        FROM machines
        WHERE machine_id = %s
    """, (machine_id,))

    machine = cursor.fetchone()

    cursor.execute("""
        SELECT
            machine_type_id,
            type_name
        FROM machine_types
        ORDER BY type_name
    """)

    machine_types = cursor.fetchall()

    cursor.close()
    connection.close()

    if machine is None:

        flash(
            "Machine not found.",
            "error"
        )

        return redirect(url_for("machines"))

    return render_template(
        "machine_form.html",
        machine=machine,
        machine_types=machine_types
    )


# =========================================================
# DELETE MACHINE
# =========================================================

@app.route("/machines/delete/<int:machine_id>", methods=["POST"])
def delete_machine(machine_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM machines
            WHERE machine_id = %s
        """, (machine_id,))

        connection.commit()

        flash(
            "Machine deleted successfully!",
            "success"
        )

    except Exception:

        connection.rollback()

        flash(
            "Machine cannot be deleted because it may "
            "be used in another table.",
            "error"
        )

    finally:

        cursor.close()
        connection.close()

    return redirect(url_for("machines"))


# =========================================================
# PRODUCTS - LIST
# =========================================================

@app.route("/products")
def products():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product_code,
            product_name,
            description,
            category,
            unit_price,
            target_quantity,
            status,
            created_at
        FROM products
        ORDER BY product_id
    """)

    products_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "products.html",
        products=products_data
    )


# =========================================================
# ADD PRODUCT
# =========================================================

@app.route("/products/add", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        product_code = request.form["product_code"].strip()
        product_name = request.form["product_name"].strip()
        description = request.form["description"].strip()
        category = request.form["category"].strip()
        unit_price = request.form["unit_price"]
        target_quantity = request.form["target_quantity"]
        status = request.form["status"]

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO products
                (
                    product_code,
                    product_name,
                    description,
                    category,
                    unit_price,
                    target_quantity,
                    status
                )
                VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                product_code,
                product_name,
                description,
                category,
                unit_price,
                target_quantity,
                status
            ))

            connection.commit()

            flash(
                "Product added successfully!",
                "success"
            )

        except Exception as e:

            connection.rollback()

            flash(
                f"Error adding product: {e}",
                "error"
            )

        finally:

            cursor.close()
            connection.close()

        return redirect(url_for("products"))

    return render_template(
        "product_form.html",
        product=None
    )


# =========================================================
# EDIT PRODUCT
# =========================================================

@app.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        product_code = request.form["product_code"].strip()
        product_name = request.form["product_name"].strip()
        description = request.form["description"].strip()
        category = request.form["category"].strip()
        unit_price = request.form["unit_price"]
        target_quantity = request.form["target_quantity"]
        status = request.form["status"]

        try:

            cursor.execute("""
                UPDATE products
                SET
                    product_code = %s,
                    product_name = %s,
                    description = %s,
                    category = %s,
                    unit_price = %s,
                    target_quantity = %s,
                    status = %s
                WHERE product_id = %s
            """, (
                product_code,
                product_name,
                description,
                category,
                unit_price,
                target_quantity,
                status,
                product_id
            ))

            connection.commit()

            flash(
                "Product updated successfully!",
                "success"
            )

        except Exception as e:

            connection.rollback()

            flash(
                f"Error updating product: {e}",
                "error"
            )

        finally:

            cursor.close()
            connection.close()

        return redirect(url_for("products"))

    cursor.execute("""
        SELECT
            product_id,
            product_code,
            product_name,
            description,
            category,
            unit_price,
            target_quantity,
            status
        FROM products
        WHERE product_id = %s
    """, (product_id,))

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    if product is None:

        flash(
            "Product not found.",
            "error"
        )

        return redirect(url_for("products"))

    return render_template(
        "product_form.html",
        product=product
    )


# =========================================================
# DELETE PRODUCT
# =========================================================

@app.route("/products/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM products
            WHERE product_id = %s
        """, (product_id,))

        connection.commit()

        flash(
            "Product deleted successfully!",
            "success"
        )

    except Exception:

        connection.rollback()

        flash(
            "Product cannot be deleted because it may "
            "be used in another table.",
            "error"
        )

    finally:

        cursor.close()
        connection.close()

    return redirect(url_for("products"))


# =========================================================
# PRODUCTION - LIST
# =========================================================

@app.route("/production")
def production():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                po.production_id,
                po.order_number,
                p.product_name,
                m.machine_name,
                e.name,
                po.planned_quantity,
                po.produced_quantity,
                po.status,
                po.created_at
            FROM production_orders po
            JOIN products p
                ON po.product_id = p.product_id
            JOIN machines m
                ON po.machine_id = m.machine_id
            JOIN employees e
                ON po.employee_id = e.employee_id
            ORDER BY po.production_id DESC
        """)

        production_orders = cursor.fetchall()

        return render_template(
            "production.html",
            production_orders=production_orders
        )

    except Exception as e:

        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Production Error</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 40px;
            background: #f5f7fa;
        }}

        .error {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            max-width: 900px;
            margin: auto;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        h2 {{
            color: #c0392b;
        }}

        pre {{
            background: #f1f1f1;
            padding: 15px;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
    </style>
</head>

<body>

<div class="error">

    <h2>Production Database Error</h2>

    <p>The Production page could not load.</p>

    <pre>{e}</pre>

</div>

</body>
</html>
"""

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# ADD PRODUCTION ORDER
# =========================================================

@app.route("/production/add", methods=["GET", "POST"])
def add_production():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        if request.method == "POST":

            order_number = request.form["order_number"].strip()
            product_id = request.form["product_id"]
            machine_id = request.form["machine_id"]
            employee_id = request.form["employee_id"]
            planned_quantity = request.form["planned_quantity"]
            produced_quantity = request.form["produced_quantity"]
            start_time = request.form["start_time"] or None
            end_time = request.form["end_time"] or None
            status = request.form["status"]

            try:

                cursor.execute("""
                    INSERT INTO production_orders
                    (
                        order_number,
                        product_id,
                        machine_id,
                        employee_id,
                        planned_quantity,
                        produced_quantity,
                        start_time,
                        end_time,
                        status
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    )
                """, (
                    order_number,
                    product_id,
                    machine_id,
                    employee_id,
                    planned_quantity,
                    produced_quantity,
                    start_time,
                    end_time,
                    status
                ))

                connection.commit()

                flash(
                    "Production order added successfully!",
                    "success"
                )

                return redirect(
                    url_for("production")
                )

            except Exception as e:

                connection.rollback()

                flash(
                    f"Error adding production order: {e}",
                    "error"
                )

        cursor.execute("""
            SELECT
                product_id,
                product_code,
                product_name
            FROM products
            ORDER BY product_name
        """)

        products = cursor.fetchall()

        cursor.execute("""
            SELECT
                machine_id,
                machine_code,
                machine_name
            FROM machines
            ORDER BY machine_name
        """)

        machines = cursor.fetchall()

        cursor.execute("""
            SELECT
                employee_id,
                employee_code,
                name
            FROM employees
            ORDER BY name
        """)

        employees = cursor.fetchall()

        return render_template(
            "production_form.html",
            production_order=None,
            products=products,
            machines=machines,
            employees=employees
        )

    except Exception as e:

        return f"""
<h2>Production Form Error</h2>
<pre>{e}</pre>
"""

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# EDIT PRODUCTION ORDER
# =========================================================

@app.route(
    "/production/edit/<int:production_id>",
    methods=["GET", "POST"]
)
def edit_production(production_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        if request.method == "POST":

            order_number = request.form["order_number"].strip()
            product_id = request.form["product_id"]
            machine_id = request.form["machine_id"]
            employee_id = request.form["employee_id"]
            planned_quantity = request.form["planned_quantity"]
            produced_quantity = request.form["produced_quantity"]
            start_time = request.form["start_time"] or None
            end_time = request.form["end_time"] or None
            status = request.form["status"]

            cursor.execute("""
                UPDATE production_orders
                SET
                    order_number = %s,
                    product_id = %s,
                    machine_id = %s,
                    employee_id = %s,
                    planned_quantity = %s,
                    produced_quantity = %s,
                    start_time = %s,
                    end_time = %s,
                    status = %s
                WHERE production_id = %s
            """, (
                order_number,
                product_id,
                machine_id,
                employee_id,
                planned_quantity,
                produced_quantity,
                start_time,
                end_time,
                status,
                production_id
            ))

            connection.commit()

            flash(
                "Production order updated successfully!",
                "success"
            )

            return redirect(
                url_for("production")
            )

        cursor.execute("""
            SELECT
                production_id,
                order_number,
                product_id,
                machine_id,
                employee_id,
                planned_quantity,
                produced_quantity,
                start_time,
                end_time,
                status
            FROM production_orders
            WHERE production_id = %s
        """, (production_id,))

        production_order = cursor.fetchone()

        if production_order is None:

            flash(
                "Production order not found.",
                "error"
            )

            return redirect(
                url_for("production")
            )

        cursor.execute("""
            SELECT
                product_id,
                product_code,
                product_name
            FROM products
            ORDER BY product_name
        """)

        products = cursor.fetchall()

        cursor.execute("""
            SELECT
                machine_id,
                machine_code,
                machine_name
            FROM machines
            ORDER BY machine_name
        """)

        machines = cursor.fetchall()

        cursor.execute("""
            SELECT
                employee_id,
                employee_code,
                name
            FROM employees
            ORDER BY name
        """)

        employees = cursor.fetchall()

        return render_template(
            "production_form.html",
            production_order=production_order,
            products=products,
            machines=machines,
            employees=employees
        )

    except Exception as e:

        return f"""
<h2>Production Edit Error</h2>
<pre>{e}</pre>
"""

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# DELETE PRODUCTION ORDER
# =========================================================

@app.route(
    "/production/delete/<int:production_id>",
    methods=["POST"]
)
def delete_production(production_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM production_orders
            WHERE production_id = %s
        """, (production_id,))

        connection.commit()

        flash(
            "Production order deleted successfully!",
            "success"
        )

    except Exception:

        connection.rollback()

        flash(
            "Production order cannot be deleted because "
            "it may be referenced by another table.",
            "error"
        )

    finally:

        cursor.close()
        connection.close()

    return redirect(url_for("production"))


# =========================================================
# INVENTORY - LIST
# =========================================================
@app.route("/inventory")
def inventory():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                i.material_id,
                rm.material_code,
                rm.material_name,
                i.quantity,
                i.warehouse_location,
                i.last_updated
            FROM inventory i
            JOIN raw_materials rm
                ON i.material_id = rm.material_id
            ORDER BY i.material_id
        """)

        inventory_data = cursor.fetchall()

        return render_template(
            "inventory.html",
            inventory=inventory_data
        )

    except Exception as e:
        return f"""
        <h2>Inventory Database Error</h2>
        <p>The Inventory page could not load.</p>
        <pre>{e}</pre>
        """

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
     
# =========================================================
# INVENTORY - STOCK TRANSACTION
# =========================================================

@app.route(
    "/inventory/transaction",
    methods=["GET", "POST"]
)
def inventory_transaction():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        if request.method == "POST":

            material_id = request.form["material_id"]

            transaction_type = request.form[
                "transaction_type"
            ]

            quantity = float(
                request.form["quantity"]
            )

            warehouse_location = request.form[
                "warehouse_location"
            ].strip()

            notes = request.form[
                "notes"
            ].strip()

            cursor.execute("""
                SELECT quantity
                FROM inventory
                WHERE material_id = %s
            """, (material_id,))

            current_stock = cursor.fetchone()

            if current_stock is None:

                if transaction_type == "Stock In":

                    current_quantity = 0

                    cursor.execute("""
                        INSERT INTO inventory
                        (
                            material_id,
                            quantity,
                            warehouse_location
                        )
                        VALUES
                        (
                            %s, %s, %s
                        )
                    """, (
                        material_id,
                        0,
                        warehouse_location
                    ))

                else:

                    flash(
                        "Inventory record does not exist.",
                        "error"
                    )

                    return redirect(
                        url_for(
                            "inventory_transaction"
                        )
                    )

            else:

                current_quantity = float(
                    current_stock[0]
                )

            if transaction_type == "Stock In":

                new_quantity = (
                    current_quantity + quantity
                )

            else:

                new_quantity = (
                    current_quantity - quantity
                )

                if new_quantity < 0:

                    flash(
                        "Stock out quantity cannot exceed "
                        "available stock.",
                        "error"
                    )

                    return redirect(
                        url_for(
                            "inventory_transaction"
                        )
                    )

            cursor.execute("""
                UPDATE inventory
                SET
                    quantity = %s,
                    warehouse_location = %s,
                    last_updated = CURRENT_TIMESTAMP
                WHERE material_id = %s
            """, (
                new_quantity,
                warehouse_location,
                material_id
            ))

            cursor.execute("""
                INSERT INTO inventory_transactions
                (
                    material_id,
                    transaction_type,
                    quantity,
                    reference_type,
                    notes
                )
                VALUES
                (
                    %s, %s, %s, %s, %s
                )
            """, (
                material_id,
                transaction_type,
                quantity,
                "Manual",
                notes
            ))

            connection.commit()

            flash(
                "Inventory transaction recorded successfully!",
                "success"
            )

            return redirect(
                url_for("inventory")
            )

        cursor.execute("""
            SELECT
                material_id,
                material_code,
                material_name,
                unit
            FROM raw_materials
            ORDER BY material_name
        """)

        materials = cursor.fetchall()

        return render_template(
            "inventory_transaction.html",
            materials=materials
        )

    except Exception as e:

        if connection:
            connection.rollback()

        return f"""
<h2>Inventory Transaction Error</h2>
<pre>{e}</pre>
"""

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# INVENTORY - TRANSACTION HISTORY
# =========================================================

@app.route("/inventory/transactions")
def inventory_transactions():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                t.transaction_id,
                rm.material_code,
                rm.material_name,
                t.transaction_type,
                t.quantity,
                t.transaction_date,
                t.reference_type,
                t.notes
            FROM inventory_transactions t
            JOIN raw_materials rm
                ON t.material_id = rm.material_id
            ORDER BY t.transaction_date DESC
        """)

        transactions = cursor.fetchall()

        return render_template(
            "inventory_transactions.html",
            transactions=transactions
        )

    except Exception as e:

        return f"""
<h2>Inventory Transactions Error</h2>
<pre>{e}</pre>
"""

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# EMPLOYEES - LIST
# =========================================================

@app.route("/employees")
def employees():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                employee_id,
                employee_code,
                name,
                department,
                job_role,
                phone,
                email,
                hire_date,
                status
            FROM employees
            ORDER BY employee_id
        """)

        employees_data = cursor.fetchall()

        return render_template(
            "employees.html",
            employees=employees_data
        )

    except Exception as e:

        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Employees Error</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 40px;
            background: #f5f7fa;
        }}

        .error {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            max-width: 900px;
            margin: auto;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        h2 {{
            color: #c0392b;
        }}

        pre {{
            background: #f1f1f1;
            padding: 15px;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
    </style>

</head>

<body>

<div class="error">

    <h2>Employees Database Error</h2>

    <p>The Employees page could not load.</p>

    <pre>{e}</pre>

</div>

</body>
</html>
"""

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# ADD EMPLOYEE
# =========================================================

@app.route(
    "/employees/add",
    methods=["GET", "POST"]
)
def add_employee():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        if request.method == "POST":

            employee_code = request.form[
                "employee_code"
            ].strip()

            name = request.form[
                "name"
            ].strip()

            department = request.form[
                "department"
            ].strip()

            job_role = request.form[
                "job_role"
            ].strip()

            phone = request.form[
                "phone"
            ].strip()

            email = request.form[
                "email"
            ].strip()

            hire_date = request.form[
                "hire_date"
            ]

            status = request.form[
                "status"
            ]

            cursor.execute("""
                INSERT INTO employees
                (
                    employee_code,
                    name,
                    department,
                    job_role,
                    phone,
                    email,
                    hire_date,
                    status
                )
                VALUES
                (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
            """, (
                employee_code,
                name,
                department,
                job_role,
                phone,
                email,
                hire_date,
                status
            ))

            connection.commit()

            flash(
                "Employee added successfully!",
                "success"
            )

            return redirect(
                url_for("employees")
            )

        return render_template(
            "employee_form.html",
            employee=None
        )

    except Exception as e:

        if connection:
            connection.rollback()

        return f"""
<h2>Employee Form Error</h2>
<pre>{e}</pre>
"""

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# EDIT EMPLOYEE
# =========================================================

@app.route(
    "/employees/edit/<int:employee_id>",
    methods=["GET", "POST"]
)
def edit_employee(employee_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        if request.method == "POST":

            employee_code = request.form[
                "employee_code"
            ].strip()

            name = request.form[
                "name"
            ].strip()

            department = request.form[
                "department"
            ].strip()

            job_role = request.form[
                "job_role"
            ].strip()

            phone = request.form[
                "phone"
            ].strip()

            email = request.form[
                "email"
            ].strip()

            hire_date = request.form[
                "hire_date"
            ]

            status = request.form[
                "status"
            ]

            cursor.execute("""
                UPDATE employees
                SET
                    employee_code = %s,
                    name = %s,
                    department = %s,
                    job_role = %s,
                    phone = %s,
                    email = %s,
                    hire_date = %s,
                    status = %s
                WHERE employee_id = %s
            """, (
                employee_code,
                name,
                department,
                job_role,
                phone,
                email,
                hire_date,
                status,
                employee_id
            ))

            connection.commit()

            flash(
                "Employee updated successfully!",
                "success"
            )

            return redirect(
                url_for("employees")
            )

        cursor.execute("""
            SELECT
                employee_id,
                employee_code,
                name,
                department,
                job_role,
                phone,
                email,
                hire_date,
                status
            FROM employees
            WHERE employee_id = %s
        """, (employee_id,))

        employee = cursor.fetchone()

        if employee is None:

            flash(
                "Employee not found.",
                "error"
            )

            return redirect(
                url_for("employees")
            )

        return render_template(
            "employee_form.html",
            employee=employee
        )

    except Exception as e:

        if connection:
            connection.rollback()

        return f"""
<h2>Employee Edit Error</h2>
<pre>{e}</pre>
"""

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# DELETE EMPLOYEE
# =========================================================

@app.route(
    "/employees/delete/<int:employee_id>",
    methods=["POST"]
)
def delete_employee(employee_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM employees
            WHERE employee_id = %s
        """, (employee_id,))

        connection.commit()

        flash(
            "Employee deleted successfully!",
            "success"
        )

    except Exception:

        connection.rollback()

        flash(
            "Employee cannot be deleted because it is "
            "being used by another table.",
            "error"
        )

    finally:

        cursor.close()
        connection.close()

    return redirect(
        url_for("employees")
    )

@app.route("/reports")
def reports():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # Summary
        cursor.execute("""
            SELECT COALESCE(SUM(produced_quantity), 0)
            FROM production_orders
        """)
        total_produced = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(planned_quantity), 0)
            FROM production_orders
        """)
        total_planned = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM products
        """)
        product_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM employees
        """)
        employee_count = cursor.fetchone()[0]


        # Production report
        cursor.execute("""
            SELECT
                po.order_number,
                p.product_name,
                m.machine_name,
                e.name,
                po.planned_quantity,
                po.produced_quantity,
                po.status
            FROM production_orders po

            JOIN products p
                ON po.product_id = p.product_id

            JOIN machines m
                ON po.machine_id = m.machine_id

            JOIN employees e
                ON po.employee_id = e.employee_id

            ORDER BY po.production_id DESC
        """)

        production_report = cursor.fetchall()


        # Inventory report
        cursor.execute("""
            SELECT
                rm.material_code,
                rm.material_name,
                i.quantity,
                i.warehouse_location
            FROM inventory i

            JOIN raw_materials rm
                ON i.material_id = rm.material_id

            ORDER BY rm.material_id
        """)

        inventory_report = cursor.fetchall()


        return render_template(
            "reports.html",
            total_produced=total_produced,
            total_planned=total_planned,
            product_count=product_count,
            employee_count=employee_count,
            production_report=production_report,
            inventory_report=inventory_report
        )


    except Exception as e:

        return f"""
        <h2>Reports Database Error</h2>
        <p>The Reports page could not load.</p>
        <pre>{e}</pre>
        """


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()
# =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )