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

### Initial Interface Display

![images/initial_interface.png](images/initial_interface.png)

"LOGIN IN" means to log in at the client end. Admin Platform is for the administrator end to log in.


### Login Interface Display

![images/administrator_login.png](images/administrator_login.png)

The SQL statement for the login function is shown in the above figure, that is, to query whether it is stored in the Account table. If there is a line in the input email and password, it will jump to the next one.
On the interface, if the account is entered incorrectly and cannot be logged in, that is, the line where the email and password do not exist will pop up the following window.


### The Password or Account is Incorrect

![images/error_occurred.png](images/error_occurred.png)

Similarly, the Administrator account uses the SQL statement to query Administrator.
Check whether there are email and password rows in the table to verify the user account information.

### Account Interface

![images/account_interface.png](images/account_interface.png)

If the user enters the correct account on the login interface, it will be redirected to the user's initial interface.
The system queries the Account table using the user's email and password to retrieve personal financial data, including Profit, Capital, Deposit, ProfitAmount (number of profitable investments), TotalAmount (total number of investments), and calculates P/T (profit-to-total ratio). This information is displayed at the top of the webpage via HTML.
It also queries the Portfolio table for the user's investment data, including StockCode, StockName, Return (investment return rate), Position (shares held), and StartDate (start date of the investment). Based on Return, it determines the investment status: gain, loss, or even.
The investment details are shown in the lower section of the HTML page, and can be sorted by StockCode, StockName, Return, Position, Status, and StartDate. Additionally, users can click the Export Report button to export portfolio data.

### Specific Information of Personal Accounts

![images/portfolio_interface.png](images/portfolio_interface.png)

Clicking the Portfolio button on the left side of the HTML page navigates to the user's detailed account information. The system queries the Account table using the login email and password to retrieve data such as Profit, Capital, Deposit, ProfitAmount, TotalAmount, and calculates P/T (profit-to-total ratio), which is displayed in the upper section of the page.
The lower section contains four buttons — Earn, Loss, Even, and All — to filter and display stocks based on performance.
A custom function SimulateProfit(portfolio, Kinds) is used to calculate the user's daily, weekly, monthly, and yearly average returns. These results are shown in the top-right corner of the page and can be toggled using the Day, Week, Month, and Year buttons.



