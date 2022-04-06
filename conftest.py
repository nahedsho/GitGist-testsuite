################################ pytest_addoption ################################################
"""
        this is a setup method will parse the --token argument from the cmd line and append it to 
        metafunc 
"""
def pytest_addoption(parser):
    parser.addoption('--token', action='append', help='token that will be used for testing')

################################ pytest_generate_tests ###########################################
"""
        this is a setup method that will read the metafunc option and search for a spacific 
        argumnet in our case is the 'token' and then it will load it to token variable as 
        a global var
"""
def pytest_generate_tests(metafunc):
    try: 
        cmdtoken  = metafunc.config.getoption("token")
        metafunc.cls.token = cmdtoken[0]
    except:
        print("No Token has been provided")