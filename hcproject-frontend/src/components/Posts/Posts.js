import React from "react";
import './Posts.css'
import Card from 'react-bootstrap/Card';

import { useState } from 'react';
import { Link } from "react-router-dom";
import { Switch } from "./../Switch/Switch"

function Posts({ part, mode }) {

  const [postTitle, setPostTitle] = useState('Post Title TEST')
  const [postTime, setPostTime] = useState('3 days')

  return <div className="Posts">
    <Card>
      <Card.Img variant="top" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" />
      <Card.Body>
        <Card.Title>{postTitle}</Card.Title>
        <Card.Text>
          Post Text
        </Card.Text>
      </Card.Body>
      <Card.Footer>
        <small className="text-muted">Posted {postTime} ago</small>
      </Card.Footer>
    </Card>
  </div>
};

export default Posts;

