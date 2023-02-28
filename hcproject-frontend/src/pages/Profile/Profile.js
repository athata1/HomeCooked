import React from 'react'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import { useState } from 'react';
import Navbar from '../../components/Navbar/Navbar';
import Posts from '../../components/Posts/Posts';

function Profile() {

  const [user, setUser] = useState('Jane Doe')
  const [pf, setPf] = useState('https://avatarfiles.alphacoders.com/101/thumb-101741.jpg')
  const [city, setCity] = useState('West Lafayette')
  const [state, setState] = useState('IN')
  const [review, setReview] = useState('★★★★')
  const [about, setAbout] = useState('About: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')



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
            <h1>{user}

            </h1>
            <h5>{city}, {state}</h5>
            <h3>{review}</h3>
            <Button variant="danger"> Edit Profile</Button>
          </Col>
        </Row>
        <Row>
          <Card className="aboutMe bg-secondary text-white my-5">
            <Card.Body>
              {about}
            </Card.Body>
          </Card>
          <h3>Posts</h3>
          <CardGroup>
            
            <Posts />
            <Posts />
            <Posts />
            <Posts />
            <Posts />
            <Posts />
            
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