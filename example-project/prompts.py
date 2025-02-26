# Content Structure Prompts
GENERATE_CATEGORIES_PROMPT = """Given a website named "{site_name}" in the {site_niche} niche, 
suggest 5-7 main content categories that would make sense for organizing the site's content.

Format the response as a JSON array of objects, where each object has:
- name: The category name (2-3 words max)
- description: A brief description explaining the category (1-2 sentences)

Example format:
[
    {{"name": "Getting Started", "description": "Fundamental concepts and beginner tutorials"}},
    {{"name": "Advanced Topics", "description": "In-depth guides for experienced users"}}
]

Keep the categories broad but specific to {site_niche}. Focus on topics that would be valuable for the target audience."""

# Add other prompts here as needed... 