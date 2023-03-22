import React, { useState, useEffect } from "react";
import { Rating } from "react-simple-star-rating";

const ReviewsShow = () => {
  const [rating, setRating] = useState(3);

  useEffect(() => {
    setRating(5);
    console.log(rating);
  }, []);

  // Catch Rating value
  const handleRating = (rate) => {
    setRating(rate);
  };
  // Optinal callback functions
  const onPointerEnter = () => console.log("Enter");
  const onPointerLeave = () => console.log("Leave");
  const onPointerMove = (value, index) => {
    Math.round(rating);
    console.log(value, index)
  };
  return (
    <div className="reviewshow-width px-5">
      <div class="card">
        <div class="card-header">
          <Rating
            onClick={handleRating}
            onPointerEnter={onPointerEnter}
            onPointerLeave={onPointerLeave}
            onPointerMove={onPointerMove}
            readonly={true}
            initialValue={rating}
            fillColorArray={['#f17a45', '#f19745', '#f1a545', '#f1b345', '#f1d045']}
            // tooltipArray={['Terrible', 'Bad', 'Average', 'Great', 'Prefect']}
            // showTooltip={true}
            allowFraction={true}
            /* Available Props */
          />
        </div>
        <div class="card-body">
          <h5 class="card-title">USERNAME</h5>
          <p class="card-text">SPLENDID STUFF LADS</p>
        </div>
      </div>
    </div>
  );
};

export default ReviewsShow;
