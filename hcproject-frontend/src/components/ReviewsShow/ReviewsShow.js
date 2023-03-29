import React, { useState, useEffect } from "react";
import { Rating } from "react-simple-star-rating";

import { useAuth } from "../../Firebase/AuthContext";

const ReviewsShow = () => {
  const [rating, setRating] = useState(3);
  const [reviews, setReviews] = useState();
  const { getToken } = useAuth();

  useEffect(() => {
    getToken().then((token) => {
      fetch(
        "http://localhost:8000/review/get?token=" + token,
        {
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
        }
      ).then((res) => {
        return res.json();
      })
      .then((data) => {
        console.log(data)
      });
    })
  }, []);

  return (
    <div className="reviewshow-width px-5">
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
            /* Available Props */
          />
        </div>
        <div class="card-body">
          <blockquote class="blockquote mb-0">
            <p>
              SPLENDID STUFF LADS
            </p>
            <footer class="blockquote-footer pt-4">
              USERNAME
            </footer>
          </blockquote>
        </div>
      </div>
    </div>
  );
};

export default ReviewsShow;
