import React, { useState, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';

import './Options.css';

import DashSidebar from '../../dashboard/src/sidebar/DashSidebar';
import { Options_SideNav } from '../../../../modules/nav/navItemsData';
import Options_home from './components/Options_home';
import Options_accessibility from './components/Options_accessibility';
import Options_themes from './components/Options_themes';

function Options_controller() {
  // Attempt to load user settings from localStorage or use default values

  return (
    <div className='newdash-frame'>
      <div className='newdash-frame-carpet'>

        < DashSidebar navDataToShow={Options_SideNav} />

        <div className="newdash-infopane-frame">
          <div className='newdash-infopane-content'>
            <Routes>
              <Route path="/options" element={<Options_home />} />
              <Route path="/accessibility" element={<Options_accessibility />} />
              <Route path="/themes" element={<Options_themes />} />
            </Routes>

          </div>
        </div>
      </div>
    </div>
  );
}

export default Options_controller;
