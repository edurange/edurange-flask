
import './Welcome.css';
import MainFrame from '../../../main_frame/MainFrame';
import {createRoot} from 'react-dom/client';
import React, { useState, useEffect } from 'react';
import { Navbar, Col, Row, Nav, Container} from 'react-bootstrap';
import WelcomeFoot from '../foot/WelcomeFoot';
import WelcomeHead from '../head/WelcomeHead';


function Welcome(props) {
    return (
        <div>
            <MainFrame>
                <WelcomeHead/>

                {/* <Navbar expand="lg" className='nb'>
                    <Container fluid>
                        <Row style={{width:"100%"}}>

                            <Col xs={1}>
                                <Navbar.Brand href="#home">
                                    <img src={eduRangeLogo}
                                    width="auto"
                                    height="auto"
                                    className="d-flex align-top"
                                    alt="/home/exoriparian/dev/edurange/ws/mainframe/src/img/5.jpeg"
                                    />
                                </Navbar.Brand>
                            </Col>
            
                            <Col xs={{ span: 10}}>
                                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                                <Navbar.Collapse id="basic-navbar-nav">
                                    <Nav className="justify-content-end" style={{ width: "100%" }}>
                                    <Nav.Link className='nb' href="#home">Docs/Links</Nav.Link>
                                    <Nav.Link className='nb' href="#link">Options</Nav.Link>
                                    <Nav.Link className='nb pucs-text-orange-strong' href="#link2">Login</Nav.Link>
                                    </Nav>
                                </Navbar.Collapse>
                            </Col>
                            
                        </Row>
                    </Container>
                </Navbar> */}

                <section id='browser-frame'>
                    <div id="app-container">
                        We are checking...
                        {/* PAGE COMPONENT HERE */}

                    </div>
                </section>

                {/* <Navbar expand="lg" className='nb'>
                    <Container fluid>
                        <Row style={{width:"100%"}}>
                            <Col xs={{ span: 12 }}>
                                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                                <Navbar.Collapse id="basic-navbar-nav">
                                    <Nav className="justify-content-end" style={{ width: "100%" }}>
                                        <Nav.Link className='nb' href="#home">Link1</Nav.Link>
                                        <Nav.Link className='nb' href="#link">Link2</Nav.Link>
                                        <Nav.Link className='nb' href="#link2">Link3</Nav.Link>
                                    </Nav>
                                </Navbar.Collapse>
                            </Col>
                        </Row>
                    </Container>
                </Navbar> */}
                <WelcomeFoot/>

            </MainFrame>
    </div>
    );
}

export default Welcome;

var e = document.getElementById('welcome-page');
const root=createRoot(e);

root.render(<Welcome/>);






