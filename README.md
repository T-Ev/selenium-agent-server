# WIP: Selenium Agent Server

API to Anything

# Mission

Create a docker server that can deploy "modules", which define an API endpoint, a Selenium Workflow on a target URL, and parser to convert the scraped information into a standard response format.

# Required functionality

- Must be fully self contained dockerized server
- Must be able to spawn selenium tabs and scrape based on a https request queue
- File structure should be conducive to defining new modules
- Performance log access is required
- support parallel selenium usage to avoid queue backlog
- Aggressive api response caching
- Modules must be able to support error states and handle them properly
- Modules must be able to securely handle auth inside of urls

# Stage 2

- Have all created APIs be function callable
- Support cron jobs
- add LLM to automatically design parsers and allow modules to be spawned dynamically based on calling a /create endpoint
- Use multimodal to dynamically create selenium workflows for new modules based on screen recordings (imitation learning)
