import requests

from graphql import build_ast_schema, parse, print_ast, build_client_schema
from graphql.utilities import get_introspection_query, build_client_schema

from config import QueryConfig, EXPOEventNotFoundError

url = QueryConfig.url
headers = QueryConfig.headers

def event_query(event_id):

    # Define your GraphQL query
    query = QueryConfig.event_query
    variables = {
        "eventId": event_id
    }
    
    response = requests.post(url=url, headers=headers, 
                             json={'query': query, 'variables': variables})

    # Check if the request was successful
    if not response.status_code == 200:
        # Raise the error if the request failed
        raise EXPOEventNotFoundError(response.status_code, response.text)
    
    return response


def people_search_query(event_id, search):

    # Define your GraphQL query
    query = QueryConfig.people_search_query
    variables = {
        'eventId': event_id,
        'search': search
    }

    response = requests.post(url=url, headers=headers, 
                             json={'query': query, 'variables': variables})

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response content
        print(response.json())

    else:
        # Print the error message if the request failed
        print('Request failed with status code:', response.status_code)
        print('Error message:', response.text)
    
    return response

def people_filter_query(event_id, filters):

    # Define your GraphQL query
    query = QueryConfig.people_filter_query
    variables = {
        'eventId': event_id,
        'filters': filters
    }

    response = requests.post(url=url, headers=headers, 
                             json={'query': query, 'variables': variables})

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response content
        print(response.json())

    else:
        # Print the error message if the request failed
        print('Request failed with status code:', response.status_code)
        print('Error message:', response.text)
    
    return response