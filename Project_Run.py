from datetime import datetime

import numpy as np
import pandas as pd
import pymssql
from flask import Flask, render_template, request, session, url_for, jsonify
from werkzeug.utils import redirect

app = Flask(__name__, template_folder="templates")
app.secret_key = "121"  # Replace it with a random key

email = ''
password = ''

# introduce
@app.route('/')
def introduce():
    return render_template('introduce.html')

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"SELECT * FROM Account WHERE Email = {email} AND Password = {password}")

        conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
        with conn.cursor() as cursor:
            cursor.execute((f"SELECT * FROM Account WHERE Email = '{email}' AND Password = '{password}'"))
            user = cursor.fetchone()

        if user:
            # login successfully
            session['user_email'] = email
            session['user_password'] = password
            return redirect(url_for('home'))
        else:
            # Login failed and an error message was displayed
            error_msg = "Invalid email or password"
            print(f"Error message: {error_msg}")
            return render_template('login.html', error_msg=error_msg)

    # Display the login page
    return render_template('login.html')

# home page
@app.route('/home')
def home():
    email = session['user_email']
    password = session['user_password']
    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    try:
        with conn.cursor(as_dict=True) as cursor:
            # query = f"SELECT * FROM Account WHERE Email = '{email}' AND Password = '{password}'"
            query = f"SELECT *, CONCAT(ProfitAmount, '/', TotalAmount) AS [P/T] FROM Account WHERE Email = '{email}' AND Password = '{password}'"
            cursor.execute(query)
            result = cursor.fetchone()
            profit_value = result['Profit']
            capital_value = result['Capital']
            profit_amount_value = result['ProfitAmount']

            profit_proportion_value = result['P/T']
            deposit_value = result['Deposit']

            query = f"SELECT p.Email, p.StockCode, m.StockName, p.[Return], p.Position, " \
                     "CASE " \
                     "WHEN CAST(REPLACE(p.[Return], '%', '') AS FLOAT) > 0 THEN 'gain' " \
                     "WHEN CAST(REPLACE(p.[Return], '%', '') AS FLOAT) = 0 THEN 'even' " \
                     "ELSE 'loss' " \
                     "END AS Status, " \
                     f"p.StartDate " \
                     f"FROM Portfolio p JOIN Manystocks m ON p.StockCode = m.StockCode" \
                     f" WHERE Email = '{email}'"
            cursor.execute(query)
            portfolios = cursor.fetchall()
            for portfolio in portfolios:
                portfolio['Return'] = float(portfolio['Return'].strip('%')) / 100.0
                portfolio['Return'] = round(portfolio['Return'], 2)

    finally:
        conn.close()

    return render_template('home.html', profit=profit_value, capital=capital_value,
                           profit_amount=profit_amount_value, profit_proportion=profit_proportion_value,
                           deposit=deposit_value, portfolios=portfolios)

@app.route('/portfolio')
def portfolio():
    email = session['user_email']
    password = session['user_password']

    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    try:
        with conn.cursor(as_dict=True) as cursor:
            # query = f"SELECT * FROM Account WHERE Email = '{email}' AND Password = '{password}'"
            query = f"SELECT *, CONCAT(ProfitAmount, '/', TotalAmount) AS [P/T] FROM " \
                    f"Account WHERE Email = '{email}' AND Password = '{password}'"
            cursor.execute(query)
            result = cursor.fetchone()
            profit_amount = round(float(result['Profit']), 2)
            capital_value = result['Capital']
            profit_amount_value = result['ProfitAmount']
            profit_proportion_value = result['P/T']
            deposit_value = result['Deposit']

            query = f"SELECT p.Email, p.StockCode, m.StockName, p.[Return], p.Position, " \
                     "CASE " \
                     "WHEN CAST(REPLACE(p.[Return], '%', '') AS FLOAT) > 0 THEN 'gain' " \
                     "WHEN CAST(REPLACE(p.[Return], '%', '') AS FLOAT) = 0 THEN 'even' " \
                     "ELSE 'loss' " \
                     "END AS Status, " \
                     f"p.StartDate " \
                     f"FROM Portfolio p JOIN Manystocks m ON p.StockCode = m.StockCode" \
                     f" WHERE Email = '{email}'"
            cursor.execute(query)
            portfolios = cursor.fetchall()

            for portfolio in portfolios:
                portfolio['Return'] = float(portfolio['Return'].strip('%')) / 100.0
                portfolio['Return'] = round(portfolio['Return'], 2)

            query = f"SELECT m.StockName, m.Industry AS industry, 'gain' AS Status, p.[Return], p.[Position], p.StockCode " \
                    f"FROM Portfolio p JOIN Manystocks m ON p.StockCode = m.StockCode " \
                    f"WHERE p.Email = '{email}' AND p.[Return] NOT LIKE '-%' AND p.[Return] != '0%'"
            cursor.execute(query)
            result = cursor.fetchall()
            earndata = [
                {"stockname": row['StockName'], "stockcode": row['StockCode'], "industry": row['industry'],
                 "status": row['Status'], "return": row['Return'],
                 "position": row['Position']}
                for row in result
            ]

            query = f"SELECT m.StockName, m.Industry AS industry, 'loss' AS Status, p.[Return], p.[Position], p.StockCode " \
                    f"FROM Portfolio p JOIN Manystocks m ON p.StockCode = m.StockCode " \
                    f"WHERE p.Email = '{email}' AND p.[Return] LIKE '-%'"
            cursor.execute(query)
            result = cursor.fetchall()
            lossdata = [
                {"stockname": row['StockName'], "stockcode": row['StockCode'], "industry": row['industry'],
                 "status": row['Status'], "return": row['Return'],
                 "position": row['Position']}
                for row in result
            ]
            ##even
            query = f"SELECT m.StockName, m.Industry AS industry, 'even' AS Status, p.[Return], p.[Position], p.StockCode " \
                    f"FROM Portfolio p JOIN Manystocks m ON p.StockCode = m.StockCode " \
                    f"WHERE p.Email = '{email}' AND p.[Return] = '0%'"
            cursor.execute(query)
            result = cursor.fetchall()
            evendata = [
                {"stockname": row['StockName'], "stockcode": row['StockCode'], "industry": row['industry'],
                 "status": row['Status'], "return": row['Return'],
                 "position": row['Position']}
                for row in result
            ]
            # all
            query = f"SELECT m.StockName, m.Industry AS industry, " \
                    "CASE " \
                    "WHEN CAST(REPLACE(p.[Return], '%', '') AS FLOAT) > 0 THEN 'gain' " \
                    "WHEN CAST(REPLACE(p.[Return], '%', '') AS FLOAT) = 0 THEN 'even' " \
                    "ELSE 'loss' " \
                    "END AS Status, " \
                    f"p.[Return], p.[Position], p.StockCode " \
                    f"FROM Portfolio p JOIN Manystocks m ON p.StockCode = m.StockCode " \
                    f"WHERE p.Email = '{email}'"
            cursor.execute(query)
            result = cursor.fetchall()
            alldata = [
                {"stockname": row['StockName'], "stockcode": row['StockCode'], "industry": row['industry'],
                 "status": row['Status'], "return": row['Return'],
                 "position": row['Position']}
                for row in result
            ]
    finally:
        conn.close()
    percentage_value = round((int(profit_amount) / int(capital_value)) * 100, 2)
    print('ok')
    return render_template('portfolio.html', profit_amount=profit_amount_value, profit_proportion=profit_proportion_value,
                           total_profit=profit_amount, percentage_value=percentage_value, total_capital=capital_value, total_deposit=deposit_value, earndata=earndata, lossdata=lossdata,evendata=evendata, alldata=alldata)

@app.route('/get_earning_chart_data/<series_type>', methods=['GET'])
def get_earning_chart_data(series_type):
    email = session['user_email']
    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')

    cursor = conn.cursor()

    query = f"SELECT StockCode, Position, CONVERT(VARCHAR, StartDate, 120), '2023-12-14' AS EndDate " \
            f"FROM Portfolio " \
            f"WHERE Email='{email}'"

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        results_list = [list(result) for result in results]

        # Output the query result
        # for result in results_list:
        #     print(result)
    except Exception as e:
        print("Query failed:", e)

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

    profit_sequence = SimulateProfit(results_list, series_type)
    print(profit_sequence)

    response_data = {'columnData': profit_sequence}

    return jsonify(response_data)

def SimulateProfit(portfolio,Kinds):

    def inside1(StockNote,  StartTime, EndTime):
        conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
        try:
            query_time = f"SELECT Num FROM Times WHERE Time >= '{StartTime}' AND Time <= '{EndTime}' ORDER BY Time"
            time_df = pd.read_sql_query(query_time, conn)
            if len(time_df) < 2:
                raise ValueError("Not enough data for the specified time range.")
            Num1, Num2 = time_df['Num'].iloc[0], time_df['Num'].iloc[-1]
            num1 = int(Num1[6:])
            num2 = int(Num2[6:])
            query_data = f"SELECT * FROM OpenPriceDay WHERE StockCode = '{StockNote}'"
            data_df = pd.read_sql_query(query_data, conn)
            selected_data = data_df.loc[0, Num1:Num2]

            return selected_data, num1, num2

        finally:
            conn.close()

    def inside2(portfolio):
        profit = {key: 0 for key in range(3, 476)}
        for por in portfolio:
            StockNote, Capital, StartTime, EndTime=por[0],int(por[1]),por[2],por[3]
            selected_data, num1, num2 = inside1( StockNote, StartTime, EndTime)
            for i in range(1, len(selected_data)):
                difference =(((selected_data[i]) - (selected_data[0]))*Capital/(selected_data[0])).round(2)
                key=i+num1
                profit[key]=profit[key]+difference
            if num2 != 475:
                for j in range(num2+1,476):
                    difference=(((selected_data[num2-num1]) - (selected_data[0]))*Capital/(selected_data[0])).round(2)
                    profit[j] = profit[j] + difference
        pro=list(profit.values())
        return pro

    pro= inside2(portfolio)
    if Kinds=="day":
        return pro
    if Kinds=="week":
        # Add up every five numbers and take the average
        sums = [np.mean(pro[i:i + 5]) for i in range(0, len(pro), 5)]
        # keep two decimals
        rounded_sums = [round(num, 2) for num in sums]
        return rounded_sums
    if Kinds == "month":
        # Add up every 20 numbers and take the average
        sums = [np.mean(pro[i:i + 20]) for i in range(0, len(pro), 20)]
        # keep two decimals
        rounded_sums = [round(num, 2) for num in sums]
        return rounded_sums
    if Kinds == "year":
        # Add up every 250 numbers and take the average
        sums = [np.mean(pro[i:i + 250]) for i in range(0, len(pro), 250)]
        # keep two decimals
        rounded_sums = [round(num, 2) for num in sums]
        return rounded_sums

@app.route('/delete-item', methods=['POST'])
def delete_item():
    data = request.get_json()
    email = session['user_email']

    stockcode = data.get('stockcode')
    print(f"Deleting item with stockcode: {stockcode}")
    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    try:
        with conn.cursor(as_dict=True) as cursor:
            query = f"DELETE FROM Portfolio WHERE StockCode = '{stockcode}' AND Email = '{email}'"
            cursor.execute(query)
        conn.commit()  # Explicitly commit the transaction
        print('ok')

    finally:
        conn.close()

    response_data = {'status': 'success', 'reload_page': True, 'message': f'Deleted item with stockcode: {stockcode}'}
    return jsonify(response_data)

@app.route('/editstock.html', methods=['GET', 'POST'])
def editstock():
    stockcode = request.args.get('stockcode')
    stockname = request.args.get('stockname')
    industry = request.args.get('industry')
    position = request.args.get('position')
    print(f"Editing stock with code {stockcode}, name {stockname}, industry {industry}, position {position}")
    if request.method == 'POST':
        stock_name = request.form.get('stockName')
        stock_code = request.form.get('stockCode')
        stock_industry = request.form.get('stockIndustry')
        position = request.form.get('position')
        password = request.form.get('password')

        # print(f"Received stock name: {stock_name}")
        # print(f"Received stock code: {stock_code}")
        # print(f"Received stock industry: {stock_industry}")
        # print(f"Received position: {position}")
        # print(f"Received password: {password}")
        email = session['user_email']
        if password != None:
            conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
            try:
                with conn.cursor(as_dict=True) as cursor:
                    cursor.execute(f"SELECT * FROM Account WHERE Email = '{email}' AND Password = '{password}'")
                    account_exists = cursor.fetchone()
                    if account_exists:
                        current_datetime = datetime.now()
                        current_date = current_datetime.date()
                        print("当前日期：", current_date)
                        update_query = f"UPDATE Portfolio SET position = '{position}', StartDate = '{current_date}' " \
                                       f"WHERE Email = '{email}' AND StockCode = '{stock_code}'"

                        cursor.execute(update_query)
                        print(update_query)
                        conn.commit()
                        print("Data updated successfully into Portfolio table.")
                    else:
                        print("Account not found in the Account table.")
            finally:
                conn.close()

    return render_template('editstock.html', stockname=stockname, stockcode=stockcode, industry=industry, position=position)

@app.route('/stockview', methods=['GET', 'POST'])
def stockview():
    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    try:
        with conn.cursor(as_dict=True) as cursor:
            query = "SELECT StockCode, StockName, Industry, EstablishTime, BusinessSize, StaffNum FROM ManyStocks"
            cursor.execute(query)
            stocks = cursor.fetchall()
            # print(stocks)
    finally:
        conn.close()

    if request.method == 'POST':
        search_term = request.form['search']
        print(f"Received search term: {search_term}")
        conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
        try:
            with conn.cursor(as_dict=True) as cursor:
                query = f"SELECT StockCode, StockName, Industry, BusinessSize, StaffNum, EstablishTime FROM ManyStocks WHERE " \
                        f"StockCode LIKE '%{search_term}%' OR StockName LIKE '%{search_term}%' " \
                        f"OR Industry LIKE '%{search_term}%' OR BusinessSize LIKE '%{search_term}%'" \
                        f"OR StaffNum LIKE '%{search_term}%' OR EstablishTime LIKE '%{search_term}%';"
                cursor.execute(query)
                stocks = cursor.fetchall()
                # print(stocks)
        finally:
            conn.close()
        return render_template('stockview.html', stocks=stocks)

    return render_template('stockview.html',stocks=stocks)


@app.route('/addstock', methods=['GET', 'POST'])
def addstock():
    email = session['user_email']

    stockcode = request.form.get('stockCode')
    stockname = request.form.get('stockName')
    industry = request.form.get('industry')

    if request.method == 'POST':
        stock_name = request.form.get('stockName')
        stock_code = request.form.get('stockCode')
        stock_industry = request.form.get('stockIndustry')
        position = request.form.get('position')
        password = request.form.get('password')

        # print(f"Received stock name: {stock_name}")
        # print(f"Received stock code: {stock_code}")
        # print(f"Received stock industry: {stock_industry}")
        # print(f"Received position: {position}")
        # print(f"Received password: {password}")
        if password != None:
            conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
            try:
                with conn.cursor(as_dict=True) as cursor:
                    cursor.execute(f"SELECT * FROM Account WHERE Email = '{email}' AND Password = '{password}'")
                    account_exists = cursor.fetchone()
                    if account_exists:

                        current_datetime = datetime.now()
                        current_date = current_datetime.date()
                        email = session['user_email']
                        # print("current date：", current_date)
                        insert_query = f"INSERT INTO Portfolio (Email, StockCode, [Return], Position, Status, StartDate) " \
                                       f"VALUES ('{email}', '{stock_code}', '0%', '{position}', 'even', '{current_date}')"

                        cursor.execute(insert_query)
                        conn.commit()

                        print("Data inserted successfully into Portfolio table.")
                    else:
                        print("Account not found in the Account table.")
            finally:
                conn.close()

    return render_template('addstock.html', stockname=stockname, stockcode=stockcode, industry=industry)


# stocksingle page
@app.route('/stocksingle')
def stocksingle():
    stockcode = request.args.get('stockcode')
    print(stockcode)
    session['stockcode'] = stockcode
    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    try:
        with conn.cursor(as_dict=True) as cursor:
            query = f"SELECT OpenPrice, ClosePrice, MaxPrice, MinPrice, InsideTrade, OutsideTrade, " \
                    f"StaffNum, StockName, Industry, BusinessSize FROM ManyStocks WHERE StockCode = '{stockcode}'"
            cursor.execute(query)
            stock_message = cursor.fetchone()
            if stock_message:
                open_price = stock_message['OpenPrice']
                close_price = stock_message['ClosePrice']
                max_price = stock_message['MaxPrice']
                min_price = stock_message['MinPrice']
                inside_trade = stock_message['InsideTrade']
                outside_trade = stock_message['OutsideTrade']
                staff_num = stock_message['StaffNum']
                stock_name = stock_message['StockName']
                industry = stock_message['Industry']
                business_size = stock_message['BusinessSize']

                return render_template('stocksingle.html', open_price=open_price, close_price=close_price,
                                       max_price=max_price, min_price=min_price,
                                       inside_trade=inside_trade, outside_trade=outside_trade, staffnum=staff_num,
                                       stockcode=stockcode, stockname=stock_name,
                                       industry=industry, bussinesssize=business_size)
            else:
                print(f'No data found for Stock Code: {stockcode}')
    finally:
        conn.close()

@app.route('/get_data/<time_period>')
def get_data_route(time_period):
    data = get_data(time_period)
    labels = get_labels(time_period)
    return jsonify({'data': data, 'labels': labels})

def getSearchQuery(time_period, stock_code):
    if time_period == 'week':
        return f"SELECT * FROM OpenPriceWeek WHERE StockCode = '{stock_code}'"
    elif time_period == 'month':
        return f"SELECT * FROM OpenPriceMonth WHERE StockCode = '{stock_code}'"
    elif time_period == 'year':
        return f"SELECT * FROM OpenPriceYear WHERE StockCode = '{stock_code}'"
    elif time_period == 'all':
        return f"SELECT * FROM OpenPriceDay WHERE StockCode = '{stock_code}'"

def get_data(time_period):
    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    result_sequence=[]
    try:
        with conn.cursor(as_dict=True) as cursor:
            print(session['stockcode'])
            print(getSearchQuery(time_period, session['stockcode']))
            cursor.execute(getSearchQuery(time_period, session['stockcode']))
            result_row = cursor.fetchone()
            if result_row:
                result_sequence = list(result_row.values())[2:]
                print(result_sequence)
    finally:
        conn.close()
    return result_sequence

def get_labels(time_period):
    if time_period == 'year':
        return ['2020', '2021', '2022', '2023']
    else:
        return []

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # email = request.form['email']
        # password = request.form['password']
        email = request.form.get('email')
        password = request.form.get('password')
        Email = email
        Password = password
        print(f"SELECT * FROM Account WHERE Email = {email} AND Password = {password}")
        conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
        with conn.cursor() as cursor:
            cursor.execute((f"SELECT * FROM Administrator WHERE Email = '{email}' AND Password = '{password}'"))
            user = cursor.fetchone()

        if user:
            session['user_email'] = email
            session['user_password'] = password
            return redirect(url_for('admin_user_management'))
        else:
            error_msg = "Invalid email or password"
            print(f"Error message: {error_msg}")

    # Display the login page
    return render_template('admin_login.html')

##User information management interface  add edit 和delete
@app.route('/admin_user_management')
def admin_user_management():
    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    try:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute("SELECT * FROM individual")
            retrieved_data = cursor.fetchall()
        formatted_data = []
        for record in retrieved_data:
            formatted_record = {
                "name": f"{record['FirstName']} {record['LastName']}",
                "email": record['Email'],
                "speciality": record['Speciality'],
                "gender": record['Gender'],
                "riskgrade": record['RiskGrade'],
                "preference": record['Preference'],
                "country": record['Country']
            }
            print(record['Preference'])
            formatted_data.append(formatted_record)

    finally:
        conn.close()

    return render_template('admin_user_management.html', profiles=formatted_data)

@app.route('/admin_user_add', methods=['GET', 'POST'])
def admin_user_add():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        specialty = request.form['specialty']
        preference = request.form['preference']
        gender = request.form['gender']
        birth = request.form['birth']
        phone = request.form['phone']
        email = request.form['email']
        country = request.form['country']
        risk_grade = request.form['riskgrade']
        password = request.form['password']
        # print("First Name:", first_name)
        # print("Last Name:", last_name)
        # print("Specialty:", specialty)
        # print("Preference:", preference)
        # print("Gender:", gender)
        # print("Birth:", birth)
        # print("Phone:", phone)
        # print("Email address:", email)
        # print("Country:", country)
        # print("RiskGrade:", risk_grade)
        # print("Password:", password)
        conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
        try:
            with conn.cursor(as_dict=True) as cursor:
                cost="0"
                insert_query = f"INSERT INTO Individual (FirstName, LastName, Email, Password, Birth, Speciality, RiskGrade, Gender, Phone, Country, Preference, Cost) " \
                               f"VALUES ('{first_name}', '{last_name}', '{email}', '{password}', '{birth}', '{specialty}', '{risk_grade}', '{gender}', '{phone}', '{country}', '{preference}', '{cost}')"
                cursor.execute(insert_query)
                conn.commit()
        finally:
            conn.close()
        return redirect(url_for('admin_user_management'))
    return render_template('admin_user_add.html')

@app.route('/admin_user_edit', methods=['GET', 'POST'])
def admin_user_edit():
    email = request.args.get('email', '')
    print(email)
    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    try:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute(f"SELECT * FROM individual WHERE Email = '{email}'")
            result = cursor.fetchone()
            if result:
                first_name = result['FirstName']
                last_name = result['LastName']
                specialty = result['Speciality']
                preference = result['Preference']
                birth = result['Birth']
                gender = result['Gender']
                phone = result['Phone']
                selected_country = result['Country']
                riskgrade = result['RiskGrade']
                password = result['Password']
                session['selected_email'] = email
    finally:
        conn.close()

    if request.method == 'POST':
        email = session.get('selected_email', '')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        specialty = request.form.get('specialty')
        preference = request.form.get('preference')
        gender = request.form.get('gender')
        birth = request.form.get('birth')
        phone = request.form.get('phone')
        country = request.form.get('country')
        riskgrade = request.form.get('riskgrade')
        password = request.form.get('password')
        # print(f"First Name: {first_name}")
        # print(f"Last Name: {last_name}")
        # print(f"Specialty: {specialty}")
        # print(f"Preference: {preference}")
        # print(f"Birth: {birth}")
        # print(f"Gender: {gender}")
        # print(f"Phone: {phone}")
        # print(f"Selected Country: {country}")
        # print(f"RiskGrade: {riskgrade}")
        # print(f"Password: {password}")
        conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
        try:
            with conn.cursor(as_dict=True) as cursor:
                print(email)
                update_query = f"UPDATE Individual SET FirstName = '{first_name}', LastName = '{last_name}', Password = '{password}', Birth = '{birth}', " \
                               f"Speciality = '{specialty}', RiskGrade = '{riskgrade}', Gender = '{gender}', Phone = '{phone}', Country = '{country}', " \
                               f"Preference = '{preference}' WHERE Email = '{email}'"

                cursor.execute(update_query)
                conn.commit()
                print("ok")
        finally:
            conn.close()
        return redirect(url_for('admin_user_management'))


    return render_template('admin_user_edit.html', email=email, first_name=first_name, last_name=last_name, specialty=specialty, preference=preference,
                           birth=birth, gender=gender, phone=phone, selected_country=selected_country, riskgrade=riskgrade, password=password)

@app.route('/admin_user_delete', methods=['POST'])
def admin_user_delete():
    email_to_delete = request.form.get('email')
    print(email_to_delete)
    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    try:
        with conn.cursor(as_dict=True) as cursor:
            delete_query = f"DELETE FROM Individual WHERE Email = '{email_to_delete}'"
            cursor.execute(delete_query)

            conn.commit()
    finally:
        conn.close()
    return jsonify({'message': 'User deleted successfully', 'reload_page': True})

@app.route('/admin_user_follow', methods=['POST'])
def admin_user_follow():
    try:
        data = request.get_json()
        print(data['email'])
        email=data['email']
        session['user_email'] = data['email']
        password =''
        conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
        try:
            with conn.cursor(as_dict=True) as cursor:
                query = f"SELECT Password FROM individual WHERE Email = '{email}'"
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    password = result['Password']
        finally:
            conn.close()

        session['user_password'] = password
        print(session['user_password'])
        return render_template(url_for('/portfolio'))

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin_user_costbill', methods=['POST'])
def admin_user_costbill():
    try:
        data = request.get_json()
        email = data['email']
        session['user_email'] = data['email']
        print(email)
        password = ''
        conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
        try:
            with conn.cursor(as_dict=True) as cursor:
                query = f"SELECT Password FROM individual WHERE Email = '{email}'"
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    password = result['Password']
        finally:
            conn.close()
        session['user_password'] = password
        conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
        try:
            with conn.cursor(as_dict=True) as cursor:
                query = f"SELECT FirstName, LastName, CONCAT(FirstName, ' ', LastName) AS name, " \
                        f"Speciality, Country, Phone, Cost FROM Individual WHERE Email = '{email}'"
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    name = result['name']
                    speciality = result['Speciality']
                    country = result['Country']
                    phone = result['Phone']
                    total_cost = result['Cost']
                query2 = f"SELECT StockName, Trade, Amount, " \
                         f"CASE " \
                         f"WHEN CONVERT(INT, Amount) <= 5000 THEN '10%' " \
                         f"WHEN CONVERT(INT, Amount) <= 10000 THEN '8%' " \
                         f"WHEN CONVERT(INT, Amount) <= 20000 THEN '5%' " \
                         f"ELSE '3%' " \
                         f"END AS Rate, " \
                         f"CONVERT(INT, Amount) * " \
                         f"CASE " \
                         f"WHEN CONVERT(INT, Amount) <= 5000 THEN 0.1 " \
                         f"WHEN CONVERT(INT, Amount) <= 10000 THEN 0.08 " \
                         f"WHEN CONVERT(INT, Amount) <= 20000 THEN 0.05 " \
                         f"ELSE 0.03 " \
                         f"END AS Cost " \
                         f"FROM BrokerageCost WHERE Email = '{email}'"

                cursor.execute(query2)
                result = cursor.fetchall()

                costbilldata = [
                    {"StockName": row['StockName'], "Trade": row['Trade'], "Amount": row['Amount'], "Rate": row['Rate'],
                     "Cost": row['Cost']}
                    for row in result
                ]
        finally:
            # Close the database connection
            conn.close()

        return render_template(url_for('/admin_costbill'))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin_costbill')
def admin_costbill():
        conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
        try:
            with conn.cursor(as_dict=True) as cursor:
                email = session['user_email']
                query = f"SELECT FirstName, LastName, CONCAT(FirstName, ' ', LastName) AS name, Speciality, Country, Phone, Cost FROM Individual WHERE Email = '{email}'"
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    name = result['name']
                    speciality = result['Speciality']
                    country = result['Country']
                    phone = result['Phone']
                    total_cost = result['Cost']
                query2 = f"SELECT StockName, Trade, Amount, " \
                         f"CASE " \
                         f"WHEN CONVERT(INT, Amount) <= 5000 THEN '10%' " \
                         f"WHEN CONVERT(INT, Amount) <= 10000 THEN '8%' " \
                         f"WHEN CONVERT(INT, Amount) <= 20000 THEN '5%' " \
                         f"ELSE '3%' " \
                         f"END AS Rate, " \
                         f"CONVERT(INT, Amount) * " \
                         f"CASE " \
                         f"WHEN CONVERT(INT, Amount) <= 5000 THEN 0.1 " \
                         f"WHEN CONVERT(INT, Amount) <= 10000 THEN 0.08 " \
                         f"WHEN CONVERT(INT, Amount) <= 20000 THEN 0.05 " \
                         f"ELSE 0.03 " \
                         f"END AS Cost " \
                         f"FROM BrokerageCost WHERE Email = '{email}'"
                cursor.execute(query2)
                result = cursor.fetchall()

                costbilldata = [
                    {"StockName": row['StockName'], "Trade": row['Trade'], "Amount": row['Amount'], "Rate": row['Rate'],
                     "Cost": row['Cost']}
                    for row in result
                ]
        finally:
            conn.close()

        return render_template('admin_costbill.html', name=name, speciality=speciality, country=country,
                               email=email, phone=phone, costbilldata=costbilldata, total_cost=total_cost)

@app.route('/admin_simulated')
def admin_simulated():
    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    try:
        with conn.cursor(as_dict=True) as cursor:
            query = f"SELECT StockName, Industry FROM ManyStocks"
            cursor.execute(query)
            results = cursor.fetchall()
            stockdata = []

            for result in results:
                stock_entry = {
                    "StockName": result['StockName'],
                    "Industry": result['Industry'],
                }
                stockdata.append(stock_entry)

    finally:
        conn.close()

    return render_template('admin_simulated.html', stockdata=stockdata)

@app.route('/admin_simulated_selected_stocks', methods=['POST'])
def receive_simulated_stock_data():
    try:
        data = request.get_json()
        # print(data)

        selected_stocks = data.get('selectedStocks', [])
        # print(selected_stocks)

        session['selected_stocks'] = selected_stocks
        session['selected_stocks'] = selected_stocks
        # print(session['selected_stocks'])

        return  redirect(url_for('admin_simulated_analytics'))

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/admin_simulated_analytics')
def admin_simulated_analytics():
    selected_stocks = session.get('selected_stocks', [])
    # print(selected_stocks)

    conn = pymssql.connect(host='localhost', user='sa', password='561521HhHh', database='Project202312', charset='utf8')
    stockdata = []
    try:
        with conn.cursor(as_dict=True) as cursor:
            for stock in selected_stocks:
                stock_name = stock['StockName']
                query = f"SELECT StockCode FROM ManyStocks WHERE StockName = '{stock_name}'"
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    stock_code = result['StockCode']
                    formatted_stock_result = {
                        'StockName': stock_name,
                        'StockCode': stock_code,
                        'Position': stock['Position'],
                        'StartDate': stock['StartDate'],
                        'EndDate': stock['EndDate']
                    }
                    # print(stock_name)
                    # print(stock_code)
                    stockdata.append(formatted_stock_result)
                else:
                    print(f"StockName: {stock_name} not found in ManyStocks")
    finally:
        # Close the database connection
        conn.close()
    formatted_data = [
        [stock['StockCode'], int(stock['Position']), stock['StartDate'], stock['EndDate']]
        for stock in stockdata
    ]
    # print(formatted_data)

    profit_list = SimulateProfit(formatted_data, 'day')
    total_amount = len(formatted_data)
    labels=[]
    for i in (0, len(profit_list)):
        labels.append(i+1)
    # labels = [1, 2, 3, 4, 5, 6, 7, 8]
    first_non_zero_index = next((i for i, x in enumerate(profit_list) if x != 0), None)
    if first_non_zero_index is not None:
        profit_list = profit_list[first_non_zero_index:]
    series = profit_list
    total_profit = profit_list[-1]
    data=stockdata
    # print(data)
    # return '0'
    return render_template('admin_simulated_analytics.html', total_profit=total_profit, total_amount=total_amount,
                           labels=labels, series=series, data=data)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
    # import pymssql
    #
    # try:
    #     conn = pymssql.connect(server='localhost\SQLEXPRESS', port=1433, user='sa', password='561521HhHh', database='Project202312')
    #
    #     print("连接成功！")
    #     conn.close()
    # except Exception as e:
    #     print("连接失败：", e)

