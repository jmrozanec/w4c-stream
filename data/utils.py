"""Utilities module"""

import json
import os
import sqlite3
import sys
import urllib.parse
import urllib.request
from datetime import datetime


def init_environment():
    """Initialize environment variables, etc.

    Returns
    -------
    None

    """
    # Append data directory to system path to alow local module imports.
    sys.path.append(get_data_path())

    # FIX `Basemap` import error...
    # if 'PROJ_LIB' not in os.environ:
    #     if 'WINDIR' in os.environ:
    #         # ...in Windows
    #         os.environ['PROJ_LIB'] = os.path.join(os.environ['CONDA_PREFIX'], 'Library', 'share')
    #     else:
    #         # ...in Unix
    #         pass


def get_google_api_key(verbose=True):
    """Get google api key from `GOOGLE_API_KEY` environment variable, if defined.

    Parameters
    ----------
    verbose : bool
        Enable verbose output.

    Returns
    -------
    str
        Google api key if defined, `None` otherwise.

    """
    api_key = None

    if 'GOOGLE_API_KEY' in os.environ:
        api_key = os.environ['GOOGLE_API_KEY']
    elif verbose:
        print('Google API key not found. Please set `GOOGLE_API_KEY` environment variable.')

    return api_key


def get_data_path(*args):
    """Get file system path relative to data directory from given arguments.

    Parameters
    ----------
    args : list[str]
        List of subdirectory names.

    Returns
    -------
    str
        File system path generated from given list of subdirectories, relative to data directory, if `args` list is
        not empty, path to data directory otherwise.

    """
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *args)


def parse_date(date):
    """Parse given date string.

    Parameters
    ----------
    date : str
        Date string in %Y-%m-%d format.

    Returns
    -------
    datetime or None
        Parsed date.

    """
    return datetime.strptime(date, '%Y-%m-%d')


def get_water_definitions(archive=''):
    """Get water definitions for given archive.

    Parameters
    ----------
    archive : str
        Archive name.

    Returns
    -------
    dict
        Water definitions for given archive if archive name is provided, all definitions otherwise.

    """
    definitions = {
        'surface': {
            'body': 'watercourse',
            'feature': 'level'
        },
        'ground': {
            'body': 'aquifer',
            'feature': 'altitude'
        }
    }

    return definitions[archive] if archive else definitions


def connect_to_db():
    """Connect to database.

    Returns
    -------
    sqlite3.Connection
        SQLite database connection.

    """
    return sqlite3.connect(get_data_path('data.db'))


def read_from_url(url, query=None, decode='utf-8', verbose=True):
    """Download HTML from given URL.

    Query string is generated from `query` dictionary and appended to URL if provided.

    Parameters
    ----------
    url : str
        Base URL.

    query : dict[str, str] or None
        Key-value pairs of URL query string.

    decode : str or bool
        Indicates if downloaded data should be decoded and which encoding to use.

    verbose : bool
        Enable verbose output.

    Returns
    -------
    str or bytearray
        Data downloaded from given URL.

    """
    url_query = f'{url}?{urllib.parse.urlencode(query)}' if query else url

    if verbose:
        print(f'Reading: {url_query}')

    response = urllib.request.urlopen(url_query)
    data = response.read()

    if decode:
        data = data.decode(decode)

    return data


def save_json(data, file_path):
    """Save given data to specified file in JSON format.

    Parameters
    ----------
    data : object
        Data object to be saved.

    file_path : str
        Path to a JSON file, where data object will be saved.

    Returns
    -------
    None

    """
    # Create parent directory if necessary.
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Save data.
    with open(file_path, 'w') as file:
        json.dump(data, file)

