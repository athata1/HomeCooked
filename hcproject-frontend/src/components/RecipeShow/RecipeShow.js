import React, { useEffect, useState } from 'react'
import { useAuth } from '../../Firebase/AuthContext';
import Recipes from '../Recipes/Recipes';
import './RecipeShow.css'

export default function RecipeShow({mode, isRecipe, isArchived, isPost}) {
  
  const [url, setUrl] = useState('');
  const {getToken} = useAuth();
  const [responses, setResponses] = useState([]);

  function removeResponseByPK(pk) {
    let index = responses.findIndex((res) => {
      return res.pk === pk;
    })
    let values = responses;
    responses.splice(index, 1);
  }

  function recipeProducer() {
    fetch(url, {
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
    }).then((res) => {
      return res.json();
    }).then((data) => {
      data = JSON.parse(data);
      setResponses(data);
    })
  }
  function postProducer() {
    
  }

  useEffect(() => {
    console.log(mode);
    console.log(isRecipe)
    console.log(isArchived)
    console.log(isPost)
    if (isRecipe && mode === 'producer') {
      getToken().then((token) => {
        console.log(token)
        setUrl(`http://localhost:8000/recipe/get?token=${token}`)
      })
    }
  }, [isRecipe, isPost, isArchived, mode])

  useEffect(() => {
    if (url === '')
      return;
    
    if (isRecipe && mode === 'producer') {
      recipeProducer();
    }

    if (isPost && mode === 'producer') {
      postProducer();
    }

  }, [url])
  
  return (
    <div className="recipe-show-container">
      <div className='recipe-show'>
        {isRecipe && mode === 'producer' ? responses.map((response) => {
          return <Recipes key={response.pk} mode={mode} isArchived={isArchived} isRecipe={isRecipe} isPost={isPost} response={response}/>
        }) : ""}
      </div>
    </div>
  )
}
