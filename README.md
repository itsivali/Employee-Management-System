Employee Management System (CLI)
================================

Introduction
------------

The **Employee Management System (EMS)** is a command line interface (CLI) tool built using Python, SQLAlchemy, and SQLite to manage employees, departments, and roles in an organization. This application allows users to perform basic CRUD (Create, Read, Update, Delete) operations for managing these entities directly from the command line.

With EMS, users can:

*   Add, update, delete, and view departments.
    
*   Add, update, delete, and view roles.
    
*   Add, update, delete, and view employees, with department and role assignments.
    

This project is designed for simplicity and is strictly a terminal-based application without a web interface, making it ideal for small-scale or local employee management tasks.

Features
--------

*   **Manage Departments**: Add, update, delete, and view departments in the organization.
    
*   **Manage Roles**: Add, update, delete, and view roles available in the organization.
    
*   **Manage Employees**: Add, update, delete, and view employee details, including their assigned department, role, and salary.
    
*   **Relational Database**: Departments and roles are linked to employees via foreign keys, ensuring that employees are correctly assigned within the system.
    

Technologies Used
-----------------

*   **Python 3.x**
    
*   **SQLAlchemy**: ORM (Object Relational Mapper) for managing the database and models.
    
*   **SQLite**: Embedded database for storing departments, roles, and employees.
    
*   **Click**: Python library for building command-line interfaces.
    
*   **Tabulate** (optional): For neatly formatting the output in tables.
    

Prerequisites
-------------

Before setting up the application, make sure you have the following installed:

*   **Python 3.x**
    
*   **Virtual environment** 
    

Installation Instructions
-------------------------

Follow these steps to set up the Employee Management System (EMS) on your local machine.

### 1\. Clone the Repository

`   https://github.com/itsivali/employee-management-cli.git  cd employee-management-cli   `

### 2\. Set Up a Virtual Environment 

`   python3 -m venv venv  source venv/bin/activate    # On Linux/Mac  venv\Scripts\activate        # On Windows   `

### 3\. Install Dependencies

Install the required Python packages by running:

`   pip install -r requirements.txt   `

If you don’t have a requirements.txt file yet, you can manually install the dependencies using:

`   pip install sqlalchemy click tabulate   `

### 4\. Set Up the Database

The database is automatically set up the first time you run the application. It will create a SQLite database (employee\_management.db) in the current directory.

### 5\. Running the Application

To launch the EMS application, run the following command:

`   python cli.py main-menu   `

You will be given the main menu to choose which entity to manage (departments, roles, or employees).

Usage Instructions
------------------

Once the application is running, you can navigate through the following menus:

### Main Menu

`   1. Manage Departments  `
` 2. Manage Roles ` 
`3. Manage Employees `
` 4. Exit   `

### Managing Departments

In the "Manage Departments" menu, you can:

*   **Add a Department**: Enter a new department name.
    
*   **Update a Department**: Choose an existing department and rename it.
    
*   **Delete a Department**: Choose an existing department to delete.
    
*   **View Departments**: View a list of all current departments.
    

### Managing Roles

In the "Manage Roles" menu, you can:

*   **Add a Role**: Enter a new role title.
    
*   **Update a Role**: Choose an existing role and rename it.
    
*   **Delete a Role**: Choose an existing role to delete.
    
*   **View Roles**: View a list of all current roles.
    

### Managing Employees

In the "Manage Employees" menu, you can:

*   **Add an Employee**: Enter employee details (name, department, role, and salary).
    
*   **Update an Employee**: Choose an employee to update details like name, department, role, or salary.
    
*   **Delete an Employee**: Choose an existing employee to delete.
    
*   **View Employees**: View a list of all employees, along with their department, role, and salary information.
    

Example Commands
----------------

*   Add a new department:
    

 `code1 -> Manage Departments -> 1 -> Enter department name: "HR"`

*   View all roles:
    

 `code2 -> Manage Roles -> 4`

*   Add a new employee:
    

 `code3 -> Manage Employees -> 1 -> Enter employee name: "John Doe" -> Select department -> Select role -> Enter salary`

Exiting the Application
-----------------------

You can exit the application at any point by selecting the "Exit" option in the main menu or pressing Ctrl+C to terminate the script.

Future Enhancements
-------------------

*   Add validation for inputs such as employee salary.
    
*   Improve the user interface by adding color-coded outputs.
    
*   Add search functionality for employees, roles, and departments.
    

License
-------

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
