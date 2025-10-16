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


# 🧪 Code Review

---

## 🌐 CORS Configuration
The backend should allow CORS requests from `localhost` to enable smooth local development and prevent browser-related blocking issues during testing.

---

## ❌ Incorrect Status Code on Missing Resource
- **Issue:** The `/answer/{answer_id}` endpoint currently returns a `200` status code even when the resource is not found.  
- **Expected Behavior:** Return a `404 Not Found` status code for missing resources to align with REST best practices.

---

## 🧭 Path Validations
Add proper path validations for both `answer_id` and `question_id` to:
- Ensure data integrity  
- Reduce invalid requests hitting the backend  
- Provide clearer error messages to the frontend

---

## ⚡ Inefficient Data Fetching
- **Current:** The application fetches **all answers** and then filters them on the frontend by `question_id`.  
- **Problem:** This impacts performance, especially as data grows.  
- **Recommendation:** Filter answers **on the backend** and return only relevant data to the client.

---

## 🏗️ Backend Structure
The current structure can be improved by separating:
- Routers  
- Models  
- Schemas  

**Benefits:**  
- Improved readability  
- Easier maintenance  
- Better scalability for future features

---

## 🧠 Separate Classes for Operations
Introduce separate classes (e.g., `Read` and `Create`) to better organize operations and keep logic modular.

---

## 📬 Proper Status Code on Creation
When creating new resources:
- **Current:** Returns `200 OK`
- **Expected:** Return `201 Created` to clearly indicate a successful creation.

---

## ✍️ Input Validation
- **Issue:** Submitting a question with only spaces still triggers the submit action, leading to empty records.  
- **Recommendation:** Add input validation on **both frontend and backend** to prevent invalid data submissions.

---

## 🧭 Frontend Routing Issue
The **Answer page** currently displays a `404 Not Found` error. This should be addressed to improve user navigation and experience.

---

## 🌐 Server-Side Rendering (SSR)
Currently, questions and answers are loaded **client-side only**. Moving this logic to **server-side rendering** will:
- Improve performance  
- Enhance SEO  
- Provide faster initial page loads

---

## 🛣️ Route Structure
- **Current:** `/answer/{id}`  
- **Recommended:** `/question/{id}/answers`  

This structure more accurately reflects the relationship between questions and their answers, following RESTful principles.

---

## 🔄 Answer Refresh Bug
The answer refresh functionality on the frontend is **inconsistent** and sometimes fails to fetch updated data. This needs:
- Debugging the current implementation  
- Implementing a more reliable refresh mechanism

---

## 🧹 Code Cleanup
Some **unused code** exists inside `layout` and `homepage` components. This should be cleaned up or refactored to reduce clutter and improve maintainability.

---

## 📝 Note
I have already implemented fixes for many of the issues listed above.  
Please review my improvements and share any additional feedback or suggestions.




# 🚀 Improvements & Next Steps – Polling App


## 🧪 Testing & Code Quality

- ✅ **Backend API Tests**  
  Implement unit and integration tests for all backend routes and business logic to ensure reliability and catch regressions early.

- ✅ **Frontend Tests**  
  Expand frontend test coverage to include:
  - UI interactions
  - Edge cases (e.g., empty states)

 **Frontend Tweeks**  
  - Add env files and add API variable 

## 📄 Data Loading & Performance

- 🧭 **Load More / Pagination**  
  Add “Load More” or pagination functionality for **questions** and **answers** to improve performance and avoid fetching large datasets unnecessarily.

---

## 🎨 UI/UX Enhancements

- ✨ **Improved Styling & Layouts**  
  Enhance the visual design, responsiveness, and component consistency for a polished look and feel.

- 🧭 **Better UX Flows**  
  Streamline the navigation between questions and answers to minimize friction.

- 💬 **Empty & Loading States**  
  Add friendly placeholders for no data, skeleton loaders, and error states to make the experience feel more dynamic and intentional.

---

## 📝 Content Management Features

- ✏️ **Edit & Delete**  
  Allow users (or admins) to edit and delete questions and answers after submission.

- 🗑️ **Soft Deletes & Undo**  
  Implement soft deletes with a short “undo” window to prevent accidental deletions.

---

## 📊 Advanced Features


- 🧠 **Multiple Question Types**  
  Support more question formats beyond open text:
  - Multiple Choice
  - Rating Scales
  - Word Clouds
  - Yes/No or True/False

---

## 🧰 Backend

- 📡 **API Versioning**  
  Introduce versioned APIs (e.g., `/api/v1`) to prepare for future expansions without breaking existing clients.

---