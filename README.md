# Car Dealership Inventory System

A full-stack Car Dealership Inventory System built as a TDD interview kata.  
Users can browse, search, and purchase vehicles. Admins can fully manage the inventory.

## 🌐 Live Demo

| Service | URL |
|---------|-----|
| **Frontend** | [car-dealership-inventory-one.vercel.app](https://car-dealership-inventory-one.vercel.app) |
| **Backend API** | [car-dealership-api-ytuh.onrender.com](https://car-dealership-api-ytuh.onrender.com) |
| **API Docs** | [Swagger UI](https://car-dealership-api-ytuh.onrender.com/docs) |

## Tech Stack

| Layer            | Technology                            |
|------------------|---------------------------------------|
| Backend          | Python, FastAPI, SQLAlchemy, SQLite   |
| Authentication   | JWT + bcrypt                          |
| Frontend         | React, TypeScript, Tailwind CSS, Vite |
| Testing          | pytest, pytest-cov, httpx             |
| Version Control  | Git + GitHub                          |

## Features

### Authentication
- User registration and login
- JWT-based authentication
- Role-based access (User / Admin)

### Vehicle Management
- View all vehicles in a responsive card layout
- Search & filter by make, model, category, and price range
- Purchase vehicles (stock decreases automatically)
- Purchase button is disabled when quantity is 0

### Admin Features
- Add new vehicles
- Edit existing vehicles
- Delete vehicles
- Restock vehicles

### UI/UX
- Clean and modern design with Tailwind CSS
- Fully responsive (mobile, tablet, desktop)
- Loading states, empty states, and toast notifications

## API Endpoints

### Auth
| Method | Endpoint             | Auth | Description              |
|--------|----------------------|------|--------------------------|
| POST   | `/api/auth/register` | No   | Register a new user      |
| POST   | `/api/auth/login`    | No   | Login and receive JWT    |
| GET    | `/api/auth/me`       | Yes  | Get current user profile |

### Vehicles
| Method | Endpoint                      | Admin | Description             |
|--------|-------------------------------|-------|-------------------------|
| POST   | `/api/vehicles`               | Yes   | Add a new vehicle       |
| GET    | `/api/vehicles`               | No    | List all vehicles       |
| GET    | `/api/vehicles/search`        | No    | Search vehicles         |
| GET    | `/api/vehicles/{id}`          | No    | Get single vehicle      |
| PUT    | `/api/vehicles/{id}`          | Yes   | Update vehicle          |
| DELETE | `/api/vehicles/{id}`          | Yes   | Delete vehicle          |
| POST   | `/api/vehicles/{id}/purchase` | No    | Purchase vehicle        |
| POST   | `/api/vehicles/{id}/restock`  | Yes   | Restock vehicle         |

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Txnuu/car-dealership-inventory.git
cd car-dealership-inventory
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Backend URL: http://localhost:8000  
- Swagger Docs: http://localhost:8000/docs

### 3. Seed Demo Data (Optional)
```bash
python seed_data.py
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

### 5. Create an Admin Account
1. Go to the Register page
2. Fill in the details
3. Check **“Register as admin”**
4. Submit

## Test Report

```
========================= 43 passed in 48.51s =========================
```

| Module         | Tests | Status     |
|----------------|-------|------------|
| Authentication | 9     | All Passed |
| Vehicle CRUD   | 13    | All Passed |
| Inventory      | 11    | All Passed |
| Search         | 10    | All Passed |
| **Total**      | **43**| **100%**   |

**Code Coverage:** 96%

To run the tests yourself:
```bash
cd backend
pytest --cov=app --cov-report=html tests/ -v
```

## My AI Usage

### Tools Used
- **DeepSeek** — Primary AI assistant for backend and frontend implementation
- **Bolt** — Used for architecture planning and UI design reference
- **Grok** — Used for initial project guidance and Git workflow help

### How AI Was Used
- Generated FastAPI models, schemas, routers, and services
- Created comprehensive test suites following TDD (Red → Green → Refactor)
- Helped design and implement the React frontend with TypeScript + Tailwind
- Assisted with debugging, Git commits, and documentation

### Reflection
AI tools significantly accelerated development while still requiring careful review and decision-making. I used AI for boilerplate and repetitive tasks, then focused on understanding the architecture, writing meaningful tests, and polishing the user experience. Every AI-generated piece of code was reviewed before being committed.

All commits include proper `Co-authored-by` trailers for transparency.

## Project Structure

```
car-dealership-inventory/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── routers/
│   │   └── main.py
│   ├── tests/
│   ├── seed_data.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── context/
│   │   └── lib/
│   └── package.json
├── PROMPTS.md
├── test_report.txt
└── README.md
```

## License
This project was built for an interview kata.  
All code is original work augmented by AI tools.