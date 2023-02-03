import sys
import json
import logging
import argparse
import subprocess
from json.decoder import JSONDecodeError

parser = argparse.ArgumentParser(description="Github org repository scanner")
parser.add_argument(
    "-d",
    "--debug",
    help="Show debug logs",
    action="store_const",
    dest="loglevel",
    const=logging.DEBUG,
    default=logging.INFO,
)
args = parser.parse_args()

logging.basicConfig(
    level=args.loglevel,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
    ],
)
logger = logging.getLogger()


github_json_fields = (
    "name",
    "nameWithOwner",
    "url",
    "isTemplate",
    "isEmpty",
    "isFork",
    "isInOrganization",
    "createdAt",
    "updatedAt",
    "homepageUrl",
    "description",
    "languages",
)

command = [
    "gh",
    "repo",
    "list",
    "hmcts",
    "--no-archived",
    "--json",
    ",".join(github_json_fields),
    "--limit 3000",
]

try:
    run_command = subprocess.run(command, capture_output=True)
    result = json.loads(run_command.stdout.decode("utf-8"))

    logger.info(f"Processing {len(result)} repositories...")

    for repo in result:
        logger.info(f'Processing {repo["name"]}')

except JSONDecodeError:
    print("gh cli error")
except Exception as e:
    logger.error("Unknown error occurred")
    raise Exception(e)
