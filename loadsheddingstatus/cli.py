import logging
import sys
import time
from dataclasses import dataclass

import apprise
import click
import requests


@dataclass
class Configuration:
    """
        loadsheddingstatus configuration
    """

    endpoint: str = 'http://loadshedding.eskom.co.za/LoadShedding/GetStatus'
    last_status: str = None


c = Configuration()
apobj = apprise.Apprise()

log = logging.getLogger(__name__)
ch = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

log.setLevel(logging.DEBUG)
log.addHandler(ch)


# Start the Click command group
@click.group()
@click.option('--notifier', '-t', required=False, help='The notifier to use.')
def cli(notifier) -> None:
    if not notifier:
        log.warning('No notifier configured!')
    else:
        apobj.add(notifier)


@cli.command()
def ping():
    """
        Ping the loadshedding endpoint
    """

    log.info(f'Checking out {c.endpoint}...')
    try:
        r = requests.get(c.endpoint)
        log.info(f'The endpoint responded with {r.text}')
    except requests.exceptions.ConnectionError as e:
        log.error(f'Request failed with {e}')
    except Exception as e:
        log.error(f'An unhandled exception occured: {e}')


@cli.command()
@click.option('--sleep', '-s', default=60, help='Time to sleep between update checks')
def poll(sleep):
    """
        Poll for LoadShedding updates and notify on changes.
    """

    while True:
        try:
            r = requests.get(c.endpoint, timeout=15)
            log.info(f'The endpoint {c.endpoint} responded with {r.text}')

            if c.last_status is None:
                c.last_status = r.text
                continue

            if c.last_status != r.text:
                apobj.notify(
                    body=f'Eskom loadshedding stage update: {c.last_status} => {r.text}',
                    title='Loadshedding update'
                )

                c.last_status = r.text

        except requests.exceptions.ConnectionError as e:
            log.error(f'Request failed with {e}')
        except Exception as e:
            log.error(f'An unhandled exception occured: {e}')

        time.sleep(sleep)


if __name__ == '__main__':
    cli()
