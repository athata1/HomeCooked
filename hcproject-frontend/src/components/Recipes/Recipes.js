import React from "react";
import './Recipes.css'
import Card from 'react-bootstrap/Card';

import { useState } from 'react';
import { Link } from "react-router-dom";
import { Switch } from "./../Switch/Switch"

function Recipes({ part, mode }) {

  const [recipeTitle, setRecipeTitle] = useState('Recipe Title')
  const [recipeText, setRecipeText] = useState('Recipe Text')
  const [recipeTime, setRecipeTime] = useState('3 days')

  return <div className="Posts">
    <Card>
      <Card.Img variant="top" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" />
      <Card.Body>
        <Card.Title>{recipeTitle}</Card.Title>
        <Card.Text>
          {recipeText}
        </Card.Text>
        <Card.Text>
          test
        </Card.Text>
      </Card.Body>
      <Card.Footer>
        <small className="text-muted">Posted {recipeTime} ago</small>
      </Card.Footer>
    </Card>
  </div>
};

export default Recipes;

