import React, {useState, useEffect} from 'react';
import { Navbar, Nav, Container, Col, Row } from 'react-bootstrap';

import 'bootstrap/dist/css/bootstrap.css';
import './WelcomeHead.css';

export const WelcomeContext = React.createContext();

function WelcomeHead() {
    return (
        <div className='pucs-frame-tester'>

        <div className='pucs-header-main'>
            WelcomeHead.js says hello
            <Navbar expand="lg" className='nb'>
                <Container fluid>
                    <Row style={{width:"100%"}}>

                        <Col xs={1}>
                            {/* <Navbar.Brand href="#home">
                                <img src={eduRangeLogo}
                                width="auto"
                                height="auto"
                                className="d-flex align-top"
                                alt="./5.jpeg"
                                />
                            </Navbar.Brand> */}
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
            </Navbar>

            
        </div>
    </div>
    );
}

export default WelcomeHead;
