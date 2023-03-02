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

