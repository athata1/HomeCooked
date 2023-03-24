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
import RecipeShow from '../../components/RecipeShow/RecipeShow';

import { useAuth } from '../../Firebase/AuthContext';
import { CgProfile } from "react-icons/cg";
import ProfileSettings from '../../components/ProfileSettings/ProfileSettings';
import { useNavigate } from 'react-router-dom';
import ReactStars from "react-rating-stars-component";
import ReviewsShow from '../../components/ReviewsShow/ReviewsShow';

function Profile() {

  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const {getToken, getCurrentPhoto, userMode} = useAuth()
  const [about, setAbout] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [selectedState, setSelectedState] = useState('');
  const [photoSource, setPhotoSource] = useState(null);
  const [edit, setEdit] = useState(false);
  const [rating, setRating] = useState(3);
  const [a, b] = useState(3);
  const [responses, setResponses] = useState([]);
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

    getCurrentPhoto().then((url) => {
      if (url.length !== 0) {
        setPhotoSource(url);
      }
    })

    getToken().then((token) => {
      let url = "http://localhost:8000/review/average?fid=" + token;
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
        console.log(typeof data.response)
        setRating(data.response);
      })
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

  useEffect(() => {
    navigate("/profile")
  }, [photoSource])

  return (
    <div>
      <Navbar part="Profile" mode="none" />
      <span>&nbsp;&nbsp;</span>
      { !edit ? <Container>
        <Row>
          <Col md={3}>
            {photoSource ?
              <Image src={photoSource} roundedCircle style={{width: "150px", height: "150px"}}/>
              : <CgProfile size={150}/>
            }

          </Col>

          <Col>
            <div> </div>
            <h1>{username}

            </h1>
            <h5>{selectedCity}, {selectedState}</h5>

            {/*<ReactStars
              count={5}
              value={rating}
              size={24}
              isHalf={true}
              edit={false}
              emptyIcon={<i className="far fa-star"></i>}
              halfIcon={<i className="fa fa-star-half-alt"></i>}
              fullIcon={<i className="fa fa-star"></i>}
              activeColor="#ffd700"
              
          />*/}
            <h5>Average review score: {rating}/5</h5>


            <Button variant="danger" onClick={() => {setEdit(true)}}> Edit Profile</Button>
          </Col>
        </Row>
        <Row>
          <Card className="aboutMe bg-secondary text-white my-5">
            <Card.Body>
              {about}
            </Card.Body>
          </Card>
        </Row>
        <span>&nbsp;&nbsp;</span>
      </Container> : <ProfileSettings 
                      callback={setEdit} 
                      cityCallback={setSelectedCity}
                      stateCallback={setSelectedState}
                      usernameCallback={setUsername}
                      photoCallback={setPhotoSource}
                      aboutCallback={setAbout}
                      />}
        <h1 className='px-5'>Reviews</h1>
        <hr />
        <ReviewsShow />
        <br />
        <br />
        <h1 className='px-5'>Posts</h1>
        <hr />
        <RecipeShow responses={responses} setResponses={setResponses} mode="producer" showMode={2} profileMode={true}/>
    </div>
  );
}

export default Profile;