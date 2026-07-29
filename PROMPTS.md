# AI Prompts Log

This file contains the complete conversation history and prompts used with AI tools during the development of the Car Dealership Inventory System.

---

## AI Tools Used

- **DeepSeek** — Primary AI assistant for step-by-step implementation
- **Bolt** — Architecture planning and UI design reference
- **Grok** — Initial project guidance, Git workflow, and documentation help

---

## Bolt Conversation

### Initial Prompt to Bolt

TDD Kata: Car Dealership Inventory System
Objective: Design, build, and test a full-stack Car Dealership Inventory System.

Technology Stack:
- Backend: Python, FastAPI, SQLite (SQLAlchemy ORM), JWT (python-jose), passlib + bcrypt, Pydantic, pytest + httpx + pytest-cov
- Frontend: React, TypeScript, Vite, Tailwind CSS, React Router
- Other: Git + GitHub, Swagger UI

Core Requirements:
- User authentication (register/login with JWT)
- Vehicle CRUD (admin-only for create/update/delete)
- Vehicle search by make, model, category, price range
- Purchase vehicles (decrease quantity)
- Restock vehicles (admin only, increase quantity)
- Responsive, visually appealing frontend
- TDD with Red-Green-Refactor pattern

### Bolt's Architecture Plan

Bolt generated the following project structure and implementation plan:

Backend Structure:
- app/core/ — config.py, database.py, security.py
- app/models/ — User and Vehicle models
- app/schemas/ — Pydantic validation schemas
- app/services/ — Business logic (inventory_service.py)
- app/routers/ — auth.py, vehicles.py
- tests/ — conftest.py, test_auth.py, test_vehicles.py, test_inventory.py, test_search.py

Database Design:
- User: id, username, email, hashed_password, is_admin
- Vehicle: id, make, model, category, price, quantity, image_url

API Endpoints:
- POST /api/auth/register, POST /api/auth/login, GET /api/auth/me
- POST/GET /api/vehicles, GET /api/vehicles/search, GET /api/vehicles/{id}
- PUT/DELETE /api/vehicles/{id} (admin)
- POST /api/vehicles/{id}/purchase, POST /api/vehicles/{id}/restock

Frontend Components:
- Navbar, ProtectedRoute, VehicleCard
- LoginPage, RegisterPage, DashboardPage
- EditVehicleModal, RestockModal
- API client, AuthContext

Test Plan:
- 9 auth tests, 13 vehicle CRUD tests, 11 inventory tests, 10 search tests
- Target: 96%+ code coverage

---

## Conversation Log with DeepSeek + Grok

### 1. Project Initialization

Prompt:  
"this is for my interview..please help me out how to approach this and how to do everything from scratch"

Response Summary:  
Provided a structured incremental approach with recommended tech stack (FastAPI + React), TDD workflow, and Git strategy. Recommended starting with backend TDD first, then frontend.

---

### 2. Git and Project Setup

Prompt:  
"I also dont know how to use git...actually I know nothing...please give correct steps like when to commit and how to commit"

Response Summary:  
Step-by-step Git guide from absolute zero covering:
- Installing Git
- git init, git config, git add, git commit, git push
- Creating GitHub repository
- Co-authorship trailers for AI tools
- When to commit (after each small, complete piece of work)

Steps Completed:
- Step 1: Create project folder and git init
- Step 2: Configure Git with name and email
- Step 3: Create README.md, PROMPTS.md, .gitignore
- Step 4: Fill initial files
- Step 5: First commit
- Step 6: Create backend/ and frontend/ folders
- Step 7: Set up Python virtual environment and install dependencies
- Step 8: Create GitHub repo (Txnuu/car-dealership-inventory) and push

---

### 3. Backend Core Files

Prompt: Request for Step 9 (core files)

Files Created:
- app/core/config.py
- app/core/database.py
- app/core/security.py
- app/models/user.py
- app/models/vehicle.py

Commit: feat: add core config, database, security, and models

---

### 4. Schemas and Failing Tests (Red Phase)

Prompt: Request for Step 10

Files Created:
- Pydantic schemas (UserCreate, UserOut, LoginRequest, Token, VehicleCreate, VehicleUpdate, VehicleOut, etc.)
- tests/conftest.py
- tests/test_auth.py (9 tests)

Result: All 9 tests failed with 404 (correct Red phase)

Commit: test: add comprehensive auth tests and fixtures (Red phase)

---

### 5. Auth Implementation (Green Phase)

Prompt: Request for Step 11

Files Updated:
- app/core/config.py
- app/core/database.py
- app/core/security.py
- app/routers/auth.py

Bug Fixed: bcrypt compatibility issue on newer Python versions  
pip install bcrypt==4.2.1

Result: All 9 auth tests passed

Commit: feat: implement auth endpoints (Green phase)

---

### 6. Vehicle, Inventory & Search Tests (Red Phase)

Prompt: Request for Step 12

Files Created:
- tests/test_vehicles.py (13 tests)
- tests/test_inventory.py (11 tests)
- tests/test_search.py (10 tests)

Result: 30 tests failed (correct Red phase)

Commit: test: add comprehensive tests for vehicles, inventory, and search (Red phase)

---

### 7. Inventory Service and Vehicle Router (Green Phase)

Prompt: "give me codes to copy"

Files Created:
- app/services/inventory_service.py
- app/routers/vehicles.py
- Updated app/main.py

Result: All 43 tests passed

Commit: feat: implement vehicles router and inventory service (Green phase)

---

### 8. Missing Endpoint & Coverage

Prompt: "does our backend follow all the instructions....is there something remaining"

Change: Added missing GET /api/vehicles/{id} endpoint

Final Coverage: 96%

Commit: feat: add GET /api/vehicles/:id endpoint - 96% coverage

---

### 9. Frontend Setup

Prompt: Request for Step 15

Commands:
npm create vite@latest . -- --template react-ts
npm install react-router-dom axios lucide-react
npm install -D tailwindcss @tailwindcss/vite

Files Created:
- src/lib/api.ts
- src/context/AuthContext.tsx
- src/App.tsx

Commit: feat: set up frontend with Vite, React, Tailwind, API client and auth context

---

### 10. Frontend Components

Prompt: "ready for pages"

Components Created:
- ProtectedRoute.tsx
- Navbar.tsx
- LoginPage.tsx
- RegisterPage.tsx
- VehicleCard.tsx
- EditVehicleModal.tsx
- RestockModal.tsx
- DashboardPage.tsx

---

### 11. Image URL Feature + UI Improvements

Prompt:  
"in add vehicle option i also want to give an option for add image"  
"This is too simple in terms of creativity......I also want to add images of cars so that it can look more attractive"

Changes:
- Added image_url field to Vehicle model and schemas
- Added image input in Add/Edit forms
- Used Unsplash images for default cars
- Added hero banner and improved card design

Commit: feat: add image_url field, car images, and hero banner

---

### 12. Seed Data Script

Prompt: "I want a car inventory dataset along with images"

Created: seed_data.py with 10 realistic vehicles and Unsplash images

Commit: feat: add seed script with 10 vehicles and images

---

## Summary of AI Usage

| Tool      | Main Contribution                          |
|-----------|--------------------------------------------|
| Bolt      | Architecture, project structure, UI design |
| DeepSeek  | Step-by-step implementation & debugging    |
| Grok      | Git guidance, README & PROMPTS.md help     |

All major commits include proper Co-authored-by trailers for transparency.
