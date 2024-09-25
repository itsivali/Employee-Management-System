from sqlalchemy.orm import Session
from .models import Department, Role, Employee
from .utils import validate_name, validate_salary, get_all_department_names, get_all_role_titles, get_department_id_by_name, get_role_id_by_name

# CRUD for managing Departments
def add_department(session: Session, name: str):
    department = Department(name=name)
    session.add(department)
    session.commit()

def update_department(session: Session, department_id: int, new_name: str):
    department = session.query(Department).filter_by(id=department_id).first()
    if department:
        department.name = new_name
        session.commit()

def delete_department(session: Session, department_id: int):
    department = session.query(Department).filter_by(id=department_id).first()
    if department:
        session.delete(department)
        session.commit()

def get_all_departments(session: Session):
    return session.query(Department).all()

# CRUD for managing Roles
def add_role(session: Session, title: str):
    role = Role(title=title)
    session.add(role)
    session.commit()

def update_role(session: Session, role_id: int, new_title: str):
    role = session.query(Role).filter_by(id=role_id).first()
    if role:
        role.title = new_title
        session.commit()

def delete_role(session: Session, role_id: int):
    role = session.query(Role).filter_by(id=role_id).first()
    if role:
        session.delete(role)
        session.commit()

def get_all_roles(session: Session):
    return session.query(Role).all()

# CRUD for managing Employees
def add_employee(session: Session, name: str, department_id: int, role_id: int, salary: float):
    employee = Employee(name=name, department_id=department_id, role_id=role_id, salary=salary)
    session.add(employee)
    session.commit()

def update_employee(session: Session, employee_id: int, name: str, department_id: int, role_id: int, salary: float):
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        employee.name = name
        employee.department_id = department_id
        employee.role_id = role_id
        employee.salary = salary
        session.commit()

def delete_employee(session: Session, employee_id: int):
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        session.delete(employee)
        session.commit()

def get_all_employees(session: Session):
    return session.query(Employee).all()
