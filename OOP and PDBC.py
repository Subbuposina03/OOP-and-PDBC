import regex
import random
import MySQLdb

con = MySQLdb.connect(
    host='localhost',
    user='root',
    password='root123',
    database='bankdb'
)

cur = con.cursor()


class Bank:
    Holder_details = []
    def create_Account(self):
        new_holder = {}
        new_holder['Holder_name'] = input('Enter Holder name: ')
        Mobile = input('Enter Mobile Number: ')

        c = regex.fullmatch("[6-9]{1}[0-9]{9}", Mobile)

        if c:

            new_holder['Mobile'] = Mobile
            new_holder['Aadhar'] = input('Enter Aadhar number: ')
            new_holder['IFSC'] = "SBI0123"
            new_holder['Account_num'] = random.randint(
                1000000000, 9999999999
            )

            n = input(
                'Enter Type of Account (saving/zero): ').lower()
            while True:
                 if n == 'saving':
                    Amount = int(
                        input(
                            'Your account is saving account, deposit 1000: '
                        )
                    )

                    if Amount >= 1000:

                        new_holder['Type_Account'] = 'saving'
                        new_holder['Balance'] = Amount
                        break

                    else:
                        print('--- Deposit minimum 1000 ---')

                 elif n == 'zero':

                    a = int(
                        input(
                            'Your account is zero account, deposit 500: '
                        )
                    )

                    if a >= 500:

                        new_holder['Type_Account'] = 'zero'
                        new_holder['Balance'] = a
                        break

                    else:
                        print('--- Deposit minimum 500 ---')

                 else:
                    print('Enter saving or zero')
                    n = input(
                        'Enter Type of Account: '
                    ).lower()

            # Python list
            Bank.Holder_details.append(new_holder)

            # INSERT INTO DATABASE
            sql = """
            INSERT INTO bank_account
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """

            values = (
                new_holder['Holder_name'],
                new_holder['Mobile'],
                new_holder['Aadhar'],
                new_holder['IFSC'],
                new_holder['Account_num'],
                new_holder['Type_Account'],
                new_holder['Balance']
            )

            cur.execute(sql, values)
            con.commit()

            print('Account Created Successfully')
            print(new_holder)

        else:
            print('-- Enter Valid Mobile Number --')


    def deposit(self):

        print('---- Welcome to Deposit ----')

        acc_num = int(
            input('Enter Account number: ')
        )

        for x in Bank.Holder_details:

            if x['Account_num'] == acc_num:

                Amount = int(
                    input('Enter Deposit Amount: ')
                )

                x['Balance'] += Amount

                # UPDATE DATABASE
                sql = """
                UPDATE bank_account
                SET Balance = %s
                WHERE Account_num = %s
                """

                cur.execute(
                    sql,
                    (x['Balance'], acc_num)
                )

                con.commit()

                print(x)
                break

        else:
            print('--- Invalid Account number ---')


    def withdraw(self):

        print('----- Withdraw method -----')

        Account_num = int(
            input('Enter Account number: ')
        )

        for x in Bank.Holder_details:

            if x['Account_num'] == Account_num:

                Amount = int(
                    input('Enter withdraw Amount: ')
                )

                if Amount <= x['Balance']:

                    x['Balance'] -= Amount

                    # UPDATE DATABASE
                    sql = """
                    UPDATE bank_account
                    SET Balance = %s
                    WHERE Account_num = %s
                    """

                    cur.execute(
                        sql,
                        (x['Balance'], Account_num)
                    )

                    con.commit()

                    print(x)
                    break

                else:
                    print('----- Check your Balance -----')
                    break

        else:
            print('------ Invalid Account number ------')


    def Details(self):

        print('----- Details -----')

        Account_num = int(
            input('Enter Account number: ')
        )

        # SELECT FROM DATABASE
        sql = """
        SELECT *
        FROM bank_account
        WHERE Account_num = %s
        """

        cur.execute(sql, (Account_num,))

        data = cur.fetchone()

        if data:

            columns = [
                'Holder_name',
                'Mobile',
                'Aadhar',
                'IFSC',
                'Account_num',
                'Type_Account',
                'Balance'
            ]

            for k, v in zip(columns, data):
                print(k, '===>', v)

        else:
            print('----- Invalid Account number -----')


obj = Bank()

while True:

    print('--------------------------')

    print('''
1) Create Account
2) Deposit
3) Withdraw
4) Details
5) Exit
''')

    print('--------------------------')

    k = int(
        input('Select one option: ')
    )

    if k == 1:
        obj.create_Account()

    elif k == 2:
        obj.deposit()

    elif k == 3:
        obj.withdraw()

    elif k == 4:
        obj.Details()

    elif k == 5:
        break

    else:
        print('Invalid option')



cur.close()
con.close()