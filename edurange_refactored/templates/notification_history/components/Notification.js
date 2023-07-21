import './Notification.css';
import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';

function Notification(props) {
  const notif_json = JSON.parse(props.notifications, (key, value) => {
    if (typeof value === 'number') {
      return value.toString();
    }
    return value;
  });

  const notifCount = Object.keys(notif_json).length;

  const myNotifs = [];

  for (let i = 0; i < notifCount; i++) {
    const notif_id = notif_json[i].id;
    const notif_timeStamp = notif_json[i].date;
    const notif_content = notif_json[i].detail;
    myNotifs.push([notif_id, notif_timeStamp, notif_content]);
  };

  console.log(myNotifs);

  const buildNotificationTable = (input) => {
    return input.map((item, index) => (
      <tr key={index}>
        <td>{item[0]}</td>
        <td>{item[1]}</td>
        <td>{item[2]}</td>
      </tr>
    ));
  };

  const notifTemp = buildNotificationTable(myNotifs);

  return (
    <div id="notification-page">
      <form method="POST">
        {/* {{ deleteNotify.csrf_token }}  idk what this does... */}
        <input
          name="clearButton"
          className="btn btn-dark"
          type="submit"
          value="Clear all notifications"
        />
      </form>
      <p></p>
      <table className="table">
        <caption>Table of Notification history</caption>
        <thead className="thead-dark">
          <tr>
            <th data-sort="string" scope="col">
              Notification ID
            </th>
            <th data-sort="string" scope="col">
              Time Stamp
            </th>
            <th data-sort="float" data-sort-default="desc" scope="col">
              Message
            </th>
          </tr>
        </thead>
        <tbody>{notifTemp}</tbody>
      </table>
    </div>
  );
}

export default Notification;

const e = document.getElementById('notification-page');
const root=createRoot(e);
root.render(<Notification notifications={e.attributes.notifications.value} />);
