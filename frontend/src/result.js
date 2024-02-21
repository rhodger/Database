import React, {useState} from 'react';

/**
 * Component representing an individual result, either of a search or of a similar company check.
 * 
 * @param {string} name - The name of this result
 * @param {function} onClick - onClick handler
 */
const Result = ({name, onClick}) => {
    return <p class="presult" onClick={onClick}>{name}</p>
}

export default Result;