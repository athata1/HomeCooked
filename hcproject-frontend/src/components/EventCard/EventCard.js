import React, { useEffect, useRef, useState } from 'react'
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import { useAuth } from '../../Firebase/AuthContext';
export default function EventCard(response) {
  const titleRef = useRef()
  const locationRef = useRef()
  const textRef = useRef()
  const timeRef = useRef()

  const [location, setLocation] = useState();
  const [title, setTitle] = useState();
  const [description, setDescription] = useState();
  const [date, setDate] = useState();
  const [time, setTime] = useState();
  const [id, setId] = useState();
  const [url, setUrl] = useState("");
  const {getToken} = useAuth()


  useEffect(() => {
    setLocation(response.response.fields.event_location);
    setTitle(response.response.fields.event_name)
    setDescription(response.response.fields.event_desc)
    setDate(response.response.fields.event_date)
    setTime(response.response.fields.event_time);
    setId(response.response.pk)
  }, [])

  function formatURLDate(date) {
    let year=date.getFullYear();
    let month=date.getMonth().toString().padStart(2,'0');
    let day=date.getDate().toString().padStart(2,'0');
    var minutes = date.getMinutes().toString().padStart(2,'0');
    var hour = ((date.getHours() ) % 24).toString().padStart(2, '0');
    return `${year}${month}${day}T${hour}${minutes}00Z`
  }

  useEffect(() => {
    let ms = Date.parse(date + " " + time)
    let start = formatURLDate(new Date(ms))
    let end = formatURLDate(new Date(ms + 2*60*60*1000));

    setUrl(`https://www.google.com/calendar/render?action=TEMPLATE&text=${title}&details=${description}&location=${location}&dates=${start}}%2F${end}`)
  }, [date, time, title, description,location])

  function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  }
  
  function handleInit() {
    textRef.current.value = description
    locationRef.current.value = location
    titleRef.current.value = title
    let ms = Date.parse(date + " " + time)
    let newDate = new Date(ms)
    timeRef.current.value = formatDate(newDate)
  }

  function handleChange(e) {
    console.log(timeRef.current.value);
    if (timeRef.current.value === '') {
      alert("Event must have a start time");
      return;
    }
    if (titleRef.current.value.length < 6) {
      alert("Title must have at least 6 characters");
      return;
    }
    if (textRef.current.value.length < 10) {
      alert("Description must have at least 20 characters");
      return;
    }
    if (locationRef.current.value.length < 10) {
      alert("Location must have at least 20 characters");
      return;
    }
      
    let date = new Date(timeRef.current.value);
    let millis = date.getTime();
    getToken().then((token) => {
      let url = 'http://localhost:8000/event/change?' +
      'token=' + token +
      '&event-id=' + id + 
      '&title=' + titleRef.current.value +
      '&desc=' + textRef.current.value + 
      '&location=' + locationRef.current.value + 
      '&time=' + millis
      fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
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
      }).then((data)=> {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const seconds = date.getSeconds().toString().padStart(2, '0');
        const militaryTime = `${hours}:${minutes}:${seconds}`;

        setLocation(locationRef.current.value)
        setTitle(titleRef.current.value);
        setDescription(textRef.current.value)
        setDate(date.toISOString().split('T')[0])
        setTime(militaryTime)
      })
    })
  }

  return (
    <div>
      <div
          className="modal fade"
          id={"eventModal" + id}
          tabIndex="-1"
          aria-labelledby={"eventModalLabel" + id}
          aria-hidden="true"
        >
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id={"eventModalLabel" + id}>
                  Update Event
                </h5>
                <button
                  type="button"
                  className="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div className="modal-body">
                <input
                  type="title"
                  className="form-control settings-input"
                  placeholder="Title"
                  ref={titleRef}
                // value={deleteAccountPassword}
                // onChange={(e) => setDeleteAccountPassword(e.target.value)}
                />
                <span>&nbsp;&nbsp;</span>
                <textarea
                  placeholder="Text"
                  className="form-control"
                  id="email_body"
                  rows="7"
                  ref={textRef}
                // placeholder="Text"
                // type="textarea"
                // multiline={true} 
                // style={{padding: 10}} 
                // textAlignVertical="top"
                // className="form-control settings-input"
                // style={{height: "100px"}}

                // value={deleteAccountPassword}
                // onChange={(e) => setDeleteAccountPassword(e.target.value)}
                />
                <span>&nbsp;&nbsp;</span>

                {/* <div>
                  <label for="#formFileLg" className="form-label">Input Image</label>
                  <input onChange={(e) => {handleChangeImage(e);}}className="form-control form-control-md" id="formFileLg" type="file" />
                </div>*/}
                <span>&nbsp;&nbsp;</span>
                <div>
                  <input
                    type="location"
                    className="form-control settings-input"
                    placeholder="Location"
                    ref={locationRef} />
                </div>
                <span>&nbsp;&nbsp;</span>
                <div>
                  <label for="meeting-time">Time of Event: </label>
                  <span>&nbsp;&nbsp;</span>
                  <input ref={timeRef} id="meeting" type="datetime-local" name="meetingdate" />

                  {/* <InputTag tags={ingredients} setSelected={setIngredients} placeholder="Add ingredients to recipe" /> */}
                </div>

              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Close
                </button>
                <button
                  type="button"
                  className="btn btn-primary"
                  data-bs-dismiss="modal"
                  onClick={(e) => { handleChange(e) }}
                >
                  Add Recipe
                </button>
              </div>
            </div>
          </div>
        </div>
      <Card style={{marginLeft: '20px', marginRight: '20px', marginBottom: '20px'}}>
        <Card.Header>{title}</Card.Header>
        <Card.Body>
          <Card.Title>
            Location: {location}
          </Card.Title>
          <Card.Title>
            Date: {date}
          </Card.Title>
          <Card.Title>
            Start Time: {time}
          </Card.Title>
          <Card.Text>
            {description}
          </Card.Text>
          {
            <a href={url}>
              <Button variant="primary">Add to Calendar</Button>
            </a>
          }
          {" "}
          <Button onClick={handleInit} variant="danger" data-bs-target={"#eventModal" + id} data-bs-toggle="modal">Edit</Button>
        </Card.Body>
      </Card>
    </div>
  )
}
