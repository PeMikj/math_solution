import React, { useState, useEffect } from 'react';

function TaskHistory() {
  const [problems, setProblems] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProblems = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found. Please log in.');
        setLoading(false);
        return;
      }
      try {
        const response = await fetch('http://localhost:8000/api/problems/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to fetch problems.');
        }
        const data = await response.json();
        setProblems(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProblems();
  }, []);

  if (loading) return <div>Loading task history...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;
  if (problems.length === 0) return <div>No tasks found.</div>;

  return (
    <div>
      <h2>Task History</h2>
      <ul>
        {problems.map((problem) => (
          <li key={problem.id}>
            <p><strong>Problem:</strong> {problem.problem_text}</p>
            <p><strong>Status:</strong> {problem.status}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TaskHistory;