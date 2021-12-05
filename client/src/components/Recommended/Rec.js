import React, { useState, useEffect } from 'react';
import { Row, Card, Col, Container, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router'
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Rec.css'

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


    useEffect(() => {
        axios.get('/usr-recommended').then((res) => {
          setMovies(res.data.movies)
        })
      }, [])

    const redirectHome = () => {
        navigate('/home')
    }

    return(
        <div>
            <h1>Here are your Recommended Movies: </h1>
            <MovieListing movies={movies}></MovieListing>
            <Button onClick={redirectHome}>Rate More Movies</Button>
        </div>
    )
}

export default Recommended;