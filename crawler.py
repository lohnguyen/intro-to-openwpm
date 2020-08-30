import pandas as pd
from openwpm.automation import CommandSequence, TaskManager

DB_VANILLA = './db/vanilla'
DB_UBLOCK = './db/ublock'
PATH_CSV = './top-1m.csv'
NUM_BROWSERS = 1

# The list of sites that we wish to crawl

data = pd.read_csv(PATH_CSV)
# sites = data.iloc[0:9, 1].values
sites = data.iloc[0:99, 1].values

# Loads the default manager params
# and NUM_BROWSERS copies of the default browser params
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i]['http_instrument'] = True
    # Record cookie changes
    browser_params[i]['cookie_instrument'] = True
    # Record JS Web API calls
    browser_params[i]['js_instrument'] = True
    # Turn on uBlock Origin
    browser_params[i]['ublock-origin'] = True
    # Launch browsers headless
    browser_params[i]['display_mode'] = 'headless'

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = DB_UBLOCK
manager_params['log_directory'] = DB_UBLOCK

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites
for site in sites:
    site = 'http://' + site
    # Parallelize sites over all number of browsers set above.
    command_sequence = CommandSequence.CommandSequence(
        site, reset=True,
        callback=lambda success, val=site:
        print("CommandSequence {} done".format(val)))

    # Start by visiting the page
    command_sequence.get(sleep=3, timeout=60)

    # Run commands across the three browsers (simple parallelization)
    manager.execute_command_sequence(command_sequence)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
