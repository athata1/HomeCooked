import React, { useEffect, useState } from "react";
import { Rating } from "react-simple-star-rating";

const ReviewList = ({ description, user_id, rating }) => {
  const [username, setUsername] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/users/id?id=" + user_id, {
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
        console.log("HERE", JSON.parse(data.data)[0].fields.user_uname);
        setUsername(JSON.parse(data.data)[0].fields.user_uname);
      });
  }, []);

  return (
    <div>
      <div class="card">
        <div class="card-header">
          <Rating
            readonly={true}
            initialValue={rating}
            fillColorArray={[
              "#f17a45",
              "#f19745",
              "#f1a545",
              "#f1b345",
              "#f1d045",
            ]}
            allowFraction={true}
          />
        </div>
        <div class="card-body">
          <blockquote class="blockquote mb-0">
            <p>{description}</p>
            <footer class="blockquote-footer pt-4">{username}</footer>
          </blockquote>
        </div>
      </div>
    </div>
  );
};

export default ReviewList;
