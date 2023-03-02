import React, { useEffect } from "react";
import './Recipes.css'
import Card from 'react-bootstrap/Card';

import { useState } from 'react';
import { Link } from "react-router-dom";
import { Switch } from "./../Switch/Switch"

function Recipes({mode, isArchived, isRecipe, isPost, response}) {

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [tags, setTags] = useState([]);
  const [sysTags, setSysTags] = useState([]);
  const [index, setIndex] = useState(-1);
  const [recipeURL, setRecipeURL] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');


  useEffect(() => {
    console.log(response);
    setTitle(response.fields.recipe_name)
    setDescription(response.fields.recipe_desc)
    setTags(JSON.parse(response.fields.recipe_tags))
    let json = JSON.parse(response.fields.recipe_sys_tags).healthLabels
    let res = [];
    if (res.includes('VEGAN')) {
      res.append("Vegan")
    }
    if (res.includes("VEGETARIAN")) {
      res.append("Vegetarian")
    }
    if (res.includes("PESCATARIAN")) {
      res.append("Pescatarian")
    }

    if (res.includes("PORK_FREE")) {
      res.append("Pork free");
    }

    setSysTags(res);
    console.log(JSON.parse(response.fields.recipe_tags));
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


  return (
  <div className="recipe">
    {JSON.stringify(response)}
    <div className="recipe-header">
      <div className="title">
        
      </div>
    </div>
  </div>)
};

export default Recipes;

