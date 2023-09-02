import query
from config import GeneralConfig, NameTagConfig, QueryConfig

EVENT_ID = QueryConfig.event_id

people_filter = {'qrCodes': inputs['BRID']}
person = query.people_filter_query(EVENT_ID, people_filter)
