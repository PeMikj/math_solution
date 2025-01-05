# math_solver
Multiagent solver for math problems with given answers. Can generate new paths for your problem.



Sprint 1: Project Setup & Minimal API
Backend Tasks

    Initialize Repository & Environments
        Create a Git repo.
        Set up Python virtual environment.
        Choose a framework (e.g., FastAPI) and create a skeleton project.
    Minimal Endpoint
        Implement /ping or /health endpoint to confirm the server is running.
        Return a JSON response like {"status": "ok"}.
    Dockerization (Optional Minimal)
        Create a Dockerfile that installs dependencies and runs FastAPI.
        Optionally create a docker-compose.yml with at least the backend service.

End-of-Sprint Deliverable

    A running container (or local dev) with a minimal FastAPI backend and a React (or Vue) frontend that can ping the backend and display a response.

Sprint 2: User Auth & Problem Submission (With Known Answer)
Backend Tasks

    Database Setup
        Pick a DB (Postgres, SQLite for dev).
        Create tables:
            User (id, username, hashed_password, created_at).
            Problem (id, user_id, problem_text, known_answer, status, created_at).
    User Registration & Login
        Implement endpoints:
            POST /register – create user.
            POST /login – returns JWT or session cookie.
        Use a library like passlib for hashing passwords.
    Authenticated Submission
        POST /problems – user submits a problem text and the known answer (as a string or numeric field).
        Store in DB with status = “pending” or “unattempted”.
        Protect this endpoint so only logged-in users can submit.

Instructions (for LLMs or devs)

    Create a User model with SQLAlchemy (or your ORM).
    Implement password hashing (e.g., passlib).
    Implement an auth dependency in FastAPI, e.g., @router.post("/login") returning a JWT.
    Implement POST /problems that inserts a record into the DB with problem_text, known_answer.

Frontend Tasks

    Auth UI
        Create a Registration page and a Login page.
        Store JWT/token in local storage (or cookies) after login.
    Problem Submission Form
        A form with fields: problem_text and known_answer.
        A submit button that POSTs to /problems (include auth token).

Instructions (for LLMs or devs)

    Create Register.jsx and Login.jsx components with forms.
    Use fetch/axios to POST to /register and /login, storing the JWT in localStorage.
    Create NewProblem.jsx with fields for text and known answer, POST to /problems with the JWT in the header (Authorization: Bearer <token>).

End-of-Sprint Deliverable

    A user can register, log in, submit a problem with a known answer.
    Problems are stored in the DB, with each record associated with a user.

Sprint 3: Single-Agent Solver (Iterative) — Basic Structure
Backend Tasks

    Single-Agent Endpoint
        Add a background function or service that attempts to solve the problem once.
        For now, can be a dummy “echo” solver or a simple LLM call (e.g., to ChatGPT).
    Iteration Logic
        After a new problem is created, immediately attempt to solve it (synchronously or via a queue like Celery).
        Compare the solver’s output with known_answer.
        If correct, set status = "solved".
        If incorrect, keep track of an attempt_count. If attempt_count < max_tries, try again.
            For now, keep it simple (like up to 3 tries) in a loop.
    Storing Attempts
        Create a ProblemAttempt table (problem_id, attempt_number, proposed_solution, correctness, timestamp).
        Each time the solver tries, store the result here.

Instructions (for LLMs or devs)

    Implement an attempt_solve_problem(problem_id) function that:
        Fetches the problem from DB.
        Calls a dummy or LLM-based solver, returns a string solution.
        Compares solution to problem.known_answer.
        Inserts a record into ProblemAttempt.
        If correct, update problem.status = "solved"; else increment attempt_count and re-try if under threshold.

Frontend Tasks

    Problem List & Status
        Create a page that lists all problems the user has submitted, including status (solved or failed or in-progress).
    Attempts View
        When user clicks a problem, show the attempts: proposed solution, correctness, attempt time.

Instructions (for LLMs or devs)

    Create ProblemList.jsx to fetch from GET /problems and display.
    Create ProblemDetails.jsx to fetch from GET /problems/{id}/attempts and display each attempt’s data.

End-of-Sprint Deliverable

    After a user submits a problem with known answer, a single agent tries to solve it up to N times (e.g., 3).
    The user can see the attempts in the UI and whether it eventually matched the known answer.Sprint 1: Project Setup & Minimal API
Backend Tasks

    Initialize Repository & Environments
        Create a Git repo.
        Set up Python virtual environment.
        Choose a framework (e.g., FastAPI) and create a skeleton project.
    Minimal Endpoint
        Implement /ping or /health endpoint to confirm the server is running.
        Return a JSON response like {"status": "ok"}.
    Dockerization (Optional Minimal)
        Create a Dockerfile that installs dependencies and runs FastAPI.
        Optionally create a docker-compose.yml with at least the backend service.

Instructions (for LLMs or devs)

    Create a new FastAPI app called app.py.
    Add the /ping route returning "status": "ok".
    Create a Dockerfile based on python:3.10-slim, install dependencies from requirements.txt, expose port 8000.

Frontend Tasks

    Initialize Frontend
        Use React, Vue, or similar.
        Create a minimal page with a “Ping server” button to test the backend.
    API Call
        On button click, call the /ping endpoint.
        Display the JSON response on the page.

Instructions (for LLMs or devs)

    Create a React app via create-react-app.
    Create a component PingTest.jsx that fetches from http://localhost:8000/ping and shows the result.

End-of-Sprint Deliverable

    A running container (or local dev) with a minimal FastAPI backend and a React (or Vue) frontend that can ping the backend and display a response.

Sprint 2: User Auth & Problem Submission (With Known Answer)
Backend Tasks

    Database Setup
        Pick a DB (Postgres, SQLite for dev).
        Create tables:
            User: id, username, hashed_password, created_at.
            Problem: id, user_id, problem_text, known_answer, status, created_at.

    User Registration & Login
        Implement endpoints:
            POST /register: Create user.
            POST /login: Return JWT or session cookie.
        Use passlib for hashing passwords.

    Authenticated Problem Submission
        POST /problems: Submit problem_text and known_answer.
            Store in DB with status = "pending" or "unattempted".
            Protect the endpoint so only logged-in users can submit problems.

Frontend Tasks

    Auth UI
        Create Registration and Login pages.
        Store JWT/token in local storage (or cookies) after login.

    Problem Submission Form
        Create a form with fields:
            problem_text
            known_answer
        Submit button POSTs to /problems (include auth token).

End-of-Sprint Deliverable

    A user can:
        Register, log in, and submit a problem with a known answer.
        Problems are stored in the DB, with each record associated with a user.

Sprint 3: Improved Navigation, Problem Submission, and History
Backend Tasks

    Task History Endpoint
        GET /user/problems:
            Fetch all problems submitted by the logged-in user.

    Redirect After Login
        Update the /login endpoint or frontend logic to transition users to the task submission page.

    User-Centric Filters
        Add filtering to /problems for user-specific queries:
            Example: GET /problems?user_id=<id>.

Frontend Tasks

    Automatic Redirect After Login
        Automatically transition users to the task submission screen after successful login.

    Task History Page
        Create a TaskHistory.jsx component:
            Fetch and display user-specific problems with:
                Problem text.
                Status (solved, in-progress, failed).
            Link to view problem details.

    Enhanced Navigation
        Add navigation options for:
            Submit Task: Redirects to task submission form.
            Task History: Redirects to history page.

End-of-Sprint Deliverable

    After login, users are automatically redirected to the task submission page.
    Users can view their task history, including problem statuses and details.

Sprint 4: Single-Agent Solver (Iterative) — Basic Structure
Backend Tasks

    Single-Agent Endpoint
        Add a background function or service that attempts to solve the problem once:
            For now, use a dummy solver or a simple LLM call (e.g., ChatGPT).

    Iteration Logic
        After a new problem is created, immediately attempt to solve it (synchronously or via a queue like Celery).
        Compare the solver's output with known_answer.
        Update problem.status:
            If correct: solved.
            If incorrect: Retry up to max_tries (e.g., 3 attempts).

    Storing Attempts

        Create a ProblemAttempt table:
            problem_id, attempt_number, proposed_solution, correctness, timestamp.

        Each solver attempt should create a record here.

Frontend Tasks

    Problem List & Status
        Create a page that lists all problems submitted by the user, including their statuses.

    Attempts View
        When a user clicks on a problem, show all attempts:
            Proposed solution.
            Correctness.
            Timestamp.

End-of-Sprint Deliverable

    A single agent tries to solve a user-submitted problem up to N times (e.g., 3).
    Users can:
        View all their problems with statuses.
        See detailed attempts for each problem.
