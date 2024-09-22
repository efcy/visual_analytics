import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const InteractiveMarker = ({ position, setPosition }) => {
  const map = useMapEvents({
    click(e) {
      setPosition(e.latlng);
      map.flyTo(e.latlng, map.getZoom());
    },
  });

  return position ? (
    <Marker position={position}>
      <Popup>You clicked here!</Popup>
    </Marker>
  ) : null;
};

const MapComponent = ({ center = [51.41274136352273, 5.481214767496865], zoom = 13 }) => {
  const [markerPosition, setMarkerPosition] = useState(null);
  return (
    <MapContainer center={center} zoom={zoom} style={{ height: '400px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <InteractiveMarker position={markerPosition} setPosition={setMarkerPosition} />
    </MapContainer>
  );
};

export default MapComponent;