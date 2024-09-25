from sqlalchemy.orm import Session
from .models import Department, Role, Employee  # Import your models

# Department CRUD Operations
def add_department(session: Session, name: str):
    department = Department(name=name)
    session.add(department)
    session.commit()

def update_department(session: Session, old_name: str, new_name: str):
    department = session.query(Department).filter_by(name=old_name).first()
    if department:
        department.name = new_name
        session.commit()

def delete_department(session: Session, name: str):
    department = session.query(Department).filter_by(name=name).first()
    if department:
        session.delete(department)
        session.commit()

def get_all_departments(session: Session):
    return session.query(Department).all()


# Role CRUD Operations
def add_role(session: Session, title: str):
    role = Role(title=title)
    session.add(role)
    session.commit()

def update_role(session: Session, old_title: str, new_title: str):
    role = session.query(Role).filter_by(title=old_title).first()
    if role:
        role.title = new_title
        session.commit()

def delete_role(session: Session, title: str):
    role = session.query(Role).filter_by(title=title).first()
    if role:
        session.delete(role)
        session.commit()

def get_all_roles(session: Session):
    return session.query(Role).all()


# Employee CRUD Operations
def add_employee(session: Session, name: str, department_name: str, role_title: str, salary: float):
    department = session.query(Department).filter_by(name=department_name).first()
    role = session.query(Role).filter_by(title=role_title).first()
    if department and role:
        employee = Employee(name=name, department_id=department.id, role_id=role.id, salary=salary)
        session.add(employee)
        session.commit()

def update_employee(session: Session, old_name: str, new_name: str, department_name: str, role_title: str, salary: float):
    employee = session.query(Employee).filter_by(name=old_name).first()
    department = session.query(Department).filter_by(name=department_name).first()
    role = session.query(Role).filter_by(title=role_title).first()
    if employee and department and role:
        employee.name = new_name
        employee.department_id = department.id
        employee.role_id = role.id
        employee.salary = salary
        session.commit()

def delete_employee(session: Session, name: str):
    employee = session.query(Employee).filter_by(name=name).first()
    if employee:
        session.delete(employee)
        session.commit()

def get_all_employees(session: Session):
    return session.query(Employee).all()
