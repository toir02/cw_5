from src.utils import get_employers, create_db, create_tables, fill_db
from config import config

database_name = 'cw'
params = config()

create_db(database_name, params)
create_tables(database_name, params)
fill_db(get_employers([78638, 84585]), database_name, params)
