import React from 'react';
import Notification from './Notification';

function CalendarInviteCard(props) {
    const you = "arvind.rajaraman@berkeley.edu";
    const emails = props.emails.filter(name => name !== you);
    const youAndEmails = ["you", ...emails];

    var title = "🗓️  Event created with ";
    if (emails.length == 1) {
        title += emails[0];
    } else {
        title += emails.length + " other attendees";
    }

    var description = "A calendar event was created with " + youAndEmails.join(', ').replace(/,([^,]*)$/, ' and$1') + ". " + props.description;

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
