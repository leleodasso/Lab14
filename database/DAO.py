from database.DB_connect import DBConnect
from model.order import Order


class DAO():
    @staticmethod
    def getListaStore():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select distinct * 
                    from stores s """
        cursor.execute(query, ())

        result = []
        for row in cursor:
            result.append((row["store_name"], row["store_id"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getNodes(store_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select *
                from orders o 
                where o.store_id = %s"""
        cursor.execute(query, (store_id,))

        result = []
        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAllArchi(store_id, num_giorni):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT   o1.order_id, 
                            o2.order_id, 
                            o1.order_date, 
                            o2.order_date, 
                            (q1.total_quantity + q2.total_quantity) AS peso
                        FROM 
                            orders o1, 
                            orders o2,
                            (SELECT order_id, SUM(quantity) AS total_quantity 
                             FROM order_items 
                             GROUP BY order_id) AS q1,
                            (SELECT order_id, SUM(quantity) AS total_quantity 
                             FROM order_items 
                             GROUP BY order_id) AS q2
                        WHERE 
                            o1.store_id = %s
                            AND o1.store_id = o2.store_id
                            AND o1.order_id <> o2.order_id
                            AND DATEDIFF(o1.order_date, o2.order_date) < %s
                            AND o1.order_date > o2.order_date
                            AND q1.order_id = o1.order_id
                            AND q2.order_id = o2.order_id
                        GROUP BY 
                            o1.order_id, o2.order_id
                          """

        cursor.execute(query, (store_id, num_giorni))

        result = []
        for row in cursor:
            result.append((row["o1.order_id"], row["o2.order_id"], row["peso"]))

        cursor.close()
        conn.close()

        return result

