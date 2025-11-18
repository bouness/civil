import json
import os
import re

info = {
    "Easy": "note",
    "Medium": "caution",
    "Hard": "danger",
    "Conceptual": "tip",
}

def sanitize_filename(name):
    """Convert a string to a safe filename."""
    name = re.sub(r'[^\w\s-]', '', name.lower())
    name = re.sub(r'[-\s]+', '_', name)
    return name.strip('-_')

def sanitize_category(name):
    """Convert category to folder name."""
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '_', name)
    return name.lower().strip('-_')

def format_math_delimiters(text):
    """
    Ensure display math $$...$$ has proper newlines:
    Convert $$...$$ to \n$$\n...\n$$\n
    """
    # Pattern to find display math blocks
    pattern = r'\$\$(.*?)\$\$'
    
    def replace_math(match):
        math_content = match.group(1).strip()
        return f'\n$$\n{math_content}\n$$\n'
    
    # Replace all display math blocks
    formatted_text = re.sub(pattern, replace_math, text, flags=re.DOTALL)
    
    return formatted_text

def create_markdown_files():
    """Main function to convert JSON to markdown files."""
    
    # Step 1: Read the JSON file
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Step 2: Track categories for sidebar
    categories = set()
    
    # Step 3: Process each question
    total_questions = len(data)
    print(f"Found {total_questions} questions in data.json")
    
    for i, item in enumerate(data, 1):
        # Get category and create folder name
        category = item.get('category', 'Uncategorized')
        category_folder = sanitize_category(category)
        categories.add(category)
        
        # Create category directory
        output_dir = f'questions/{category_folder}'
        os.makedirs(output_dir, exist_ok=True)
        
        # Create filename from title
        filename = sanitize_filename(item['title']) + '.mdx'
        filepath = os.path.join(output_dir, filename)
        
        # Format the question and solution text to fix math delimiters
        question_text = format_math_delimiters(item['question'])
        solution_text = format_math_delimiters(item['solution'])
        
        # Strip quotes from title and description
        title = str(item['title']).replace('"', '').replace("'", "")
        description = str(item['title']).replace('"', '').replace("'", "")
        
        # Create the markdown content with Tabs
        markdown_content = f"""---
title: {title}
description: {description}
---
import {{ Tabs, TabItem }} from '@astrojs/starlight/components';

<Tabs>
<TabItem label='Question'>
:::{info.get(item['difficulty'], 'note')}[Difficulty: **{item['difficulty']}** - Category: **{category}**]
{question_text}
:::
</TabItem>

<TabItem label='Solution'>
:::tip[Solution]
{solution_text}
:::
</TabItem>
</Tabs>"""
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Created {i}/{total_questions}: {output_dir}/{filename}")
    
    # Step 4: Generate sidebar navigation
    print("\n" + "="*60)
    print("SIDEBAR NAVIGATION CONFIG - Add this to your astro.config.mjs:")
    print("="*60)
    
    # Sort categories alphabetically
    sorted_categories = sorted(categories)
    
    for category in sorted_categories:
        category_folder = sanitize_category(category)
        print(f"""{{
  label: '{category}',
  autogenerate: {{ directory: 'questions/{category_folder}' }},
}},""")
    
    print(f"\nDone! All markdown files saved in category folders inside 'questions/'")

# Test the math formatting
def test_math_formatting():
    """Test that math delimiters are formatted correctly."""
    test_input = "Calculate the formula: $$q_u = 0.4(120)(5)(45) + (120)(3)(41)$$ and then use $E = mc^2$."
    result = format_math_delimiters(test_input)
    print("Before formatting:")
    print(test_input)
    print("\nAfter formatting:")
    print(result)

if __name__ == "__main__":
    # Uncomment to test the formatting
    # test_math_formatting()
    
    # Run the main conversion
    create_markdown_files()
