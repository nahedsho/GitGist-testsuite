#
# using python image to build testing environment 
#
FROM python:latest 

#
# declaring build argument and environment varable to be used to save the token and will pass it 
# to the pytest script 
#
ARG utoken="123456789"
ENV utoken=$utoken

#
# installing openjdk for allure reporting plugin 
#
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;

#
# declaring the working directory
#
WORKDIR /testsuite-gist

#
# getting the allure plugin and unzip to WORKDIR
#
RUN wget https://github.com/allure-framework/allure2/releases/download/2.17.3/allure-2.17.3.zip && \
    unzip allure-2.17.3.zip

#
# copying requirements.txt to WORKDIR for preperation to run the code
#
COPY requirements.txt .

#
# install the the needed packaeges that will be used in code 
#
RUN pip install -r requirements.txt

#
# copying the rest file to WORKDIR
#
COPY .  .

#
# opening port to externl usage this port will be used in the allure service
#
EXPOSE 31031

#
# run the all GIST test suite and saving the output in /testreport and running the allure service
#
CMD pytest ./gistest.py -v -rs --token=$utoken --alluredir=./testreport && \
    ./allure-2.17.3/bin/allure serve ./testreport --port 31031