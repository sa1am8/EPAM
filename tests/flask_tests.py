import unittest
import sys
sys.path.insert(1, '/home/toshka/PycharmProjects/EPAM linux/EPAM')
from app.app import app


class BasicTestCase(unittest.TestCase):

    def setUp(self) -> None:
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_123(self):
        pass

if __name__ == '__main__':

    unittest.main()
