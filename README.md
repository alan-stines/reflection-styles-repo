# Reflection Styles Repository

A collection of creative prompts to force students out of their comfort zones when writing weekly lab reflections. 

## Wait, Why Does This Exist?

Let's be real for a second: as an instructor, I am incredibly tired of reading the same straight-up, soulless AI slop week after week. If I wanted to read predictive-text regurgitation on how "transformative" and "insightful" learning to configure a firewall was, I'd just talk to a chatbot myself.

This repository exists because **working with AI should be a tool for learning, not just a shortcut to achieve a grade.** 

By adopting the persona of Yoda, a pirate captain, or a malfunctioning C-3PO, students are forced to actually engage with the material and see their experiences from a new perspective. Plus—and arguably more importantly—it makes reading these reflections significantly more entertaining for me.

## The Setup

This project is a static site generator built with Python. It reads the original prompts (which are safely hidden away from public eyes in `.docx` files) and compiles them into a sleek, Bootstrap 5-powered site.

### How to use
1. Make sure Python 3 is installed.
2. Edit the `.docx` files or add new ones in the `_docs/` folder.
3. Run the extraction script to convert Word documents to text: `python extract.py`
4. Run the build script to generate the HTML site: `python build.py`
5. The final site will be ready in the `public/` folder for deployment.
