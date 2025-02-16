import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
    baseURL: 'http://localhost:8000',  // FastAPI default port
    headers: {
        'Content-Type': 'application/json',
    },
});

// API functions
export const apiService = {
    healthCheck: async () => {
        try {
            const response = await api.get('/api/health');
            return response.data;
        } catch (error) {
            console.error('API Health Check Error:', error);
            throw error;
        }
    },
    
    // Example CRUD operations
    createItem: async (item: { name: string; description: string }) => {
        try {
            const response = await api.post('/graph', item);
            return response.data;
        } catch (error) {
            console.error('Create Item Error:', error);
            throw error;
        }
    },
    
    getItems: async () => {
        try {
            const response = await api.get('/api/items');
            return response.data;
        } catch (error) {
            console.error('Get Items Error:', error);
            throw error;
        }
    }
}; 