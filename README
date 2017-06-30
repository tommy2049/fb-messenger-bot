# This is a template for writing facebook messenger bots using google app engine. 


## **Pre-requisite**

Ensure you have a clean working directory with python2.7 since google cloud platform does not support python 3.6 yet. I recommend using virtualenv to create an isolated environment for python2.7 development. Virtualenv ensures there is no depency issues between python 2.x and 3.x, for more info read up on http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/.

Usually on ubuntu linux, the set up for virtual env goes like this ... 

1. "pip install virtualenv"  
2. "virtualenv -p python2.7 my_project"    This creates a bin dir in the working directory
3. "cd my_project" then "source bin/activate"   Once you activate, a "sandbox" environment is created


## **Instructions on setting up**

1. "git clone https://github.com/tommy1995/fb-messenger-bot" to clone project into your working directory
2. "cd fb-messenger-bot" 
3. install python modules by calling "sudo pip install -t lib -r requirements.txt", this will create a lib directory 
4. in app.yaml file, there is a "PAGE_ACCESS_TOKEN", which you get when you create your facebook page, fill in with your facebook page's page access token
5. assuming your google sdk is installed on your environment, or you're using google cloud shell, run "gcloud app deploy --project my_project_name"
6. when deployed successfully, take your project's url and complete webhook set up on facebook side


## **Customizing Bot's message**

In main.py, modify the content of "process_text" which for now only echoes back whatever the user speaks to it. You might wanna use an nlu library or write a simple function to extract user input's intent and reply with some meaningful messages. 