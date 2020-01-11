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
