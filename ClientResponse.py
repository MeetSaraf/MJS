"""
    Class -  Client Handler.
    Used pandas dataframe to save sessions.
"""

from shutil import rmtree
import os
import time
import pandas as pd


class ClientResponse():
    """
    Class Client Handler

    Attributes:
    -----------------
        username : str
            username

        is_login : bool
            User login status.

        login_session_data : pandas dataframe
            Registered user passwords and privileges.

        logged_users : pandas dataframe
            Logged in users.

        client_directory : str
            current subdirectory

    Methods:
    -----------------
        load_session_data():
            Sync the pandas dataframes with session.

        get_response(request):
            Return proper response of command request.

        commands():
            Return list of commands.

        login_valid(user):
            Set user to logged in.

        get_password(user):
            Return password from server data.

        login(username, password):
            Login.

        quit():
            Logout.

        list():
            List of all files and folders.

        change_folder(directory):
            Change folder to desired directory.

        read_file(path):
            Read a specified file.

        write_file(path, data):
            Write file with data.

    """
    def __init__(self):
        """
            Initialize needed variables
        """
        self.username = None
        self.is_login = False
        self.login_session_data = None
        self.logged_users = None
        self.load_session_data()
        self.client_directory = None
        self.read_file_index = {}
        self.char_count = 100

    def load_session_data(self):
        """
            Load a session data
        """
        self.login_session_data = pd.read_csv("serverSession/users.csv")
        self.logged_users = pd.read_csv("serverSession/loginUsers.csv")

    def get_response(self, request):
        """
            Get response of specified command.

            Return : str
                Response
        """
        self.load_session_data()
        if str(self.username) not in self.login_session_data['username'].tolist():
            self.quit()
        request = request.rstrip("\n").rstrip(" ").lstrip(" ")
        if request.split(" ")[0] == "commands":
            return self.commands()
        if request.split(" ")[0] == "register":
            if len(request.split(" ")) == 4:
                return self.register(request.split(" ")[1], request.split(" ")[2], request.split(" ")[3])
            return "Are you sure you typed correct command?"
        if request.split(" ")[0] == "quit":
            return self.quit()
        if request.split(" ")[0] == "logout":
            return self.quit()
        if request.split(" ")[0] == "login":
            if len(request.split(" ")) == 3:
                return self.login(request.split(" ")[1], request.split(" ")[2])
            return "Are you sure you typed correct command?"
        if request.split(" ")[0] == "list":
            return self.list()
        if request.split(" ")[0] == "change_folder":
            if len(request.split(" ")) == 2:
                return self.change_folder(request.split(" ")[1])
            return "Are you sure you typed correct command?"
        if request.split(" ")[0] == "read_file":
            if len(request.split(" ")) == 1:
                return self.reset_read_file()
            return self.read_file(request.split(" ")[1])
        if request.split(" ")[0] == "write_file":
            if len(request.split(" ")) >= 2:
                return self.write_file(request.split(" ")[1], " ".join(request.split(" ")[2:]))
            return "Are you sure you typed correct command?"
        if request.split(" ")[0] == "create_folder":
            if len(request.split(" ")) == 2:
                return self.create_folder(request.split(" ")[1])
            return "Are you sure you typed correct command?"
        if request.split(" ")[0] == "delete":
            if len(request.split(" ")) == 2:
                return self.delete(request.split(" ")[1], request.split(" ")[2])
            return "Are you sure you typed correct command?"
        return "Are you sure you typed correct command?"

    def commands(self):
        """
            Return all commands.

            Return : str
                Commands
        """
        commands = ["commands\n", "View all commands\n",
                    "login <username> <password>\n", "Log in with <username> and <password>\n",
                    "register <username> <password> <privileges>\n", "Register with the <username> <password> and <privileges>.\n",
                    "list\n", "Get all directory details.\n",
                    "change_folder <name>\n", "Change directory to <name>\n",
                    "read_file <name>\n", "Print 100 characters from file <name>.\n",
                    "write_file <name> <input>\n", "Write data in <input> to end of file <name> in current directory\n",
                    "create_folder <name>\n", "Create a new folder with <name> in current directory\n",
                    "delete <username> <password>\n", "Delete the user with <username> from server. (Only for admins).\n",
                    "logout\n", "Logout the user.\n",
                    "quit\n", "Logout and quit"
                    ]

        response = ""
        count = 0
        while True:
            oneline = "".join([commands[count], commands[count+1]])
            response += "~~~~~~\n" + oneline
            count += 2
            if count == len(commands):
                break
        return response
   
    def login_valid(self, user):
        """
            Set login as valid for user.
        """
        self.is_login = True
        self.username = user
        self.client_directory = ""
        temp = pd.DataFrame(columns=['username'])
        temp['username'] = [user]
        self.logged_users = self.logged_users.append(temp)
        self.logged_users.to_csv("serverSession/loginUsers.csv", index=False)


    def get_password(self, user):
        """
            Get password from session data for user.

            Return : str
                password of user
        """
        return str(self.login_session_data.loc[self.login_session_data['username'] == user, 'password'].iloc[0])


    def login(self, user, password):
        """
            Login

            Return : str
                response
        """
        self.load_session_data()
        if self.is_login:
            return "\nAlready logged in"
        if user not in self.login_session_data['username'].tolist():
            return "\nUsername not registered"
        if password != self.get_password(user):
            return "\nWrong password!"
        if user in self.logged_users['username'].tolist():
            return "\nLogged in from different IP"
        self.login_valid(user)
        return "\nLogin completed."

    def quit(self):
        """
            Quit command.

            Return : str
                Response
        """
        try:
            if self.username in self.logged_users['username'].tolist():
                temp_list = self.logged_users['username'].tolist().remove(self.username)
                self.logged_users['username'] = temp_list
                self.logged_users.to_csv("serverSession/loginUsers.csv", index=False)
            self.client_directory = ""
            self.is_login = False
            self.username = None
            self.read_file_index = {}
            return "\nSigned out"
        except KeyError:
            return "\nSigned out"


    def register(self, user, password, privileges):
        """
            Registers a new user by saving its data in server session.

            Return : str
                Response
        """
        if user in self.login_session_data['username'].tolist():
            return "\nUsername not available"
        if user == "" or password == "" or privileges == "":
            return "\nYou cannot register empty user"
        temp = pd.DataFrame(columns=['username'])
        temp['username'] = [user]
        temp['password'] = password
        if privileges.lower() == 'admin':
            temp['isAdmin'] = 1
        else:
            temp['isAdmin'] = 0
        self.login_session_data = self.login_session_data.append(temp)
        self.login_session_data.to_csv("serverSession/users.csv", index=False)
        self.load_session_data()
        os.mkdir(os.path.join("data", user))
        return "\nRegistered user successfully."

    def get_privilege(self, username):
        """
            Get privileges of user.

            Return : int
                1 if user is admin , else 0.
        """
        return int(self.login_session_data.loc[self.login_session_data['username'] == username, 'isAdmin'].iloc[0])

    def delete(self, user, password):
        """
            Delete user from the server database.
            If user is logged in from other machine, he/she will be logged out.
            If user if self, then it logs out self too.

            Return : str
                Response
        """
        self.load_session_data()
        if not self.is_login:
            return "\nYou need to login."
        if self.get_privilege(self.username) != 1:
            return "\nYou should be admin."
        if user not in self.login_session_data['username'].tolist():
            return "\nNo user with username " + user + " found"
        if password != self.get_password(self.username):
            return "\nYou have entered wrong password"
        temp = pd.DataFrame(columns=['username', 'password', 'isAdmin'])
        for user_loop, pass_loop, privi_loop in zip(self.login_session_data['username'].tolist(), self.login_session_data['password'].tolist(), self.login_session_data['isAdmin'].tolist()):
            if user_loop != user:
                temp2 = pd.DataFrame(columns=['username', 'password', 'isAdmin'])
                temp2['username'] = [user_loop]
                temp2['password'] = pass_loop
                temp2['isAdmin'] = privi_loop
                temp = temp.append(temp2)
        temp.to_csv("serverSession/users.csv", index=False)
        self.load_session_data()
        if user == self.username:
            self.quit()
        user_path = os.path.join("data", user)
        rmtree(user_path)
        return "\nDeleted user with username " + user + " successfully"
