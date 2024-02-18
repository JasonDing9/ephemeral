import React from 'react';
import Notification from './Notification';

function SuggestionCard(props) {
    const title = "💡 Assistant's Thoughts";
    const subtitle = "";

    console.log(props);

    return props.suggestions.map((suggestion, index) => (
        <Notification
            key={index}
            timestamp={props.timestamp}
            title={title}
            subtitle={subtitle}
            text={suggestion.replace(/^AI Assistant said: (.*)$/, '$1')}
        />
    ));
}

export default SuggestionCard;
