import unittest
from Functions.Arrival import setup


class LoginTest(unittest.TestCase):

    def test(self):
        setup()
    # TODO: Take out the hard-coded path


if __name__ == "__main__":
    unittest.main()