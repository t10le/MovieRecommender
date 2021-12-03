import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css';
import App from './components/LoginPage/App';
import Home from './components/HomePage/Home'

ReactDOM.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/home" element={<Home/>} />
    </Routes>
  </BrowserRouter>,
  document.getElementById('root')
);
