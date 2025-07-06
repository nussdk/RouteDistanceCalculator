from app.client import GoogleClient
from app import parse_csv
import logging
import dotenv

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s | %(name)s-%(lineno)s | %(levelname)s | %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def main():
    logger.debug("Hello from routedistancecalculator!")

    dotenv.load_dotenv(".env.local")

    # file = parse_csv.select_file()

    # print(f"Selected file: {file}")

    # exit()

    client = GoogleClient()

    client.calc_distance_and_time("GVSU")


if __name__ == "__main__":
    main()
