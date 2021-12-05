import React, { useState, useEffect } from 'react';
import { Row, Card, Col, Container, Button, ButtonGroup } from 'react-bootstrap';
import { useNavigate } from 'react-router'
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Home.css'

function Home() {
  const [movies, setMovies] = useState([])
  const [ratings, setRatings] = useState({})
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('/movies').then((res) => {
      setMovies(res.data.movies)
    })
  }, [])

  const update_ratings = (e,id) => {
    setRatings({...ratings, ...{[id]: e.target.value}})
  }

  const sendRatings = () => {
    axios.post('/usr-rated', ratings)
      .then((res) => {
        if(res.data.status === "success")
        {
          navigate('/recommended')
        }
      })
  }

  return (
    <div>
      Home Page
      <Container className="posters">
        <Row xs={1} md={2} className="g-4">
        {Object.keys(movies).map((movieId, _) => (
          <Col md={4}>
            <Card>
              <Card.Img variant="top" 
                        src={`https://image.tmdb.org/t/p/original${movies[movieId].poster_path}`}/>
              <Card.Body>
                <Card.Title>{movies[movieId].title}</Card.Title>
                <Row>
                  <Col xs={8}>
                    <ButtonGroup aria-label="First group">
                      <Button value="0" onClick={(e) => update_ratings(e,movieId)}>0</Button>
                      <Button value="1" onClick={(e) => update_ratings(e,movieId)}>1</Button>
                      <Button value="2" onClick={(e) => update_ratings(e,movieId)}>2</Button>
                      <Button value="3" onClick={(e) => update_ratings(e,movieId)}>3</Button>
                      <Button value="4" onClick={(e) => update_ratings(e,movieId)}>4</Button>
                      <Button value="5" onClick={(e) => update_ratings(e,movieId)}>5</Button>
                    </ButtonGroup>
                  </Col>
                  <Col xs={4}>
                    <Card.Text className="rated">{movieId in ratings ? ratings[movieId] : "0"}</Card.Text>
                  </Col>
                </Row>
              </Card.Body>
            </Card>
          </Col>
        ))}
        </Row>
      </Container>
      <br/>
      <div className="submission">
        <h1>Send Ratings</h1>
        <Button onClick={sendRatings}>Send</Button>
      </div>
    </div>
  );
}

export default Home;
