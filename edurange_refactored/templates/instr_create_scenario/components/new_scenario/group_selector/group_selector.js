import React, {useState, useEffect} from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import "./group_selector.css";
import { Button } from 'react-bootstrap';

export default function group_selector() {
  const [groupOptions, setGroupOptions] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState("");
  useEffect (() => {
    console.log("group achieved")
    setGroupOptions(["aGroup", "anotherGroup", "ratKing"]);
  }, []);
    return (
    <div>
        <h1>{selectedGroup}</h1>
       <Dropdown>
        <Dropdown.Toggle id="dropdown-basic">
      Select Group
        </Dropdown.Toggle>
          <Dropdown.Menu>
          {groupOptions.map((groupName, index) => (
                      <Dropdown.Item key={index} onClick={() => setSelectedGroup(groupName)}>
                          {groupName}
                      </Dropdown.Item>
                    ))}  
              <Dropdown.Item>Agh</Dropdown.Item>
          </Dropdown.Menu>
       </Dropdown>
       <Button>Next Page</Button>
    </div>
  )
}

/* <Dropdown>
            <Dropdown.Toggle>Something Here</Dropdown.Toggle>
            <Dropdown.Menu> 
                  {groupOptions.map((groupName, index) => (
                    <Dropdown.Item key={index}>{groupName}</Dropdown.Item>
                  ))}  
            </Dropdown.Menu>
        </Dropdown> */