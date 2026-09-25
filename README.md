# Data.gov Scraper

Extract datasets from Data.gov, the US government's open data portal. Perfect for AI research, data discovery, and automated dataset curation for LLM training.

## Features

- 🔍 Search by keywords, organization, and tags
- 📊 Extract dataset metadata, tags, and resource counts
- 🏛️ Access 300,000+ government datasets
- ⚡ Fast httpx-based scraping (no browser needed)
- 🤖 Compatible with Claude, ChatGPT & AI agents via Apify MCP

## Input

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| searchQuery | string | Dataset keywords (e.g. 'climate', 'health') | "" |
| organization | string | Filter by organization (e.g. 'nasa', 'noaa', 'cdc') | "" |
| tags | string | Filter by tags (comma-separated) | "" |
| maxResults | integer | Maximum number of datasets to scrape | 3 |
| proxyConfiguration | object | Proxy settings (optional) | - |

## Output

Each dataset contains:

- `datasetUrl` - Full URL to the dataset page
- `datasetTitle` - Dataset name
- `organization` - Publishing organization (NASA, NOAA, CDC, etc.)
- `tags` - Topic tags
- `notes` - Dataset description
- `resources` - Number of downloadable files
- `lastModified` - Last update timestamp
- `scrapedAt` - When the data was scraped

## Use Cases

1. **AI Training Data Discovery** - Find datasets for fine-tuning LLMs
2. **Research Automation** - Auto-collect government research data
3. **Data Journalism** - Monitor new government data releases
4. **Policy Analysis** - Track datasets by organization/topic
5. **Academic Research** - Discover datasets for thesis/papers

## Integration with AI Agents

This scraper is compatible with Claude Code, ChatGPT, and other AI agents via the Apify MCP (Model Context Protocol). Use it to:

- Auto-discover datasets matching research topics
- Build curated dataset libraries for LLM training
- Monitor new releases from specific agencies (NASA, CDC, NOAA)
- Generate research reports from government data

## Pricing

- **Per Result**: $0.003 per dataset scraped
- **Startup Fee**: $0.03 per actor run

Example: Scraping 100 datasets = $0.03 + (100 × $0.003) = **$0.33**

## Example

```json
{
  "searchQuery": "climate change",
  "organization": "noaa",
  "maxResults": 50
}
```

## FAQ

**Q: How many datasets are available?**
A: Over 300,000 datasets from federal, state, and local government agencies.

**Q: What organizations are covered?**
A: NASA, NOAA, CDC, EPA, DOE, USGS, Census Bureau, and 100+ other agencies.

**Q: Can I download the actual data?**
A: This actor extracts dataset *metadata*. Use the `datasetUrl` to access download links on data.gov.

**Q: Is this compatible with ChatGPT/Claude?**
A: Yes! Fully compatible with AI agents via Apify MCP integration.

---

Built for AI agents | Compatible with Claude, ChatGPT & AI agents via Apify MCP
