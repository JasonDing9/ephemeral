import React, { useState, useEffect } from 'react';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
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
        const timeDifference = new Date() - new Date(props.timestamp);
        const newTimeString = timeAgo(new Date(props.timestamp));
        setTimeString(newTimeString);
      };
  
      const intervalId = setInterval(updateTime, 1000);
  
      return () => clearInterval(intervalId);
    }, [props.timestamp]);
    
    useEffect(() => {
        const collapseTimeout = setTimeout(() => {
          setCollapsed(true);
        }, 5000);
    
        return () => clearTimeout(collapseTimeout);
      }, []);
    
      const openLink = (linkUrl) => {
        window.open(linkUrl, '_blank');
      };
    
    return (
        <Card className='card' style={{'color': "#000", 'backgroundColor': "rgba(255, 255, 255, 0.8)"}}>
            <Card.Text  className={`cardHeader ${collapsed ? 'collapsed' : ''}`} onClick={() => setCollapsed(!collapsed)}>
                {collapsed ? props.title : timeAgo(props.timestamp)}

                <div style={{ float: 'right' }}>
                    {collapsed ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                </div>
            </Card.Text>
            {!collapsed && <Card.Body style={{"textAlign": "center"}}>
                <Card.Title>{props.title}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">{props.subtitle}</Card.Subtitle>
                <Card.Text>{props.text}</Card.Text>
                {props.links && Array.isArray(props.links) && props.links.map((link, index) => (
                    <Button variant="light" onClick={() => openLink(link.url)}>{link.name}</Button>
                ))}
            </Card.Body>}
        </Card>
    );

}

export default Notification;