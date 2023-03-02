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

const Dashboard = () => {
  const { currentUser, getToken, userMode, setUserMode } = useAuth();
  const [token, setToken] = useState();
  const [tags, setTags] = useState([])
  const [ingredients, setIngredients] = useState([]);


  const titleRef = useRef()
  const textRef = useRef()
  const [image, setImage] = useState(null);
  const [showRecipes, setShowRecipes] = useState(false);
  const [showPosts, setShowPosts] = useState(false);
  const [showArchived, setShowArchived] = useState(false);



  const handleNewPost = (e) => {
    e.preventDefault();
    console.log(titleRef.current.value);
    console.log(textRef.current.value);
    console.log(image);
    console.log(JSON.stringify(tags))
    console.log(JSON.stringify(ingredients))
    if (image === null) {
      alert("Error: Please add image")
      return;
    }
    if (titleRef.current.value.length < 6) {
      alert("Error: title must be at least 6 characters")
      return;
    }
    if (textRef.current.value < 10) {
      alert("Error: description must be at least 10 characters")
      return;
    }
    if (tags.length < 1) {
      alert("Error: There must be at least 1 tag")
      return;
    }
    if (ingredients.length < 1) {
      alert("Error: There must be at least 1 ingredient")
      return;
    }


    getToken().then((token) => {
      let rand = crypto.randomUUID();
      const imageRef = ref(storage, "images/" + rand);
      uploadBytes(imageRef, image).then((e) => {
        getDownloadURL(e.ref).then((url) => {
          return [token, url]
      }).then((tokenURL) => {
        let fetchUrl = 'http://localhost:8000/recipe/create?' + 'title=' + titleRef.current.value + 
        '&ingredients=' + JSON.stringify(ingredients) +'&tags=' + JSON.stringify(tags) + '&image=' + tokenURL[1] + '&desc=' + textRef.current.value + '&fid=' + tokenURL[0]
        console.log(fetchUrl);
        fetch(fetchUrl, {
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
          return res.json()
        }).then((data) => {
          console.log(data);
          titleRef.current.value = '';
          textRef.current.value = '';
          setTags([]);
          setIngredients([]);
          setImage(null);
        })
      })
    })
    })

  };

  const handleRecipes = (e) => {
    e.preventDefault();
    setShowRecipes(true);
  };

  useEffect(() => {
    getToken().then((t) => {
      setToken(t);
    });
  }, []);

  const handleChangeImage = (e) => {
    e.preventDefault();
    if (e.target.files[0].type !== "image/png" && e.target.files[0].type !== "image/jpeg" ) {
      return;
    }
    setImage(e.target.files[0]);
  };

  return (
    <div className="dashboard">
      <Navbar part="Posts" mode={userMode} />
      <span>&nbsp;&nbsp;</span>
      <div >
        <Container>
          {userMode == "producer" ?
            <Row>
              <ButtonGroup>
                <Button
                  variant="success"
                  data-bs-toggle="modal"
                  data-bs-target="#exampleModal"
                  onClick={() => {
                    setShowRecipes(false);
                    setShowArchived(false);
                    setShowPosts(false);
                  }}
                 >New Recipe</Button>
                <Button
                  variant="warning"
                  onClick={() => {
                    setShowRecipes(true);
                    setShowArchived(false);
                    setShowPosts(false);
                  }}
                >
                  Recipes</Button>
                <Button
                  onClick={() => {
                    setShowRecipes(false);
                    setShowArchived(false);
                    setShowPosts(true);
                  }}
                >Posts</Button>
                <Button variant="danger"
                onClick={() => {
                  setShowRecipes(false);
                  setShowArchived(true);
                  setShowPosts(false);
                }}>Archives</Button>
              </ButtonGroup>
            </Row> : ""}
          <Row>
              {showArchived || showPosts || showRecipes ? <RecipeShow mode={userMode} isArchived={showArchived} isRecipe={showRecipes} isPost={showPosts} /> : ""}
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
                  Create a Recipe
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

                <div>
                  <label for="formFileLg" class="form-label">Input Image</label>
                  <input onChange={(e) => {handleChangeImage(e);}}class="form-control form-control-md" id="formFileLg" type="file" />
                </div>

                <span>&nbsp;&nbsp;</span>
                <div>
                  <InputTag tags={tags} setSelected={setTags} placeholder="Add tags to recipe" />
                </div>
                <span>&nbsp;&nbsp;</span>
                <div>
                  <InputTag tags={ingredients} setSelected={setIngredients} placeholder="Add ingredients to recipe" />
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
                  onClick={(e) => {handleNewPost(e)}}
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

export default Dashboard;
