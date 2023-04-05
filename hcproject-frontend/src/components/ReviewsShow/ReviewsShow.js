import React, { useState, useEffect } from "react";
import { Rating } from "react-simple-star-rating";

import { useAuth } from "../../Firebase/AuthContext";
import ReviewList from "../ReviewList/ReviewList";
import "./ReviewsShow.css"

const ReviewsShow = () => {
  const [rating, setRating] = useState(3);
  const [reviews, setReviews] = useState();
  const { getToken } = useAuth();
  const [username, setUsername] = useState([]);

  useEffect(() => {
    getToken().then((token) => {
      fetch("http://localhost:8000/review/get?token=" + token, {
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
          let sorted = JSON.parse(data.response).sort((a,b) => {
            return b.fields.review_rating - a.fields.review_rating
          })
          setReviews(sorted);
          console.log(sorted);
          return data;
        }).then(data => {
            console.log(JSON.parse(data));
        });
    });
  }, []);

  return (
    <div className="overflow-auto reviewsshow-width">
      <div className="px-5 overflow-auto">
        {reviews?.map((review, i) => {
          return (
            <ReviewList key={i} description={review?.fields?.review_desc} rating={review.fields.review_rating} user_id={review.fields.review_giver} />
          );
        })}
      </div>
    </div>
  );
};

export default ReviewsShow;
