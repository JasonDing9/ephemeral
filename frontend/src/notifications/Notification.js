import React, { useState, useEffect } from 'react';
import Card from 'react-bootstrap/Card';
import { ChevronUp, ChevronDown } from 'react-bootstrap-icons';

function timeAgo(date) {
    const now = new Date();
    const diff = now - date;

    const seconds = diff / 1000;
    const minutes = seconds / 60;
    const hours = minutes / 60;
    const days = hours / 24;
    const months = days / 30;
    const years = months / 12;

    if (years > 1) {
        return `${Math.floor(years)} year${years > 1 ? 's' : ''} ago`;
    } else if (months > 1) {
        return `${Math.floor(months)} month${months > 1 ? 's' : ''} ago`;
    } else if (days > 1) {
        return `${Math.floor(days)} day${days > 1 ? 's' : ''} ago`;
    } else if (hours > 1) {
        return `${Math.floor(hours)} hour${hours > 1 ? 's' : ''} ago`;
    } else if (minutes > 1) {
        return `${Math.floor(minutes)} minute${minutes > 1 ? 's' : ''} ago`;
    } else {
        return `${Math.floor(seconds)} second${seconds > 1 ? 's' : ''} ago`;
    }
}

function Notification(props) {
    const [timeString, setTimeString] = useState("");
    const [collapsed, setCollapsed] = useState(false);

    useEffect(() => {
      const updateTime = () => {
        const timeDifference = new Date() - props.timestamp;
        const newTimeString = timeAgo(props.timestamp);
        setTimeString(newTimeString);
      };
  
      const intervalId = setInterval(updateTime, 1000);
  
      return () => clearInterval(intervalId);
    }, [props.timestamp]);

    const timeDifference = new Date() - props.timestamp;
    const importance = (timeDifference < 30000) ? "importance2" : "importance1";
    

    return (
        <Card className={`card ${importance}`}>
            <Card.Header className="cardHeader" onClick={() => setCollapsed(!collapsed)}>
                {collapsed ? props.title : timeAgo(props.timestamp)}

                <div style={{ float: 'right' }}>
                    {collapsed ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
                </div>
            </Card.Header>
            {!collapsed && <Card.Body>
                <Card.Title>{props.title}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">{props.subtitle}</Card.Subtitle>
                <Card.Text>{props.body}</Card.Text>
                {props.links.map((link, index) => (
                    <Card.Link key={index} href={link.url}>{link.name}</Card.Link>
                ))}
            </Card.Body>}
        </Card>
    );

}

export default Notification;

