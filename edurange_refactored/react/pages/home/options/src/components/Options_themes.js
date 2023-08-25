import React, { useState, useEffect } from 'react';
import '../Options.css';

function Options_themes() {
  // Attempt to load user settings from localStorage or use default values
  const defaultSettings = {
    dropdown1: 'option1',
    dropdown2: 'option2',
    buttonSelection: '',
    checkboxValue: false,
    radioButtonValue: 'radio1',
    sliderValue: 50,
  };

  const [settings, setSettings] = useState(
    JSON.parse(localStorage.getItem('userSetting')) || defaultSettings
  );

  const userSetting = {
    dropdown1: settings.dropdown1,
    dropdown2: settings.dropdown2,
    buttonSelection: settings.buttonSelection,
    checkboxValue: settings.checkboxValue,
    radioButtonValue: settings.radioButtonValue,
    sliderValue: settings.sliderValue,
  };

  // Save to localStorage whenever settings change
  useEffect(() => {
    localStorage.setItem('userSetting', JSON.stringify(userSetting));
  }, [settings]);

  function handleDropdownChange(event) {
    const { name, value } = event.target;
    setSettings({ ...settings, [name]: value });
  };

  function handleButtonClick(value) {
    setSettings({ ...settings, buttonSelection: value });
  };

  function handleCheckboxChange() {
    setSettings({ ...settings, checkboxValue: !settings.checkboxValue });
  };

  function handleRadioButtonChange(event) {
    setSettings({ ...settings, radioButtonValue: event.target.value });
  };

  function handleSliderChange(event) {
    setSettings({ ...settings, sliderValue: event.target.value });
  };

  return (
    <div className='options-menu-frame'>
      <div className="options-menu-carpet">

        {/* TOP-LEFT */}
        <div className='edu3-options-pane'>
          <div className="checkmark-grid">

            <select className="selectybox" value={settings.dropdown1} onChange={handleDropdownChange}>
              <option value="option1">Option 1</option>
              <option value="option2">Option 2</option>
            </select>
            <select className="selectybox" value={settings.dropdown1} onChange={handleDropdownChange}>
              <option value="option1">Option 1</option>
              <option value="option2">Option 2</option>
            </select>
            <select className="selectybox" value={settings.dropdown1} onChange={handleDropdownChange}>
              <option value="option1">Option 1</option>
              <option value="option2">Option 2</option>
            </select>
            <select className="selectybox" value={settings.dropdown1} onChange={handleDropdownChange}>
              <option value="option1">Option 1</option>
              <option value="option2">Option 2</option>
            </select>

            <div className='boxfix'>
              <div className='boxfix'>
                <select className='selectybox' name="dropdown1" value={settings.dropdown1} onChange={handleDropdownChange}>
                  <option value="option1">Option 1</option>
                  <option value="option2">Option 2</option>
                </select>
              </div>
            </div>

            <select className="selectybox" value={settings.dropdown1} onChange={handleDropdownChange}>
              <option value="option1">Option 1</option>
              <option value="option2">Option 2</option>
            </select>
            <select className="selectybox" value={settings.dropdown1} onChange={handleDropdownChange}>
              <option value="option1">Option 1</option>
              <option value="option2">Option 2</option>
            </select>
            <select className="selectybox" value={settings.dropdown1} onChange={handleDropdownChange}>
              <option value="option1">Option 1</option>
              <option value="option2">Option 2</option>
            </select>

          </div>
        </div>

        {/* TOP-RIGHT */}
        <div className='edu3-options-pane'>
          <div className="checkmark-grid">
            <button onClick={() => handleButtonClick('button1')}>Button 1</button>
            <button onClick={() => handleButtonClick('button2')}>Button 2</button>
            <button onClick={() => handleButtonClick('button2')}>Button 2</button>
            <button onClick={() => handleButtonClick('button2')}>Button 2</button>
            <button onClick={() => handleButtonClick('button2')}>Button 2</button>
            <button onClick={() => handleButtonClick('button2')}>Button 2</button>
            <button onClick={() => handleButtonClick('button2')}>Button 2</button>
            <button onClick={() => handleButtonClick('button2')}>Button 2</button>
          </div>
        </div>

        {/* BOTTOM-LEFT */}
        <div className="edu3-options-pane">
          <div className="checkmark-grid">
            <div className="checkmark-item"><input type="checkbox" id="option1" /><label htmlFor="option1">Option 1</label></div>
            <div className="checkmark-item"><input type="checkbox" id="option2" /><label htmlFor="option2">Option 2</label></div>
            <div className="checkmark-item"><input type="checkbox" id="option3" /><label htmlFor="option3">Option 3</label></div>
            <div className="checkmark-item"><input type="checkbox" id="option4" /><label htmlFor="option4">Option 4</label></div>
            <div className="checkmark-item"><input type="checkbox" id="option5" /><label htmlFor="option5">Option 5</label></div>
            <div className="checkmark-item"><input type="checkbox" id="option6" /><label htmlFor="option6">Option 6</label></div>
            <div className="checkmark-item"><input type="checkbox" id="option7" /><label htmlFor="option7">Option 7</label></div>
            <div className="checkmark-item"><input type="checkbox" id="option8" /><label htmlFor="option8">Option 8</label></div>
          </div>
        </div>

        {/* BOTTOM-RIGHT */}
        <div className='edu3-options-pane'>
          <input className='options-menu-slider-frame' type="range" min="0" max="100" value={settings.sliderValue} onChange={handleSliderChange} />
          <input className='options-menu-slider-frame' type="range" min="0" max="100" value={settings.sliderValue} onChange={handleSliderChange} />
        </div>

      </div>
    </div>
  );
}

export default Options_themes;
