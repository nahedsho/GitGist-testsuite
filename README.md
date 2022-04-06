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