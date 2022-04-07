from requests import request
import pytest
import allure


"""
Class Description : 
    This class has 7 method that implementing the GIST API requests for Github account

Sources:
    https://docs.github.com/en/rest/reference/gists

Dependencies:
    # the method require a token for all GIST API requests, it will be passed as --token arguments

    # Python Frameworks : 
    - requests                 2.27.1 
    - pytest                   7.1.1
    - allure-pytest            2.9.45
    - allure-python-commons    2.9.45

Challenges: 
    there was two challenges in this testing suite that i have to do a workaround
    pytest.mark.skipif((pytest.mugistid == ''),reason="token in invalid"):
        i could use this decorator for that last four method but i it will fail
        cause this pytest decorator will evaluate at the beginning of the test
        execution so the global parameter pytest.mugistid will be empty always,
        so i had to do if condition inside those methods
    pytest.mark.parametrize(pytest.mugistid,code'),[...]:
        i could use this decorator for that last three method but the test
        execution will get pytest.mugistid as empty always, so 
        i had to do ugistid variable to take pytest.mugistid inside those methods
Usage: 
    run the script name using pytest will valid token
    # pytest ./gistest.py --token="your-token" *--alluredir=./testreport
"""


@allure.suite("GIST - Test Suite")
class Test_github_gists:
    token = ''              # it used to save the token
    pytest.mugistid = ''    # it will be used for GIST id

    ################################ Authorization ################################################
    """
        this is a setup method that should check if the token is valid or not.
        if it valid it will continue to the next method and if it not it will skip the other
        methods.
    """
    @allure.step
    @allure.title("Authorizion step")
    @allure.description("Method - will check the validaion of token")
    @pytest.fixture(scope="class", autouse=True)
    def auth(self):
        url = "https://api.github.com/user"
        rheader = {
            "Authorization": "Bearer "+self.token,
            "Accept": "application/vnd.github.v3+json"}
        myres = request("GET", url, headers=rheader)
        if myres.status_code != 200:
            print(myres.status_code)
            print(myres.json()["message"])
            pytest.skip("Your Token is not vaild")
        # print stdout for allure report
        print("using username: "+myres.json()["login"])

    ################################ Listing user gists ###########################################
    """
        this method will get the GISTs list for the spacified used, using the token and 3 paramters 
        dictionary 
            {
                per_page = used for "Results per page"
                since = used for "show notifications updated after the given time"
            }
        code = for checking the return code 
        expected = to check the counting of the nodes in the body
        it has two testcases
            - first testcase will post with valid data
            - second testcase will post with invalid date
    """
    @allure.step
    @allure.title("List GIST step")
    @allure.description("Method - will get list of GISTs in a specific user using token")
    @pytest.mark.parametrize('paramters,code,expected', [({'per_page': '100', 'since': '2022-04-03T14:09:56Z'}, 200, 0), ({'per_page': '500', 'since': '2022-04-30T14:09:56Z'}, 200, -1)])
    def test_getallgistslist(self, paramters, code, expected):
        url = "https://api.github.com/gists"
        rheader = {
            "Authorization": "Bearer "+self.token,
            "Accept": "application/vnd.github.v3+json"}
        myres = request("GET", url, headers=rheader, params=paramters)
        assert myres.status_code == code, "List of GIST didn't get the expected return code"
        assert (len(myres.json()) >
                expected), "didn't get the expected result"
        # print stdout for allure report
        if len(myres.json()) != 0:
            for gist in range(len(myres.json())):
                print("GIST: "+myres.json()[gist]["url"])

    ################################ Creation of a gist ###########################################
    """
        this method will create a new GIST, using the token and 4 paramters 
        description = GIST description
        file =  GIST filename
        content =  GIST content
        code = for checking the return code 
        it has two testcases
            - first testcase will post with valid data
            - second testcase will post with invalid date

        this method will get the created 'gist id' and will load it to > pytest.mugistid  
        and will be used in the following testcases 
    """
    @allure.step
    @allure.title("Create GIST step")
    @allure.description("Method - will create GIST to a specific user using usertoken")
    @pytest.mark.parametrize('description,file,content,code', [("creating gist from API", "testfromapi.txt", "String file contents 1st", 201), ("creating gist from API", "!!@ @@@/", "String file contents", 422)])
    def test_creategist(self, description, file, content, code):
        url = "https://api.github.com/gists"
        rbody = {"description": description,
                 "files":
                 {
                     file:
                     {
                         "content": content
                     }
                 }
                 }

        rheader = {
            "Authorization": "Bearer "+self.token,
            "Accept": "application/vnd.github.v3+json"}
        myres = request("POST", url, headers=rheader, json=rbody)
        assert (myres.status_code == code), "didn't get the expected results"
        if myres.status_code == 201:
            pytest.mugistid = myres.json()['id']
            # print stdout for allure report
            print("created GIST id: " + myres.json()['id'])

    ################################ Edit of an existing gist ######################################
    """
        this method will update exsisting GIST, using the token and 4 paramters and 1 global var
        description = GIST description
        file =  GIST filename
        content =  GIST content
        code = for checking the return code 
        pytest.mugistid  = GIST id
        it has three testcases
            - first testcase will update gist contents for first time
            - second testcase will update gist contents for second time
            - third testcase will test with invalid data
    """
    @allure.step
    @allure.title("Update GIST step")
    @allure.description("Method - will update GIST using gistid and usertoken")
    @pytest.mark.parametrize('description,file,content,code', [("updating the created gist from API", "testfromapi.txt", "replace all the string - 2nd", 200), ("updating the created gist from API for 3nd", "testfromapi.txt", "replace all the string - 3rd", 200),("updating the created gist from API for 2nd time", "testfromapi /", "replace all the string for 3nd time", 422)])
    def test_updategist(self, description, file, content, code):
        if pytest.mugistid != '':
            url = "https://api.github.com/gists/"+pytest.mugistid
            rbody = {"description": description,
                     "files":
                     {
                         file:
                         {
                             "content": content
                         }
                     }
                     }

            rheader = {
                "Authorization": "Bearer "+self.token,
                "Accept": "application/vnd.github.v3+json"}
            myres = request("POST", url, headers=rheader, json=rbody)
            assert myres.status_code == code, "the GIST updated didn't get the expected return code"
        else:
            pytest.skip("there are no GIST ID was empty")

    ################################ Get previous revision of a gist ###############################
    """
        this method will get the previous revision for the created GIST, 
        using the token and 1 paramters and 1 global var 
        ugistid = will take the pytest.mugistid  
        code = for checking the return code 
        it has two testcases
            - first testcase will test with valid data
            - third testcase will test with invalid data

        this method will get the contents from the previous revision of a gist by using another
        request the dependens on 200 code for the first testcase
    """
    @allure.step
    @allure.title("Previous Revision GIST step")
    @allure.description("Method - will get the previous revision of a GIST using gistid and usertoken")
    @pytest.mark.parametrize('ugistid,code', [("valid", 200), ("123456789", 404)])
    def test_getpreviousrevision(self, ugistid, code):
        if ugistid == "valid":
            ugistid = pytest.mugistid
        if ugistid != '':
            url = "https://api.github.com/gists/"+ugistid
            rheader = {
                "Authorization": "Bearer "+self.token,
                "Accept": "application/vnd.github.v3+json"}
            myres = request("POST", url, headers=rheader)
            assert (myres.status_code ==
                    code), "didn't get the expected return code"
            # getting the contents from previous revision
            if myres.status_code == 200:
                if len(myres.json()['history']) > 1:
                    assert (ugistid in myres.json()[
                            'history'][1]["url"]), "failed to get the last revision"
                    revurl = myres.json()['history'][1]["url"]
                    try:
                        myres2 = request("GET", revurl, headers=rheader)
                        getfiles = myres2.json()["files"]
                        for file in getfiles:
                            # print stdout for allure report
                            print("Content from previous revision: " +
                                  getfiles[file]["content"])
                    except:
                        pytest.xfail("fail on getting the previous revision")
        else:
            pytest.skip("your token is not valid")

    ################################ Star a gist ###################################################
    """
        this method will star the created GIST, using the token and 1 paramters and 1 global var 
        ugistid = will take the pytest.mugistid  
        code = for checking the return code 
        it has two testcases
            - first testcase will test with valid data
            - third testcase will test with invalid data
    """
    @allure.step
    @allure.title("Star GIST step")
    @allure.description("Method - will STAR GIST using gistid and usertoken")
    @pytest.mark.parametrize('ugistid,code', [("valid", 204), ("123456789", 404)])
    def test_stargist(self, ugistid, code):
        if ugistid == "valid":
            ugistid = pytest.mugistid
        if ugistid != '':
            url = "https://api.github.com/gists/"+ugistid+"/star"
            rheader = {
                "Authorization": "Bearer "+self.token,
                "Accept": "application/vnd.github.v3+json"}
            myres = request("PUT", url, headers=rheader)
            assert (myres.status_code ==
                    code), "adding a star for GIST was failed - didn't get the expected return code"
            # print stdout for allure report
            if myres.status_code == 204:
                print("GIST id: " + pytest.mugistid +
                      " was STAR-ed successfully")
        else:
            pytest.skip("your token is not valid")

    ################################ Delete a gist ##################################################
    """
        this method will deleted the created GIST, using the token and 1 paramters and 1 global var 
        ugistid = will take the pytest.mugistid  
        code = for checking the return code 
        it has two testcases
            - first testcase will test with valid data
            - third testcase will test with invalid data
    """
    @allure.step
    @allure.title("Delete GIST step")
    @allure.description("Method - will delete GIST using gistid and usertoken")
    @pytest.mark.parametrize('ugistid,code', [("valid", 204), ("123456789", 404)])
    def test_deletegist(self, ugistid, code):
        if ugistid == "valid":
            ugistid = pytest.mugistid
        if ugistid != '':
            url = "https://api.github.com/gists/"+ugistid
            rheader = {
                "Authorization": "Bearer "+self.token,
                "Accept": "application/vnd.github.v3+json"}
            myres = request("DELETE", url, headers=rheader)
            assert (myres.status_code ==
                    code), "deleting a GIST was failed - didn't get the expected return code"
            # print stdout for allure report
            if myres.status_code == 204:
                print("GIST id : "+pytest.mugistid+" was Deleted successfully")

        else:
            pytest.skip("your token is not valid")
