import React from 'react'
import { useState, useEffect, useRef } from "react";
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Navbar from '../../components/Navbar/Navbar';
import { useAuth } from '../../Firebase/AuthContext';
import Posts from '../../components/Posts/Posts';
import InputTag from '../../components/InputTag/InputTag';
import { ref, uploadBytes } from "firebase/storage";
import { storage } from "../../Firebase/firebase";
import { getDownloadURL } from "firebase/storage";
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Button from 'react-bootstrap/Button';
import RecipeShow from '../../components/RecipeShow/RecipeShow';

const Events = () => {
  const { currentUser, getToken, userMode, setUserMode } = useAuth();
  const [tags, setTags] = useState([])
  const [ingredients, setIngredients] = useState([]);


  const titleRef = useRef()
  const locationRef = useRef()
  const textRef = useRef()
  const timeRef = useRef();
  const [showMode, setShowMode] = useState(0);
  const [responses, setResponses] = useState([]);



  const handleNewEvent = (e) => {
    e.preventDefault();
    if (timeRef.current.value === '') {
      alert("Event must have a start time");
      return;
    }
    if (titleRef.current.value.length < 6) {
      alert("Title must have at least 6 characters");
      return;
    }
    if (textRef.current.value.length < 10) {
      alert("Description must have at least 20 characters");
      return;
    }
    if (locationRef.current.value.length < 10) {
      alert("Location must have at least 20 characters");
      return;
    }

    let date = new Date(timeRef.current.value);
    let millis = date.getTime();
    getToken().then((token) => {
      let url = 'http://localhost:8000/event/create?' +
      "token=" + token +
      '&desc=' + textRef.current.value + 
      '&title=' + titleRef.current.value + 
      '&location=' + locationRef.current.value + 
      '&time=' + millis;
      fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
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
        return res.json();
      }).then((data) => {
        timeRef.current.value = '';
        titleRef.current.value = '';
        textRef.current.value = '';
        locationRef.current.value = '';
        alert("Event Created");
      })
    })
  };

  return (
    <div className="events">
      <Navbar part="Events" mode={userMode} />
      <span>&nbsp;&nbsp;</span>
      <div >
        <Container>
          <Row>
            <ButtonGroup>
              {userMode == "producer" ?
                <>
                  <Button
                    variant="success"
                    data-bs-toggle="modal"
                    data-bs-target="#exampleModal"
                    onClick={() => {
                      setResponses([])
                      setShowMode(0);
                    }}
                  >New Event</Button>
                </> : ""}
              <Button
                disabled={showMode === 2}
                onClick={() => {
                  setResponses([])
                  setShowMode(2)
                }}
              >Current Events</Button>

            </ButtonGroup>
          </Row>

        </Container>

        {/* <button
            className="btn btn-primary settings-button-remove settings-delete-account-button"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
            onClick={handleNewPost}
          >
            New Recipe
          </button> */}
        <div
          className="modal fade"
          id="exampleModal"
          tabIndex="-1"
          aria-labelledby="exampleModalLabel"
          aria-hidden="true"
        >
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="exampleModalLabel">
                  Create an Event
                </h5>
                <button
                  type="button"
                  className="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div className="modal-body">
                <input
                  type="title"
                  className="form-control settings-input"
                  placeholder="Title"
                  ref={titleRef}
                // value={deleteAccountPassword}
                // onChange={(e) => setDeleteAccountPassword(e.target.value)}
                />
                <span>&nbsp;&nbsp;</span>
                <textarea
                  placeholder="Text"
                  className="form-control"
                  id="email_body"
                  rows="7"
                  ref={textRef}
                // placeholder="Text"
                // type="textarea"
                // multiline={true} 
                // style={{padding: 10}} 
                // textAlignVertical="top"
                // className="form-control settings-input"
                // style={{height: "100px"}}

                // value={deleteAccountPassword}
                // onChange={(e) => setDeleteAccountPassword(e.target.value)}
                />
                <span>&nbsp;&nbsp;</span>

                {/* <div>
                  <label for="#formFileLg" className="form-label">Input Image</label>
                  <input onChange={(e) => {handleChangeImage(e);}}className="form-control form-control-md" id="formFileLg" type="file" />
                </div>
*/}
                <span>&nbsp;&nbsp;</span>
                <div>
                  <input
                    type="location"
                    className="form-control settings-input"
                    placeholder="Location"
                    ref={locationRef} />
                </div>
                <span>&nbsp;&nbsp;</span>
                <div>
                  <label for="meeting-time">Time of Event: </label>
                  <span>&nbsp;&nbsp;</span>
                  <input ref={timeRef} id="meeting" type="datetime-local" name="meetingdate" />

                    {/* <InputTag tags={ingredients} setSelected={setIngredients} placeholder="Add ingredients to recipe" /> */}
                </div>

              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Close
                </button>
                <button
                  type="button"
                  className="btn btn-primary"
                  data-bs-dismiss="modal"
                  onClick={(e) => { handleNewEvent(e) }}
                >
                  Add Recipe
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* <Container>
        <Row>
          <Col>
            <h2>Post Feed</h2>
            <Posts />
            <Posts />
          </Col>
          <Col>
            <h2>Recipe Feed</h2>
            <Posts />
            <Posts />
          </Col>
          
        </Row>
      </Container> */}

    </div>

  )
}

export default Events;