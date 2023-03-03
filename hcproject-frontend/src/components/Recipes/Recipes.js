import React, { useEffect } from "react";
import './Recipes.css'
import Card from 'react-bootstrap/Card';
import Badge from 'react-bootstrap/Badge';
import Button from "react-bootstrap/esm/Button";
import ButtonGroup from 'react-bootstrap/ButtonGroup';

import { useState } from 'react';
import { Link } from "react-router-dom";
import { Switch } from "./../Switch/Switch"
import { ListGroup } from "react-bootstrap";
import { useAuth } from "../../Firebase/AuthContext";
import { filterBad } from "../../utils/badwords";

function Recipes({mode, response, removeCallback, postIndex, showMode}) {

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [tags, setTags] = useState([]);
  const [sysTags, setSysTags] = useState([]);
  const [index, setIndex] = useState(-1);
  const [recipeURL, setRecipeURL] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [ingredients, setIngredients] = useState([])
  const {getToken} = useAuth();

  useEffect(() => {
    setTitle(response.fields.recipe_name)
    setDescription(response.fields.recipe_desc)
    setTags(JSON.parse(response.fields.recipe_tags))
    setIngredients(JSON.parse(response.fields.recipe_ingredients))
    let json = JSON.parse(response.fields.recipe_sys_tags).healthLabels
    let res = [];
    if (json.includes('VEGAN')) {
      res.push("Vegan")
    }
    if (res.includes("VEGETARIAN")) {
      res.push("Vegetarian")
    }
    if (json.includes("PESCATARIAN")) {
      res.push("Pescatarian")
    }

    if (json.includes("PORK_FREE")) {
      res.push("Pork free");
    }
    if (json.includes("TREE_NUT_FREE")) {
      res.push("Tree Nut Free")
    }
    setSysTags(res);
    setRecipeURL(response.fields.recipe_img)

    fetch("http://localhost:8000/users/get/id?id="+response.fields.recipe_user, {
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
    }).then(res => {
      return res.json();
    }).then(response =>  {
      response = JSON.parse(response.data)[0];
      setCity(response.fields.user_city)
      setState(response.fields.user_state)
    })

  }, [])


  function handleDelete() {
    if (mode === 'producer' && showMode === 1) {
      let decision = window.confirm("Are you sure you want to delete this recipe?");
      if (!decision)
        return;
      getToken().then((token) => {
        fetch("http://localhost:8000/recipe/delete?token=" + token + "&recipe_id=" + response.pk, {
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
          alert("Deleted Recipe");
        })
      })
    }
    if (mode === 'producer' && showMode === 2) {
      getToken().then((token) => {
        fetch("http://localhost:8000/posts/delete?token=" + token + "&post_id=" + postIndex, {
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
          alert("Deleted Post");
          removeCallback(postIndex);
        })
      })
    }
  }

  function handlePost() {
    getToken().then((token) => {
      fetch("http://localhost:8000/posts/?token=" + token  + "&type=Create&recipe=" + response.pk, {
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
        alert("Created Post");
      })
    })
  }


  return <div className="posts mb-3">
  <Card>
    <Card.Img variant="top" src={recipeURL} />
    <Card.Body>
      <Card.Title >{filterBad(title)} - {city}, {state}</Card.Title>
      <Card.Text>
        {filterBad(description)}
      </Card.Text>
      <Card.Subtitle>Ingredients</Card.Subtitle>
      <ListGroup className="mb-3">
        {ingredients.map((ingredient) => {
          return <ListGroup.Item variant="success">
            {ingredient}
          </ListGroup.Item>
        })}
      </ListGroup>
      <div>
        <div className="mb-3">
          <Card.Subtitle>Systems Tags</Card.Subtitle>
          {sysTags.map((tag) => {
              return <div style={{marginRight: "2px", display: "inline-block"}}><Badge bg="danger">
                {tag}
              </Badge></div>
          })}
        </div>
        <div className="mb-3">
          <Card.Subtitle>User Tags</Card.Subtitle>
          {tags.map((tag) => {
              return <div style={{marginRight: "2px", display: "inline-block"}}><Badge bg="primary">
                {tag}
              </Badge></div>
          })}
        </div>
      </div>

      <ButtonGroup style={{ float: 'right' }}>
        {showMode === 1  && mode==="producer"?
        <Button onClick={handlePost} variant="success">Post</Button> : "" }
        {(showMode === 1 && mode==="producer") || (showMode === 2 && mode==="producer")?
        <Button onClick={handleDelete} variant="danger">Delete</Button> : ""}
      </ButtonGroup>
    </Card.Body>
  </Card>
</div>
};

export default Recipes;

