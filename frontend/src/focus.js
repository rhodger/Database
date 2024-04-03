import React, {useState} from 'react';
import Result from './result';

/**
 * Component representing the section of a page displaying information reliant on currently focused
 * company.
 * 
 * @param {Array.<string>} target - The details of the company to be focused
 * @param {Array.<string>} similar - A list of names of similar companies
 * @param {function} onClick - onClick handler
 */
const Focus = ({target, similar, onClick}) => {
    return <div className="Focus">
        <div className="FocusContent">
            <h2>{target['company_name']}</h2>
            <h4 className="Subtitle" >{target['industry']}, {target['country']}</h4>
            <p>{target['about']}</p>
        </div>
        <div className="Related">
            <p>Related: {similar.map(x => {return <Result name={x} onClick={() => onClick(x)} />})}</p>
        </div>
    </div>
}

export default Focus;