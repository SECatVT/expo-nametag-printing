class NameTagConfig:

    years = [
        "Freshman", 
        "Sophomore", 
        "Junior", 
        "Senior", 
        "Masters", 
        "Doctorate"
        ]

    majors = [
        "Aerospace Engineering",
        "Biological Systems Engineering",
        "Biomedical Engineering",
        "Chemical Engineering",
        "Civil Engineering",
        "Computer Engineering",
        "Computer Science",
        "Construction Engineering and Management",
        "Electrical Engineering",
        "Engineering Science and Mechanics",
        "General Engineering",
        "Industrial and Systems Engineering",
        "Materials Science Engineering",
        "Mechanical Engineering",
        "Mining Engineering",
        "Ocean Engineering"
        ]

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
    people_search_query= '''
        query eventPerson($eventId: ID!, $search: String!) {
            eventPerson(eventId: $eventId, search: $search) {
                nodes {
                id
                userId
                email
                firstName
                lastName
                jobTitle
                secondJobTitle
                photoUrl
                organization
                websiteUrl
                biography
                tags
                isVisible
                source
                createdAt
                updatedAt
                type
                engagementScore
                clientIds
                }
            }
        }
    '''
    people_filter_query= '''
        query eventPerson($eventId: ID!, $filters: [EventPersonFilter!]) {
            eventPerson(eventId: $eventId, filters: $filters) {
                nodes {
                id
                userId
                email
                firstName
                lastName
                jobTitle
                secondJobTitle
                photoUrl
                organization
                websiteUrl
                biography
                tags
                isVisible
                source
                createdAt
                updatedAt
                type
                engagementScore
                clientIds
                }
            }
        }
    '''

class EXPOEventNotFoundError(Exception):

    def __init__(self, status_code: int, message: str) -> None:

        self.status_code = status_code
        self.message = 'Request status code: ' + str(self.status_code) + '\n' + message
        super().__init__(self.message)
