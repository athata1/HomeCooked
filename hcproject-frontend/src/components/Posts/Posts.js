import React, { useEffect } from "react";
import './Posts.css'
import Card from 'react-bootstrap/Card';

import { useState } from 'react';
import { Link } from "react-router-dom";
import { Switch } from "./../Switch/Switch"
import Recipes from "../Recipes/Recipes";

function Posts({mode, response, removeCallback, showMode}) {

  const [recipeResponse, setRecipeResponse] = useState(null)

  useEffect(() => {
    fetch("http://localhost:8000/recipe/get/id?recipe_id=" + response.fields.post_recipe,
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
    ).then((res) => {
      return res.json();
    }).then((data) => {
      setRecipeResponse(JSON.parse(data.response)[0]);
    })
  }, [])

  return (
  <div className="Posts">
    {recipeResponse ? <Recipes showMode={showMode} removeCallback={removeCallback} key={response.pk} mode={mode} postIndex={response.pk} response={recipeResponse} post_id={response.pk}/> : ""}
  </div>)
};

export default Posts;

