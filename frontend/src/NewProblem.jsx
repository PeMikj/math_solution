import React, { useState } from 'react';

function NewProblem() {
  const [problemText, setProblemText] = useState('');
  const [answerText, setAnswerText] = useState('');
  const [message, setMessage] = useState('');
  const [solution, setSolution] = useState('');

  const handleSubmitProblem = async (e) => {
    e.preventDefault();
    setMessage('');

    const token = localStorage.getItem('token');
    if (!token) {
      setMessage('Unauthorized. Please log in again.');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/problems', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ 
          problem_text: problemText,
          known_answer: answerText,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Problem and answer submitted successfully');
        setProblemText('');
        setAnswerText('');
        getSolution(problemText, answerText);
      } else {
        setMessage(data.detail || 'Submission failed');
      }
    } catch (error) {
      console.error('Error submitting problem and answer:', error);
      setMessage('An error occurred. Please try again.');
    }
  };

  const getSolution = async (problemText, knownAnswer) => {
    const token = localStorage.getItem('token');
    if (!token) {
      setMessage('Unauthorized. Please log in again.');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/problems/solve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ problem_text: problemText, known_answer: knownAnswer }),
      });

      const data = await response.json();

      if (response.ok) {
        setSolution(data.solution);
      } else {
        setMessage(data.detail || 'Failed to get solution');
      }
    } catch (error) {
      console.error('Error getting solution:', error);
      setMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div>
      <h2>Submit a New Problem</h2>
      <form onSubmit={handleSubmitProblem}>
        <textarea
          placeholder="Describe your problem here..."
          value={problemText}
          onChange={(e) => setProblemText(e.target.value)}
          required
        />
        <textarea
          placeholder="Provide the answer here..."
          value={answerText}
          onChange={(e) => setAnswerText(e.target.value)}
          required
        />
        <button type="submit">Get Solution</button>
      </form>
      {message && <p>{message}</p>}
      {solution && (
        <div>
          <h3>Solution</h3>
          <p>{solution}</p>
        </div>
      )}
    </div>
  );
}

export default NewProblem;