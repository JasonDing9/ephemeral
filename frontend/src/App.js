import './App.css';
import axios from 'axios';

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
  const [calendarInvites, setCalendarInvites] = useState([]);
  const [emailDrafts, setEmailDrafts] = useState([]);
  const [openLinks, setOpenLinks] = useState([]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios.get('http://127.0.0.1:5000').then(response => {
        response.data.forEach(item => {
          switch (item['action']) {
            case 'email':
              setEmailDrafts(emailDrafts => [...emailDrafts, item]);
              break;
            case 'schedule':
              setCalendarInvites(calendarInvites => [...calendarInvites, item]);
              break;
            case 'link':
              setOpenLinks(openLinks => [...openLinks, item]);
              break;
          }
        });
        // console.log(JSON.parse(response.data[0]));
      });
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

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
            {calendarInvites.map((invite, index) => (
              <CalendarInviteCard
                key={index}
                timestamp={invite.timestamp}
                emails={invite.emails}
                description={invite.description}
                eventTitle={invite.eventTitle}
                url={invite.url}
              />
            ))}
            <EmailDraftCard
              timestamp={new Date(now.getTime() - 25000)} // 25 seconds before now
              recipient="ayushi.batwara@berkeley.edu"
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
