class QueryConfig: 

    event_id = 'RXZlbnRfMTEyNDY4Ng=='
    url = 'https://developer.swapcard.com/event-admin/graphql'
    headers = {
        'Authorization': 'NjRhOGNiNjc4MTMxY2RhZTMwYmIyN2E0OmYxOGZiMmY0YWZlMjQxMWViY2M1NGRiOTQ3ZTY3YzBh',
        'Accept': 'application/json'
    }
    event_query = '''
        query EventById($eventId: ID!) {
            event(id: $eventId) {
                id
                slug
                title
                beginsAt
                endsAt
                createdAt
                htmlDescription
                banner {
                    imageUrl
                }
                address {
                    place
                    street
                    city
                    zipCode
                    state
                    country
                }
                isLive
                updatedAt
                language
                timezone
                totalPlannings
                totalExhibitors
                totalSpeakers
                groups {
                    id
                    name
                    peopleCount
                }
            }
        }
    '''
    people_query= '''
        query eventPerson($eventId: ID!, $search: String!) {
            eventPerson(eventId: $eventId, search: $search) {
                nodes {
                id
                email
                createdAt
                firstName
                lastName
                jobTitle
                organization
                userId
                }
            }
        }
    '''
    
class EXPOEventNotFoundError(Exception): 
    
    def __init__(self, status_code: int, message: str) -> None:

        self.status_code = status_code
        self.message = 'Request status code: {}\n'.format(self.status_code) + message
        super().__init__(self.message)