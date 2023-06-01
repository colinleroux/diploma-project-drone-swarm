import React, { useState } from 'react';
import axios from 'axios';
import ReactPlayer from 'react-player';
import './output.css';
function App() {
  const [message, setMessage] = useState('');

  // Function to send the command to the backend
  const sendCommand = async (command) => {
    try {
      const response = await axios.post('http://localhost:8000/api/commands', { command });
      setMessage(response.data.message); // Set the received message
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Drone Controller</h1>
      <div className="w-1/2 aspect-w-16 aspect-h-9 mb-6">
        <ReactPlayer url="http://localhost:8000/video-stream" playing width="100%" height="100%" />
      </div>
      <div className="flex space-x-4 mb-6">
        <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded" onClick={() => sendCommand('left')}>Left</button>
        <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded" onClick={() => sendCommand('right')}>Right</button>
        <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded" onClick={() => sendCommand('up')}>Up</button>
        <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded" onClick={() => sendCommand('down')}>Down</button>
      </div>
      <div className="flex space-x-4">
        <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded" onClick={() => sendCommand('takeoff')}>Takeoff</button>
        <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded" onClick={() => sendCommand('land')}>Land</button>
      </div>
      {message && <p className="mt-6">{message}</p>}
    </div>
  );
}

export default App;