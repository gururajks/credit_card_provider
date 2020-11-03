import unittest
from account import Account


class TestAccount(unittest.TestCase):

    def setUp(self) -> None:
        self.test_account = Account(None, None)

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
