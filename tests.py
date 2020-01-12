import unittest
import sys
import unittest
import random
import string
import pandas as pd
from clientResponse import ClientResponse


def random_folder(string_length=6):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))

def init_login():
    temp = pd.DataFrame(columns=['username'])
    temp['username'] = ['test']
    temp['password'] = ['123']
    temp['isAdmin'] = 1
    return temp

def reset_login():
    reset_login = pd.DataFrame(columns=['username'])
    reset_login.to_csv("serverSession/loginUsers.csv", index=False)

class ClientResponseClassTestingStepTwo(unittest.TestCase):
    """Handles the tests for login and listing the files"""

    def test_ClientResponse_login(self):
        """
        This test will check login.
        Test1 : Wrong password
        Test2 : Wrong username
        Test3 : Proper login
        """
        test_class = ClientResponse()
        test_class.login_session_data = init_login()
        expected_results = ["\nWrong password!", "\nUsername not registered", "\nLogin completed."]
        results = []
        tests = [
            ["test", "1234"],
            ["test2", "123"],
            ["test", "123"]
        ]

        for test in tests:
            results.append(test_class.login(
                test[0], test[1]))
        test_class.quit()
        reset_login()

        self.assertListEqual(results, expected_results)

    def test_ClientResponse_list(self):
        """
        This test will check list command.
        Test1 : Listing without login.
        Test2 : Listing folder for user test
        """
        results = []
        expected_results = ["\nCan you login first?"]
        test_class = ClientResponse()
        test_class.login_session_data = init_login()
        results.append(test_class.list())
        test_class.login("test", "123")
        results.append(test_class.list())
        test_class.quit()
        reset_login()

        self.assertListEqual([results[0]], expected_results)
        self.assertIn("testfolder1", results[1])
        
     class ClientResponseClassTestingStepOne(unittest.TestCase):
    """Handles the test for command and quit response"""

    def test_commands_response(self):
        """
        This test will check whether ClientResponse responds commands.
        """

        test_class = ClientResponse()

        output = test_class.commands()

        test_class.quit()
        reset_login()

        self.assertTrue(output)

    def test_commands_quit(self):
        """
        This test will check quit response.
        """
        expected_results = ["\nSigned out"]
        results = []

        test_class = ClientResponse()

        results.append(test_class.quit())
        reset_login()

        self.assertListEqual(results, expected_results)

class ClientResponseClassTestingStepThree(unittest.TestCase):
    """Handles the tests to check response for change folder and create folder"""

    def test_ClientResponse_change_folder(self):
        """
        This test will check response for change folder.
        Test1 : Change folder without login.
        Test2 : Wrong directory change.
        Test3 : Proper directory change.
        """
        results = []
        expected_results = ["\nCan you login first?", "\nWrong directory name.", "\nChanged directory to testfolder1 successfully"]
        test_class = ClientResponse()
        test_class.login_session_data = init_login()
        results.append(test_class.change_folder("testfolder1"))
        test_class.login("test", "123")
        results.append(test_class.change_folder("testfolder2"))
        results.append(test_class.change_folder("testfolder1"))
        test_class.quit()
        reset_login()

        self.assertListEqual(results, expected_results)

    def test_ClientResponse_create_folder(self):
        """
        This test will check response for create folder.
        Test1 : Create already present directory.
        Test2 : Proper directory with random name.
        """
        results = []
        expected_results = ["\nDirectory Already Present", "\nSuccess."]
        test_class = ClientResponse()
        test_class.login_session_data = init_login()
        test_class.login("test", "123")
        results.append(test_class.create_folder("testfolder1"))
        test_class.change_folder("testfolder1")
        results.append(test_class.create_folder("test" + random_folder()))
        test_class.quit()
        reset_login()

        self.assertListEqual(results, expected_results)
        
        
        class ClientResponseClassTestingStepFour(unittest.TestCase):
    """Handles the final part of the tests inculting tests for read and write the files"""

    def test_ClientResponse_read_file(self):
        """
        This test will check read file.
        Test1 : Read the non existing file.
        Test2 : Proper read file.
        """
        results = []
        expected_results = ["\nFile not found.", "\nCommand - read_file from 0 to 100 are - \nDontChangeThisContent"]
        test_class = ClientResponse()
        test_class.login_session_data = init_login()
        test_class.login("test", "123")
        test_class.change_folder("testfolder1")
        results.append(test_class.read_file("test_read2.txt"))
        results.append(test_class.read_file("test_read.txt"))
        test_class.quit()
        reset_login()

        self.assertListEqual(results, expected_results)
