import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [fastResult, setFastResult] = useState(null);
  const [slowResult, setSlowResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFastClick = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/process/fast');
      setFastResult(response.data);
    } catch (error) {
      setError('Error occurred while processing fast task.');
    }

    setLoading(false);
  };

  const handleSlowClick = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/process/slow');
      setSlowResult(response.data);
    } catch (error) {
      setError('Error occurred while processing slow task.');
    }

    setLoading(false);
  };

  return (
    <div>
      <button onClick={handleFastClick} disabled={loading}>
        {loading ? 'Processing...' : 'Process Fast Task'}
      </button>
      <button onClick={handleSlowClick} disabled={loading}>
        {loading ? 'Processing...' : 'Process Slow Task'}
      </button>

      {error && <p>{error}</p>}

      {fastResult && (
        <div>
          <h2>Fast Task Result:</h2>
          <pre>{JSON.stringify(fastResult, null, 2)}</pre>
        </div>
      )}

      {slowResult && (
        <div>
          <h2>Slow Task Result:</h2>
          <pre>{JSON.stringify(slowResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
