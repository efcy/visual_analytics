import { useState, useEffect } from "react";
import api from "../api";
import Note from "../components/Note"
import "../styles/Home.css"
import GridSystem from '../components/GridSystem';

function Home() {
    //An array of objects
  const albums = [
    {
      id: 0,
      title: 'Album One',
      artist: 'Alex'
    },
    {
      id: 1,
      title: 'Album Two',
      artist: 'Percy'
    },
    {
      id: 2,
      title: 'Album Three',
      artist: 'Kevin'
    },
    {
      id: 3,
      title: 'Album Four',
      artist: 'John'
    },
    {
      id: 4,
      title: 'Album Five',
      artist: 'Stacy'
    },
    {
      id: 4,
      title: 'Album Five',
      artist: 'Stacy'
    },
    {
      id: 4,
      title: 'Album Five',
      artist: 'Stacy'
    }
  ]
   //The UI for the items to be shown inside the grid
   const Item = props => {
    //destrcture the props
    const { title, artist } = props

    return (
      <div className='album'>
        <h3>{title}</h3>
        <p>Artist: {artist}</p>
      </div>
    )
  }
  return (
    <div className='App'>
      {/* colCount is the number of columns for our grid system.
          md is a bootstrap breakpoint (will discuss breakpoints in the article)
      */}
      <GridSystem colCount={2} md={6}>
        {/* Here we are mapping every element to an <Item /> and pass props.
            map returns an array of JSX that the grid system will take as children.
        */}
        { albums.length > 0 ? albums.map(item => <Item key={item.id} id={item.id} title={item.title} artist={item.artist} />) : [<p>No tracks are found.</p>] }
      </GridSystem>
    </div>
  );
}

export default Home;