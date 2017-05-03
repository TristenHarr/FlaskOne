import unittest
from Functions.Arrival import *

class LoginTest(unittest.TestCase):

    def test(self):
        x = make_password("stuff")
        y = check_password("stuff", x)
        self.assertTrue(y)

# if __name__ == "__main__":
#     unittest.main()