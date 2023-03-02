import React from "react";
import './Recipes.css'
import Card from 'react-bootstrap/Card';
import Badge from 'react-bootstrap/Badge';
import Button from "react-bootstrap/esm/Button";
import ButtonGroup from 'react-bootstrap/ButtonGroup';

import { useState } from 'react';
import { Link } from "react-router-dom";
import { Switch } from "./../Switch/Switch"

function Recipes({ part, mode }) {

  const [recipeTitle, setRecipeTitle] = useState('Recipe Title')
  const [recipeText, setRecipeText] = useState('Recipe Text')
  const [recipeTime, setRecipeTime] = useState('3 days')
  const [recipeLoc, setRecipeLoc] = useState('West Lafayette')
  const [postTag, setPostTag] = useState('Post Tag')
  const [ingredientsTag, setIngredientsTag] = useState('Ingredients Tag')
  const [systemTag, setSystemTag] = useState('System Tag')
  const [recipeImage, setRecipeImage] = useState('https://images.pexels.com/photos/1640772/pexels-photo-1640772.jpeg?cs=srgb&dl=pexels-ella-olsson-1640772.jpg&fm=jpg')

  const handleDeleteRecipes = (e) => {
    // e.preventDefault();
    // this.setState({showRecipes: true});
  };

  const handlePostRecipes = (e) => {
    // e.preventDefault();
    // this.setState({showRecipes: true});
  };

  return <div className="Posts">
    <Card>
      <Card.Img variant="top" src={recipeImage} />
      <Card.Body>
        <Card.Title>{recipeTitle} - {recipeLoc}</Card.Title>
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

        <ButtonGroup style={{ float: 'right' }}>
          <Button variant="success" onClick={handlePostRecipes}>Post</Button>
          <Button variant="danger" onClick={handleDeleteRecipes}>Delete</Button>
        </ButtonGroup>
      </Card.Body>
      <Card.Footer>
        <small className="text-muted">Posted {recipeTime} ago</small>
      </Card.Footer>
    </Card>
  </div>
};

export default Recipes;

