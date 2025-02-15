# Hacklahoma 2025 Project

A web application built for Hacklahoma 2025 using React frontend and Python/LangGraph backend with MongoDB database.

## Project Structure

```
project/
├── frontend/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.tsx
│   └── package.json
│
├── backend/                 # Python backend
│   ├── src/
│   │   ├── config/         # Configuration files
│   │   ├── graphs/         # LangGraph flows
│   │   ├── models/         # Data models
│   │   ├── routes/         # API routes
│   │   └── api/           # API endpoints
│   ├── .env                # Environment variables
│   └── requirements.txt
│
└── README.md
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB installed locally or MongoDB Atlas account

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

3. Configure MongoDB:
   - Create a `.env` file in the backend directory:
     ```
     MONGODB_URL=mongodb://localhost:27017
     DATABASE_NAME=hacklahoma
     ```
   - For MongoDB Atlas, replace the URL with your connection string

### Frontend Setup
1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

### Start MongoDB
1. Local MongoDB:
   ```bash
   mongod
   ```
   Or ensure your MongoDB Atlas cluster is running

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
  - MongoDB
  - Motor (Async MongoDB driver)

## Team Members
[Add team members here]

## License
[Add license information]
