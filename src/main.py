import query
from config import QueryConfig

event_id = QueryConfig.event_id

event = query.event_query(event_id).json()

people_search = 'justinf19@vt.edu'
person = query.people_query(event_id, people_search)