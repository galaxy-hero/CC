import MySQLdb


class MySQLConnection:
    connector = None

    @classmethod
    def init(cls, host='localhost', port=3306, user='root', passwd='', db='products'):
        if cls.connector is None:
            cls.connector = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db)
