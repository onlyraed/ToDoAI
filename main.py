<<<<<<< HEAD
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from plyer import filechooser
import matplotlib.pyplot as plt
from Database import DB
from datetime import datetime

# calling database class
db = DB()


# login screen class
class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        pass

    # check login
    def Check_login(self):
        S_user = ''
        S_pass = ''
        # getting text from text fields
        L_user = self.ids.Username.text
        L_pass = self.ids.Password.text
        # if fields values not empty
        if L_user != '' or L_pass != '':
            # get data from database check user data
            res = db.get_user(L_user.upper())
            # if data found
            if res is not None:
                # store data in variables
                S_user = res[1]
                S_pass = res[2]
            # if filed and db data match username
            if L_user.upper() == S_user.upper():
                # if filed and db data match password
                if S_pass == L_pass:
                    # empty password field
                    self.ids.Password.text = ''
                    # access MainPage and add "Hi User"
                    self.parent.get_screen('MainPage').ids.username.text = f"Hi {L_user.upper()} !"
                    # change screen to MainPage
                    self.parent.current = 'MainPage'
                else:
                    # if password field is incorrect
                    toast("Password is incorrect")
            else:
                # if username field is incorrect
                toast("Invalid Username")
        else:
            # # if username and password field is null
            toast("Username and Password Can't be Null")


# Register Class
class Registration(Screen):
    def __init__(self, **kwargs):
        super(Registration, self).__init__(**kwargs)

    # function for clearing fields
    def Registration_clear(self):
        self.ids.R_Username.text = ''
        self.ids.R_Password.text = ''
        self.ids.Confirm_password.text = ''
        self.ids.Email.text = ''

    # Check registration function
    def Check_registration(self):
        # get data from text fields
        user = self.ids.R_Username.text
        pw = self.ids.R_Password.text
        cpw = self.ids.Confirm_password.text
        email_f = self.ids.Email.text
        # if username is not empty and username is greater equal to 4 words
        if user != '' and len(user) >= 4:
            # if password is not empty and password is greater equal to 4 words and pass and confirm pass match
            if pw == cpw and (pw != '' and cpw != '') and len(pw) >= 4:
                # store user info in list
                data = [user.upper(), pw, email_f]
                # insert data in db by calling insert profile function
                msg = db.insert_profile(data)
                # Clear fields
                self.Registration_clear()
                # show success or error message
                toast(msg)
            # if password len is less the 4 words
            elif len(pw) < 4:
                toast("Password must have at least 4 words")
            # if password and confirm password not match
            else:
                toast("Password and Confirm Password Not matched")
        # if username len is less the 4 words
        elif len(user) < 4:
            toast("Username must contain 3 alphabet empty")
        # if username is empty
        else:
            toast("Username field cannot be empty")


# Main Screen class
class MainPage(Screen):
    # variables for kv file
    date = StringProperty()
    greeting = StringProperty()
    today_total_tasks = StringProperty()

    # call function when Main screen open
    def on_enter(self, *args):
        # clear task list area field
        self.ids.task_list.clear_widgets()
        # get timer function
        self.timer()
        # get current date
        now = datetime.now()
        # get hours
        time = now.hour
        # if hours is less than 12
        if time < 12:
            self.greeting = 'Good Morning !'
        # if hours is between than 12  and 18
        elif 12 <= time < 18:
            self.greeting = 'Good Afternoon !'
        # if hours is between than 18 and 22
        elif 18 <= time < 22:
            self.greeting = 'Good Evening!'
        # if hours greater then 22
        else:
            self.greeting = 'Good Night!'

        # convert date format
        date = str(now.strftime('%Y-%m-%d'))
        # Schedule Interval for timer function with 1 sec
        Clock.schedule_interval(self.timer, 1.0)
        # color list
        color = ['red', 'gold', 'green']
        # get data from db
        data = db.get_daily_tasks(date)
        # show total task label on GUI
        self.today_total_tasks = f'You have {len(data)} tasks today...'
        # loop through data
        for i in data:
            # task range is MID
            if i[4] == 'Mid':
                selected_color = color[1]
            # task range is HIGH
            elif i[4] == 'High':
                selected_color = color[0]
            # task range is low
            else:
                selected_color = color[2]
            # create a list view with task name
            self.task = Task_View(text=f'{i[1]}', color=selected_color)
            # bind on press with show detail function
            self.task.bind(on_press=lambda x, i=i: self.show_detail(i))
            # show list on GUI
            self.ids.task_list.add_widget(self.task)

    # show detail function
    def show_detail(self, data):
        # format variable
        self.format = f" [b]Task Name:[/b] {data[1]}\n\n " \
                      f"[b]Task Date:[/b] {data[2]}\n\n " \
                      f"[b]Task Range:[/b] {data[3]} \n\n" \
                      f" [b]Task Level:[/b] {data[4]} \n\n " \
                      f"[b]Task Quote:[/b] {data[5]} " \
                      f"\n\n [b]Image:[/b]"
        # access detail page
        self.detail_page = self.manager.get_screen('Task_detail')
        # set format text on GUI
        self.detail_page.ids.detail.text = self.format
        # set task id
        self.detail_page.ids.task_id.text = str(data[0])
        # show image on GUI
        self.detail_page.ids.task_img.source = data[6]
        # switch screen to Task detail
        self.manager.current = 'Task_detail'

    # timer function
    def timer(self, *args):
        # get current date and time
        now = datetime.now()
        # change format
        now = now.strftime('%A - %d %B, %Y %I:%M:%S %p')
        # date variable equal to new date and time
        self.date = str(now)

    # which option user select from side menu (All task or complete task)
    def which_option(self, option):
        # access all task page
        self.all_tasks_page = self.manager.get_screen('all_task')
        # set title
        self.all_tasks_page.ids.bar_title.title = f"{option} Task's"
        # change screen
        self.manager.current = 'all_task'


# Task Screen class
class TaskPage(Screen):
    # constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # variables
        self.range = None
        self.level = None

    # add task function
    def add_task(self):
        # get values from text fields
        name = self.ids.task_name.text
        date = self.ids.task_date.ids.text_field.text
        quote = self.ids.quote.text
        image_path = self.ids.attach_image.source
        # if name and date is not empty
        if name != '' and date != '':
            # insert data in db
            msg = db.dml_queries('inserting', [name, date, self.range, self.level, quote, image_path, 0], None)
            # show success or error msg
            toast(msg)
            # clear field's data
            self.clear_data()
        else:
            # if name and date is empty
            toast("Task Name or Date can't be null")

    # clear fields function
    def clear_data(self):
        self.ids.task_name.text = ''
        self.ids.task_date.ids.text_field.text = ''
        self.ids.quote.text = ''
        self.ids.attach_image.source = ''

    # on leave screen
    def on_leave(self, *args):
        self.range = None
        self.level = None

    # get task range and level
    def set_range_level(self, value, state):
        # if state equal to range
        if state == 'range':
            self.range = value
        # if it's level
        else:
            self.level = value

    # browser file function
    def file_browser(self):
        try:
            filechooser.open_file(on_selection=self.selected)
        except NotImplemented:
            pass

    # if image select call this function
    def selected(self, select):
        if select is not None:
            self.ids.attach_image.source = select[0]


# Task Detail Screen
class TaskDetailPage(Screen):
    # Complete or delete task function
    def task_completed_or_delete(self, state):
        # get task id
        task_id = self.ids.task_id.text
        # update or delete task from db
        msg = db.dml_queries(state, None, task_id)
        # show success or error msg
        toast(msg)
        self.manager.current='MainPage'

# all task Screen
class All_Tasks(Screen):
    # call this function when this screen open
    def on_enter(self, *args):
        # clear show task area field
        self.ids.show_task_area.clear_widgets()
        # get title
        title = self.ids.bar_title.title
        # get all task data from database
        data = db.get_all_Tasks()
        # get completed task data from database
        c_data = db.get_completed_Tasks()
        # if title is all Task's
        if title == "All Task's":
            # call load_tasks function
            self.load_tasks(data)
        else:
            # call load_tasks function
            self.load_tasks(c_data)

    # load task function
    def load_tasks(self, data):
        # if data found
        if data:
            # loop with data
            for cnt, row in enumerate(data):
                # convert date
                date = datetime.strptime(row[2], '%Y-%m-%d')
                date = date.strftime('%A %d-%b')
                # get task name
                task_name = row[1]
                # get task range
                task_range = row[4]
                # if range is HIGH
                if task_range == 'High':
                    color = '#f05951'
                # if range is MID
                elif task_range == 'Mid':
                    color = 'gold'
                # if range is Low
                else:
                    color = '#81e691'
                # if current record date and previous date not same
                if row[2] != data[cnt - 1][2]:
                    # add label
                    self.label = MDLabel(text=str(date), theme_text_color='Custom',
                                         text_color='#654eb6', bold=True)
                    # show it on GUI
                    self.ids.show_task_area.add_widget(self.label)
                    # add Line
                    self.ids.show_task_area.add_widget(MDSeparator())
                # add Task card with color
                self.card = Task_Card(text=task_name, color=color)
                # bind on press function with show detail
                self.card.bind(on_press=lambda x, i=row: self.show_detail(i))
                # show card on GUI
                self.ids.show_task_area.add_widget(self.card)
        else:
            # if now data found
            toast('No Task Found...')

    # function show detail
    def show_detail(self, data):
        # format variable
        self.format = f" [b]Task Name:[/b] {data[1]}\n\n " \
                      f"[b]Task Date:[/b] {data[2]}\n\n " \
                      f"[b]Task Range:[/b] {data[3]} \n\n" \
                      f" [b]Task Level:[/b] {data[4]} \n\n " \
                      f"[b]Task Quote:[/b] {data[5]} " \
                      f"\n\n [b]Image:[/b]"
        # access task detail page
        self.detail_page = self.manager.get_screen('Task_detail')
        # set format text
        self.detail_page.ids.detail.text = self.format
        # get task id
        self.detail_page.ids.task_id.text = str(data[0])
        # show Image
        self.detail_page.ids.task_img.source = data[6]
        # switch Task detail Screen
        self.manager.current = 'Task_detail'


# Task stats class
class Task_Stats(Screen):

    # stats function
    def stats(self, state):
        # getting current date
        current_date = datetime.now()
        # changing format
        current_date = current_date.strftime("%Y-%m-%d")
        # x values for graph
        x = ['Completed', 'Remaining', 'Total']
        # y values from database.py file by calling get_stats_data
        y = db.get_stats_data(current_date, state)
        print(y)
        # if total tasks not 0
        if y[2] != 0:
            # getting chart area on GUI from kv file
            bar_graph = self.ids.chart
            # clearing existing graph
            bar_graph.clear_widgets()
            plt.close()
            # creating bar graph
            plt.bar(x, y, color='#654eb6')
            # adding y label
            plt.ylabel('Task Qty')
            # adding graph
            bar_graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            # adding result of complete, remaining, total tasks
            self.format = f"{state} info\n\nCompleted ({y[0]})\n\n Remaining ({y[1]})\n\nTotal ({y[2]})"
            self.ids.info.text = self.format
        else:
            # if no task data found
            toast("No Task's Found")

    # call function when leave this screen
    def on_leave(self, *args):
        # clear chart area and format text to empty
        self.ids.chart.clear_widgets()
        self.ids.info.text = ''

# customized widgets classes
# for Show task in MainPage
class Task_View(OneLineAvatarListItem):
    text = StringProperty()
    color = StringProperty()


# for adding textfield with Icon in add Task page
class TextFieldWithIcon(MDRelativeLayout):
    icon = StringProperty()
    hint_text = StringProperty()


# for adding Radio buttons in add Task page
class RadioButton(MDBoxLayout):
    text = StringProperty()
    group = StringProperty()


# # for adding task in color card in all & Competed Task's page
class Task_Card(MDCard):
    text = StringProperty()
    color = StringProperty()


# ScreenManager class for managing screens
class Screen_Manager(ScreenManager):
    sm = ScreenManager()


# Main App Class that control App
class Taskmain(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field = None

    # function which will build app
    def build(self):
        db.create_database_structure()
        return Builder.load_file("main.kv")

    # call function when user select date
    def on_date_select(self, instance, value, date_range):
        print(instance, value, date_range)
        self.field.text = str(value)

    # call when you did not select any date and press cancel button
    def on_cancel(self, instance, value):
        self.field.text = ''

    # date picker function
    def show_date_picker(self, field):
        # get filed
        self.field = field
        # create date picker
        date_dialog = MDDatePicker(primary_color='#654eb6', selector_color='#654eb6', text_button_color='#654eb6')
        # bind function on ok and cancel button
        date_dialog.bind(on_save=self.on_date_select, on_cancel=self.on_cancel)
        # open date picker
        date_dialog.open()

    # function for switch to Main Page
    def home_page(self):
        self.root.current = 'MainPage'


# run app
if __name__ == '__main__':
    Taskmain().run()
=======
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from plyer import filechooser
import matplotlib.pyplot as plt
from Database import DB
from datetime import datetime

# calling database class
db = DB()


# login screen class
class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        pass

    # check login
    def Check_login(self):
        S_user = ''
        S_pass = ''
        # getting text from text fields
        L_user = self.ids.Username.text
        L_pass = self.ids.Password.text
        # if fields values not empty
        if L_user != '' or L_pass != '':
            # get data from database check user data
            res = db.get_user(L_user.upper())
            # if data found
            if res is not None:
                # store data in variables
                S_user = res[1]
                S_pass = res[2]
            # if filed and db data match username
            if L_user.upper() == S_user.upper():
                # if filed and db data match password
                if S_pass == L_pass:
                    # empty password field
                    self.ids.Password.text = ''
                    # access MainPage and add "Hi User"
                    self.parent.get_screen('MainPage').ids.username.text = f"Hi {L_user.upper()} !"
                    # change screen to MainPage
                    self.parent.current = 'MainPage'
                else:
                    # if password field is incorrect
                    toast("Password is incorrect")
            else:
                # if username field is incorrect
                toast("Invalid Username")
        else:
            # # if username and password field is null
            toast("Username and Password Can't be Null")


# Register Class
class Registration(Screen):
    def __init__(self, **kwargs):
        super(Registration, self).__init__(**kwargs)

    # function for clearing fields
    def Registration_clear(self):
        self.ids.R_Username.text = ''
        self.ids.R_Password.text = ''
        self.ids.Confirm_password.text = ''
        self.ids.Email.text = ''

    # Check registration function
    def Check_registration(self):
        # get data from text fields
        user = self.ids.R_Username.text
        pw = self.ids.R_Password.text
        cpw = self.ids.Confirm_password.text
        email_f = self.ids.Email.text
        # if username is not empty and username is greater equal to 4 words
        if user != '' and len(user) >= 4:
            # if password is not empty and password is greater equal to 4 words and pass and confirm pass match
            if pw == cpw and (pw != '' and cpw != '') and len(pw) >= 4:
                # store user info in list
                data = [user.upper(), pw, email_f]
                # insert data in db by calling insert profile function
                msg = db.insert_profile(data)
                # Clear fields
                self.Registration_clear()
                # show success or error message
                toast(msg)
            # if password len is less the 4 words
            elif len(pw) < 4:
                toast("Password must have at least 4 words")
            # if password and confirm password not match
            else:
                toast("Password and Confirm Password Not matched")
        # if username len is less the 4 words
        elif len(user) < 4:
            toast("Username must contain 3 alphabet empty")
        # if username is empty
        else:
            toast("Username field cannot be empty")


# Main Screen class
class MainPage(Screen):
    # variables for kv file
    date = StringProperty()
    greeting = StringProperty()
    today_total_tasks = StringProperty()

    # call function when Main screen open
    def on_enter(self, *args):
        # clear task list area field
        self.ids.task_list.clear_widgets()
        # get timer function
        self.timer()
        # get current date
        now = datetime.now()
        # get hours
        time = now.hour
        # if hours is less than 12
        if time < 12:
            self.greeting = 'Good Morning !'
        # if hours is between than 12  and 18
        elif 12 <= time < 18:
            self.greeting = 'Good Afternoon !'
        # if hours is between than 18 and 22
        elif 18 <= time < 22:
            self.greeting = 'Good Evening!'
        # if hours greater then 22
        else:
            self.greeting = 'Good Night!'

        # convert date format
        date = str(now.strftime('%Y-%m-%d'))
        # Schedule Interval for timer function with 1 sec
        Clock.schedule_interval(self.timer, 1.0)
        # color list
        color = ['red', 'gold', 'green']
        # get data from db
        data = db.get_daily_tasks(date)
        # show total task label on GUI
        self.today_total_tasks = f'You have {len(data)} tasks today...'
        # loop through data
        for i in data:
            # task range is MID
            if i[4] == 'Mid':
                selected_color = color[1]
            # task range is HIGH
            elif i[4] == 'High':
                selected_color = color[0]
            # task range is low
            else:
                selected_color = color[2]
            # create a list view with task name
            self.task = Task_View(text=f'{i[1]}', color=selected_color)
            # bind on press with show detail function
            self.task.bind(on_press=lambda x, i=i: self.show_detail(i))
            # show list on GUI
            self.ids.task_list.add_widget(self.task)

    # show detail function
    def show_detail(self, data):
        # format variable
        self.format = f" [b]Task Name:[/b] {data[1]}\n\n " \
                      f"[b]Task Date:[/b] {data[2]}\n\n " \
                      f"[b]Task Range:[/b] {data[3]} \n\n" \
                      f" [b]Task Level:[/b] {data[4]} \n\n " \
                      f"[b]Task Quote:[/b] {data[5]} " \
                      f"\n\n [b]Image:[/b]"
        # access detail page
        self.detail_page = self.manager.get_screen('Task_detail')
        # set format text on GUI
        self.detail_page.ids.detail.text = self.format
        # set task id
        self.detail_page.ids.task_id.text = str(data[0])
        # show image on GUI
        self.detail_page.ids.task_img.source = data[6]
        # switch screen to Task detail
        self.manager.current = 'Task_detail'

    # timer function
    def timer(self, *args):
        # get current date and time
        now = datetime.now()
        # change format
        now = now.strftime('%A - %d %B, %Y %I:%M:%S %p')
        # date variable equal to new date and time
        self.date = str(now)

    # which option user select from side menu (All task or complete task)
    def which_option(self, option):
        # access all task page
        self.all_tasks_page = self.manager.get_screen('all_task')
        # set title
        self.all_tasks_page.ids.bar_title.title = f"{option} Task's"
        # change screen
        self.manager.current = 'all_task'


# Task Screen class
class TaskPage(Screen):
    # constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # variables
        self.range = None
        self.level = None

    # add task function
    def add_task(self):
        # get values from text fields
        name = self.ids.task_name.text
        date = self.ids.task_date.ids.text_field.text
        quote = self.ids.quote.text
        image_path = self.ids.attach_image.source
        # if name and date is not empty
        if name != '' and date != '':
            # insert data in db
            msg = db.dml_queries('inserting', [name, date, self.range, self.level, quote, image_path, 0], None)
            # show success or error msg
            toast(msg)
            # clear field's data
            self.clear_data()
        else:
            # if name and date is empty
            toast("Task Name or Date can't be null")

    # clear fields function
    def clear_data(self):
        self.ids.task_name.text = ''
        self.ids.task_date.ids.text_field.text = ''
        self.ids.quote.text = ''
        self.ids.attach_image.source = ''

    # on leave screen
    def on_leave(self, *args):
        self.range = None
        self.level = None

    # get task range and level
    def set_range_level(self, value, state):
        # if state equal to range
        if state == 'range':
            self.range = value
        # if it's level
        else:
            self.level = value

    # browser file function
    def file_browser(self):
        try:
            filechooser.open_file(on_selection=self.selected)
        except NotImplemented:
            pass

    # if image select call this function
    def selected(self, select):
        if select is not None:
            self.ids.attach_image.source = select[0]


# Task Detail Screen
class TaskDetailPage(Screen):
    # Complete or delete task function
    def task_completed_or_delete(self, state):
        # get task id
        task_id = self.ids.task_id.text
        # update or delete task from db
        msg = db.dml_queries(state, None, task_id)
        # show success or error msg
        toast(msg)
        self.manager.current='MainPage'

# all task Screen
class All_Tasks(Screen):
    # call this function when this screen open
    def on_enter(self, *args):
        # clear show task area field
        self.ids.show_task_area.clear_widgets()
        # get title
        title = self.ids.bar_title.title
        # get all task data from database
        data = db.get_all_Tasks()
        # get completed task data from database
        c_data = db.get_completed_Tasks()
        # if title is all Task's
        if title == "All Task's":
            # call load_tasks function
            self.load_tasks(data)
        else:
            # call load_tasks function
            self.load_tasks(c_data)

    # load task function
    def load_tasks(self, data):
        # if data found
        if data:
            # loop with data
            for cnt, row in enumerate(data):
                # convert date
                date = datetime.strptime(row[2], '%Y-%m-%d')
                date = date.strftime('%A %d-%b')
                # get task name
                task_name = row[1]
                # get task range
                task_range = row[4]
                # if range is HIGH
                if task_range == 'High':
                    color = '#f05951'
                # if range is MID
                elif task_range == 'Mid':
                    color = 'gold'
                # if range is Low
                else:
                    color = '#81e691'
                # if current record date and previous date not same
                if row[2] != data[cnt - 1][2]:
                    # add label
                    self.label = MDLabel(text=str(date), theme_text_color='Custom',
                                         text_color='#654eb6', bold=True)
                    # show it on GUI
                    self.ids.show_task_area.add_widget(self.label)
                    # add Line
                    self.ids.show_task_area.add_widget(MDSeparator())
                # add Task card with color
                self.card = Task_Card(text=task_name, color=color)
                # bind on press function with show detail
                self.card.bind(on_press=lambda x, i=row: self.show_detail(i))
                # show card on GUI
                self.ids.show_task_area.add_widget(self.card)
        else:
            # if now data found
            toast('No Task Found...')

    # function show detail
    def show_detail(self, data):
        # format variable
        self.format = f" [b]Task Name:[/b] {data[1]}\n\n " \
                      f"[b]Task Date:[/b] {data[2]}\n\n " \
                      f"[b]Task Range:[/b] {data[3]} \n\n" \
                      f" [b]Task Level:[/b] {data[4]} \n\n " \
                      f"[b]Task Quote:[/b] {data[5]} " \
                      f"\n\n [b]Image:[/b]"
        # access task detail page
        self.detail_page = self.manager.get_screen('Task_detail')
        # set format text
        self.detail_page.ids.detail.text = self.format
        # get task id
        self.detail_page.ids.task_id.text = str(data[0])
        # show Image
        self.detail_page.ids.task_img.source = data[6]
        # switch Task detail Screen
        self.manager.current = 'Task_detail'


# Task stats class
class Task_Stats(Screen):

    # stats function
    def stats(self, state):
        # getting current date
        current_date = datetime.now()
        # changing format
        current_date = current_date.strftime("%Y-%m-%d")
        # x values for graph
        x = ['Completed', 'Remaining', 'Total']
        # y values from database.py file by calling get_stats_data
        y = db.get_stats_data(current_date, state)
        print(y)
        # if total tasks not 0
        if y[2] != 0:
            # getting chart area on GUI from kv file
            bar_graph = self.ids.chart
            # clearing existing graph
            bar_graph.clear_widgets()
            plt.close()
            # creating bar graph
            plt.bar(x, y, color='#654eb6')
            # adding y label
            plt.ylabel('Task Qty')
            # adding graph
            bar_graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            # adding result of complete, remaining, total tasks
            self.format = f"{state} info\n\nCompleted ({y[0]})\n\n Remaining ({y[1]})\n\nTotal ({y[2]})"
            self.ids.info.text = self.format
        else:
            # if no task data found
            toast("No Task's Found")

    # call function when leave this screen
    def on_leave(self, *args):
        # clear chart area and format text to empty
        self.ids.chart.clear_widgets()
        self.ids.info.text = ''

# customized widgets classes
# for Show task in MainPage
class Task_View(OneLineAvatarListItem):
    text = StringProperty()
    color = StringProperty()


# for adding textfield with Icon in add Task page
class TextFieldWithIcon(MDRelativeLayout):
    icon = StringProperty()
    hint_text = StringProperty()


# for adding Radio buttons in add Task page
class RadioButton(MDBoxLayout):
    text = StringProperty()
    group = StringProperty()


# # for adding task in color card in all & Competed Task's page
class Task_Card(MDCard):
    text = StringProperty()
    color = StringProperty()


# ScreenManager class for managing screens
class Screen_Manager(ScreenManager):
    sm = ScreenManager()


# Main App Class that control App
class Taskmain(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field = None

    # function which will build app
    def build(self):
        db.create_database_structure()
        return Builder.load_file("main.kv")

    # call function when user select date
    def on_date_select(self, instance, value, date_range):
        print(instance, value, date_range)
        self.field.text = str(value)

    # call when you did not select any date and press cancel button
    def on_cancel(self, instance, value):
        self.field.text = ''

    # date picker function
    def show_date_picker(self, field):
        # get filed
        self.field = field
        # create date picker
        date_dialog = MDDatePicker(primary_color='#654eb6', selector_color='#654eb6', text_button_color='#654eb6')
        # bind function on ok and cancel button
        date_dialog.bind(on_save=self.on_date_select, on_cancel=self.on_cancel)
        # open date picker
        date_dialog.open()

    # function for switch to Main Page
    def home_page(self):
        self.root.current = 'MainPage'


# run app
if __name__ == '__main__':
    Taskmain().run()
