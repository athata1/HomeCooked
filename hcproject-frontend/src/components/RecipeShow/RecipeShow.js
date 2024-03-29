import React, { useEffect, useState } from "react";
import { useAuth } from "../../Firebase/AuthContext";
import Recipes from "../Recipes/Recipes";
import Posts from "../Posts/Posts";
import "./RecipeShow.css";

export default function RecipeShow({mode, isRecipe, isArchived, isPost, responses, setResponses, showMode, profileMode}) {
  
  const [url, setUrl] = useState('');
  const {getToken, searchMode} = useAuth();

  function removeResponseByPK(pk) {
    let index = responses.findIndex((res) => {
      return res.pk === pk;
    });
    let values = responses;
    let res = [...responses];
    res.splice(index, 1);
    setResponses(res);
  }

  function recipeProducer() {
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
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          data = JSON.parse(data.response);
          setResponses(data);
        });
    });
  }

  function postProducer() {
    getToken().then((token) => {
      let url =
        "http://localhost:8000/posts/sort?token=" + token + "&filter=open";
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
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          console.log(data.response)
          setResponses(JSON.parse(data.response));
        });
    });
  }

  function allPosts() {
    let url = "http://localhost:8000/posts/all";
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
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        setResponses(JSON.parse(data.response));
      });
  }

  function archiveProducer() {
    getToken().then((token) => {
      let url =
        "http://localhost:8000/posts/sort?token=" +
        token +
        "&filter=producer-closed";
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
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          setResponses(JSON.parse(data.response));
        });
    });
  }

  function closedConsumerPost() {
    getToken().then((token) => {
      let url = "http://localhost:8000/posts/consumer/closed?token=" + token;
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
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          setResponses(JSON.parse(data.response));
        });
    });
  }

  function closestPosts() {
    getToken().then(token => {
      let url = "http://localhost:8000/posts/consumer/dist?token=" + token;
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
        setResponses(JSON.parse(data.response))
      })
    })
  }

  useEffect(() => {
    if (showMode !== 2 || mode !== 'consumer')
      return;
    
    if (searchMode === 1 || searchMode === 2) {
      allPosts();
    }
    else {
      closestPosts();
    }
  }, [searchMode, mode, showMode])


  useEffect(() => {
    if (showMode === 1 && mode === "producer") {
      getToken().then((token) => {
        setUrl(`http://localhost:8000/recipe/get?token=${token}`);
      });
    } else if (showMode === 2 && mode === "producer") {
      getToken().then((token) => {
        setUrl("http://localhost:8000/posts?token=" + token + "&type=open");
      });
    } else if (showMode === 3 && mode === "producer") {
      getToken().then((token) => {
        setUrl(
          "http://localhost:8000/posts?token=" + token + "&type=producer_closed"
        );
      });
    } else if (showMode === 2 && mode === "consumer") {
      setUrl("http://localhost:8000/posts/all");
    } else if (showMode === 3 && mode === "consumer") {
      getToken().then((token) => {
        setUrl("http://localhost:800/posts/consumer/closed?token" + token);
      });
    }
  }, [isRecipe, showMode, mode])

  useEffect(() => {
    if (url === "") return;

    if (showMode === 1 && mode === "producer") {
      recipeProducer();
    }

    if (showMode === 2 && mode === "producer") {
      postProducer();
    }

    if (showMode === 3 && mode === "producer") {
      archiveProducer();
    }

    if (showMode === 2 && mode === "consumer") {
      allPosts();
    }

    if (showMode === 3 && mode === "consumer") {
      closedConsumerPost();
    }
  }, [url]);

  return (
    <div className="recipe-show-container">
      <div className="recipe-show">
        {showMode === 1 && mode === "producer"
          ? responses.map((response) => {
              return (
                <Recipes
                  profileMode={profileMode}
                  removeCallback={removeResponseByPK}
                  key={response.pk}
                  mode={mode}
                  isArchived={isArchived}
                  isRecipe={isRecipe}
                  isPost={isPost}
                  response={response}
                  showMode={showMode}
                />
              );
            })
          : ""}
        {(showMode === 2 || showMode === 3) && mode === "producer"
          ? responses.map((response) => {
              return (
                <Posts
                  response={response}
                  removeCallback={removeResponseByPK}
                  key={response.pk}
                  mode={mode}
                  isArchived={isArchived}
                  isRecipe={isRecipe}
                  isPost={isPost}
                  showMode={showMode}
                  profileMode={profileMode}
                />
              );
            })
          : ""}
        {(showMode === 2 || showMode === 3) && mode === "consumer"
          ? responses.map((response) => {
              return (
                <Posts
                  response={response}
                  removeCallback={removeResponseByPK}
                  key={response.pk}
                  mode={mode}
                  isArchived={isArchived}
                  isRecipe={isRecipe}
                  isPost={isPost}
                  showMode={showMode}
                />
              );
            })
          : ""}
      </div>
    </div>
  );
}
