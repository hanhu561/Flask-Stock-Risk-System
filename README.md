# Flask Stock Risk System 📈

A stock risk analysis system built with the Flask framework and backed by a SQL Server database. It supports user authentication, stock management, risk assessment, simulation analysis, and admin operations.

## 🔧 Tech Stack

- Python 3.7
- Flask
- SQL Server (via `pymssql`)
- HTML / CSS / Bootstrap
- Jinja2 (templating)

## 📁 Project Structure

SQL_Project/
│
├── static/ # Static assets (CSS, JS, images)
├── templates/ # HTML templates
│ ├── login.html
│ ├── home.html
│ ├── admin_home.html
│ └── ...
├── Project_Run.py # Main application entry
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── LICENSE


## 🚀 Features

- User registration and login (admin/user roles)
- Add and view stock data
- Analyze individual stock risk and simulate portfolio cost
- Risk evaluation and simulation tools
- Admin dashboard for user and data management

## 🛠️ Installation & Setup

1. **Clone the repository**
git clone https://github.com/hanhu561/Flask-Stock-Risk-System.git
cd Flask-Stock-Risk-System

2.Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

3.Install dependencies
pip install -r requirements.txt

4.Configure the SQL Server database
Make sure SQL Server is running locally. Update the credentials in Project_Run.py:
conn = pymssql.connect(host='localhost', user='sa', password='your_password', database='Project')

5.Run the application
python Project_Run.py
Visit http://127.0.0.1:5000 in your browser.

✅ Modules Implemented
 User login and permission control

 Stock management and analysis

 Cost simulation and portfolio tracking

 Admin management interface

 Database import via .sql script

📦 Database Info
SQL file: your_sql_file.sql (included in the root folder)

Contains table structure and sample data

🔐 Access Control
Admin: Can manage users, simulate analytics, and access all data

User: Can add/view their own stock data and run personal analysis

📌 Notes
Make sure pymssql is installed. If installation fails, consider using precompiled wheel from Gohlke

Ensure TCP/IP is enabled in your SQL Server configuration

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to ⭐ star or fork this repository. If you have any suggestions or issues, open an issue or contribute directly!

## 🖼 UI show

### Initial interface display
"LOGIN IN" means to log in at the client end. Admin Platform is for the administrator end to log in.

![images/initial_interface.png](images/initial_interface.png)


### Login interface display
![images/initial_interface.png](images/initial_interface.png)

### Login interface display

















