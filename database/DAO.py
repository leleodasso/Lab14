from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():

    @staticmethod
    def getStores():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select * from stores s   """

        cursor.execute(query, ())

        for row in cursor:
            result.append(Store(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getOrdiniStore(store):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from orders o 
                    where store_id = %s """

        cursor.execute(query, (store, ))

        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getQtaOggettiCompratiNegliOrdini(u: Order, v:Order, store, giorni):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """     select sum(oi1.quantity) + sum(oi2.quantity) as peso
                        from orders o1, orders o2, order_items oi1, order_items oi2
                        
                        where o1.store_id = %s
                        and o2.store_id = %s
                        
                        and o1.order_id = %s
                        and o2.order_id  = %s
                        
                        and oi1.order_id = %s
                        and oi2.order_id = %s
                        and o1.order_date > o2.order_date
                        and datediff(o1.order_date, o2.order_date) < %s
                        
                        and o1.order_id = oi1.order_id
                        and o2.order_id = oi2.order_id
                        
                        group by o1.order_id, o2.order_id """

        cursor.execute(query, (store, store, u.order_id, v.order_id, u.order_id, v.order_id, giorni ))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMap, store, giorni):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """  select o1.order_id as id1, o2.order_id as id2, sum(oi1.quantity) + sum(oi2.quantity) as peso
                    from orders o1, orders o2, order_items oi1, order_items oi2  
                    where o1.store_id = %s
                    and o2.store_id = %s
                    and o1.order_id <> o2.order_id
                    and o1.order_date > o2.order_date
                    and datediff(o1.order_date, o2.order_date) < %s
                    and o1.order_id = oi1.order_id
                    and o2.order_id = oi2.order_id
                    group by o1.order_id, o2.order_id  """

        cursor.execute(query, (store, store, giorni))

        for row in cursor:
            result.append((idMap[row["id1"]], idMap[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result
