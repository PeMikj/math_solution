import React, { useState } from 'react';

function PingTest() {
  const [response, setResponse] = useState('');

  const pingServer = async () => {
    try {
      const res = await fetch('http://localhost:8000/ping');
      if (!res.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await res.json();
      setResponse(data.status);
    } catch (error) {
      console.error('Error fetching from backend:', error);
      setResponse('Error');
    }
  };

  return (
    <div>
      <button onClick={pingServer}>Ping server</button>
      <p>{response}</p>
    </div>
  );
}

export default PingTest;