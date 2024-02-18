import React from 'react';
import Notification from './Notification';

function CalendarInviteCard(props) {
    const you = "Arvind Rajaraman";
    const names = props.names.filter(name => name !== you);
    const firstNames = names.map(name => name.split(' ')[0]);
    const firstNamesAndYou = ["you", ...firstNames];

    var title = "🗓️  Event created with ";
    if (firstNames.length == 1) {
        title += firstNames[0];
    } else {
        title += firstNames.length + " other attendees";
    }

    var description = "A calendar event was created with " + firstNamesAndYou.join(', ').replace(/,([^,]*)$/, ' and$1') + ". " + props.description;

    return (
        <Notification
            timestamp={props.timestamp}
            title={title}
            subtitle={props.eventTitle}
            body={description}
            links={[{url: props.url, name: "Calendar Invite"}]}
        />
    );
}

export default CalendarInviteCard;
