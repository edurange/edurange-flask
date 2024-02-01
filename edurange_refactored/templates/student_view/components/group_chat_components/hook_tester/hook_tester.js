/* Display one chat entry.
 */

import React, { useState, useEffect } from 'react';

function HookTester(props) {
    
    const [count, setCount] = useState(0)
    const [letters, setLetters] = useState("")
    
    useEffect(  ()  =>  {
        //console.log("Count changed")
        setLetters(letters + 'e');
     }, [props.messages.length]);

     function sayHello() {
        setCount(count + 1);
     }
        
    return (
      <div className="test">
        <h3>Letters: {letters}</h3>
        <h3>Count: {count}</h3>
        <button onClick={sayHello}>Add 1</button>;
      </div>
    );
}

export default HookTester;    
   



