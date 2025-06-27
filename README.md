# libuiowa-scraper

A web crawler built with Scrapy designed to map and analyze the University of Iowa Libraries website structure. This tool creates a comprehensive web graph database that captures all pages, their metadata, and link relationships within the `lib.uiowa.edu` domain.

## Features

- **Complete Domain Mapping**: Crawls the entire UI Libraries website structure
- **Network Graph Database**: Stores pages as nodes and links as edges for graph analysis
- **Resume Capability**: Automatically resumes from where it left off if interrupted
- **Respectful Crawling**: Configurable delays, robots.txt compliance, and domain restrictions
- **Data Export**: Export to JSON format for external analysis
- **Progress Monitoring**: Real-time progress tracking during long crawls
- **Text Cleaning**: Automatically cleans whitespace and formatting from page content

## Project Structure

```
libuiowa-scraper/
├── config.yaml              # Configuration file
├── run.py                   # Main entry point
├── export_to_json.py        # Export database to JSON
├── monitor_crawl.py         # Monitor crawl progress
├── backup_database.py       # Create database backups
├── README.md               # This file
├── crawler/                # Scrapy project
│   ├── items.py           # Data structure definitions
│   ├── middlewares.py     # Custom middlewares (empty)
│   ├── pipelines.py       # Database storage pipeline
│   ├── settings.py        # Scrapy settings
│   └── spiders/
│       └── universal_spider.py  # Main spider
├── data/                   # Database storage
│   └── web_graph.db       # SQLite database
└── backups/               # Database backups (created automatically)
```

## Database Schema

### Nodes Table (Pages)
- `url` (PRIMARY KEY): Page URL
- `title`: Page title (cleaned)
- `meta_description`: Meta description (cleaned)
- `h1_text`: First H1 heading (cleaned)
- `status_code`: HTTP status code
- `mime_type`: Content type
- `first_seen_depth`: Crawl depth when first discovered
- `last_updated`: Timestamp of last update

### Edges Table (Links)
- `id` (PRIMARY KEY): Auto-incrementing ID
- `parent_url`: Source page URL
- `child_url`: Target page URL
- `depth`: Crawl depth when link was discovered
- `discovered_at`: Timestamp when link was found

## Configuration

Edit `config.yaml` to customize the crawler behavior:

```yaml
# Crawl depth (remove or comment out for unlimited depth)
depth: 3

# Delay between requests (seconds)
delay: 1.0

# Respect robots.txt
obey_robots: true

# Only follow URLs ending with lib.uiowa.edu
strict_domain: true

# Target domains
domains:
  - lib.uiowa.edu

# Starting URLs
start_urls:
  - https://www.lib.uiowa.edu
```

### Configuration Options

- **`depth`**: Set a number to limit crawl depth, or remove/comment out for unlimited depth
- **`delay`**: Seconds between requests (higher = more respectful to server)
- **`obey_robots`**: Whether to respect robots.txt files
- **`strict_domain`**: If true, only follow URLs ending with `lib.uiowa.edu`
- **`domains`**: List of allowed domains
- **`start_urls`**: URLs to start crawling from

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install scrapy pyyaml
   ```

2. **Clone or download the project files**

3. **Verify installation:**
   ```bash
   python -c "import scrapy, yaml; print('Dependencies installed successfully')"
   ```

## Usage

### Basic Crawl

Start a crawl with current configuration:
```bash
python run.py
```

### Test Crawl (Limited Depth)

For testing, set a depth limit in `config.yaml`:
```yaml
depth: 2  # Only crawl 2 levels deep
```

### Full Crawl (Unlimited Depth)

Remove or comment out the depth setting:
```yaml
# depth: 3  # Comment out for unlimited depth
```

### Monitor Progress

In a separate terminal, monitor crawl progress:
```bash
python monitor_crawl.py
```

### Create Backup

Create a timestamped backup of the database:
```bash
python backup_database.py
```

### Export to JSON

Export the database to JSON format:
```bash
python export_to_json.py
```

## Long-Running Crawls

For full crawls that may take hours:

### 1. Start the Crawler
```bash
python run.py
```

### 2. Monitor Progress (Optional)
In another terminal:
```bash
python monitor_crawl.py
```

### 3. Create Periodic Backups (Recommended)
Every few hours:
```bash
python backup_database.py
```

### 4. Resume if Interrupted
If the crawl is interrupted, simply restart:
```bash
python run.py
```
The crawler will automatically resume from where it left off.

## Database Queries

### Basic Statistics
```sql
-- Total pages crawled
SELECT COUNT(*) FROM nodes;

-- Total links found
SELECT COUNT(*) FROM edges;

-- Pages by depth
SELECT first_seen_depth, COUNT(*) 
FROM nodes 
GROUP BY first_seen_depth 
ORDER BY first_seen_depth;
```

### Network Analysis
```sql
-- Pages with most incoming links
SELECT child_url, COUNT(*) as incoming_links
FROM edges 
GROUP BY child_url 
ORDER BY incoming_links DESC 
LIMIT 10;

-- Pages with most outgoing links
SELECT parent_url, COUNT(*) as outgoing_links
FROM edges 
GROUP BY parent_url 
ORDER BY outgoing_links DESC 
LIMIT 10;
```

### Find Specific Content
```sql
-- Search for pages with specific text in title
SELECT url, title 
FROM nodes 
WHERE title LIKE '%research%';

-- Find all pages linking to a specific URL
SELECT parent_url 
FROM edges 
WHERE child_url = 'https://www.lib.uiowa.edu/about/';
```

## Performance Considerations

### Expected Performance
- **Small test (depth 1)**: ~1 minute, ~50 pages
- **Medium test (depth 3)**: ~10 minutes, ~1,500 pages  
- **Full crawl**: 2-6 hours, 5,000-15,000 pages

### Database Size
- **Current (1,594 pages)**: ~932KB
- **Full crawl estimate**: 5-15MB

### Memory Usage
- **Peak memory**: ~100MB
- **Database growth**: ~600 bytes per page

## Troubleshooting

### Common Issues

**"Import scrapy could not be resolved"**
- Install scrapy: `pip install scrapy`

**Database errors**
- Check if `data/` directory exists
- Verify SQLite is working: `python -c "import sqlite3"`

**Crawl taking too long**
- Increase delay in `config.yaml`
- Set a depth limit for testing

**Resume not working**
- Check that `data/web_graph.db` exists
- Verify database permissions

### Logs
- Check console output for error messages
- Log level is set to INFO by default
- Change to DEBUG in `crawler/settings.py` for more detail

## Data Analysis

The resulting database can be used for:
- **Network analysis** (centrality, communities, paths)
- **Content analysis** (page titles, descriptions, structure)
- **Link analysis** (most linked pages, link patterns)
- **Site structure mapping** (depth analysis, navigation patterns)

## Contributing

This project is designed for the University of Iowa Libraries website. To adapt for other sites:
1. Update `config.yaml` with new domains and start URLs
2. Modify `strict_domain` logic in `universal_spider.py` if needed
3. Adjust delays and settings for the target site

## License

This project is for educational and research purposes. Please respect robots.txt and be considerate of web servers when crawling. 