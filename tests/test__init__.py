import unittest
import os
import sys
import autodl.__init__
from nose.tools import assert_equal
import mock
import custom_errors
import time

class TestInit(unittest.TestCase):
    """
    test the __init__ functions
    """

    def test_parse_options_error(self):
        sys.argv[1:] = ["useless", "-t", "test"]
        with self.assertRaises(SystemExit):
            autodl.__init__.parse_options()

    def set_env(self):
        os.environ['ODL_CONFIG'] = "test_config"
        os.environ['ODL_USER_SETTINGS'] = "test_user_settings"
        os.environ['ODL_SERVER_IP'] = "test_server_ip"
        os.environ['ODL_SERVER_PORT'] = "test_server_port"
        os.environ['ODL_USER'] = "test_user"
        os.environ['ODL_PASSWORD'] = "test_password"


    def teardown_env(self):
        os.environ.pop('ODL_CONFIG')
        os.environ.pop('ODL_USER_SETTINGS')
        os.environ.pop('ODL_SERVER_IP')
        os.environ.pop('ODL_SERVER_PORT')
        os.environ.pop('ODL_USER')
        os.environ.pop('ODL_PASSWORD')

    def set_args(self):
        sys.argv = []
        sys.argv[1:] = ["useless", "-c", "test_config", "-s", "test_user_settings", "-a", 
                "test_server_ip", "-u", "test_user", "-P", "test_server_port",
                "-p", "test_password"]

    def test_parse_options_with_env_var(self):
        self.set_env()

        sys.argv = []
        result = autodl.__init__.parse_options()
        #print result
        assert_equal(result, {'CONFIG_FILE': 'test_config', 'SERVER_IP': 
            'test_server_ip', 'USER': 'test_user', 'SERVER_PORT': 
            'test_server_port', 'PASSWORD': 'test_password', 
            'USER_SETTINGS_FILE': 'test_user_settings'})
        assert isinstance(result, dict)
        #with self.assertRaises(IOError):
        #    autodl.utils.get_webpage("/tmp/errorpage.html")

        self.teardown_env()

    def test_parse_options_with_args(self):
        self.set_args()
        result = autodl.__init__.parse_options()
        #print result
        assert_equal(result, {'CONFIG_FILE': 'test_config', 'SERVER_IP': 
            'test_server_ip', 'USER': 'test_user', 'SERVER_PORT': 
            'test_server_port', 'PASSWORD': 'test_password', 
            'USER_SETTINGS_FILE': 'test_user_settings'})
        assert isinstance(result, dict)
    
    def test_parse_options_help(self):
        sys.argv = []
        sys.argv[1:] = ["useless", "-h"]
        with self.assertRaises(SystemExit):
            autodl.__init__.parse_options()
    
    def test_parse_options_warnings(self):
        self.set_env()
        self.set_args()

        result = autodl.__init__.parse_options()

        #print result
        assert_equal(result, {'CONFIG_FILE': 'test_config', 'SERVER_IP': 
            'test_server_ip', 'USER': 'test_user', 'SERVER_PORT': 
            'test_server_port', 'PASSWORD': 'test_password', 
            'USER_SETTINGS_FILE': 'test_user_settings'})
        assert isinstance(result, dict)

        self.teardown_env

    def test_set_defaults(self):
        DICT = {'CONFIG_FILE': 'test_config', 'SERVER_IP': 'test_server_ip', 'USER': 'test_user', 'SERVER_PORT': None, 'PASSWORD': 'test_password', 'USER_SETTINGS_FILE': 'test_user_settings'}

        autodl.__init__.set_defaults(DICT)
        #print DICT

        assert_equal(DICT['SERVER_PORT'], '8000')

    def test_set_defaults_err(self):
        DICT = {'CONFIG_FILE': 'test_config', 'SERVER_IP': None, 'USER': 'test_user', 'SERVER_PORT': None, 'PASSWORD': 'test_password', 'USER_SETTINGS_FILE': 'test_user_settings'}

        with self.assertRaises(ValueError):
            autodl.__init__.set_defaults(DICT)

    @mock.patch('time.sleep')
    @mock.patch('autodl.scheduler.Scheduler')
    def test_main(self, sleep, scheduler):
        self.set_env()

        time.sleep.side_effect = custom_errors.ErrorAfter(2)

        scheduler.return_value = 0

        sys.argv = []
        with self.assertRaises(custom_errors.CallableExhausted):
            autodl.__init__.main()

        self.teardown_env    
