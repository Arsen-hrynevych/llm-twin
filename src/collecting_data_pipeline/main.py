import logging
from typing import Dict

from collecting_data_pipeline.crawlers.linkedin import LinkedInCrawler
from collecting_data_pipeline.dispatcher import CrawlerDispatcher


logger = logging.getLogger(__name__)


_dispatcher = CrawlerDispatcher()
_dispatcher.register("linkedin", LinkedInCrawler)


def handler(event: Dict[str, str]) -> Dict[str, str]:
    """
    Process the event and execute data extraction using appropriate crawler.

    Args:
        event (Dict[str, str]): Event containing 'user' and 'link' fields

    Returns:
        Dict[str, str]: Response with status code and message
    """

    user = event.get("user")
    link = event.get("link")

    if not user or not link:
        logger.error("Missing required fields")
        return {"statusCode": 400, "body": "User or link is missing"}

    try:
        crawler = _dispatcher.get_crawler(link)
        if not crawler:
            logger.warning(f"No crawler found for link: {link}")
            return {"statusCode": 404, "body": "No suitable crawler found"}

        crawler.extract_information(link=link, user=user)
        logger.info(f"Successfully processed link for user: {user}")
        return {"statusCode": 200, "body": "Link processed successfully"}

    except Exception as exc:
        logger.error(f"Error processing link: {str(exc)}")
        return {"statusCode": 500, "body": f"An error occurred: {str(exc)}"}


if __name__ == "__main__":
    test_event = {
        "user": "Arsen Hrynevych",
        "link": "https://www.linkedin.com/in/arsen-hrynevych/",
    }
    response = handler(test_event)
