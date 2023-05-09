import sqlite3 as sql
from datetime import datetime, timedelta


# class
class DB:
    # constructor
    def __init__(self, **kwargs):
        super(DB, self).__init__(**kwargs)
        # creating or connecting to DB
        self.conn = sql.connect('Task_DB.db')
        # creating cursor for DML operation queries
        self.cur = self.conn.cursor()
        # calling function
        self.create_database_structure()

    def create_database_structure(self):
        # create table if not exist
        self.cur.execute("""Create table If not exists Users (U_id Integer primary key autoincrement, 
                            Username Text NOT NULL UNIQUE,
                            Password Text Not Null, 
                            Email Text)""")

        # create table Task which will hold all the Task's data
        self.cur.execute("""Create table If not exists Task (T_id Integer primary key autoincrement, 
                    Task_Name Text Not Null,
                    Task_Date Text Not Null,
                    Range Text,
                    Level Text,
                    Quote Text,
                    Image_path Text,
                    Status int Not Null,
                    u_id int Not Null)""")

    # fetch user by giving the username
    def get_user(self, username):
        # select query
        self.cur.execute("Select * from Users where username=?", (username,))
        # get result
        res = self.cur.fetchall()
        if res:
            self.id=res[0][0]
            # return result if there is any
            return res[0]
        else:
            # else return none
            return None

    # get Task info function
    def get_all_Tasks(self):
        # select query
        self.cur.execute('Select * from Task where u_id=? order by Task_Date', (self.id,))
        # get data from DB
        res = self.cur.fetchall()
        # return result
        return res

    # get task data for stats
    def get_stats_data(self, date, state):
        # if state is all
        if state != 'All':
            # if state is not Day
            if state != 'Day':
                # get the date in format
                end_date = datetime.strptime(date, '%Y-%m-%d')
                # add seven days
                end_date = end_date + timedelta(days=7)
                # convert the data into string
                end_date = str(end_date.strftime("%Y-%m-%d"))
                print(end_date)
            else:
                # if state is day
                end_date = date
            print(date, end_date)
            # Query for day and week
            self.cur.execute("Select completed, remaining, completed+remaining as total from (SELECT count(status) "
                             "as 'completed' FROM Task where status = 1 and task_date "
                             "BETWEEN ? and ? and u_id=?) join (SELECT count(status) as 'remaining' "
                             "FROM Task where status = 0 and task_date BETWEEN ? and ? and u_id=?); ",
                             (date, end_date, self.id, date, end_date, self.id))
        else:
            # query for All
            self.cur.execute("Select completed, remaining, completed+remaining as total from (SELECT count(status) "
                             "as 'completed' FROM Task where status = 1 and u_id=?) join (SELECT count(status) as 'remaining' "
                             "FROM Task where status = 0 and u_id=?);" , (self.id, self.id))
        res = self.cur.fetchall()
        return res[0]

    # get Completed Task info function
    def get_completed_Tasks(self):
        # select query
        self.cur.execute('Select * from Task where status=1 and u_id=? order by Task_Date', (self.id,))
        # get data from DB
        res = self.cur.fetchall()
        # return result
        return res

    # get daily task
    def get_daily_tasks(self, date):
        # select query
        self.cur.execute('Select * from Task where task_date = ? and status=0 and u_id=?', (date, self.id))
        # get data from DB
        res = self.cur.fetchall()
        # return result
        return res

    # dml queries like insert/update/delete
    def dml_queries(self, operation, details, t_id):
        try:
            # if updating
            if operation == 'update':
                # update query
                self.cur.execute("Update Task set status=? where t_id=?", (1, t_id))
                msg = 'Task Completed successfully'
            # if deleting
            elif operation == 'delete':
                # delete query
                self.cur.execute("Delete from Task where T_id=?", (t_id,))
                msg = 'Task Deleted successfully'
            else:
                # if inserting query
                self.cur.execute("Insert into Task Values (Null, ?, ?, ?, ?, ?, ?, ?, ?)",
                                 (details[0], details[1], details[2], details[3], details[4], details[5], details[6],
                                  self.id))
                msg = 'Task Inserted successfully'
            # save DB
            self.conn.commit()
            return msg
        except Exception as e:
            return str(e)

    # register user function
    def insert_profile(self, data):
        try:
            # update query
            self.cur.execute("Insert into Users Values ( Null, ?, ?, ?)", (data[0], data[1], data[2]))
            # save DB
            self.conn.commit()
            msg = 'User Register successfully'
        except Exception as e:
            msg = str(e)
        return msg
