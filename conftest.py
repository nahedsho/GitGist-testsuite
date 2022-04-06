def pytest_addoption(parser):
    parser.addoption('--token', action='append', help='token that will be used for testing')

def pytest_generate_tests(metafunc):
    try: 
        cmdtoken  = metafunc.config.getoption("token")
        metafunc.cls.token = cmdtoken[0]
    except:
        print("No Token has been provided")