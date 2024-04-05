import React, {useState} from 'react';
import { animated, useSpring } from '@react-spring/web';

/**
 * Component representing an individual result, either of a search or of a similar company check.
 * 
 * @param {string} name - The name of this result
 * @param {function} onClick - onClick handler
 */
const Result = ({name, onClick}) => {
    const springs = useSpring({
        config: {mass:1, tension:200, friction:50},
        from: {
            height: '0em',
        },
        to: {
            height: '1em',
        }
    })
    return (
        <animated.div style={{...springs}}>
            <p class="presult" onClick={onClick}>{name}</p>
        </animated.div>
    )
}

export default Result;