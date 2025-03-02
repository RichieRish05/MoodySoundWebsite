import { useState, useEffect } from 'react'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import axios from 'axios'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL


import HomePage from './pages/HomePage/HomePage'
import CallbackPage from './pages/CallbackPage/CallbackPage';

function App() {


  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/callback" element={<CallbackPage />} />
      </Routes>
    </Router>
  )
}

export default App
