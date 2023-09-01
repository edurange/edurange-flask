import React, {useState, useEffect} from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import "./group_selector.css";
import { Button } from 'react-bootstrap';
import axios from 'axios';

export default function group_selector() {
  const [groupOptions, setGroupOptions] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState("");
  async function beginTest() {
    try {
        const response = await axios.get("/api/groups");
        if (response.data) {
          let groupNames = [];
          for (let i = 0; i < response.data.length; i++) {
            groupNames.push(response.data[i].name);
          }
          setGroupOptions(groupNames)
        };
    }
    catch (error) {console.log('groups error:', error);};
};
  useEffect (() => {
    beginTest();
  }, []);
    return (
    <div>
        <h1>SELECTED GROUP{selectedGroup}</h1>

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
          </Dropdown.Menu>
       </Dropdown>
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