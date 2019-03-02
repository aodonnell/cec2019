import backend
import utils

LOG = utils.get_logger(__file__)

def main():
    LOG.info('Starting service...')

if __name__ == '__main__':
    try:
        main()
    finally:
        backend.delete_instance()
        LOG.info('Instance removed...')