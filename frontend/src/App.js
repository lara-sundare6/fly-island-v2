// frontend/src/App.js
import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import PipelineChart from './components/PipelineChart';

const socket = io('http://localhost:5000'); // Adjust the URL as needed

function App() {
    const [data, setData] = useState({ labels: [], values: [] });
    const [error, setError] = useState(null);

    useEffect(() => {
        // Fetch initial data
        fetch('/ci_cd_status')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const labels = data.map(item => item.timestamp);
                const values = data.map(item => item.status);
                setData({ labels, values });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setError(error.message);
            });

        // Listen for real-time updates
        socket.on('pipeline_status_update', (update) => {
            const labels = update.map(item => item.timestamp);
            const values = update.map(item => item.status);
            setData({ labels, values });
        });

        // Request initial pipeline status
        socket.emit('request_pipeline_status');

        return () => {
            socket.off('pipeline_status_update');
        };
    }, []);

    return (
        <div className="App">
            <h1>CI/CD Pipeline Dashboard</h1>
            {error ? (
                <p>Error: {error}</p>
            ) : (
                <PipelineChart data={data} />
            )}
        </div>
    );
}

export default App;