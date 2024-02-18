import React from 'react';
import Notification from './Notification';

const emailMap = new Map([
    ['arvind.rajaraman@berkeley.edu', 'Arvind'],
    ['ayushi.batwara@berkeley.edu', 'Ayushi'],
    ['pgasawa@berkeley.edu', 'Parth'],
    ['jasonding@berkeley.edu', 'Jason']
]);


function CalendarInviteCard(props) {
    // const you = "arvind.rajaraman@berkeley.edu";
    // const emails = props.emails.filter(name => name !== you);
    // const youAndEmails = ["you", ...emails];

    const emails = props.emails
    const names = emails.map(email => emailMap.get(email) || email);

    var title = "🗓️  Event created with ";
    if (emails.length == 2) {
        title += names[0] + " and " + names[1];
    } else {
        title += names[0] + " and " + (names.length - 1) + " other attendees";
    }

    var description = "A calendar event was created with " + names.join(', ').replace(/,([^,]*)$/, ' and$1') + " at " + props.start_time + ". " + props.description;

    return (
        <Notification
            timestamp={props.timestamp}
            title={title}
            subtitle={props.eventTitle}
            text={description}
            links={[{url: props.url, name: "Calendar Invite"}]}
        />
    );
}

export default CalendarInviteCard;
