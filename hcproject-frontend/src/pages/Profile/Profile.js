import React,{ useState, useEffect }  from 'react'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Navbar from '../../components/Navbar/Navbar';
import { useAuth } from '../../Firebase/AuthContext';
import { CgProfile } from "react-icons/cg";

function Profile() {


  const [username, setUsername] = useState('');
  const {getToken, getCurrentPhoto} = useAuth()
  const [about, setAbout] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [selectedState, setSelectedState] = useState('');
  const [photoSource, setPhotoSource] = useState(null);

  useEffect(() => {

    getCurrentPhoto().then((url) => {
      if (url.length !== 0) {
        setPhotoSource(url);
      }
    })

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
      <Navbar part="Profile" mode="none"/>
      <span>&nbsp;&nbsp;</span>
      <Container>
        <Row>
          <Col md={3}>
            {photoSource ?
              <Image src={photoSource} roundedCircle style={{width: "150px", height: "150px"}}/>
              : <CgProfile size={150}/>
            }

          </Col>

          <Col md={{ offset: 0 }}>
            <div> </div>
            <h1>{username}
              
            </h1>
            <h5>{selectedCity}, {selectedState}</h5>
            <h3>★★★★</h3>
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