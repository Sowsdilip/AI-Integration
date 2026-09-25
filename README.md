
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

Day 2 25-09-2026
================

1. create a .env file to import secrets from an environment file instead of hardcoding in code

2.**Pydantic deep dive**
- Explored lax type coercion (`"10000.00"` silently becomes `10000` for an `int` field) vs `StrictInt`, 
  which rejects that instead — relevant for validating LLM-extracted data later
- Learned `EmailStr` validation via `pydantic[email]`
- Clarified: Python doesn't support constructor overloading like Java — one `__init__` per class; 
  use default arguments or `@classmethod` alternates instead
- Clarified: `class X(BaseModel)` is inheritance (like Java's `extends`); pydantic auto-generates `__init__` 
  from declared fields, similar to Lombok's `@AllArgsConstructor`
- Discussed how production Python teams enforce discipline Java gets for free: mypy/pyright for type 
  checking, `__slots__` to block dynamic attributes, dataclasses/pydantic as the default over bare classes, 
  linters (ruff/pylint) in CI

3.**Setup**
- Created Claude Console account (separate from claude.ai chat), added prepaid credit, set a monthly 
  spend limit under Settings → Limits, created a **Default**-scope API key, stored it in `.env`

4.  **Debugging (the real learning today)**
- Fixed a `.env` file that was accidentally named `key.env` — python-dotenv expects the literal filename `.env`
- Hit a broken venv: prompt showed `(venv)` as active, but `python`/`pip` still pointed to the global install. 
  Root-caused it with `sys.executable` and `where python`/`where pip`, then recreated the venv from scratch
- Learned: don't trust the `(venv)` prompt alone — verify with `python -c "import sys; print(sys.executable)"`
