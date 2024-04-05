import React, {useState} from 'react';
import Result from './result';

/**
 * This component represents the combined search bar and results
 * 
 * @param {function} onChange - onChange handler
 */
const SearchBar = ({onChange}) => {
    const [content, setContent] = useState("");
    const [results, setResults] = useState([]);

    /**
     * Handles changed focus
     * 
     * @param {string} name - Pass changed focus up
     */
    const changeFocus = (name) => {
        setContent("");
        setResults([]);
        onChange(name);
    }

    /**
     * Handles an update in the value held by the searchbar
     * 
     * @param {Event} e - change event
     */
    const handleChange = (e) => {
        const readable_value = e.target.value;
        setContent(readable_value);

        // Percent encode updated value for http request
        const new_value = encodeURIComponent(readable_value);

        // Retrieve search results for updated value
        fetch(`http://localhost:3068/api/search?name=${new_value}`).then(async response => {
            const rbody = await response.json();
            setResults(rbody.map(x => {
                return <Result name={x} onClick={() => changeFocus(x)} />;
            }));
        });
    };

    return <div className='Search'>
        <input
            type="search"
            placeholder="Search here"
            onChange={handleChange}
            value={content}
        />
        <div className="results">
            {results}
        </div>
    </div>
}

export default SearchBar;