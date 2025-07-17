# Poll Code Challenge

A full-stack poll application built with **Svelte** (frontend) and **FastAPI** (backend).

## Features

- Create and manage Questions
- See Answers to Questions

## Tech Stack

- **Frontend:** [Svelte](https://svelte.dev/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)


## Run & Develop

See:
 - **Frontend:** [Readme](./fe/README.md)
 - **Backend:** [Readme](./be/README.md)



# Code Challenge Solution:

## Backend:
 - Add CORS Middleware
 - Fix error status code 200 to 404
 - Create Visits put endpoint


## Frontend:
 - Use env variable and .env file instead of hardcoded BE url. 
 - Cleanup unused code from `fe/src/routes/+page.svelte`
 - Create Answers page which list all answers
 - Remove `event.preventDefault()` in handleSubmit as it is already added as decorator to the `on:submit`
 - Improve UI styles for answers and questions page. 
 - Log visits on Answers page
 - Added question to the answers page for more clarity. 
 - Added key to each loops


## Potential Improvements:
 - Create an endpoint to get answers by question Id instead of getting all answers and filter on the FE. 
 - Better error handling and loading state
 - Use store to handle the questions & answers
 - Create the page with visits counts 


## Note: 
 - The output here is the result of 2 crash courses for Svelte and FastAPI as I didn't had opportunity to work with them before.
