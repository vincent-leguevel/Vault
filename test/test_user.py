import unittest, user


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = user.User('test','password')

    def test_should_not_instantiate(self):
        with self.assertRaises(ValueError):
            user.User(1)


    def test__should_set_name(self):
        self.user.name = 'test1'

        self.assertEqual(self.user.name, 'test1')

    def test__should_not_set_name(self):
        with self.assertRaises(ValueError):
            self.user.name = 1

    def test__get_name(self):
        print self.user.name
        self.assertTrue(self.user.name == 'test')

    def test__set_password(self):
        self.fail()

    def test__get_password(self):
        self.fail()

    def test_connect(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
