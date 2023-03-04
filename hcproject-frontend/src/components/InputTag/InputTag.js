import React, {useState} from 'react'
import './InputTag.css'
export default function InputTag({tags, setSelected, placeholder}) {

    const removeTags = indexToRemove => {
      setSelected([...tags.filter((_, index) => index !== indexToRemove)]);
    };
    const addTags = event => {
      if (event.target.value !== "") {
        setSelected([...tags, event.target.value]);
        event.target.value = "";
      }
    };
  return (
    <div className="tags-input">
        <ul id="tags">
          {tags.map((tag, index) => (
            <li key={index} className="tag">
              <span className='tag-title'>{tag}</span>
              <span className='tag-close-icon'
                onClick={() => removeTags(index)}
              >
                x
              </span>
            </li>
          ))}
        </ul>
        <input
          type="text"
          onKeyUp={event => event.key === "Enter" ? addTags(event) : null}
          placeholder={placeholder}
        />
      </div>
  )
}
