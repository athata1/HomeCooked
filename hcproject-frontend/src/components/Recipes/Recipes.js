import React from "react";
import './Recipes.css'
import Card from 'react-bootstrap/Card';
import Badge from 'react-bootstrap/Badge';

import { useState } from 'react';
import { Link } from "react-router-dom";
import { Switch } from "./../Switch/Switch"

function Recipes({ part, mode }) {

  const [recipeTitle, setRecipeTitle] = useState('Recipe Title')
  const [recipeText, setRecipeText] = useState('Recipe Text')
  const [recipeTime, setRecipeTime] = useState('3 days')
  const [postTag, setPostTag] = useState('Post Tag')
  const [ingredientsTag, setIngredientsTag] = useState('Ingredients Tag')
  const [systemTag, setSystemTag] = useState('System Tag')
  const [recipeImage, setRecipeImage] = useState('https://images.pexels.com/photos/1640772/pexels-photo-1640772.jpeg?cs=srgb&dl=pexels-ella-olsson-1640772.jpg&fm=jpg')

  return <div className="Posts">
    <Card>
      <Card.Img variant="top" src={recipeImage} />
      <Card.Body>
        <Card.Title>{recipeTitle}</Card.Title>
        <Card.Text>
          {recipeText}
        </Card.Text>
        <Badge bg="primary">
          {postTag}
        </Badge>{' '}
        <Badge bg="success">
          {ingredientsTag}
        </Badge>{' '}
        <Badge bg="danger">
          {systemTag}
        </Badge>
      </Card.Body>
      <Card.Footer>
        <small className="text-muted">Posted {recipeTime} ago</small>
      </Card.Footer>
    </Card>
  </div>
};

export default Recipes;

