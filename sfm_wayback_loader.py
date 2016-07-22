from sfmutils.consumer import BaseConsumer, MqConfig, EXCHANGE
from subprocess import check_output, CalledProcessError
import logging
import argparse
import os

log = logging.getLogger(__name__)


class WaybackLoader(BaseConsumer):
    def __init__(self, data_filepath, wb_collection_name="sfm", mq_config=None):
        BaseConsumer.__init__(self, mq_config=mq_config)
        self.data_filepath = data_filepath
        self.wb_collection_name = wb_collection_name
        self.collection_filepath = os.path.join(self.data_filepath, "collections", wb_collection_name)
        if not os.path.exists(self.data_filepath):
            log.info("Creating %s", self.data_filepath)
            os.makedirs(self.data_filepath)
        if not os.path.exists(self.collection_filepath):
            log.info("Initing %s", self.wb_collection_name)
            check_output("wb-manager init {}".format(self.wb_collection_name), shell=True, cwd=self.data_filepath)
            # Create empty index file
            open(os.path.join(self.collection_filepath, "indexes/index.cdxj"), 'w').close()

    def on_message(self):
        # Message should be WARC created
        warc_filepath = self.message["warc"]["path"]
        warc_symlink_filepath = os.path.join(self.collection_filepath, "archive", (os.path.basename(warc_filepath)))

        os.symlink(warc_filepath, warc_symlink_filepath)

        cmd = "wb-manager index {} {}".format(self.wb_collection_name, warc_symlink_filepath)

        try:
            log.info("Loading %s", warc_filepath)

            check_output(cmd, shell=True, cwd=self.data_filepath)
            log.debug("Loading %s completed.", warc_filepath)
        except CalledProcessError, e:
            log.error("%s returned %s: %s", cmd, e.returncode, e.output)

if __name__ == "__main__":
    # Logging
    logging.basicConfig(format='%(asctime)s: %(name)s --> %(message)s', level=logging.DEBUG)

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("username")
    parser.add_argument("password")
    parser.add_argument("queue")
    parser.add_argument("data_filepath")
    parser.add_argument("--collection-name", default="sfm")
    parser.add_argument("--debug", type=lambda v: v.lower() in ("yes", "true", "t", "1"), nargs="?",
                        default="False", const="True")

    args = parser.parse_args()

    # Logging
    logging.basicConfig(format='%(asctime)s: %(name)s --> %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)

    # Adding a queue name that is prefixed with this host. This will allow sending messages directly
    # to this queue. This approach could be generalized so that the queue specific binding is created
    # and the queue name is automatically removed.
    loader = WaybackLoader(
        args.data_filepath,
        wb_collection_name=args.collection_name,
        mq_config=MqConfig(args.host, args.username, args.password, EXCHANGE,
                           {args.queue: ["warc_created", "{}.warc_created".format(args.queue)]}))
    loader.run()
