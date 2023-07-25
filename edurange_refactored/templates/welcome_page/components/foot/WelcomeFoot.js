import React, {useState, useEffect} from 'react';
import { Navbar, Nav, Container, Col, Row } from 'react-bootstrap';

import eduRangeLogo from './../img/logo_menu.png'

import 'bootstrap/dist/css/bootstrap.css';
import './WelcomeFoot.css';
// import './unified.css';

export const WelcomeContext = React.createContext();

function WelcomeFoot() {
    return (
        <div>
            <Navbar expand="lg" className='nb'>
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
            </Navbar>
        </div>
    );
}

export default WelcomeFoot;
