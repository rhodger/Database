import React, {useState} from 'react'
import logo from './logo.svg';
import './App.css';

import SearchBar from './searchBar';
import Focus from './focus';

function App() {
  const [focus, setFocus] = useState("");
  const [similar, setSimilar] = useState([]);


  /**
   * Change the currently focused company.
   * 
   * Replaces the focus content with retrieved information about the newly selected company and the
   * related section with names of retrieved related companies.
   * 
   * @param {string} name - The name of the newly focused company
   */
  const changeFocus = (name) => {
    // Percent encode name to be sent as querystring
    const encoded_name = encodeURIComponent(name);

    // Retrieve full company details
    fetch(`http://localhost:3068/api/retrieve?name=${encoded_name}`).then(async response => {
        const rbody = await response.json();
        setFocus(rbody);
    });

    // Retrieve similar companies
    fetch(`http://localhost:3068/api/similar?name=${encoded_name}`).then(async response => {
        const rbody = await response.json();
        setSimilar(rbody);
    });
  };


  return (
    <div className="App">
      <h1><a href="/">Company Database</a></h1>
      <SearchBar onChange={changeFocus}/>
      <Focus target={focus} onClick={changeFocus} similar={similar} />
    </div>
  );
}

export default App;