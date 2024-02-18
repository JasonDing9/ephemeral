import React from 'react';
import Notification from './Notification';

function OpenLinkCard(props) {
    const title = "🔗 " + props.description;
    return (
        <Notification
            timestamp={props.timestamp}
            title={title}
            subtitle=""
            text="We think the following link may be relevant to your discussion!"
            links={[{url: props.url, name: "Open"}]}
        />
    );
}

export default OpenLinkCard;
