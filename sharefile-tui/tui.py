"""
Demonstrates a dynamic Layout

"""

import configuration
from datetime import datetime
from urllib import parse
import urllib.request
import json
import http.client

from rich import box

from time import sleep
from rich.json import JSON
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.table import Table

rawUrl = 'https://storage-usw-121.sharefile.com/download.ashx?dt=dt5f63254bd85f4ba4464e00552c807c64&cid=3oZttEpJ52U2kBxBgbRIf2fme6pfaCQV&zoneid=zp68549224-de4a-4a86-d9f2-9868fs3fc9&exp=1674076760&zsid=F7&h=LIh9udygee2a8I59qPzH%2FZ8Xlpk2CwhaaAgHgGJ0Ge8%3D'
rawUrl = 'https://docs.python.org/3/howto/urllib2.html?q=alkdsjf'
rawUrl = 'https://spencersmolen.sf-api.com/sf/v3/Users'
rawUrl = 'https://spencersmolen.sf-api.com/sf/v3/Users(251db3cf-3b99-479e-976c-d560570f7068)'


def authenticate(hostname, client_id, client_secret, username, password):
    """ Authenticate via username/password. Returns json token object.

    Args:
    string hostname - hostname like "myaccount.sharefile.com"
    string client_id - OAuth2 client_id key
    string client_secret - OAuth2 client_secret key
    string username - my@user.name
    string password - my password """

    uri_path = '/oauth/token'

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'password', 'client_id': client_id, 'client_secret': client_secret,
              'username': username, 'password': password}

    conn = http.client.HTTPSConnection(hostname)
    conn.request('POST', uri_path, urllib.parse.urlencode(
        params), headers=headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    token = None

    if response.status == 200:
        token = json.loads(response.read())
        print('Received token info', token)
    else:
        print("FUCKKKK")
        exit()

    conn.close()
    return token


def get_hostname(token):
    return '%s.sf-api.com' % (token['subdomain'])

# def tableUrlElems(parsedUrl):
#     table = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL_DOUBLE_HEAD)
#     table.add_column("URL Component", style="bold cyan",
#                      width=15, justify="right", no_wrap=False)
#     table.add_column("Value", no_wrap=False)
#
#     # Per https://docs.python.org/3.10/library/urllib.parse.html#urllib.parse.urlparse,
#     #  SCHEME://NETLOC/PATH;PARAMETERS?QUERY#FRAGMENT
#
#     elemNames = ["scheme", "netloc", "path", "params", "query", "fragment"]
#     for idx, x in enumerate(elemNames):
#         table.add_row(x, parsedUrl[idx])
#     return table
#
#
# def parseUrlElems(url, printTable=False):
#     parsedUrl = parse.urlparse(rawUrl)
#     if printTable == True:
#         tableUrlElems(parsedUrl)
#     return parse.urlparse(rawUrl)
#


console = Console()


def make_layout():
    layout = Layout()

    layout.split(
        Layout(name="header", size=1),
        Layout(name="URI", ratio=1),
        Layout(ratio=3, name="Components"),
        Layout(ratio=12, name="main"),
        Layout(size=10, name="footer"),
    )

    layout["main"].split_row(Layout(name="side"), Layout(name="body", ratio=2))

    # layout["side"].split(Layout(name="URI Components"), Layout(name="URI Arguments"))

    layout["body"].update(
        Align.center(
            Text(
                """REQUEST NOT SENT""",
                justify="center",
            ),
            vertical="middle",
        )
    )

    return layout


class Header:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text("ShareFile API Debug Tool", no_wrap=False, style="bold magenta", justify="center")


class UriComponents:
    """Renders the time in the center of the screen."""

    def __init__(self, uri):

        self.uri = uri
        self.components = parse.urlparse(uri)

        # headers = get_authorization_header()
        # req = urllib.request.Request(uri, None, headers)
        # self.response = urllib.request.urlopen(uri)
        # self.parameters = parse.parse_qsl(self.components)

    def tableUrlElems(self, parsedUrl):
        table = Table(show_header=True, header_style="bold magenta",
                      box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column("URL Component", style="bold cyan",
                         width=15, justify="right", no_wrap=False)
        table.add_column("Value", no_wrap=False)

        # Per https://docs.python.org/3.10/library/urllib.parse.html#urllib.parse.urlparse,
        #  SCHEME://NETLOC/PATH;PARAMETERS?QUERY#FRAGMENT

        elemNames = ["scheme", "netloc", "path", "params", "query", "fragment"]
        for idx, x in enumerate(elemNames):
            table.add_row(x, parsedUrl[idx])
        return table

    def parseUrlElems(self, url, printTable=False):
        parsedUrl = parse.urlparse(rawUrl)
        if printTable == True:
            self.tableUrlElems(parsedUrl)
        return parse.urlparse(rawUrl)

    def __rich__(self) -> Table:
        return self.tableUrlElems(self.components)


class UriResponse:
    """Renders the time in the center of the screen."""

    def set_authorization_header(self):
        self.auth_header = {'Authorization': 'Bearer %s' % (
            self.token['access_token'])}
        return self.auth_header

    def __init__(self, uri, apiToken):
        self.uri = uri
        self.token = apiToken
        self.auth_header = {
            'Authorization': 'Bearer %s' % (apiToken['access_token'])}

        self.auth_header = self.set_authorization_header()
        req = urllib.request.Request(
            uri, headers=self.set_authorization_header())
        self.response = urllib.request.urlopen(req).read().decode()
        # self.parameters = parse.parse_qsl(self.components)

    # def fetchRequest(self):
    #     resp = urllib.request.get(self.uri)

    #     if resp.ok:
    #         return "FAILED TO FETCH HTML."
    #     else:
    #         return resp.text

    # def printUrlArgs(self):
    #     table = Table(show_header=True, header_style="bold magenta",
    #                   box=box.MINIMAL_DOUBLE_HEAD)
    #     table.add_column("Argument", style="bold cyan",
    #                      width=15, justify="right")
    #     table.add_column("Value")
    #     for x, y in self.arguments:
    #         table.add_row(x, y)
    #     return table

    def __rich__(self) -> JSON:
        jsonResponse = JSON(self.response)
        return jsonResponse
        # return jsonResonse.from_data(self.response)


class UriArguments:
    """Renders the time in the center of the screen."""

    def __init__(self, uri):
        self.uri = uri
        self.arguments = parse.parse_qsl(parse.urlparse(uri).query)

    def printUrlArgs(self):
        table = Table(show_header=True, header_style="bold magenta",
                      box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column("Argument", style="bold cyan",
                         width=15, justify="right")
        table.add_column("Value")
        for x, y in self.arguments:
            table.add_row(x, y)
        return table

    def __rich__(self) -> Table:
        return self.printUrlArgs()


def main():
    config = configuration.load_config()
    print(config.get("General", "subdomain"))
    print(config.get("General", "subdomain"))
    apiToken = authenticate(config.get("General", "subdomain"),
                            config.get("Credentials", "client_id"),
                            config.get("Credentials", "client_secret"),
                            config.get("Credentials", "username"),
                            config.get("Credentials", "password")
    )
    # apiToken = authenticate('spencersmolen.sharefile.com', '6e0w2gbWgoZTt6KMcHZUppDGHuCqgmHW', 'YzTXjEnJd28fMGdH3N2LHr4Wvta7086CcEiHzzc4SnhBuI6G', 'spencer.smolen@citrix.com', 'gjvgomrrjjlto33c')
    accessToken = apiToken["access_token"]

    layout = make_layout()
    # layout["header"].update(Header())
    layout["URI"].update(Panel(rawUrl))
    # layout["body"].update(Panel(UriArguments(rawUrl)))
    layout["body"].update(Panel(UriResponse(rawUrl, apiToken)))
    # layout["URI Components"].update(Panel(UriComponents(rawUrl),expand=False))
    layout["side"].update(Panel(UriArguments(rawUrl)))
    layout["Components"].update(Panel(UriComponents(rawUrl), expand=True))
    layout["footer"].visible = False

    with Live(layout, screen=True, redirect_stderr=False) as live:
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            pass


main()
