import psycopg2


class Register():
    def __init__(self, first_name, last_name, teoudate_zeoute, password):
        self.first_name = first_name
        self.last_name = last_name
        self.teoudate_zeoute = teoudate_zeoute
        self.password = password

    def __open_database(self):
        HOSTNAME = 'localhost'
        USERNAME = 'postgres'
        PASSWORD = 'Famille24'
        DATABASE = 'Application'
        self.connect = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        self.cursor = self.connect.cursor()

    def save_info(self):
        self.__open_database()
        self.cursor.execute(
            f"insert into clients(first_name,last_name,teoudate_zeoute,password_user) values('{self.first_name}','{self.last_name}','{self.teoudate_zeoute}','{self.password}');")
        self.connect.commit()
        self.connect.close()


class Login():
    def __init__(self, teoudate_zeoute, password):
        self.teoudate_zeoute = teoudate_zeoute
        self.password = password

    def get_user_access(self):
        HOSTNAME = 'localhost'
        USERNAME = 'postgres'
        PASSWORD = 'Famille24'
        DATABASE = 'Application'
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        query = f"select * from clients where teoudate_zeoute = {self.teoudate_zeoute}"
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        id, first_name, last_name, teoudate_zeoute, password, money = result[0]
        connection.close()
        if password == self.password:
            return True
        else:
            print("You make a mistake with your identifiant")
            print(results)
            return False


class Bank():
    def __init__(self, teoudate_zeoute, password):
        self.teoudate_zeoute = teoudate_zeoute
        self.password = password

    def __open_database(self):
        HOSTNAME = 'localhost'
        USERNAME = 'postgres'
        PASSWORD = 'Famille24'
        DATABASE = 'Application'
        self.connect = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        self.cursor = self.connect.cursor()

    def view_account(self):
        HOSTNAME = 'localhost'
        USERNAME = 'postgres'
        PASSWORD = 'Famille24'
        DATABASE = 'Application'
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        query = f"select * from clients where teoudate_zeoute = {self.teoudate_zeoute}"
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        id, first_name, last_name, teoudate_zeoute, password, money = result[0]
        print(f'you have {money} $ in your account')

    def deposit_money(self):
        money = int(input('Please insert how much money you want to deposit: \n'))
        self.__open_database()
        self.cursor.execute(f"update clients set money_user ={money}  where teoudate_zeoute = '{self.teoudate_zeoute}'")
        self.connect.commit()
        self.connect.close()

    def transfer_money(self):
        tz_transfer = input('Please insert teoudate zeoute of the user you want to tranfer money: \n')
        money_transfer = int(input('Please inser how much money you want to transfer: \n'))
        self.__open_database()
        self.cursor.execute(f"select * from clients where teoudate_zeoute = {self.teoudate_zeoute}")
        self.connect.commit()
        results = self.cursor.fetchall()
        self.connect.close()
        id, name, last_name, taz, password, money_client1 = results[0]

        self.__open_database()
        self.cursor.execute(f"select * from clients where teoudate_zeoute = {tz_transfer}")
        self.connect.commit()
        results_client2 = self.cursor.fetchall()
        self.connect.close()
        id, name, last_name, taz, password, money_client2 = results_client2[0]

        if (money_transfer > money_client1):
            print("You can't transfer this amount of money, you don't have enough money in your bank account")
        else:
            self.__open_database()
            self.cursor.execute(
                f"update clients set money_user ={money_client2 + money_transfer}  where teoudate_zeoute = '{tz_transfer}'")
            self.connect.commit()
            self.connect.close()

        self.__open_database()
        self.cursor.execute(
            f"update clients set money_user ={money_client1 - money_transfer}  where teoudate_zeoute = '{self.teoudate_zeoute}'")
        self.connect.commit()
        self.connect.close()

class shop():
    def __init__(self, items=[], qtys=[]):
        self.items = items
        self.qtys = qtys
        self.my_shop = {'carotte': 3,
                        'pomme': 4,
                        'poire': 3.5,
                        'pates': 5,
                        'poulet': 10,
                        'steak': 12,
                        'couscous': 6,
                        'frite': 7.5,
                        'sinta': 14}

    def add_to_panier(self, item, qty):
        self.items.append(item)
        self.qtys.append(qty)

    def remove_item(self,item):
        for x in range(len(self.qtys)):
            if self.items[x] == item:
                del self.items[x]
                del self.qtys[x]


    def diplay_shop(self):
        print(self.my_shop)

    def display_panier(self):
        for x in range(len(self.qtys)):
            print(f"you have in your bag {self.qtys[x]}  {self.items[x]}")


    def get_sum_of(self, arr_item, arr_qty):
        sum = 0
        for x in range(len(arr_qty)):
            price = self.my_shop[arr_item[x]] * arr_qty[x]
            sum += price
        return sum

    def pay_my_bag(self, password):
        sum = self.get_sum_of(self.items, self.qtys)
        # recupere largent du compte
        HOSTNAME = 'localhost'
        USERNAME = 'postgres'
        PASSWORD = 'Famille24'
        DATABASE = 'Application'
        connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        query = f"select money_user , password_user from clients WHERE password_user = '{password}';"
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        results = cursor.fetchall()
        connection.close()
        argent, b= results[0]
        if (argent < sum):
            print("you doesnt have enough to buy ")
        else:
            argent = argent - sum
            HOSTNAME = 'localhost'
            USERNAME = 'postgres'
            PASSWORD = 'Famille24'
            DATABASE = 'Application'
            connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
            query = f"UPDATE clients SET money_user = {argent} WHERE password_user = '{password}';"
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            connection.close()

def menu_shop():
    bool = False
    sh = shop([], [])
    while (bool == False):
        rep3 = input(
            f" view the shop (v) \n add element to the bag (a) \n remove (r) \n show the bag (s) \n pay my bag (p) \n Exit (e)")
        if rep3 == 'v':
            sh.diplay_shop()
        elif rep3 == 'a':
            item = input("write your item :")
            qty = int(input("the amount of your item :"))
            sh.add_to_panier(item, qty)
        elif rep3 == 'r':
            item = input("write your item :")
            sh.remove_item(item)
        elif rep3 == 's':
            sh.display_panier()
        elif rep3 == 'p':
            password = input("give your password account ")
            sh.pay_my_bag(password)
        elif rep3 == 'e':
            quit()


def bank_menu():
    bool = False
    teoudate_password = int(input('Please input youre number of Teoudate Zeoute: \n'))
    password = input('Please enter your password: \n')
    bank = Bank(teoudate_password, password)

    while (bool == False):
        answer = input(f'View money in account(v) \n Deposit money (d) \n Transfer Money(t)\n Exit (e)\n')
        if answer == 'v':
            bank.view_account()
        elif answer == 'd':
            bank.deposit_money()

        elif answer == 't':
            bank.transfer_money()

        elif answer == 'e':
            quit()


def deuxieme_menu():
    bool2 = False
    while (bool2 == False):
        rep2 = input(f' go to the shop (s) \n access to the bank (b) \n Exit(e)')
        if (rep2 == 's'):
            menu_shop()
        elif (rep2 == 'b'):
            bank_menu()
        elif (rep2 == 'e'):
            quit()


def main_menu():
    bool = False
    Pass = True
    while (bool == False):
        answer = input(f' Register (r) \n Sign in (s) \n Exit(e)\n')
        if answer == 'r':
            first_name = input('Please enter your first name: \n')
            last_name = input('Please enter your last name: \n')
            teouda_zeoute = int(input('Please enter your number of teoudate zeoute: \n'))
            while (teouda_zeoute > 1000000000 or teouda_zeoute < 99999999):
                teouda_zeoute = int(input('There is a probleme with your teoudate zeoute, try again :\n'))
            password = input('Please enter your password :\n')
            profil_register = Register(first_name, last_name, teouda_zeoute, password)
            profil_register.save_info()
            print('You successfuly register\n')

        elif (answer == 's'):
            teouda_zeoute = int(input('To login we need your number of teoudate zeoute: \n'))
            while (teouda_zeoute > 1000000000 or teouda_zeoute < 99999999):
                teouda_zeoute = int(input('There is a problem with your teoudate zeoute try again: \n'))
            password = input('Please enter youre password: \n')
            log = Login(teouda_zeoute, password)
            bool = log.get_user_access()
            Pass = False

        elif (answer == 'e'):
            quit()
        #         Pass = True
        #         bool = True
        # if bool == True and Pass == False:
        deuxieme_menu()


main_menu()