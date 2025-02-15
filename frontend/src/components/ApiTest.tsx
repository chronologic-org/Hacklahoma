import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export const ApiTest = () => {
    const [status, setStatus] = useState<string>('');
    const [error, setError] = useState<string>('');

    useEffect(() => {
        const checkHealth = async () => {
            try {
                const response = await apiService.healthCheck();
                setStatus(response.status);
            } catch (err) {
                setError('Failed to connect to backend');
            }
        };

        checkHealth();
    }, []);

    return (
        <div>
            <h2>API Connection Test</h2>
            {status && <p>Backend Status: {status}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}; 