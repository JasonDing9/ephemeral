import React from 'react';
import Notification from './Notification';

function ClarifyCard(props) {
    const title = "Potential Insight❓";
    return (
        <Notification
            timestamp={props.timestamp}
            title={title}
            subtitle=""
            text={props.description}
            // links={[{url: props.url, name: "Open"}]}
        />
    );
}

export default ClarifyCard;