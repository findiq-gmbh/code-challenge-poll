# Running a FastAPI Project with `uv`

[uv](https://github.com/astral-sh/uv) is a fast Python package manager and runner. To run a FastAPI project using `uv`, follow these steps after installing uv:

```bash
    uv run fastapi run
    source .venv/bin/activate
```


## Find as many backend and frontend bugs as possible 
### Backend
- Import: Unused imports
  - Any/Union, found with the new added python linter "[Ruff package](https://github.com/astral-sh/ruff)"

- Question & Answer: Model
    - **To discuss:** "text" could mean everything, we should go more specific, like question_title or something.
    - **Required:** i strongly recommed of adding a strict limitation of the allowed length of the fields.
    - **Optional:** i recommend to add a description to the fields, so if you only have a look into the database, you can read those descriptions within the structure. Ofc. for self explained fields it doesn't add any values, but i added as a example for now
    - field "id"
      - **Hint:** Depending on the target database, later a "unsigned" could makes sense. To give more room for the unsigned numbers. As this is not a language default (and not supported directly by sqlmodel), i would skip this for now.
      - To discuss: It could make sense to use a UUId instead of a int. [UUID-Documentation](https://sqlmodel.tiangolo.com/advanced/uuid/).
    - field "text": does not need to have a index, as we don't search it

- "Database engine creation"
  - **Required:** variable "`sqlite_url`" and "`sqlite_file_name`"
    - It does make sense to bring both variables together and name it to a more generic name "database_url".
      - As you do not know, if you maybe layter want to work again a MySQL Database Server. So a file does not exists there.
   - It does make sense  to make the new variable "`database_url`" configurable from the outer. So it gives flexibility which database i want to use. E.g. in production i want to use mysql, or for a testing environment, which maybe doesn't want to touch the existing database file for the developers normal environment.
  - **Required:** `on_startup` -> `create_db_and_tables`, there should be a wrapper, that a creation is only required in development & testing environments. On production, we work with "migrations", e.g. so that it is possible to rollback database changes if a new application code creating issues and a rollback of it is required.
  - **Required:** `@app.on_event("startup")` [deprecated](https://fastapi.tiangolo.com/advanced/events/#alternative-events-deprecated), if we introduce new code, we should use the newest options. We have to use lifespans instead.
  - **Required**: Connection handling, in general, if you open a connection you have to close it. There are limitations by the database, or underlaying operating system (how much can be opened). Those you don't have in control. Depending on the app usage and configuration, it could be get quick out of control with open and not closed connections and you could potentially run in those limits. As we use a connection pool, with engine & session, we have to close the session after a request was performed. And we have to close the connection pool of the engine after the application was closed.
   - Possible that session close is not required, because maybe the dependency management close the connection on destruct. I do not have that deep knowledge in python, sqlmodel, fastapi
-  Router/Controller/Actions however you name it :D
   - **Required**: REST Routes
     - It's best practise to name paths [like a collection](https://restfulapi.net/resource-naming/).
     - It's not common of having a ending slash.
   - **Required:** I strongly recommend to seperate the models from the underlaying storage (database) models. So having at the end database models/entities and Request & Response models.
     - If a develeoper extend the models, e.g. by the user ip, it will now print out the personal information for every user.
       - Additional to that, on the request side, a change will touch the api interface so clients can potential break.
       - It blocks you, to collect informations from different databaseses and apis. You are always be bounded to the database itself.
       - If you add a validation to the models, it should not be part of the database models. That should happened before, because maybe there are different cases for validations.
   - **Required:** `def read_questions(`
    - as we get a list of questions back, the variable should be named to `questions`
   - **Optional:** HTTPException
     -  It could make sense to add keys to the exception throws & rendinering. So that a error mapping and translation by the frontend is easier
   -  **Question:** `def read_answers(`
      - Is there a reason  why not returning direct "`return answer`"?
  - **Required:**  `def read_answer(`, wrong http status code
    - In the http exception, the status could should be `404`  and not `200`
- Testing
  - We should have tests, so that we know we get what we expect. As we do not have that high service complexity i recommend to start with [api tests](https://fastapi.tiangolo.com/de/tutorial/testing/).
- Architecture
  - As good starting point for a new application with that feature complexity a easy [MVC] makes sense(https://martinfowler.com/eaaCatalog/modelViewController.html)
  - I would also recommend that structure, until we have more use cases and more domain logic
    - Folder structure
      - Controller
      - Model
      - [Repository](https://martinfowler.com/eaaCatalog/repository.html)
      - Enum
      - test
    - With the new structure, everything is a little abstract. But thats fine for the moment, as we do not want to develop more than we need. We will have a look later, how we want proceed architecture wise.
    - Later it could be helpful, of having a `src` folder and `test` folder on the backend root level. But i will not change it for now.
- Clean Code
  - Numbers
    -  If you refer to numbers it's always better to give it a name, do unterstand what that magic number means. In our case, there is a http status code 404. So either using a constant, enum or variable for that. Its always good to have a look into the library or framework, if they deliver already such constants
-  Not now:
   - Later it could make sense to adjust the CORS settings.
- Documentation
  - It's helpful to have more enhanced openapi description, for the models and endpoint itself


## What was not completed?
 - Not all api tests are completd
 - No unit tests exists
 - As i got currently import problems, i could not realy test, have to fix it first. But no time left for that :)
 - Frontend was not checked