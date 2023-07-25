var lib =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/static/build/";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./MainFrame.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./MainFrame.css":
/*!***********************!*\
  !*** ./MainFrame.css ***!
  \***********************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("// extracted by mini-css-extract-plugin\n    if(false) { var cssReload; }\n  \n\n//# sourceURL=webpack://lib/./MainFrame.css?");

/***/ }),

/***/ "./MainFrame.js":
/*!**********************!*\
  !*** ./MainFrame.js ***!
  \**********************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _MainFrame_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./MainFrame.css */ \"./MainFrame.css\");\n/* harmony import */ var _MainFrame_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_MainFrame_css__WEBPACK_IMPORTED_MODULE_0__);\n!(function webpackMissingModule() { var e = new Error(\"Cannot find module './../../assets/css/style.css;'\"); e.code = 'MODULE_NOT_FOUND'; throw e; }());\n// import React, {useState, useEffect} from 'react';\n// import { Navbar, Nav, Container, Col, Row } from 'react-bootstrap';\n\n// import eduRangeLogo from './../img/logo_menu.png'\n\n// import 'bootstrap/dist/css/bootstrap.css';\n\n\n\n// export const WelcomeContext = React.createContext();\n\nfunction MainFrame() {\n  return /*#__PURE__*/React.createElement(\"div\", null, /*#__PURE__*/React.createElement(Navbar, {\n    expand: \"lg\",\n    className: \"nb\"\n  }, /*#__PURE__*/React.createElement(Container, {\n    fluid: true\n  }, /*#__PURE__*/React.createElement(Row, {\n    style: {\n      width: \"100%\"\n    }\n  }, /*#__PURE__*/React.createElement(Col, {\n    xs: 1\n  }, /*#__PURE__*/React.createElement(Navbar.Brand, {\n    href: \"#home\"\n  }, /*#__PURE__*/React.createElement(\"img\", {\n    src: eduRangeLogo,\n    width: \"auto\",\n    height: \"auto\",\n    className: \"d-flex align-top\",\n    alt: \"LOGO\"\n  }))), /*#__PURE__*/React.createElement(Col, {\n    xs: {\n      span: 10\n    }\n  }, /*#__PURE__*/React.createElement(Navbar.Toggle, {\n    \"aria-controls\": \"basic-navbar-nav\"\n  }), /*#__PURE__*/React.createElement(Navbar.Collapse, {\n    id: \"basic-navbar-nav\"\n  }, /*#__PURE__*/React.createElement(Nav, {\n    className: \"justify-content-end\",\n    style: {\n      width: \"100%\"\n    }\n  }, /*#__PURE__*/React.createElement(Nav.Link, {\n    className: \"nb\",\n    href: \"#home\"\n  }, \"Docs/Links\"), /*#__PURE__*/React.createElement(Nav.Link, {\n    className: \"nb\",\n    href: \"#link\"\n  }, \"Options\"), /*#__PURE__*/React.createElement(Nav.Link, {\n    className: \"nb pucs-text-orange-strong\",\n    href: \"#link2\"\n  }, \"Login\"))))))), /*#__PURE__*/React.createElement(\"section\", {\n    id: \"browser-frame\"\n  }, /*#__PURE__*/React.createElement(\"div\", {\n    id: \"app-container\"\n  }, \"PAGE COMPONENT HERE\")), /*#__PURE__*/React.createElement(Navbar, {\n    expand: \"lg\",\n    className: \"nb\"\n  }, /*#__PURE__*/React.createElement(Container, {\n    fluid: true\n  }, /*#__PURE__*/React.createElement(Row, {\n    style: {\n      width: \"100%\"\n    }\n  }, /*#__PURE__*/React.createElement(Col, {\n    xs: {\n      span: 12\n    }\n  }, /*#__PURE__*/React.createElement(Navbar.Toggle, {\n    \"aria-controls\": \"basic-navbar-nav\"\n  }), /*#__PURE__*/React.createElement(Navbar.Collapse, {\n    id: \"basic-navbar-nav\"\n  }, /*#__PURE__*/React.createElement(Nav, {\n    className: \"justify-content-end\",\n    style: {\n      width: \"100%\"\n    }\n  }, /*#__PURE__*/React.createElement(Nav.Link, {\n    className: \"nb\",\n    href: \"#home\"\n  }, \"Link1\"), /*#__PURE__*/React.createElement(Nav.Link, {\n    className: \"nb\",\n    href: \"#link\"\n  }, \"Link2\"), /*#__PURE__*/React.createElement(Nav.Link, {\n    className: \"nb\",\n    href: \"#link2\"\n  }, \"Link3\"))))))));\n}\n/* harmony default export */ __webpack_exports__[\"default\"] = (MainFrame);\n\n//# sourceURL=webpack://lib/./MainFrame.js?");

/***/ })

/******/ });