import React, {useContext, useState, useEffect} from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import "./group_selector.css";
import { Button } from 'react-bootstrap';
import axios from 'axios';
import { CreateScenarioContext } from '../../src/create_scenario';


export default function group_selector() {

  const [groupOptions, setGroupOptions] = useState([]);
  const { groupNameSelection, setGroupNameSelection } = useContext( CreateScenarioContext );

  async function getGroupList() {
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
    getGroupList();
  }, []);

    return (
        <div>
          <Dropdown>
            <Dropdown.Toggle id="dropdown-basic">
          Select Group
            </Dropdown.Toggle>
              <Dropdown.Menu>
              {groupOptions.map((groupName, index) => (
                          <Dropdown.Item key={index} onClick={() => setGroupNameSelection(groupName)}>
                              {groupName}
                          </Dropdown.Item>
                        ))}  
              </Dropdown.Menu>
          </Dropdown>
        </div>
      )
  }

