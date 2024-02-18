import React from 'react';
import Notification from './Notification';

function SuggestionCard(props) {
    return (
        <Notification
            timestamp={props.timestamp}
            title="💡 AI Assistant said"
            subtitle="To break the ice, share one thing you are looking forward to this week."
            suggestions=""
            links={[]}
        />
    );
}

export default SuggestionCard;
