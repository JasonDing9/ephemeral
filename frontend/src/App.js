import './App.css';

import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import CalendarInviteCard from './notifications/CalendarInviteCard';
import EmailDraftCard from './notifications/EmailDraftCard';
import OpenLinkCard from './notifications/OpenLinkCard';
import React, { useState, useEffect } from 'react';

function App() {
  const now = new Date();

  return (
    <div>
      <Navbar className="bg-body-secondary">
        <Container>
          <Navbar.Brand>App Name</Navbar.Brand>
        </Container>
      </Navbar>
      <Container>
        <br />
        <Row>
          <Col>
            <CalendarInviteCard
              timestamp={now}
              names={['Arvind Rajaraman', 'Ayushi Batwara', 'Parth Asawa']}
              description="This debugging session is for getting the video decompression module to work."
              eventTitle="Arvind / Ayushi Debugging Session 🐛"
              url="https://google.com"
            />
            <EmailDraftCard
              timestamp={new Date(now.getTime() - 25000)} // 25 seconds before now
              recipient="Ayushi Batwara"
              emailTitle="Follow-up on meeting"
              emailBody="Hi Ayushi, Just following up on the email I sent yesterday. Best, Arvind"
              url="https://google.com"
            />
            <OpenLinkCard
              timestamp={new Date(now.getTime() - 10 * 60000)} // 10 minutes before now
              url="https://docs.google.com/document/d/1eXAcPF0r35dyT_zn38gOPHIMLsN2G1MxM8f-rjSWodY/edit"
              description="Tree Hacks Project Ideation Doc"
            />
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
