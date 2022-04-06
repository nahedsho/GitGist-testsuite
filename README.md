# Docker image rapid7-testsuite
==========================
this image will test the GIST API requests options 



## Quick start
1. Start a Docker container with your github personal token 

```bash
docker run -p 31031:31031 -e utoken='yourToken' nahedsh/testsuite-gist
```

2. go to http://localhost:31031 to see the allure report for all the testcases 

3. That's it! 