import './App.css';
import axios from 'axios';

import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import CalendarInviteCard from './notifications/CalendarInviteCard';
import EmailDraftCard from './notifications/EmailDraftCard';
import OpenLinkCard from './notifications/OpenLinkCard';
import ClarifyCard from './notifications/ClarifyCard';
import SuggestionCard from './notifications/SuggestionCard';
import React, { useState, useEffect } from 'react';

import backgroundImage from './background.gif'

function App() {
  const now = new Date();
  const [notifications, setNotifications] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000');
      const sortedData = response.data.sort((a, b) => b.creation_time - a.creation_time);
      const sortedNotifications = sortedData.filter(item => item.action !== "suggestion");
      const sortedSuggestions = sortedData.filter(item => item.action === "suggestion").slice(-1);

      setNotifications(sortedNotifications);
      setSuggestions(sortedSuggestions);
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
    <div className='wrapper' style={{'backgroundImage': `url(${backgroundImage})`, 'height': '100%', 'filter': 'invert(100%) hue-rotate(200deg) saturate(60%)'}}>
      <Navbar className="bg-body-secondary">
        <Container>
          <Navbar.Brand>Ephemeral</Navbar.Brand>
        </Container>
      </Navbar>
      <Container>
        <br />
        <Tabs defaultActiveKey="notifications">
          <Tab eventKey="notifications" title="Notifications">
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
                    case 'clarify':
                      return (
                        <ClarifyCard
                          key={index}
                          timestamp={item.creation_time}
                          description={item.result}
                        />
                      )
                    default:
                      return null;
                  }
                })}
              </Col>
            </Row>
          </Tab>
          <Tab eventKey="suggestions" title="Suggestions">
            <br />
            {suggestions.map((item, index) => (
              <SuggestionCard
                key={index}
                timestamp={item.creation_time}
                suggestions={item.suggestion}
              />
            ))}
          </Tab>
        </Tabs>
        <br />
      </Container>
    </div>
  );
}

export default App;
