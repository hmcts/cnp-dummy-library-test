import os
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
    "--limit",
    "100",
    "--visibility",
    "public",
    "--json",
    ",".join(github_json_fields),
]

try:
    run_command = subprocess.run(command, capture_output=True)

    results = json.loads(run_command.stdout.decode("utf-8"))

    # Convert languages object to a list in each of GH repo responses.
    for item in results:
        languages = item.get("languages")
        if languages:
            item["languages"] = [language["node"]["name"] for language in languages]

    logging.debug(json.dumps(results[0], indent=4))

    # Sort all responses by name, required for job slicing to overcome /256 per job.
    results_sorted = sorted(results, key=lambda x: x["name"])

    # Generate matrix objects for 2048 possible items
    matrix00 = json.dumps(results_sorted[0:256])
    matrix01 = json.dumps(results_sorted[256:512])
    matrix02 = json.dumps(results_sorted[512:768])
    matrix03 = json.dumps(results_sorted[768:1024])
    matrix04 = json.dumps(results_sorted[1024:1280])
    matrix05 = json.dumps(results_sorted[1280:1536])
    matrix06 = json.dumps(results_sorted[1536:1792])
    matrix07 = json.dumps(results_sorted[1792:2048])

    response_json = json.dumps(results_sorted)

    logger.info(f'GH CLI arguments for debugging: {" ".join(command)}')
    logger.info(
        f"Processing {len(results_sorted)} repositories "
        f"over {round(len(results_sorted)/256)} matrix jobs..."
    )

    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        print(f"matrix00={matrix00}", file=fh)
        print(f"matrix01={matrix01}", file=fh)
        print(f"matrix02={matrix02}", file=fh)
        print(f"matrix03={matrix03}", file=fh)
        print(f"matrix04={matrix04}", file=fh)
        print(f"matrix05={matrix05}", file=fh)
        print(f"matrix06={matrix06}", file=fh)
        print(f"matrix07={matrix07}", file=fh)

except JSONDecodeError as e:
    logger.error("Github CLI execution error\n\n")
    logger.error(e)
except Exception as e:
    logger.error("Unknown error occurred")
    raise Exception(e)
