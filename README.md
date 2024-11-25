# Website Crawler

An advanced website crawler tool that maps and discovers website structure and hidden paths. The tool supports both standard and aggressive crawling modes.

## Features

- Standard crawling mode for basic site mapping
- Aggressive mode to discover hidden paths and directories
- Real-time progress tracking with visual progress bars
- Automatic URL normalization and validation
- Support for common web protocols (HTTP/HTTPS)
- Configurable crawl depth and scope
- Results saved to easily readable text files

## Installation

1. Ensure Python 3.6+ is installed  
2. Clone this repository  
3. No additional dependencies required  

## Usage

Run the crawler using:

```
python crawler.py
```

You will be prompted to:  
1. Enter the target website URL  
2. Choose between standard or aggressive crawling mode  

### Crawling Modes

**Standard Mode**:  
- Follows links found in HTML pages  
- Respects robots.txt and site structure  
- Suitable for basic site mapping  

**Aggressive Mode**:  
- Tests common paths and directories  
- Discovers hidden endpoints  
- Uses wordlist from `words.txt` for path discovery  
- May find sensitive URLs  

## Output

Results are saved to a text file named after the target domain:  
- `example_com.txt` for `example.com`  
- One URL per line  
- Sorted alphabetically  

## Components

- `crawler.py`: Main entry point  
- `crawler_core.py`: Core crawling logic  
- `url_utils.py`: URL handling utilities  
- `progress.py`: Progress tracking  
- `words.txt`: Common paths wordlist  

## Notes

- Use responsibly and respect website terms of service  
- Consider rate limiting for production use  
- Some discovered URLs in aggressive mode may be sensitive  
- Press Ctrl+C to stop crawling and save current results  

## License

MIT License - Feel free to use and modify as needed  