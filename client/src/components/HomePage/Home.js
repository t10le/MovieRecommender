import React, { useState, useEffect } from 'react';
import { Row, Card, Col, Container, Button, ButtonGroup, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router'
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Home.css'
import NavBar from '../NavBar/navbar';

function Home() {
  const [movies, setMovies] = useState([])
  const [ratings, setRatings] = useState({})
  const [isLoaded, setLoaded] = useState(false)
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('/movies').then((res) => {
      setMovies(res.data.movies)
      setLoaded(true)
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
      <NavBar/>
      <div className="intro">
        <h2 className="title-page">Welcome to the Movie Recommender System</h2>
        <p>
          Here are some movies which you have not rated. Rate as many movies possible
          on a scale of 0 to 5, then click <strong>Get Recommendations</strong>. If you want <br/>
          to see your recommendations based on previous ratings only, then click the tab 
           <strong> My Recommended</strong>.
          
        </p>
      </div>
      {isLoaded ? 
        <>
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
      <div className="btn-region">
        <Button onClick={sendRatings} className="submission">Get Recommendations</Button>
      </div> 
      </>:
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
  );
}

export default Home;
