import click
from sqlalchemy.orm import sessionmaker
from .models import Base
from .services import (
    add_department, update_department, delete_department, get_all_departments,
    add_role, update_role, delete_role, get_all_roles,
    add_employee, update_employee, delete_employee, get_all_employees
)
from .utils import (
    validate_name, validate_salary,
    get_all_department_names, get_all_role_titles,
    get_department_id_by_name, get_role_id_by_name
)

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
    session = ctx.obj['session']
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
            department_id = click.prompt("Enter department ID to update", type=int)
            new_name = click.prompt("Enter new department name", type=str)
            update_department(session, department_id, new_name)
            click.echo("Department updated successfully.")
        elif choice == 3:
            department_id = click.prompt("Enter department ID to delete", type=int)
            delete_department(session, department_id)
            click.echo("Department deleted successfully.")
        elif choice == 4:
            view_departments(ctx)
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
            role_id = click.prompt("Enter role ID to update", type=int)
            new_title = click.prompt("Enter new role title", type=str)
            update_role(session, role_id, new_title)
            click.echo("Role updated successfully.")
        elif choice == 3:
            role_id = click.prompt("Enter role ID to delete", type=int)
            delete_role(session, role_id)
            click.echo("Role deleted successfully.")
        elif choice == 4:
            view_roles(ctx)
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
            department_names = get_all_department_names(session)

            click.echo("\n--- Select a Department ---")
            for i, dept_name in enumerate(department_names, start=1):
                click.echo(f"{i}. {dept_name}")
            dept_index = click.prompt("Select a department by number", type=int) - 1
            department_id = get_department_id_by_name(session, department_names[dept_index])

            role_titles = get_all_role_titles(session)
            click.echo("\n--- Select a Role ---")
            for i, title in enumerate(role_titles, start=1):
                click.echo(f"{i}. {title}")
            role_index = click.prompt("Select a role by number", type=int) - 1
            role_id = get_role_id_by_name(session, role_titles[role_index])

            salary = validate_salary(click.prompt("Enter salary", type=float))
            add_employee(session, name, department_id, role_id, salary)
            click.echo("Employee added successfully.")

        elif choice == 2:
            employee_id = click.prompt("Enter employee ID to update", type=int)
            name = validate_name(click.prompt("Enter new employee name", type=str))
            department_names = get_all_department_names(session)

            click.echo("\n--- Select a Department ---")
            for i, dept_name in enumerate(department_names, start=1):
                click.echo(f"{i}. {dept_name}")
            dept_index = click.prompt("Select a department by number", type=int) - 1
            department_id = get_department_id_by_name(session, department_names[dept_index])

            role_titles = get_all_role_titles(session)
            click.echo("\n--- Select a Role ---")
            for i, title in enumerate(role_titles, start=1):
                click.echo(f"{i}. {title}")
            role_index = click.prompt("Select a role by number", type=int) - 1
            role_id = get_role_id_by_name(session, role_titles[role_index])

            salary = validate_salary(click.prompt("Enter new salary", type=float))
            update_employee(session, employee_id, name, department_id, role_id, salary)
            click.echo("Employee updated successfully.")

        elif choice == 3:
            employee_id = click.prompt("Enter employee ID to delete", type=int)
            delete_employee(session, employee_id)
            click.echo("Employee deleted successfully.")
        elif choice == 4:
            view_employees(ctx)
        elif choice == 5:
            break
        else:
            click.echo("Invalid choice. Please try again.")

def view_departments(ctx):
    """View Departments"""
    session = ctx.obj['session']
    departments = get_all_departments(session)
    if departments:
        click.echo("\n--- Departments ---")
        for dept in departments:
            click.echo(f"ID: {dept.id}, Name: {dept.name}")
    else:
        click.echo("No departments found.")

def view_roles(ctx):
    """View Roles"""
    session = ctx.obj['session']
    roles = get_all_roles(session)
    if roles:
        click.echo("\n--- Roles ---")
        for role in roles:
            click.echo(f"ID: {role.id}, Title: {role.title}")
    else:
        click.echo("No roles found.")

def view_employees(ctx):
    """View Employees"""
    session = ctx.obj['session']
    employees = get_all_employees(session)
    if employees:
        click.echo("\n--- Employees ---")
        for emp in employees:
            # Fetching role name based on role_id
            role = session.query(Role).filter_by(id=emp.role_id).first()
            role_name = role.title if role else "Unknown Role"
            click.echo(f"ID: {emp.id}, Name: {emp.name}, Salary: {emp.salary}, Department ID: {emp.department_id}, Role: {role_name}")
    else:
        click.echo("No employees found.")

if __name__ == '__main__':
    cli()
