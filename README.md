
Day 1  24-09-2026 
=================
1.Created a virtual environament to run my project
**python -m venv venv**
2.activated it
**.\venv\Scripts\activate**
3. Installed pydantic,anthropic and .env packages using pip install(like maven install)
**pip install pydantic anthropic python-dotenv**
pydantic is for schema validation kind when I am expecting a json response or sending json requests it helps me validate with schema
anthropic => to connect to claude apis
.env => to store secrets 
4. created a gitingnore file to skip unwanted file commits
venv/ , .env, __pycahce__/  added these 3 to the file
5. created one basic python file hello.py
**print("Environment Working")**
6.Refreshed python basics
datatypes,list,dict,function,class
