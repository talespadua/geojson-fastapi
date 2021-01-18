# FastAPI + MongoDB + GeoJson
Playing a bit with this stack


## How to run it:

Having docker and make installed, run the project with:  
`make env/raise`

With this, the server will run locally on port `8080`.

You can shutdown the server using  

`make env/shutdown`

## How to test it:

### After raising the infrastructure, you can run the test using:
  
`make test`

### To run specific tests:

`make test-single test=<test_path>`

where `<test_path>` is the path for the test, module or folder you want to test

### To run all QA Pipeline, with linter and type checking:

`make pipeline/qa`

This will run [Black](https://black.readthedocs.io/en/stable/), [Flake8](https://flake8.pycqa.org/en/latest/), [Mypy](http://mypy-lang.org/) and the test suite

### To seed DB and play a bit:

`make env/db/seed`

### To drop db

`make env/db/drop`

## API docs and Swagger

After running the server, go to `/docs` for Swagger and `/redoc` for Redoc

This project should be easily deployed with the Dockerfile provided
