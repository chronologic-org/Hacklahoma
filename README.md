# Hacklahoma 2025 Project

A web application built for Hacklahoma 2025 using React frontend and Python/LangGraph backend using GenAI.

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
│   │   │   ├── nodes/     # Individual graph nodes
│   │   │   └── flows/     # Graph flow definitions
│   │   ├── models/         # Data models
│   │   ├── routes/         # API routes
│   │   ├── utils/          # Utility functions
│   │   └── api/           # API endpoints
│   ├── tests/              # Test files
│   │   ├── test_nodes.py  # Node unit tests
│   │   ├── test_flow.py   # Flow integration tests
│   │   └── test_api.py    # API endpoint tests
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
- OpenAI API key
- Groq API key

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

3. Configure environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your settings
   # Particularly, add your Groq API key
   ```
   
   Required environment variables:
   - `GROQ_API_KEY`: Your Groq API key
   - `MONGODB_URL`: MongoDB connection string
   - `DATABASE_NAME`: Name of the MongoDB database
   - `MODEL_NAME`: Groq model to use (default: mixtral-8x7b-32768)
   - `MODEL_TEMPERATURE`: Model temperature (default: 0.2)
   - `MAX_ITERATIONS`: Maximum feedback loop iterations (default: 3)
   - `LOG_LEVEL`: Logging level (default: INFO)

4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install dependencies
   ```

## Running Tests

### Backend Tests
```bash
cd backend
pytest tests/
```

Available test suites:
- `test_nodes.py`: Unit tests for individual LangGraph nodes
- `test_flow.py`: Integration tests for the graph flow
- `test_api.py`: API endpoint tests

### Frontend Tests
```bash
cd frontend
npm test
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

## API Flow
1. Planning Node: Analyzes user input and creates integration plan
2. Supervisor Node: Divides work into coding and testing tasks
3. Parallel Execution:
   - Coder Node: Generates implementation code
   - Tester Node: Creates test cases
4. Evaluator Node: Reviews code and test results
5. Feedback Loop: Supervisor reviews and decides on next steps

## Technologies Used
- Frontend:
  - React
  - TypeScript
  - Tailwind
  - Vite
  - Axios
- Backend:
  - Python
  - FastAPI
  - LangGraph
  - LangChain
  - PyTest (Testing)

## Development Guidelines
1. Run tests before committing changes
2. Check logs in `backend/logs/` for debugging
3. Maximum 3 iterations for API integration feedback loop
4. Use type hints and documentation
5. Follow error handling patterns in BaseNode

## Team Members
Louis, Raeed, Kyumin, and Devi

## License
[Add license information]
