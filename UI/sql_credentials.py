schema=""
host=""
user=""
password=""
port=3306
con = f'mariadb+pymysql://{user}:{password}@{host}:{port}/{schema}'