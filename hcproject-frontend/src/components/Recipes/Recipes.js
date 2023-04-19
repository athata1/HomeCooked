import React, { useEffect } from "react";
import "./Recipes.css";
import Card from "react-bootstrap/Card";
import Badge from "react-bootstrap/Badge";
import Button from "react-bootstrap/esm/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";

import { useState } from "react";
import { Link } from "react-router-dom";
import { Switch } from "./../Switch/Switch";
import { ListGroup } from "react-bootstrap";
import { useAuth } from "../../Firebase/AuthContext";
import { filterBad } from "../../utils/badwords";
import { Rating } from "react-simple-star-rating";
import {getZip} from '../../utils/location'

import { Store } from 'react-notifications-component';
function createNotification(messageTitle, messageMessage, messageType) {
  Store.addNotification({
    title: messageTitle,
    message: messageMessage,
    type: messageType,
    insert: "top",
    container: "top-center",
    animationIn: ["animate__animated", "animate__fadeIn"],
    animationOut: ["animate__animated", "animate__fadeOut"],
    dismiss: {
      duration: 1000,
      onScreen: true
    }
  })
}

function Recipes({
  mode,
  response,
  removeCallback,
  postIndex,
  showMode,
  post_id,
  profileMode,
}) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [tags, setTags] = useState([]);
  const [sysTags, setSysTags] = useState([]);
  const [index, setIndex] = useState(-1);
  const [recipeURL, setRecipeURL] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [ingredients, setIngredients] = useState([]);
  const { getToken } = useAuth();
  const [rating, setRating] = useState(0);
  const [reviewDescription, setReviewDescription] = useState("");
  const [visible, setVisible] = useState(false);
  const [link, setLink] = useState('');
  const [postUser, setPostUser] = useState('');
  const [userBio, setUserBio] = useState('');
  const { searchMode, searchText} = useAuth();

  useEffect(() => {
    setTitle(response.fields.recipe_name);
    setDescription(response.fields.recipe_desc);
    setTags(JSON.parse(response.fields.recipe_tags));
    setIngredients(JSON.parse(response.fields.recipe_ingredients));
    let json = JSON.parse(response.fields.recipe_sys_tags).healthLabels;
    let res = [];
    if (json.includes("VEGAN")) {
      res.push("Vegan");
    }
    if (res.includes("VEGETARIAN")) {
      res.push("Vegetarian");
    }
    if (json.includes("PESCATARIAN")) {
      res.push("Pescatarian");
    }

    if (json.includes("PORK_FREE")) {
      res.push("Pork free");
    }
    if (json.includes("TREE_NUT_FREE")) {
      res.push("Tree Nut Free");
    }
    setSysTags(res);
    setRecipeURL(response.fields.recipe_img);

    fetch(
      "http://localhost:8000/users/get/id?id=" + response.fields.recipe_user,
      {
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
      }
    )
      .then((res) => {
        return res.json();
      })
      .then((response) => {
        response = JSON.parse(response.data)[0];
        setCity(response.fields.user_city);
        setPostUser(response.fields.user_uname);
        setUserBio(response.fields.user_bio)
        setState(response.fields.user_state);
        setLink(response.fields.user_link);
      });
  }, []);

  useEffect(() => {
    console.log()
    if (showMode === 3) {
      setVisible(true);
      return;
    }
    if (searchMode === 1 && mode === "consumer") {
      let location = getZip(searchText);
      if (location === undefined) {
        setVisible(false);
        return;
      }
      if (location[0].localeCompare(city) === 0 &&
          location[1].localeCompare(state) === 0) {
        setVisible(true);
        return;
      }
      else {
        setVisible(false)
        return;
      } 
    }
    else if (searchMode === 2 && mode === "consumer") {
      let str = searchText.split(",");
      if (str.length != 2) {
        setVisible(false);
        return;
      }
      let textCity = str[0].toUpperCase();
      let textState = str[1].toUpperCase();

      if (textCity.localeCompare(city) === 0 &&
          textState.localeCompare(state) === 0) {
        setVisible(true);
        return;
      }
      else {
        setVisible(false)
      }
      return;
    }
    else if (searchMode === 4 && mode === 'consumer') {
      let show = true;
      let foods = searchText.split(' ');
      for (let i = 0; i < foods.length; i++) {
        const food = foods[i].replace('_', ' ');
        if (food === '')
          continue;
        if (!ingredients.includes(food)) {
          show = false;
          break;
        }
      }
      setVisible(show);
    }
    else {
      setVisible(true);
    }
  }, [searchMode, searchText, showMode, ingredients])

  if (!visible) {
    return "";
  }

  function handleDelete() {
    if (mode === "producer" && showMode === 1) {
      let decision = window.confirm(
        "Are you sure you want to delete this recipe?"
      );
      if (!decision) return;
      getToken().then((token) => {
        fetch(
          "http://localhost:8000/recipe/delete?token=" +
            token +
            "&recipe_id=" +
            response.pk,
          {
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
          }
        )
          .then((res) => {
            return res.json();
          })
          .then((data) => {
            removeCallback(response.pk)
            createNotification('Success', 'Deleted Recipe', 'success')
          });
      });
    }
    if (mode === "producer" && showMode === 2) {
      getToken().then((token) => {
        fetch(
          "http://localhost:8000/posts/delete?token=" +
            token +
            "&post-id=" +
            postIndex,
          {
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
          }
        )
          .then((res) => {
            return res.json();
          })
          .then((data) => {
            createNotification('Success', 'Deleted Post', 'success')
            removeCallback(postIndex);
          });
      });
    }
  }

  function handleClose() {
    let uname = prompt("Enter username of user:");
    getToken().then((token) => {
      fetch(
        "http://localhost:8000/posts/close?token=" +
          token +
          "&post-id=" +
          post_id +
          "&uname=" +
          uname,
        {
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
        }
      ).then((res) => {
        console.log(res);
        if (res.status === 200) {
          createNotification('Success', 'Gave post to user', 'success')
        }
        else {
          createNotification('Error', 'Could not find user', 'danger')
        }
      });
    });
  }

  function handlePost() {
    getToken().then((token) => {
      fetch(
        "http://localhost:8000/posts/create?token=" +
          token +
          "&recipe=" +
          response.pk,
        {
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
        }
      )
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          createNotification('Success', "Created Post", "success")
        })
    });
  }

  function handleReview() {
    if (reviewDescription.length === 0) {
      createNotification('Error', 'Please Add a Description', 'danger')
      return;
    }
    getToken().then((token) => {
      fetch(
        "http://localhost:8000/review/create?fid=" +
          token +
          "&rating=" +
          rating +
          "&description=" +
          reviewDescription +
          "&post_id=" +
          post_id,
        {
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
        }
      )
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          console.log(data)
          createNotification('Success', 'Created Review', 'success');
        });
    });
    setRating(0);
    setReviewDescription("");
  }

  const handleRating = (rate) => {
    setRating(rate);
  };
  // Optinal callback functions
  const onPointerEnter = () => console.log("Enter");
  const onPointerLeave = () => console.log("Leave");
  const onPointerMove = (value, index) => {
    // Math.round(rating);
    console.log(value);
  };

  return (
    <div className="posts mb-3">
      <Card style={{width: '400px'}}>
        <Card.Img variant="top" src={recipeURL} />
        <Card.Body>
          <Card.Title>
            {filterBad(title)} - {city}, {state}
          </Card.Title>
          <Card.Text>{filterBad(description)}</Card.Text>
          <Card.Subtitle>Ingredients</Card.Subtitle>
          <ListGroup className="mb-3">
            {ingredients.map((ingredient) => {
              return (
                <ListGroup.Item variant="success">{ingredient}</ListGroup.Item>
              );
            })}
          </ListGroup>
          <div>
            <div className="mb-3">
              <Card.Subtitle>Systems Tags</Card.Subtitle>
              {sysTags.map((tag) => {
                return (
                  <div style={{ marginRight: "2px", display: "inline-block" }}>
                    <Badge bg="danger">{tag}</Badge>
                  </div>
                );
              })}
            </div>
            <div className="mb-3">
              <Card.Subtitle>User Tags</Card.Subtitle>
              {tags.map((tag) => {
                return (
                  <div style={{ marginRight: "2px", display: "inline-block" }}>
                    <Badge bg="primary">{tag}</Badge>
                  </div>
                );
              })}
            </div>
            <div>
              <Card.Title>User Info:</Card.Title>
              <Card.Subtitle>User: {postUser}</Card.Subtitle>
              <div className="mt-3">
                <Card.Subtitle>User Bio</Card.Subtitle>
                <Card.Text className='text-wrap'>
                  {userBio}
                </Card.Text>
              </div>
            </div>
          </div>
          {!profileMode ? (
            <ButtonGroup style={{ float: "right" }}>
              
              {showMode === 2 && mode === 'consumer' ?
                <a href={link}>
                  <Button variant="success">
                    Go To Chat
                  </Button>
                </a>
              : ""}
              {showMode === 1 && mode === "producer" ? (
                <Button onClick={handlePost} variant="success">
                  Post
                </Button>
              ) : (
                ""
              )}
              {showMode === 2 && mode === "producer" ? (
                <Button onClick={handleClose} variant="success">
                  {" "}
                  Give to Consumer
                </Button>
              ) : (
                ""
              )}
              {(showMode === 1 && mode === "producer") ||
              (showMode === 2 && mode === "producer") ? (
                <Button onClick={handleDelete} variant="danger">
                  Delete
                </Button>
              ) : (
                ""
              )}
              {showMode === 3 && mode === "consumer" ? (
                <div>
                  <button
                    className="btn btn-success"
                    data-bs-toggle="modal"
                    data-bs-target="#exampleModal"
                  >
                    Create Review
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
                            Create A Review
                          </h5>
                          <button
                            type="button"
                            className="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                          ></button>
                        </div>
                        <div className="modal-body">
                          <div>
                            <h3>Rating</h3>
                            <Rating
                              onClick={handleRating}
                              onPointerEnter={onPointerEnter}
                              onPointerLeave={onPointerLeave}
                              onPointerMove={onPointerMove}
                              readonly={false}
                              initialValue={rating}
                              fillColorArray={[
                                "#f17a45",
                                "#f19745",
                                "#f1a545",
                                "#f1b345",
                                "#f1d045",
                              ]}
                              allowFraction={true}
                              className="mb-4"
                              /* Available Props */
                            />
                            <h3>Description</h3>
                            <textarea
                              className="form-control"
                              rows="5"
                              value={reviewDescription}
                              onChange={(e) =>
                                setReviewDescription(e.target.value)
                              }
                            ></textarea>
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
                            className="btn btn-success"
                            data-bs-dismiss="modal"
                            onClick={handleReview}
                          >
                            Create
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                ""
              )}
            </ButtonGroup>
          ) : (
            ""
          )}
        </Card.Body>
      </Card>
    </div>
  );
}

export default Recipes;
