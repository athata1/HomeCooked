import React, { useEffect, useState } from 'react'
import { useAuth } from '../../Firebase/AuthContext';
import Recipes from '../Recipes/Recipes';
import Posts from '../Posts/Posts';
import './RecipeShow.css'

export default function RecipeShow({mode, isRecipe, isArchived, isPost, responses, setResponses}) {
  
  const [url, setUrl] = useState('');
  const {getToken} = useAuth();

  function removeResponseByPK(pk) {
    let index = responses.findIndex((res) => {
      return res.pk === pk;
    })
    let values = responses;
    let res = [...responses];
    res.splice(index, 1);
    setResponses(res);
  }


  function recipeProducer() {
    setResponses([])
    getToken().then((token) => {
    fetch("http://localhost:8000/recipe/get?token=" + token, {
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
  })
  }

  function postProducer() {
    setResponses([])
    getToken().then((token) => {
      let url = "http://localhost:8000/posts/?token=" + token  + "&type=open"
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
        return res.json()
      }).then((data) => {
        setResponses(JSON.parse(data))
      })
    })
  }

  function postProducer() {
    setResponses([])
    getToken().then((token) => {
      let url = "http://localhost:8000/posts/?token=" + token  + "&type=open"
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
        return res.json()
      }).then((data) => {
        setResponses(JSON.parse(data))
      })
    })
  }

  function archiveProducer() {
    setResponses([])
    getToken().then((token) => {
      let url = "http://localhost:8000/posts/?token=" + token  + "&type=producer_closed"
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
        return res.json()
      }).then((data) => {
        setResponses(JSON.parse(data))
      })
    })
  }


  useEffect(() => {
    if (isRecipe && mode === 'producer') {
      getToken().then((token) => {
        setUrl(`http://localhost:8000/recipe/get?token=${token}`)
      })
    }
    else if (isPost && mode === 'producer') {
      getToken().then((token) => {
        setUrl("http://localhost:8000/posts?token=" + token + "&type=open")
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
          return <Recipes removeCallback={removeResponseByPK} key={response.pk} mode={mode} isArchived={isArchived} isRecipe={isRecipe} isPost={isPost} response={response}/>
        }) : ""}
        {(isPost || isArchived) && mode === 'producer' ? responses.map((response) => {
          return <Posts response={response} removeCallback={removeResponseByPK} key={response.pk} mode={mode} isArchived={isArchived} isRecipe={isRecipe} isPost={isPost} />
        }) : ""}
      </div>
    </div>
  )
}
