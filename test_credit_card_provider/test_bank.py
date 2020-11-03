import unittest


class BankTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_bank = Bank()

    def test_create_account(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
