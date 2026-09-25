"""Data.gov Open Data Portal Scraper"""
print("DEBUG: main.py loaded")
import os
import re
from datetime import datetime, timezone
from urllib.parse import urlencode, urljoin

import httpx
from apify import Actor
from bs4 import BeautifulSoup
print("DEBUG: imports complete")


async def main():
    """Main scraper entry point."""
    print("DEBUG: main() called")
    async with Actor:
        print("DEBUG: inside Actor context")
        # Get input
        print("DEBUG: about to get input")
        actor_input = await Actor.get_input()
        print(f"DEBUG: got input: {actor_input}")
        if not actor_input:
            actor_input = {}
        
        print("DEBUG: starting scraper")
        Actor.log.info('Starting Data.gov scraper...')
        
        # Parse input
        search_query = actor_input.get('searchQuery', '')
        organization = actor_input.get('organization', '')
        tags = actor_input.get('tags', '')
        max_results = actor_input.get('maxResults', 3)
        
        # Build search URL
        params = {}
        if search_query:
            params['q'] = search_query
        if organization:
            params['organization'] = organization
        if tags:
            params['tags'] = tags
        
        search_url = "https://catalog.data.gov/dataset"
        if params:
            search_url += f"?{urlencode(params)}"
        
        Actor.log.info(f'Search URL: {search_url}')
        
        # Setup proxy if provided
        proxy_config = actor_input.get('proxyConfiguration')
        proxy_url = None
        if proxy_config and proxy_config.get('useApifyProxy'):
            proxy_password = os.getenv('APIFY_PROXY_PASSWORD')
            if proxy_password:
                proxy_url = f"http://auto:{proxy_password}@proxy.apify.com:8000"
        
        client_kwargs = {'follow_redirects': True, 'timeout': 30.0}
        if proxy_url:
            client_kwargs['proxy'] = proxy_url
        
        results_count = 0
        
        async with httpx.AsyncClient(**client_kwargs) as client:
            # Fetch listing page
            Actor.log.info('Fetching datasets...')
            response = await client.get(
                search_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find dataset containers
            containers = soup.find_all('div', class_=lambda x: x and 'dataset' in str(x).lower())
            
            Actor.log.info(f'Found {len(containers)} datasets')
            
            if not containers:
                Actor.log.warning('No datasets found on page')
                return
            
            for container in containers[:max_results]:
                try:
                    # Extract dataset URL
                    link = container.find('a', href=True)
                    if not link:
                        continue
                    
                    dataset_url = urljoin(search_url, link['href'])
                    
                    # Extract title
                    title_elem = container.find(['h3', 'h2', 'a'], class_=lambda x: x and ('heading' in str(x).lower() or 'title' in str(x).lower()))
                    if not title_elem:
                        title_elem = link
                    dataset_title = title_elem.get_text(strip=True) if title_elem else None
                    
                    # Extract organization
                    org_elem = container.find(class_=lambda x: x and 'organization' in str(x).lower())
                    organization_name = org_elem.get_text(strip=True) if org_elem else None
                    
                    # Extract tags
                    tag_elems = container.find_all(class_=lambda x: x and 'tag' in str(x).lower())
                    tags_list = [tag.get_text(strip=True) for tag in tag_elems if tag.get_text(strip=True)]
                    
                    # Extract description
                    notes_elem = container.find(class_=lambda x: x and ('notes' in str(x).lower() or 'description' in str(x).lower()))
                    notes = notes_elem.get_text(strip=True) if notes_elem else None
                    
                    # Extract resource count
                    resource_elem = container.find(class_=lambda x: x and 'resource' in str(x).lower())
                    resources = 0
                    if resource_elem:
                        resource_text = resource_elem.get_text()
                        resource_match = re.search(r'(\d+)', resource_text)
                        if resource_match:
                            resources = int(resource_match.group(1))
                    
                    # Extract last modified
                    modified_elem = container.find(class_=lambda x: x and ('modified' in str(x).lower() or 'updated' in str(x).lower()))
                    last_modified = modified_elem.get_text(strip=True) if modified_elem else None
                    
                    # Push result
                    result = {
                        'datasetUrl': dataset_url,
                        'datasetTitle': dataset_title,
                        'organization': organization_name,
                        'tags': tags_list,
                        'notes': notes,
                        'resources': resources,
                        'lastModified': last_modified,
                        'scrapedAt': datetime.now(timezone.utc).isoformat()
                    }
                    
                    await Actor.push_data(result)
                    results_count += 1
                    Actor.log.info(f'Scraped {results_count}/{max_results}: {dataset_title}')
                    
                    if results_count >= max_results:
                        break
                        
                except Exception as e:
                    Actor.log.warning(f'Failed to parse dataset: {e}')
                    continue
        
        Actor.log.info(f'Scraping completed! Total datasets: {results_count}')
