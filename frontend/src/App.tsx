import { useState, useEffect } from 'react'
import './App.css'
import axios from 'axios'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL


function App() {

  useEffect(() => {
    axios.get(`${BACKEND_URL}/hello`, {
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then(response => response.data)
    .then(data => {
      console.log(data);
    });

    console.log(BACKEND_URL);
  })

  return (
    <Router>
      <Routes>
        <Route path="/" />
      </Routes>
    </Router>
  )
}

export default App
