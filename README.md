# Hacklahoma 2025 Project

A web application built for Hacklahoma 2025 using React frontend and Python/LangGraph backend.

## Project Structure

```
project/
├── frontend/                 # React frontend
│   ├── public/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.tsx
│   └── package.json
│
├── backend/                 # Python backend
│   ├── src/
│   │   ├── graphs/         # LangGraph flows
│   │   ├── api/           # API endpoints
│   │   └── models/        # Data models
│   └── requirements.txt
│
└── README.md
```

## Setup & Installation

### Backend Setup
1. Set up Python virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup
1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

### Start Backend Server
```bash 
cd backend
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
uvicorn main:app --reload
```

### Start Frontend Server
```bash
cd frontend
npm run dev
```

## Technologies Used
- Frontend:
  - React
  - TypeScript
  - Vite
  - Axios
- Backend:
  - Python
  - FastAPI
  - LangGraph
  - LangChain

## Team Members
[Add team members here]

## License
[Add license information]
