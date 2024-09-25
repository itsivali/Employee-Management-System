import re
from sqlalchemy.orm import Session
from .models import Department, Role

# validation and fetching data

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

def get_all_department_names(session: Session):
    return [dept.name for dept in session.query(Department).all()]

def get_all_role_titles(session: Session):
    return [role.title for role in session.query(Role).all()]

def get_department_id_by_name(session: Session, department_name: str):
    """Get the department ID by its name."""
    department = session.query(Department).filter_by(name=department_name).first()
    return department.id if department else None

def get_role_id_by_name(session: Session, role_title: str):
    """Get the role ID by its title."""
    role = session.query(Role).filter_by(title=role_title).first()
    return role.id if role else None
