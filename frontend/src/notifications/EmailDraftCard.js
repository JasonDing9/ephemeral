import React from 'react';
import Notification from './Notification';

function EmailDraftCard(props) {
    const title = "✉️ Email to " + props.recipient + " drafted";
    return (
        <Notification
            timestamp={props.timestamp}
            title={title}
            subtitle={props.emailTitle}
            body={props.emailBody}
            links={[{url: props.url, name: "Open Draft"}]}
        />
    );
}

export default EmailDraftCard;
