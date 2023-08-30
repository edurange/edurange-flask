/* This is the entry point for the parent component page and
* the super container for the other components.
*/


// Corresponding stylesheet, in the same folder as the component. 
import "./ScenarioTable.css";


import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';

import Table from 'react-bootstrap/Table';

// Your component should always begin with a capital letter.
function ScenarioTable({ scenarios }) {

	const [scenarioList, setScenarioList] = useState([]);

	useEffect(() => {
		const fakeScenarioList = 
			[
				[0,"Noogie", 1],
				[1,"Boogie", 2],
				[2, "Grog", 0],
			];
	
		setScenarioList(fakeScenarioList);	
	}, []);

	const renderScenarios = () => {
		/*const printMap = Object.values(s_list).map((scenario) => {
			console.log('-----scenario:-------');
			console.log(JSON.stringify(scenario));
			console.log('-----s_list------');
			console.log(JSON.stringify(s_list));
		});*/
		const s_list = scenarioList;
		if(s_list.length > 0) {	
			console.log("you did it");
			console.log(s_list.length);
			return s_list.map((scenario, index) => {
				<React.Fragment>
					<tr key={index}>
						
						<td>coop</td>
						<td>BS Description</td>
						<td>gymtanlaunder</td>
					</tr>
				</React.Fragment>
				});
		} else {
			console.log("you've mad an irreperable mistake")
			return;
		}
	}

       return (
	       
		<div className="Scenario_Table">
			<Table striped border hover>
	       			<thead>
	       				<tr>
	       					<th>Scenario</th>
	       					<th>Description</th>
	       					<th>Action</th>
	       				</tr>
	       			</thead>
	       			
	       			<tbody>
	       				{scenarioList.map((row, rowIndex) => (
						<tr key={rowIndex}>
							{row.map((col, colIndex) => (
								<td key={colIndex}>{col}</td>
							))}
						</tr>
					))}
	       				<tr>
						<td>Scenario Name</td>
						<td>Status</td>
						<td>Description</td>
					</tr>
	       			</tbody>
	       		</Table>
	       </div>

       );
}


export default ScenarioTable;
