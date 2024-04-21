import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [stations, setStations] = useState([]);
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    fetchStations();
  }, []);

  const fetchStations = async () => {
    try {
      const response = await axios.get('http://localhost:5000/mbajk/stations');
      const formattedStations = response.data.Stations.map(station => {
        return station
          .replace(/\u00C5\u00BD/g, 'Ž')  // Å½ -> Ž
          .replace(/\u00C5\u00A0/g, 'Š')  // Å -> Š
          .replace(/\u00E2\u20AC\u201C/g, '–');  // â€“ -> –
      });
      setStations(formattedStations);
    } catch (error) {
      console.error('Error fetching stations:', error);
    }
  };

  const handlePrediction = async (stationName) => {
    try {
      const normalizedStationName = stationName.toLowerCase().replace(/\s+/g, '_');
      const data = {
        data: [
          [5, 18, 70, 19, 0],  // Timestep 1
          [10, 20, 55, 68, 0],
          [10, 20, 55, 68, 0],
          [10, 20, 55, 68, 0],
          [10, 20, 55, 68, 0]  // Timestep 5
        ]
      };
  
      const response = await axios.post(`http://localhost:5000/mbajk/predict/${normalizedStationName}`, data);
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };
  

  return (
    <div>
      <h1>MBajk ML Predicition</h1>
      <h2>Postajalisca:</h2>
      <ul>
        {stations.map((station, index) => (
          <li key={index}>
            <button onClick={() => handlePrediction(station)}>{station}</button>
          </li>
        ))}
      </ul>
      {prediction && (
  <div>
    <h2>Predikcija:</h2>
    {prediction.map((value, index) => (
      <p key={index}>{value}</p>
    ))}
  </div>
)}
    </div>
  );
}

export default App;
