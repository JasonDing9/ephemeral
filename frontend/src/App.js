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
  const [notifications, setNotifications] = useState([]);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000');
      const sortedData = response.data.sort((a, b) => b.creation_time - a.creation_time);
      setNotifications(sortedData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetchData();
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
            {notifications.map((item, index) => {
              switch (item.action) {
                case 'email':
                  return (
                    <EmailDraftCard
                      key={index}
                      timestamp={item.creation_time}
                      recipient={item.recipient}
                      emailTitle={item.subject}
                      emailBody={item.body}
                      // url={item.link}
                    />
                  );
                case 'schedule':
                  return (
                    <CalendarInviteCard
                      key={index}
                      start_time={item.start_time}
                      timestamp={item.creation_time}
                      emails={item.attendeeEmails}
                      description={item.description}
                      eventTitle={item.summary}
                      url={item.link}
                    />
                  );
                case 'link':
                  return (
                    <OpenLinkCard
                      key={index}
                      timestamp={item.creation_time}
                      url={item.link}
                      description={item.description}
                    />
                  );
                default:
                  return null;
              }
            })}
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
