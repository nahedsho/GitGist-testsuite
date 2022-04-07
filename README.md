# Test-Suite for GIST API

This is a TestSuite that will test the GIST API for following scenarios: 
- Listing user gists
- Creation of a gist
- Edit of an existing gist
- Get previous revision of a gist
- Star a gist
- Delete a gist

Those tests are shipped as a Docker image.

___
## Quick start
1. Start a Docker container with your github personal token 

```bash
docker run -p 31031:31031 -e utoken='yourToken' nahedsh/testsuite-gist
```

2. Go to http://localhost:31031 to see the allure report for all the testcases 

3. That's it! 

## Files 

- Dockerfile : 
    this file includes the step for buiding an docker image and it includes the 
    testing script 
- requirements.txt :
    this file include the needed python pacakges that the script rely on
- conftest.py : 
    this script file it all about taking the command line argument and passing it 
    to the main testing script
- gistest.py: 
    this is the main script file it include all the methods that testing the above 
    scenarios