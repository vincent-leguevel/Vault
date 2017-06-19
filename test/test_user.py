import unittest, user


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = user.User('test','dc240e026e6688c2e48e0a7a3d9ab39127e6c3fb117f0e3a36b5d5bc1b44f36e:ab6ffb87ec614d60a9c50b2f20d2c935')

    def test_should_not_instantiate(self):
        with self.assertRaises(ValueError):
            test = user.User(1, 'password')

    def test__should_get_name(self):
        print "should get name", self.user._get_name()
        self.assertEqual(self.user._get_name(), 'test')

    def test__should_set_name(self):
        self.user._set_name('test1')
        self.assertEqual(self.user._get_name(), 'test1')

    def test__should_not_set_name(self):
        with self.assertRaises(ValueError):
            self.user._set_name(1)

    def test__should_get_password(self):
        with self.assertRaises(KeyError):
            password = self.user._get_password()


    def test__should_verify_password(self):
        print self.user.verify_password('password')
        self.assertTrue(self.user.verify_password('password'))


    def test__should_not_verify_password(self):
        self.assertFalse(self.user.verify_password('password1'))

    def test__should_set_password(self):
        self.user._set_password('password1')
        self.assertTrue(self.user.verify_password('password1'))

    def test_should_connect(self):
        self.assertTrue(self.user.connect('test', "password"))

    def test_should_not_connect_password(self):
        self.assertTrue(self.user.connect('test', "password1"))


    def test_should_not_connect_username(self):
        self.assertTrue(self.user.connect('test1', "password"))


if __name__ == '__main__':
    unittest.main()
