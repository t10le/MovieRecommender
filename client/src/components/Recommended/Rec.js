import React, { useState, useEffect } from 'react';
import { Row, Card, Col, Container, Button, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router'
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Rec.css'
import NavBar from '../NavBar/navbar';

function MovieListing(props)
{
    return(
        <Container>
        <Row xs={1} md={2} className="g-4">
        {Object.keys(props.movies).map((movieId, _) => (
          <Col md={3}>
            <Card>
              <Card.Img variant="top" 
                        src={`https://image.tmdb.org/t/p/original${props.movies[movieId].poster_path}`}/>
              <Card.Body>
                <Card.Title>{props.movies[movieId].title}</Card.Title>
                <Card.Text>{props.movies[movieId].overview.substring(0,256)}</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
        </Row>
      </Container>
    )
}

function Recommended()
{
    const [movies, setMovies] = useState({});
    const navigate = useNavigate();
    const [isLoaded, setLoaded] = useState(false);


    useEffect(() => {
        axios.get('/usr-recommended').then((res) => {
          setMovies(res.data.movies)
          setLoaded(true)
        })
      }, [])

    const redirectHome = () => {
        navigate('/home')
    }

    return(
        <div>
            <NavBar></NavBar>
            <div className="intro">
              <h1 className="title-page">Here are your Recommended Movies: </h1>
            </div>
            {isLoaded ? <>
              <MovieListing movies={movies}></MovieListing>
              <div className="btn-region">
                <Button onClick={redirectHome} className="submission">Rate More Movies</Button>
              </div>
            </> : 
            <Container>
              <Row className="load-section">
                <Col xs={4}>
                  <strong className="loading">Loading Movie Data...</strong>
                </Col>
                <Col xs={1}>
                  <Spinner animation="border" role="status" className="spinner">
                    <span className="visually-hidden">Loading...</span>
                  </Spinner>
                </Col>
              </Row>
            </Container>
            }
        </div>
    )
}

export default Recommended;