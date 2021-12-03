import React, { useState, useEffect } from 'react';
import { Row, Card, Col } from 'react-bootstrap';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function Home() {
  const [movies, setMovies] = useState([])

  useEffect(() => {
    axios.get('/movies').then((res) => {
      setMovies(res.data.movies)
    })
  }, [])

  return (
    <div>
      Home Page
      <Row xs={1} md={2} className="g-4">
      {Object.keys(movies).map((movieId, _) => (
        <Col>
          <Card>
            <Card.Img variant="top" src={movies[movieId].image} />
            <Card.Body>
              <Card.Title>{movies[movieId].title}</Card.Title>
              <Card.Text>
                  {movies[movieId].plot}
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      ))}
      </Row>
    </div>
  );
}

export default Home;
