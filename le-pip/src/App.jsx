import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [selectedDataset, setSelectedDataset] = useState('california_housing');
    const [fastResult, setFastResult] = useState(null);
    const [slowResult, setSlowResult] = useState(null);
    const [parallelResult, setParallelResult] = useState(null);
    const [parallelFitModelsResult, setParallelFitModelsResult] = useState(null);
    const [linearRegressionResult, setLinearRegressionResult] = useState(null);
    const [availableColumns, setAvailableColumns] = useState([]);
    const [selectedColumn, setSelectedColumn] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleDatasetChange = (event) => {
        setSelectedDataset(event.target.value);
    };

const handleParallelFitModelsClick = async () => {
  setLoading(true);
  setError(null);

  try {
    const response = await axios.post('/api/fit_models/parallel', {
      dataset: selectedDataset,
      target_column: selectedColumn,
      num_models: 5
    });
    setParallelFitModelsResult(response.data);
    setLoading(false);
  } catch (error) {
    setError('Error occurred while fitting models in parallel.');
    setLoading(false);
  }
    };


    useEffect(() => {
        const fetchColumns = async () => {
            try {
                const response = await axios.post('/api/get_columns', { dataset: selectedDataset });
                setAvailableColumns(response.data);
            } catch (error) {
                console.error('Error fetching columns:', error);
            }
        };

        fetchColumns();
    }, [selectedDataset]);

    const handleLinearRegressionClick = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('/api/fit_linear_regression', { dataset: selectedDataset, target_column: selectedColumn });
            setLinearRegressionResult(response.data);
        } catch (error) {
            setError('Error occurred while fitting linear regression.');
        }

        setLoading(false);
    };

    const handleFastClick = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('/api/process/fast', { dataset: selectedDataset });
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
            const response = await axios.post('/api/process/slow', { dataset: selectedDataset });
            setSlowResult(response.data);
        } catch (error) {
            setError('Error occurred while processing slow task.');
        }

        setLoading(false);
    };


    const handleParallelClick = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('/api/process/parallel', { dataset: selectedDataset });
            const taskId = response.data.task_id;

            // Poll for the result
            const pollResult = async () => {
                const resultResponse = await axios.get(`/api/process/parallel/${taskId}`);
                if (resultResponse.data.status === 'PENDING') {
                    setTimeout(pollResult, 1000); // Poll every 1 second
                } else {
                    setParallelResult(resultResponse.data);
                    setLoading(false);
                }
            };

            pollResult();
        } catch (error) {
            setError('Error occurred while processing data in parallel.');
            setLoading(false);
        }
    };


    return (
        <div className="app">
            <div className="dataset-select">
                <label htmlFor="dataset">Select Dataset:</label>
                <select id="dataset" value={selectedDataset} onChange={handleDatasetChange}>
                    <option value="california_housing">California Housing</option>
                    <option value="ames_housing">Ames Housing</option>
                </select>
            </div>
            <div className="buttons">
                <button onClick={handleFastClick} disabled={loading}>
                    {loading ? 'Processing...' : 'Process Fast Task'}
                </button>
                <button onClick={handleSlowClick} disabled={loading}>
                    {loading ? 'Processing...' : 'Process Slow Task'}
                </button>
            </div>
            <div className="column-select">
                <label htmlFor="column">Select Target Column:</label>
                <select id="column" value={selectedColumn} onChange={(e) => setSelectedColumn(e.target.value)}>
                    <option value="">Select target column</option>
                    {availableColumns.map(column => (
                        <option key={column} value={column}>{column}</option>
                    ))}
                </select>
            </div>
            <div className="buttons">
                <button onClick={handleLinearRegressionClick} disabled={loading}>
                    {loading ? 'Fitting Linear Regression...' : 'Fit Linear Regression'}
                </button>
            </div>

            <button onClick={handleParallelClick} disabled={loading}>
                {loading ? 'Processing in Parallel...' : 'Process in Parallel'}
            </button>

            <button onClick={handleParallelFitModelsClick} disabled={loading}>
                {loading ? 'Fitting Models in Parallel...' : 'Fit Models in Parallel'}
            </button>

            {error && <p className="error">{error}</p>}

            {fastResult && (
                <div className="result">
                    <h2>Fast Task Result:</h2>
                    <pre>{JSON.stringify(fastResult, null, 2)}</pre>
                </div>
            )}

            {slowResult && (
                <div className="result">
                    <h2>Slow Task Result:</h2>
                    <pre>{JSON.stringify(slowResult, null, 2)}</pre>
                </div>
            )}

            {linearRegressionResult && (
                <div className="result">
                    <h2>Linear Regression Result:</h2>
                    <pre>{JSON.stringify(linearRegressionResult, null, 2)}</pre>
                </div>
            )}


            {parallelResult && (
                <div className="result">
                    <h2>Parallel Processing Result:</h2>
                    <pre>{JSON.stringify(parallelResult, null, 2)}</pre>
                </div>
            )}


            {parallelFitModelsResult && (
                <div className="result">
                    <h2>Parallel Model Fitting Result:</h2>
                    {parallelFitModelsResult.map(result => (
                        <div key={result.model_id}>
                            <h3>Model {result.model_id}</h3>
                            <p>Train Score: {result.train_score}</p>
                            <p>Test Score: {result.test_score}</p>
                            <h4>Coefficients:</h4>
                            <ul>
                                {Object.entries(result.coefficients).map(([column, coef]) => (
                                    <li key={column}>{column}: {coef}</li>
                                ))}
                            </ul>
                            <p>Intercept: {result.intercept}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default App;
