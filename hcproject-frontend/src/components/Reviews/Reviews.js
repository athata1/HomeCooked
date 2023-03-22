import React from 'react'
import { Rating } from "react-simple-star-rating";
import { render } from "react-dom";

export default function Reviews() {
    const ratingChanged = (newRating) => {
        console.log(newRating);
    };

    const [rating, setRating] = useState(0);

  // Catch Rating value
  const handleRating = (rate) => {
    setRating(rate);

    // other logic
  };
  // Optinal callback functions
  const onPointerEnter = () => console.log("Enter");
  const onPointerLeave = () => console.log("Leave");
  const onPointerMove = (value, index) => console.log(value, index);

    return (
        <Rating
            onClick={handleRating}
            onPointerEnter={onPointerEnter}
            onPointerLeave={onPointerLeave}
            onPointerMove={onPointerMove}
            // readonly={true}
            fillColorArray={['#f17a45', '#f19745', '#f1a545', '#f1b345', '#f1d045']} 
            /* Available Props */
          />
    );
}

