#密匙

SECRET_KEY = "sdjkfvcnhu_0"




#数据库配置信息

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'demo_01'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
