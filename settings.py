from environs import Env
env = Env()
env.read_env()  # Read .env into os.environ, if it exists

domains = {
    'stage1': {
        'home': 'https://staging.osf.io',
        'api': 'https://api.staging.osf.io',
        'files': 'https://files.us.staging.osf.io',
        'cas': 'https://accounts.staging.osf.io',
        'custom_institution_domains': ['https://staging-osf-nd.cos.io'],
    },
    'stage2': {
        'home': 'https://staging2.osf.io',
        'api': 'https://api.staging2.osf.io',
        'files': 'https://files.us.staging2.osf.io',
        'cas': 'https://accounts.staging2.osf.io',
        'custom_institution_domains': [],
    },
    'stage3': {
        'home': 'https://staging3.osf.io',
        'api': 'https://api.staging3.osf.io',
        'files': 'https://files.us.staging3.osf.io',
        'cas': 'https://accounts.staging3.osf.io',
        'custom_institution_domains': [],
    },
    'test': {
        'home': 'https://test.osf.io',
        'api': 'https://api.test.osf.io',
        'files': 'https://files.us.test.osf.io',
        'cas': 'https://accounts.test.osf.io',
        'custom_institution_domains': [],
    },
    'prod': {
        'home': 'https://osf.io',
        'api': 'https://api.osf.io',
        'files': 'https://files.osf.io',
        'cas': 'https://accounts.osf.io',
        'custom_institution_domains': [
            'https://open.uwstout.edu',
            'https://osf.arizona.edu',
            'https://osf.asu.edu',
            'https://osf.fsu.edu',
            'https://osf.jmu.edu',
            'https://osf.nd.edu',
            'https://osf.nyu.edu',
            'https://osf.sc.edu',
            'https://osf.uc.edu',
            'https://osf.usc.edu',
            'https://osf.ucla.edu',
            'https://osf.ucr.edu',
            'https://osf.wustl.edu',
            'https://osf.research.vcu.edu'
        ]
    }
}

DRIVER = env('DRIVER', 'Firefox')
HEADLESS = env.bool('HEADLESS', False)

QUICK_TIMEOUT = env.int('QUICK_TIMEOUT', 4)
TIMEOUT = env.int('TIMEOUT', 10)
LONG_TIMEOUT = env.int('LONG_TIMEOUT', 30)
VERY_LONG_TIMEOUT = env.int('VERY_LONG_TIMEOUT', 60)

DOMAIN = env('DOMAIN', 'stage1')

NEW_USER_EMAIL = env('NEW_USER_EMAIL')

# Preferred node must be set to run tests on production
PREFERRED_NODE = env('PREFERRED_NODE', None)
if DOMAIN == 'prod':
    PREFERRED_NODE = env('PREFERRED_NODE')

EXPECTED_PROVIDERS = env.list(
    'EXPECTED_PROVIDERS',
    [
        'bitbucket',
        'box',
        'dataverse',
        'dropbox',
        'figshare',
        'github',
        'gitlab',
        'googledrive',
        'osfstorage',
        'owncloud',
        'onedrive',
        's3'
    ])

OSF_HOME = domains[DOMAIN]['home']
API_DOMAIN = domains[DOMAIN]['api']
FILE_DOMAIN = domains[DOMAIN]['files']
CAS_DOMAIN = domains[DOMAIN]['cas']
CUSTOM_INSTITUTION_DOMAINS = domains[DOMAIN]['custom_institution_domains']

# Browser capabilities for browserstack testing
caps = {
    'chrome': {'browser': 'Chrome', 'os': 'Windows', 'os_version': '10', 'resolution': '2048x1536'},
    'edge': {'browser': 'Edge', 'os': 'Windows', 'os_version': '10', 'resolution': '2048x1536'},
    'firefox': {'browser': 'Firefox', 'os': 'Windows', 'os_version': '10', 'resolution': '2048x1536'},
}

BUILD = DRIVER

if DRIVER == 'Remote':
    BSTACK_USER = env('BSTACK_USER')
    BSTACK_KEY = env('BSTACK_KEY')

    BUILD = env('TEST_BUILD', 'chrome')
    DESIRED_CAP = caps[BUILD]

    upper_build = BUILD.upper()

    USER_ONE = env('{}_USER'.format(upper_build), env('USER_ONE', ''))
    USER_ONE_PASSWORD = env('{}_USER_PASSWORD'.format(upper_build), env('USER_ONE_PASSWORD', ''))

    USER_TWO = env('{}_USER_TWO'.format(upper_build), env('USER_TWO', ''))
    USER_TWO_PASSWORD = env('{}_USER_TWO_PASSWORD'.format(upper_build), env('USER_TWO_PASSWORD', ''))
else:
    USER_ONE = env('USER_ONE')
    USER_ONE_PASSWORD = env('USER_ONE_PASSWORD')

    USER_TWO = env('USER_TWO')
    USER_TWO_PASSWORD = env('USER_TWO_PASSWORD')


# Used to skip certain tests on specific stagings
STAGE1 = DOMAIN == 'stage1'
STAGE2 = DOMAIN == 'stage2'
STAGE3 = DOMAIN == 'stage3'
TEST = DOMAIN == 'test'
PRODUCTION = DOMAIN == 'prod'
