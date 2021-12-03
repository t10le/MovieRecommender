import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [test, setTest] = useState(0.0)
  const [inp, setInp] = useState("")
  useEffect(() => {
    axios.get('/time').then(
      (res) => {
        setTest(res.data["time"]);
      }
    )
  }, [])

  const sendRatings = () => {
    axios.post('/usr-rated', {
      ratings: inp
    })
  }

  const storeInput = (e) => {
    setInp(e.target.value)
  }

  return (
    <div className="App">
      <h1>Here is test time data {test}</h1>
      Enter something here:<input onChange={storeInput}/>
      <button onClick={sendRatings}>send</button>
    </div>
  );
}

export default App;
