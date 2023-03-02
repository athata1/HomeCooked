import React, { useState, useEffect } from 'react'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Navbar from '../../components/Navbar/Navbar';
import Recipes from '../../components/Recipes/Recipes';

import { useAuth } from '../../Firebase/AuthContext';
import ReactStars from "react-rating-stars-component";

function Profile() {


  const [username, setUsername] = useState('');
  const [pf, setPf] = useState('https://avatarfiles.alphacoders.com/101/thumb-101741.jpg')
  const { getToken } = useAuth()
  const [about, setAbout] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [selectedState, setSelectedState] = useState('');

  const ratingChanged = (newRating) => {
    console.log(newRating);
  };

  const example = {
    size: 50,
    count: 5,
    color: "black",
    activeColor: "yellow",
    value: 5,
    a11y: true,
    isHalf: true,
    emptyIcon: <i className="far fa-star" />,
    halfIcon: <i className="fa fa-star-half-alt" />,
    filledIcon: <i className="fa fa-star" />,
    onChange: newValue => {
      console.log(`Example 2: new value is ${newValue}`);
    }
  };

  useEffect(() => {
    getToken().then((token) => {

      let url = "http://localhost:8000/users/?type=Create&fid=" + token;
      fetch(url, {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        // mode: "no-cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: "follow", // manual, *follow, error
        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      }).then((res) => {
        return res.json()
      }).then((data) => {
        let userData = JSON.parse(data.user)[0];
        console.log(userData)
        setUsername(userData.fields.user_uname);
        setSelectedState(userData.fields.user_state.toUpperCase());
        setSelectedCity(userData.fields.user_city.toUpperCase());
        setAbout(userData.fields.user_bio)
      })
    })
  }, [])

  return (
    <div>
      <Navbar part="Profile" mode="none" />
      <span>&nbsp;&nbsp;</span>
      <Container>
        <Row>
          <Col md="auto">
            <Image src={pf} roundedCircle />

          </Col>

          <Col>
            <div> </div>
            <h1>{username}

            </h1>
            <h5>{selectedCity}, {selectedState}</h5>

            <ReactStars
              count={5}
              value={4}
              onChange={ratingChanged}
              size={24}
              isHalf={true}
              emptyIcon={<i className="far fa-star"></i>}
              halfIcon={<i className="fa fa-star-half-alt"></i>}
              fullIcon={<i className="fa fa-star"></i>}
              activeColor="#ffd700"
              
            />


            <Button variant="danger"> Edit Profile</Button>
          </Col>
        </Row>
        <Row>
          <Card className="aboutMe bg-secondary text-white my-5">
            <Card.Body>
              {about}
            </Card.Body>
          </Card>
          <h3>Recipes</h3>
          <CardGroup>

            <Recipes />
            <Recipes />
            

          </CardGroup>

        </Row>
        <Row>
          <span>&nbsp;&nbsp;</span>
          <h3> Recipes </h3>
          <CardGroup>
            <Card>
              <Card.Img variant="top" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" />
              <Card.Body>
                <Card.Title>Recipe title</Card.Title>
                <Card.Text>
                  Recipe Text
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Posted 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card>
              <Card.Img variant="top" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" />
              <Card.Body>
                <Card.Title>Recipe title</Card.Title>
                <Card.Text>
                  Recipe Text
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Posted 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card>
              <Card.Img variant="top" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" />
              <Card.Body>
                <Card.Title>Recipe title</Card.Title>
                <Card.Text>
                  Recipe Text
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Posted 3 mins ago</small>
              </Card.Footer>
            </Card>
          </CardGroup>
        </Row>
        <span>&nbsp;&nbsp;</span>
      </Container>
    </div>
  );
}

export default Profile;