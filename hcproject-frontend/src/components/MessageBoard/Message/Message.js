import React, { useEffect, useRef, useState } from 'react'
import { useAuth } from '../../../Firebase/AuthContext'
import { useChatContext } from '../ChatProvider/ChatProvider';
import {MapContainer, Marker, Popup, TileLayer} from 'react-leaflet'
import osm from '../../../utils/osm-providers';
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import './Message.css'
export default function Message({message}) {

  const {currentUser} = useAuth();
  const {user} = useChatContext();
  const [text, setText] = useState();
  const [sender, setSender] = useState();

  const markerIcon = new L.Icon({
    iconUrl: require('../../../images/marker.png'),
    iconSize: [35, 45],
  })

  const [center, setCenter] = useState(null)
  const ZOOM_LEVEL = 15;
  const mapRef = useRef();

  useEffect(() => {
    setText(message.info)
    setSender(message.senderID);
    if (message.type == 'disclose') {
      let long = parseFloat(message.info.split(' ')[1])
      let lat = parseFloat(message.info.split(' ')[0])
      setCenter([lat,long])
    }
  }, [message])
  return (
    <div className='message'>
      {message.type === 'text' ?
      
      <div className={'message-box ' + (message.senderID === currentUser.uid ? 'right' : 'left')}>
        {text}
      </div>
      
      : ""}
      {message.type === 'disclose' && center ?
      <div className={'message-box ' + (message.senderID === currentUser.uid ? 'right' : 'left')}>
        <MapContainer
            center={center}
            zoom={ZOOM_LEVEL}
            ref={mapRef}
          >
            <TileLayer 
              url={osm.maptiler.url} 
              attribution={osm.maptiler.attribution} />
            {center ?
            <Marker position={[center[0], center[1]]} icon={markerIcon}>
              <Popup>
                <b>Dropoff Location</b>
              </Popup>
            </Marker>
            : ""}
        </MapContainer>
      {text}
      </div>
      : ""}
    </div>
  )
}
