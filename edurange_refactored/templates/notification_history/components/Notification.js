import { createRoot } from 'react-dom/client';
import React from 'react';
import './Notification.css';

// import './unified.css';

function Notification(props) {

    const notifs_obj = JSON.parse(props.notifications, (key, value) => {
        if (typeof value === 'number') {return value.toString();}
        return value;
    });

    function buildNotificationTable() {
        return Object.keys(notifs_obj).map((notifKey) => {
          const notif = notifs_obj[notifKey];
          return (
            <tr key={notif.id} className='pucs-table-base'>
              <td className='pucs-table-cell'>{notif.id}</td>
              <td className='pucs-table-cell'>{notif.date}</td>
              <td className='pucs-table-cell'>{notif.detail}</td>
            </tr>
          );
        });
      };
    const notifications_built = buildNotificationTable();

    return (
    <div className='main-frame'>
      <div id="notification-page">
        <table >
          <caption>Table of Notification history</caption>
          <thead className='pucs-table-head'>
            <tr>
              <th className='pucs-table-cell'>Notification ID</th>
              <th className='pucs-table-cell'>Time Stamp</th>
              <th className='pucs-table-cell'>Message</th>
            </tr>
          </thead>
          <tbody>{notifications_built}</tbody>
        </table>
      </div>
    </div>
    );
};

export default Notification;
const e = document.getElementById('notification-page');
const root = createRoot(e);
root.render(<Notification notifications={e.attributes.notifications.value} />);