import click
from sqlalchemy.orm import sessionmaker
from .models import Base, Department, Role, Employee
from .services import (
    add_department, update_department, delete_department, get_all_departments,
    add_role, update_role, delete_role, get_all_roles,
    add_employee, update_employee, delete_employee, get_all_employees
)
from .utils import validate_name, validate_salary

@click.group()
@click.pass_context
def cli(ctx):
    """Employee Management System CLI"""
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///employee_management.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    ctx.obj = {'session': Session()}

@cli.command()
@click.pass_context
def main_menu(ctx):
    """Main Menu"""
    while True:
        click.echo("\n--- Main Menu ---")
        click.echo("1. Manage Departments")
        click.echo("2. Manage Roles")
        click.echo("3. Manage Employees")
        click.echo("4. Exit")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            manage_departments(ctx)
        elif choice == 2:
            manage_roles(ctx)
        elif choice == 3:
            manage_employees(ctx)
        elif choice == 4:
            click.echo("Exiting the application.")
            break
        else:
            click.echo("Invalid choice. Please try again.")

def manage_departments(ctx):
    """Manage Departments"""
    session = ctx.obj['session']
    while True:
        click.echo("\n--- Manage Departments ---")
        click.echo("1. Add Department")
        click.echo("2. Update Department")
        click.echo("3. Delete Department")
        click.echo("4. View Departments")
        click.echo("5. Back to Main Menu")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            name = click.prompt("Enter department name", type=str)
            add_department(session, name)
            click.echo("Department added successfully.")
        elif choice == 2:
            departments = [d.name for d in get_all_departments(session)]
            old_name = click.prompt("Select department to update", type=click.Choice(departments))
            new_name = click.prompt("Enter new department name", type=str)
            update_department(session, old_name, new_name)
            click.echo("Department updated successfully.")
        elif choice == 3:
            departments = [d.name for d in get_all_departments(session)]
            name = click.prompt("Select department to delete", type=click.Choice(departments))
            delete_department(session, name)
            click.echo("Department deleted successfully.")
        elif choice == 4:
            departments = get_all_departments(session)
            click.echo("\n--- Departments ---")
            for dept in departments:
                click.echo(f"Department: {dept.name}")
        elif choice == 5:
            break
        else:
            click.echo("Invalid choice. Please try again.")

def manage_roles(ctx):
    """Manage Roles"""
    session = ctx.obj['session']
    while True:
        click.echo("\n--- Manage Roles ---")
        click.echo("1. Add Role")
        click.echo("2. Update Role")
        click.echo("3. Delete Role")
        click.echo("4. View Roles")
        click.echo("5. Back to Main Menu")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            title = click.prompt("Enter role title", type=str)
            add_role(session, title)
            click.echo("Role added successfully.")
        elif choice == 2:
            roles = [r.title for r in get_all_roles(session)]
            old_title = click.prompt("Select role to update", type=click.Choice(roles))
            new_title = click.prompt("Enter new role title", type=str)
            update_role(session, old_title, new_title)
            click.echo("Role updated successfully.")
        elif choice == 3:
            roles = [r.title for r in get_all_roles(session)]
            title = click.prompt("Select role to delete", type=click.Choice(roles))
            delete_role(session, title)
            click.echo("Role deleted successfully.")
        elif choice == 4:
            roles = get_all_roles(session)
            click.echo("\n--- Roles ---")
            for role in roles:
                click.echo(f"Role: {role.title}")
        elif choice == 5:
            break
        else:
            click.echo("Invalid choice. Please try again.")

def manage_employees(ctx):
    """Manage Employees"""
    session = ctx.obj['session']
    while True:
        click.echo("\n--- Manage Employees ---")
        click.echo("1. Add Employee")
        click.echo("2. Update Employee")
        click.echo("3. Delete Employee")
        click.echo("4. View Employees")
        click.echo("5. Back to Main Menu")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            name = validate_name(click.prompt("Enter employee name", type=str))
            departments = [d.name for d in get_all_departments(session)]
            department_name = click.prompt("Select department", type=click.Choice(departments))
            roles = [r.title for r in get_all_roles(session)]
            role_title = click.prompt("Select role", type=click.Choice(roles))
            salary = validate_salary(click.prompt("Enter salary", type=float))
            add_employee(session, name, department_name, role_title, salary)
            click.echo("Employee added successfully.")
        elif choice == 2:
            employees = [e.name for e in get_all_employees(session)]
            old_name = click.prompt("Select employee to update", type=click.Choice(employees))
            new_name = validate_name(click.prompt("Enter new employee name", type=str))
            departments = [d.name for d in get_all_departments(session)]
            department_name = click.prompt("Select new department", type=click.Choice(departments))
            roles = [r.title for r in get_all_roles(session)]
            role_title = click.prompt("Select new role", type=click.Choice(roles))
            salary = validate_salary(click.prompt("Enter new salary", type=float))
            update_employee(session, old_name, new_name, department_name, role_title, salary)
            click.echo("Employee updated successfully.")
        elif choice == 3:
            employees = [e.name for e in get_all_employees(session)]
            name = click.prompt("Select employee to delete", type=click.Choice(employees))
            delete_employee(session, name)
            click.echo("Employee deleted successfully.")
        elif choice == 4:
            employees = get_all_employees(session)
            click.echo("\n--- Employees ---")
            for emp in employees:
                department = session.query(Department).filter_by(id=emp.department_id).first()
                role = session.query(Role).filter_by(id=emp.role_id).first()
                click.echo(f"Name: {emp.name}, Department: {department.name}, Role: {role.title}, Salary: {emp.salary}")
        elif choice == 5:
            break
        else:
            click.echo("Invalid choice. Please try again.")

if __name__ == "__main__":
    cli()
