import React from 'react';
import Notification from './Notification';

function CalendarInviteCard(props) {
    // const you = "arvind.rajaraman@berkeley.edu";
    // const emails = props.emails.filter(name => name !== you);
    // const youAndEmails = ["you", ...emails];

    const emails = props.emails

    var title = "🗓️  Event created with ";
    if (emails.length == 2) {
        title += emails[0] + " and " + emails[1];
    } else {
        title += emails[0] + " and " + emails.length + " other attendees";
    }

    var description = "A calendar event was created with " + emails.join(', ').replace(/,([^,]*)$/, ' and$1') + " at " + props.start_time + ". " + props.description;

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
