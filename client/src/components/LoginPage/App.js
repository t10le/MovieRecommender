import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { Form, Button, Toast } from 'react-bootstrap';
import axios from 'axios';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [userName, setUserName] = useState("")
  const [password, setPassword] = useState("")
  const [show, setShow] = useState(false)
  const navigate = useNavigate();

  const updateEmail = (e) => {
    setUserName(e.target.value)
  }

  const updatePassword = (e) => {
    setPassword(e.target.value)
  }

  const submitSignOn = () => {
    axios.post('/signin', {
      userName:  userName,
      password: password
    }).then((res) => {
      if(res.data.status === "success")
      {
        navigate("/home");
      }
      else
      {
        setShow(true)
      }
    })
  }

  const submitRegister = () => {
    axios.post('/register', {
      userName:  userName,
      password: password
    }).then((res) => {
      if(res.data.status === "success")
      {
        navigate("/home");
      }
      else
      {
        setShow(true)
      }
    })
  }

  return (
    <div className="signon">
      <Form className="signon-form">
        <Form.Group className="mb-3" controlId="formGroupEmail">
          <Form.Label>Username</Form.Label>
          <Form.Control type="text" placeholder="Enter username" 
            onChange={updateEmail}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formGroupPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" 
            onChange={updatePassword}
          />
        </Form.Group>
        <Button variant="primary" onClick={submitSignOn}>
          Sign In
        </Button>{' '}
        <Button variant="primary" onClick={submitRegister}>
          Register
        </Button>
      </Form>
      <Toast onClose={() => setShow(false)} show={show} delay={3000} autohide>
        <Toast.Header>
          <img src="https://static.thenounproject.com/png/415502-200.png" 
                className="rounded me-2" alt="" width="25" height="25"/>
          <strong className="me-auto">Bot</strong>
          <small>Now</small>
        </Toast.Header>
        <Toast.Body className='Danger'>
          Unable to sign in. Try again or register as a new user.
        </Toast.Body>
      </Toast>
    </div>
  );
}

export default App;
