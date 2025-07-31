import asyncio
import os
import ssl
from typing import Any, Dict, List
import certifi
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_tavily import TavilyCrawl, TavilyExtract, TavilyMap

from logger import (Colors, log_error, log_header, log_info, log_success,
                    log_warning)

load_dotenv()

ssl_context = ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


embedding = OpenAIEmbeddings(
    model="text-embedding-3-small", show_progress_bar=False, chunk_size=50, retry_min_seconds=10
)

vectorstore = PineconeVectorStore(
    embedding=embedding,
    index_name=os.getenv("INDEX_NAME"),
)
tavily_extract = TavilyExtract()
tavily_map = TavilyMap(max_depth=5, max_breadth=20, max_pages=1000)
tavily_crawl = TavilyCrawl()

async def main():
    """Main async function to orchestrate the workflow."""
    log_header("VECTOR STORAGE PHASE")

    log_info("TaviliCrawl: starting to crawl documentation from https://python.langchain.com/")

    res = tavily_crawl.invoke({
        "url": "https://python.langchain.com/",
        "max_depth": 1,
        "extract_depth": "advanced",
        # "instructions": "Extract all documentation of Memory modules, including all submodules and their documentation.",
    })
    print(res)
    all_docs: List[Document] = [Document(page_content=result['raw_content'], metadata={"source": result['url']}) for result in res['results']] 
    log_success("TaviliCrawl: successfully crawled documentation")
    print(all_docs)

if __name__ == "__main__":
    asyncio.run(main())
 