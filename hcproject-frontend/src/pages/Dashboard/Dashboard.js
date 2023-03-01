import React from 'react'
import { useState, useEffect } from "react";
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Navbar from '../../components/Navbar/Navbar';
import { useAuth } from '../../Firebase/AuthContext';
import Posts from '../../components/Posts/Posts';
import InputTag from '../../components/InputTag/InputTag';

const Dashboard = () => {
  const { currentUser, getToken, userMode, setUserMode } = useAuth();
  const [token, setToken] = useState();

  const handleNewPost = (e) => {
    e.preventDefault();
  };

  useEffect(() => {
    getToken().then((t) => {
      setToken(t);
    });
  }, []);

  return (
    <div className="dashboard">
      <Navbar part="Posts" mode={userMode} />
      <span>&nbsp;&nbsp;</span>
      <div className="col mb-5 settings-save-div d-flex justify-content-center">
        <button
          className="btn btn-primary settings-button-remove settings-delete-account-button"
          data-bs-toggle="modal"
          data-bs-target="#exampleModal"
          onClick={handleNewPost}
        >
          New Post
        </button>
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
                  Create a post
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
                // value={deleteAccountPassword}
                // onChange={(e) => setDeleteAccountPassword(e.target.value)}
                />
                <span>&nbsp;&nbsp;</span>
                <textarea
                  placeholder="Text"
                  className="form-control"
                  id="email_body"
                  rows="7"
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

                <div>
                  <label for="formFileLg" class="form-label">Input Image</label>
                  <input class="form-control form-control-md" id="formFileLg" type="file" />
                </div>
                

                <div>test</div>


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
                // onClick={confirmDeleteAccount}
                >
                  Publish Post
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Container>
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
          {/* <Col>
            <h2>Post Feed</h2>
            <Card>
              <Card.Img variant="top" src="holder.js/100px160" />
              <Card.Body>
                <Card.Title>Card title</Card.Title>
                <Card.Text>
                  This is a wider card with supporting text below as a natural lead-in
                  to additional content. This content is a little bit longer.
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
            </Card>
          </Col> */}
        </Row>

      </Container>

      {/* Dashboard
      {currentUser ? currentUser.email : ""} */}
    </div>

  )
}

export default Dashboard;
