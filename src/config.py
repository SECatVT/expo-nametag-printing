class GeneralConfig:

    CURRENT_YEAR = 2023

    # google sheet log configs
    GOOGLE_LOG = True
    GOOGLE_LOG_END_TOKEN = "---END---"
    GOOGLE_LOG_KEYFILE_NAME = "google_log_service_account.json"
    GOOGLE_LOG_SHEET_NAME = "testPythonLog"
    WORKSHEET_NAME = "Log1"

    GOOGLE_BACKUP_DB_SHEET_NAME = "SwapCardBackUp"
    WORKSHEET_BACKUP_DB_NAME = "Data"
    GOOGLE_DB_END_CURSOR = "endCursor"

    GOOGLE_FIRST_NAME_COL = "C"
    GOOGLE_LAST_NAME_COL = "D"
    GOOGLE_MAJOR_COL = "E"
    GOOGLE_YEAR_COL = "F"
    GOOGLE_REGIS_ID_COL = "G"
    GOOGLE_EMAIL_COL = "H"
    GOOGLE_PHONE_NUMBER_COL = "I"

    # query structure keys
    DATA = "data"
    EVENT_PERSON = "eventPerson"
    NODE = "nodes"
    FIRST_NAME = "firstName"
    LAST_NAME = "lastName"
    EMAIL = "email"
    PHONE_NUMBER = "phoneNumbers"
    DEFINITION = "definition"
    TRANSLATION = "translations"

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
        "Building Construction",
        "Chemical Engineering",
        "Civil Engineering",
        "Computer Engineering",
        "Computer Science",
        "Construction Engineering (CEM)",
        "Electrical Engineering",
        "Engineering Science and Mechanics",
        "General Engineering",
        "Industrial and Systems Engineering",
        "Materials Science Engineering",
        "Mechanical Engineering",
        "Mining Engineering",
        "Ocean Engineering",
        "Non-Engineering"
        ]
    
    major_index = {
        "AE": 0,
        "BSE": 1,
        "BME": 2,
        "BUC": 3,
        "CHE": 4,
        "CVE": 5,
        "CPE": 6,
        "CS": 7,
        "CEM": 8,
        "EE": 9,
        "ESM": 10,
        "GE": 11,
        "ISE": 12,
        "MSE": 13,
        "ME": 14,
        "OE": 15,
        "NON": 16 
    }

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
                phoneNumbers {
                    number
                }
                jobTitle
                photoUrl
                organization
                websiteUrl
                biography
                tags
                groups {
                    name
                }
                withEvent(eventId: $eventId) {
                    fields {
                        ... on MultipleSelectField {
                            translations {
                                value
                            }
                            definition {
                                translations {
                                    name
                                }
                            }
                        }
                        ... on SelectField {
                            translations {
                                value
                            }
                            definition {
                                translations {
                                    name
                                }
                            }
                        }
                        ... on TextField {
                            value
                            definition {
                                translations {
                                    name
                                }
                            }
                        }
                        ... on NumberField {
                            studentID: value
                            definition {
                                translations {
                                    name
                                }
                            }
                        }
                    }
                    badges {
                        ... on BadgeBarcode {
                            barcode
                        }
                    }
                }
                isVisible
                source
                createdAt
                updatedAt
                type
                engagementScore
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
                phoneNumbers {
                    number
                }
                jobTitle
                photoUrl
                organization
                websiteUrl
                biography
                tags
                groups {
                    name
                }
                withEvent(eventId: $eventId) {
                    fields {
                        ... on MultipleSelectField {
                            translations {
                                value
                            }
                            definition {
                                translations {
                                    name
                                }
                            }
                        }
                        ... on SelectField {
                            translations {
                                value
                            }
                            definition {
                                translations {
                                    name
                                }
                            }
                        }
                        ... on TextField {
                            value
                            definition {
                                translations {
                                    name
                                }
                            }
                        }
                        ... on NumberField {
                            studentID: value
                            definition {
                                translations {
                                    name
                                }
                            }
                        }
                    }
                    badges {
                        ... on BadgeBarcode {
                            barcode
                        }
                    }
                }
                isVisible
                source
                createdAt
                updatedAt
                type
                engagementScore
                }
            }
        }
    '''

    mass_people_query= '''
        query eventPerson($eventId: ID!, $cursor: CursorPaginationInput) {
            eventPerson(eventId: $eventId, cursor: $cursor) {
                pageInfo {
                    hasNextPage
                    endCursor
                    totalItems
                    startCursor
                    lastPage
                    hasPreviousPage
                    currentPage
                }
                totalCount
                nodes {
                    firstName
                    lastName
                    email
                    phoneNumbers {
                        number
                    }
                    withEvent(eventId: $eventId) {
                        fields {
                            ... on MultipleSelectField {
                                translations {
                                    value
                                }
                                definition {
                                    translations {
                                        name
                                    }
                                }
                            }
                            ... on SelectField {
                                translations {
                                    value
                                }
                                definition {
                                    translations {
                                        name
                                    }
                                }
                            }
                            ... on TextField {
                                value
                                definition {
                                    translations {
                                        name
                                    }
                                }
                            }
                            ... on NumberField {
                                studentID: value
                                definition {
                                    translations {
                                        name
                                    }
                                }
                            }
                        }
                        badges {
                            ... on BadgeBarcode {
                                barcode
                            }
                        }
                    }
                    groups {
                        id
                        name
                    }
                    source
                    updatedAt
                    createdAt
                }
            }
        }
    '''

class EXPOEventNotFoundError(Exception):

    def __init__(self, status_code: int, message: str) -> None:

        self.status_code = status_code
        self.message = 'Request status code: ' + str(self.status_code) + '\n' + message
        super().__init__(self.message)
