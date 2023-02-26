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

function Profile() {
  return (
    <div>
      <Navbar />
      <span>&nbsp;&nbsp;</span>
      <Container>
        <Row>
          <Col md={3}>
            <Image src="https://avatarfiles.alphacoders.com/101/thumb-101741.jpg" roundedCircle />

          </Col>

          <Col md={{ offset: 0 }}>
            <div> </div>
            <h1>John Doe</h1>
            <h5>West Lafayette, IN</h5>
            <h3>★★★★</h3>
            <Button variant="danger"> Edit Profile</Button>
          </Col>
        </Row>
        <Row>
          <Card className="aboutMe bg-secondary text-white my-5">
            <Card.Body>
              About: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </Card.Body>
          </Card>
          <h3>Posts</h3>
          <CardGroup>
            <Card>
              <Card.Img variant="top" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" />
              <Card.Body>
                <Card.Title>Post title</Card.Title>
                <Card.Text>
                  Post Text
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Posted 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card>
              <Card.Img variant="top" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" />
              <Card.Body>
                <Card.Title>Post title</Card.Title>
                <Card.Text>
                  Post Text
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Posted 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card>
              <Card.Img variant="top" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" />
              <Card.Body>
                <Card.Title>Post title</Card.Title>
                <Card.Text>
                  Post Text
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Posted 3 mins ago</small>
              </Card.Footer>
            </Card>
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