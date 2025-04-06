import argparse
import sys
import logging
from rich.console import Console
from rich.markdown import Markdown
from utils.crawler.crawler import DocumentationCrawler
from utils.crawler.extractor import ContentExtractor
from utils.processor.indexer import DocumentProcessor
from utils.qa.query_processor import QueryProcessor
from utils.llm.gemini import GeminiLLM
import os
from dotenv import load_dotenv

load_dotenv()

console = Console()

class QAAgentCLI:
    """Command Line Interface for the Q&A Agent."""
    
    def __init__(self):
        self.vector_store = None
        self.query_processor = None
        self.llm = None
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
    def parse_args(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(description="AI-powered Documentation Q&A Agent")
        parser.add_argument("--url", required=True, help="URL of the documentation website to process")
        parser.add_argument("--max-pages", type=int, default=100, help="Maximum number of pages to crawl")
        parser.add_argument("--persist-dir", default="./chroma_db", help="Directory to persist vector store")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
        
        return parser.parse_args()
    
    def setup_logging(self, verbose=False):
        """Setup logging configuration."""
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()]
        )
    
    def initialize(self, args):
        """Initialize the agent components."""
        console.print("[bold blue]Initializing Documentation Q&A Agent...[/bold blue]")
        
        # Set up logging
        self.setup_logging(args.verbose)
        
        # Crawl documentation site
        console.print(f"[bold]Crawling documentation from {args.url}...[/bold]")
        crawler = DocumentationCrawler(args.url, max_pages=args.max_pages)
        crawled_content = crawler.crawl()
        
        if not crawled_content:
            console.print("[bold red]Error: Failed to crawl any content from the provided URL.[/bold red]")
            sys.exit(1)
        
        # Extract meaningful content
        console.print("[bold]Extracting content from crawled pages...[/bold]")
        extractor = ContentExtractor()
        for url, content in crawled_content.items():
            if content and content.get('html'):
                content['extracted'] = extractor.extract_content(content['html'])
        
        # Process and index documents
        console.print("[bold]Processing and indexing documents...[/bold]")
        processor = DocumentProcessor(api_key=self.api_key)
        documents = processor.create_documents(crawled_content)
        chunked_docs = processor.split_documents(documents)
        
        # Create vector store
        console.print("[bold]Creating vector store...[/bold]")
        self.vector_store = processor.create_vector_store(chunked_docs, args.persist_dir)
        
        # Initialize query processor
        self.query_processor = QueryProcessor(self.vector_store, self.api_key)
        
        # Initialize LLM
        self.llm = GeminiLLM(self.api_key)
        
        console.print("[bold green]Initialization complete! Ask me questions about the documentation.[/bold green]")
    
    def run_interactive_session(self):
        """Run an interactive Q&A session."""
        if not self.query_processor or not self.llm:
            console.print("[bold red]Error: Agent not properly initialized.[/bold red]")
            return
            
        history = []
        
        while True:
            try:
                # Get user input
                query = input("\n> ")
                
                # Handle exit commands
                if query.lower() in ('exit', 'quit', 'q'):
                    console.print("[bold blue]Goodbye![/bold blue]")
                    break
                
                # Process query
                contexts = self.query_processor.process_query(query)
                
                if not contexts:
                    console.print("[italic yellow]I couldn't find any relevant information in the documentation.[/italic yellow]")
                    continue
                
                # Generate answer
                result = self.llm.generate_answer(query, contexts, history)
                
                # Display answer
                console.print(Markdown(result["answer"]))
                
                # Display sources
                if result["source_urls"]:
                    console.print("\n[bold]Sources:[/bold]")
                    for url in result["source_urls"]:
                        console.print(f"- {url}")
                
                # Update history
                history.append({"query": query, "answer": result["answer"]})
                
            except KeyboardInterrupt:
                console.print("\n[bold blue]Exiting...[/bold blue]")
                break
                
            except Exception as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")
                logging.error(f"Error in interactive session: {e}", exc_info=True)

def main():
    """Main entry point for the CLI."""
    cli = QAAgentCLI()
    args = cli.parse_args()
    cli.initialize(args)
    cli.run_interactive_session()

if __name__ == "__main__":
    main() 