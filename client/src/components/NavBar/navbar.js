import React, { useState, useEffect } from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './nav.css'
import axios from 'axios';

function NavBar()
{
    const [userName, setUserName] = useState("")

    useEffect(() => {
        axios.get('/usr-info').then((res) => {
            setUserName(res.data.user_name)
        })
    }, []);

    return(
        <>
            <Navbar bg="dark" variant="dark" className="navbar">
                <Navbar.Brand href="/home">MovieRecommender</Navbar.Brand>
                <Nav className="me-auto" variant="dark">
                    <Nav.Link href="/home">Home</Nav.Link>
                    <Nav.Link href="/recommended">My Recommended</Nav.Link>
                </Nav>
                <Navbar.Toggle />
                <Navbar.Collapse className="justify-content-end">
                <Navbar.Text>
                    <NavDropdown title={`Signed in as: ${userName.toUpperCase()}`}>
                        <NavDropdown.Item href="/" id="nav-dropdown">Sign Out</NavDropdown.Item>
                    </NavDropdown>
                </Navbar.Text>
                </Navbar.Collapse>
            </Navbar>
        </>
    )
}

export default NavBar;