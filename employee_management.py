import click
import re
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from tabulate import tabulate

# Base model for SQLAlchemy
Base = declarative_base()

# SQLAlchemy ORM models
class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    salary = Column(Float, nullable=False)
    department = relationship("Department")
    role = relationship("Role")

# Application factory for initializing the app and database
def create_app(db_url='sqlite:///employee_management.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session  # Return the session factory

# Helper functions to fetch foreign keys by name
def get_department_id_by_name(session, department_name):
    """Get the department ID by its name."""
    department = session.query(Department).filter_by(name=department_name).first()
    return department.id if department else None

def get_role_id_by_name(session, role_title):
    """Get the role ID by its title."""
    role = session.query(Role).filter_by(title=role_title).first()
    return role.id if role else None

# Helper functions to retrieve all department names and role titles
def get_all_department_names(session):
    return [dept.name for dept in session.query(Department).all()]

def get_all_role_titles(session):
    return [role.title for role in session.query(Role).all()]

# Validation functions
def validate_name(name):
    """Validates that the name contains only alphabetic characters and spaces."""
    if not re.match(r"^[a-zA-Z\s]+$", name):
        raise ValueError("Name must contain only alphabetic characters and spaces.")
    return name.strip()

def validate_salary(salary):
    """Validates that the salary is a positive float."""
    try:
        salary = float(salary)
        if salary <= 0:
            raise ValueError("Salary must be a positive number.")
    except ValueError:
        raise ValueError("Invalid salary. Please enter a valid number.")
    return salary

# Main numbered menu
@click.command()
@click.pass_context
def menu(ctx):
    """Employee Management System Main Menu"""
    session = ctx.obj['session']

    while True:
        click.echo("\n--- Employee Management System ---")
        click.echo("1. Manage Departments")
        click.echo("2. Manage Roles")
        click.echo("3. Manage Employees")
        click.echo("4. View Departments")
        click.echo("5. View Roles")
        click.echo("6. View Employees")
        click.echo("7. Exit")

        choice = click.prompt("\nEnter a choice", type=int)

        try:
            if choice == 1:
                manage_departments(session)
            elif choice == 2:
                manage_roles(session)
            elif choice == 3:
                manage_employees(session)
            elif choice == 4:
                view_departments(session)
            elif choice == 5:
                view_roles(session)
            elif choice == 6:
                view_employees(session)
            elif choice == 7:
                click.echo("Exiting...")
                break
            else:
                click.echo("Invalid choice. Please try again.")
        except ValueError as e:
            click.echo(f"Error: {e}")

# Nested menu for managing departments
def manage_departments(session):
    """Manage Departments Menu"""
    while True:
        click.echo("\n--- Manage Departments ---")
        click.echo("1. Add Department")
        click.echo("2. Update Department")
        click.echo("3. Delete Department")
        click.echo("4. Back to Main Menu")

        choice = click.prompt("\nEnter a choice", type=int)

        if choice == 1:
            add_department(session)
        elif choice == 2:
            update_department(session)
        elif choice == 3:
            delete_department(session)
        elif choice == 4:
            break
        else:
            click.echo("Invalid choice. Please try again.")

# Nested menu for managing roles
def manage_roles(session):
    """Manage Roles Menu"""
    while True:
        click.echo("\n--- Manage Roles ---")
        click.echo("1. Add Role")
        click.echo("2. Update Role")
        click.echo("3. Delete Role")
        click.echo("4. Back to Main Menu")

        choice = click.prompt("\nEnter a choice", type=int)

        if choice == 1:
            add_role(session)
        elif choice == 2:
            update_role(session)
        elif choice == 3:
            delete_role(session)
        elif choice == 4:
            break
        else:
            click.echo("Invalid choice. Please try again.")

# Nested menu for managing employees
def manage_employees(session):
    """Manage Employees Menu"""
    while True:
        click.echo("\n--- Manage Employees ---")
        click.echo("1. Add Employee")
        click.echo("2. Update Employee")
        click.echo("3. Delete Employee")
        click.echo("4. Back to Main Menu")

        choice = click.prompt("\nEnter a choice", type=int)

        if choice == 1:
            add_employee(session)
        elif choice == 2:
            update_employee(session)
        elif choice == 3:
            delete_employee(session)
        elif choice == 4:
            break
        else:
            click.echo("Invalid choice. Please try again.")

# View all departments
def view_departments(session):
    """View all departments"""
    departments = session.query(Department).all()
    if departments:
        click.echo(tabulate([(dept.id, dept.name) for dept in departments], headers=['ID', 'Name']))
    else:
        click.echo("No departments found.")

    while True:
        click.echo("\n--- View Departments ---")
        click.echo("1. Back to Main Menu")
        click.echo("2. View Roles in a Department")
        click.echo("3. View Employees in a Department")

        choice = click.prompt("\nEnter a choice", type=int)

        if choice == 1:
            break
        elif choice == 2:
            view_roles_in_department(session)
        elif choice == 3:
            view_employees_in_department(session)
        else:
            click.echo("Invalid choice. Please try again.")

def view_roles_in_department(session):
    """View roles in a selected department"""
    department_names = get_all_department_names(session)
    if not department_names:
        click.echo("No departments found.")
        return

    click.echo("\n--- Departments ---")
    for i, name in enumerate(department_names, start=1):
        click.echo(f"{i}. {name}")

    dept_index = click.prompt("Select a department by number", type=int) - 1
    if 0 <= dept_index < len(department_names):
        selected_department = department_names[dept_index]
        department_id = get_department_id_by_name(session, selected_department)

        roles_in_department = session.query(Employee.role).filter_by(department_id=department_id).all()
        if roles_in_department:
            click.echo(f"\nRoles in {selected_department}:")
            click.echo(tabulate([(role.id, role.title) for role in roles_in_department], headers=['ID', 'Title']))
        else:
            click.echo(f"No roles found in {selected_department}.")
    else:
        click.echo("Invalid department selection.")

# View all roles
def view_roles(session):
    """View all roles"""
    roles = session.query(Role).all()
    if roles:
        click.echo(tabulate([(role.id, role.title) for role in roles], headers=['ID', 'Title']))
    else:
        click.echo("No roles found.")

    while True:
        click.echo("\n--- View Roles ---")
        click.echo("1. Back to Main Menu")
        click.echo("2. View Employees with a Role")

        choice = click.prompt("\nEnter a choice", type=int)

        if choice == 1:
            break
        elif choice == 2:
            view_employees_with_role(session)
        else:
            click.echo("Invalid choice. Please try again.")

# View all employees
def view_employees(session):
    """View all employees"""
    employees = session.query(Employee).all()
    if employees:
        click.echo(tabulate([(emp.id, emp.name, emp.department.name, emp.role.title, emp.salary) for emp in employees], headers=['ID', 'Name', 'Department', 'Role', 'Salary']))
    else:
        click.echo("No employees found.")

    while True:
        click.echo("\n--- View Employees ---")
        click.echo("1. Back to Main Menu")
        click.echo("2. View Employee Details")

        choice = click.prompt("\nEnter a choice", type=int)

        if choice == 1:
            break
        elif choice == 2:
            view_employee_details(session)
        else:
            click.echo("Invalid choice. Please try again.")

# CRUD for Department
def add_department(session):
    """Add a new department"""
    name = click.prompt("Enter department name", type=str)
    new_department = Department(name=name)
    session.add(new_department)
    session.commit()
    click.echo(f"Department '{name}' added successfully.")

def update_department(session):
    """Update an existing department"""
    departments = session.query(Department).all()
    if not departments:
        click.echo("No departments available for updating.")
        return

    click.echo("\n--- Update Department ---")
    for i, dept in enumerate(departments, start=1):
        click.echo(f"{i}. {dept.name}")

    dept_index = click.prompt("Select department to update by number", type=int) - 1
    if 0 <= dept_index < len(departments):
        new_name = click.prompt("Enter new department name", type=str)
        departments[dept_index].name = new_name
        session.commit()
        click.echo(f"Department updated to '{new_name}'.")
    else:
        click.echo("Invalid selection.")

def delete_department(session):
    """Delete a department"""
    departments = session.query(Department).all()
    if not departments:
        click.echo("No departments available for deletion.")
        return

    click.echo("\n--- Delete Department ---")
    for i, dept in enumerate(departments, start=1):
        click.echo(f"{i}. {dept.name}")

    dept_index = click.prompt("Select department to delete by number", type=int) - 1
    if 0 <= dept_index < len(departments):
        session.delete(departments[dept_index])
        session.commit()
        click.echo(f"Department '{departments[dept_index].name}' deleted successfully.")
    else:
        click.echo("Invalid selection.")

# CRUD for Role
def add_role(session):
    """Add a new role"""
    title = click.prompt("Enter role title", type=str)
    new_role = Role(title=title)
    session.add(new_role)
    session.commit()
    click.echo(f"Role '{title}' added successfully.")

def update_role(session):
    """Update an existing role"""
    roles = session.query(Role).all()
    if not roles:
        click.echo("No roles available for updating.")
        return

    click.echo("\n--- Update Role ---")
    for i, role in enumerate(roles, start=1):
        click.echo(f"{i}. {role.title}")

    role_index = click.prompt("Select role to update by number", type=int) - 1
    if 0 <= role_index < len(roles):
        new_title = click.prompt("Enter new role title", type=str)
        roles[role_index].title = new_title
        session.commit()
        click.echo(f"Role updated to '{new_title}'.")
    else:
        click.echo("Invalid selection.")

def delete_role(session):
    """Delete a role"""
    roles = session.query(Role).all()
    if not roles:
        click.echo("No roles available for deletion.")
        return

    click.echo("\n--- Delete Role ---")
    for i, role in enumerate(roles, start=1):
        click.echo(f"{i}. {role.title}")

    role_index = click.prompt("Select role to delete by number", type=int) - 1
    if 0 <= role_index < len(roles):
        session.delete(roles[role_index])
        session.commit()
        click.echo(f"Role '{roles[role_index].title}' deleted successfully.")
    else:
        click.echo("Invalid selection.")

# CRUD for Employee
def add_employee(session):
    """Add a new employee"""
    name = click.prompt("Enter employee name", type=str)
    department_names = get_all_department_names(session)
    if not department_names:
        click.echo("No departments available to assign.")
        return
    department_name = click.prompt("Select department", type=click.Choice(department_names))
    role_titles = get_all_role_titles(session)
    if not role_titles:
        click.echo("No roles available to assign.")
        return
    role_title = click.prompt("Select role", type=click.Choice(role_titles))
    salary = validate_salary(click.prompt("Enter salary"))

    new_employee = Employee(name=validate_name(name), salary=salary,
                            department_id=get_department_id_by_name(session, department_name),
                            role_id=get_role_id_by_name(session, role_title))
    session.add(new_employee)
    session.commit()
    click.echo(f"Employee '{name}' added successfully.")

def update_employee(session):
    """Update an existing employee"""
    employees = session.query(Employee).all()
    if not employees:
        click.echo("No employees available for updating.")
        return

    click.echo("\n--- Update Employee ---")
    for i, emp in enumerate(employees, start=1):
        click.echo(f"{i}. {emp.name}")

    emp_index = click.prompt("Select employee to update by number", type=int) - 1
    if 0 <= emp_index < len(employees):
        name = click.prompt("Enter new employee name", type=str)
        department_names = get_all_department_names(session)
        department_name = click.prompt("Select new department", type=click.Choice(department_names))
        role_titles = get_all_role_titles(session)
        role_title = click.prompt("Select new role", type=click.Choice(role_titles))
        salary = validate_salary(click.prompt("Enter new salary"))

        employees[emp_index].name = validate_name(name)
        employees[emp_index].salary = salary
        employees[emp_index].department_id = get_department_id_by_name(session, department_name)
        employees[emp_index].role_id = get_role_id_by_name(session, role_title)
        session.commit()
        click.echo(f"Employee updated to '{name}'.")
    else:
        click.echo("Invalid selection.")

def delete_employee(session):
    """Delete an employee"""
    employees = session.query(Employee).all()
    if not employees:
        click.echo("No employees available for deletion.")
        return

    click.echo("\n--- Delete Employee ---")
    for i, emp in enumerate(employees, start=1):
        click.echo(f"{i}. {emp.name}")

    emp_index = click.prompt("Select employee to delete by number", type=int) - 1
    if 0 <= emp_index < len(employees):
        session.delete(employees[emp_index])
        session.commit()
        click.echo(f"Employee '{employees[emp_index].name}' deleted successfully.")
    else:
        click.echo("Invalid selection.")

def view_employee_details(session):
    """View details of a selected employee"""
    employees = session.query(Employee).all()
    if not employees:
        click.echo("No employees available.")
        return

    click.echo("\n--- View Employee Details ---")
    for i, emp in enumerate(employees, start=1):
        click.echo(f"{i}. {emp.name}")

    emp_index = click.prompt("Select employee to view details by number", type=int) - 1
    if 0 <= emp_index < len(employees):
        emp = employees[emp_index]
        click.echo(f"Name: {emp.name}")
        click.echo(f"Department: {emp.department.name}")
        click.echo(f"Role: {emp.role.title}")
        click.echo(f"Salary: {emp.salary}")
    else:
        click.echo("Invalid selection.")

# Entry point for the application
if __name__ == '__main__':
    app = create_app()
    with app() as session:
        click.echo("Welcome to the Employee Management System!")
        menu(obj={'session': session})
