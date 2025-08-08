import sqlite3
import os

# Remove db file if it exists
if os.path.exists('database.db'):
    os.remove('database.db')

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

import werkzeug.security

# Add test users
users = [
    ('admin', werkzeug.security.generate_password_hash('admin')),
    ('alice', werkzeug.security.generate_password_hash('alice123')),
    ('bob', werkzeug.security.generate_password_hash('bob456')),
    ('charlie', werkzeug.security.generate_password_hash('charlie789'))
]
for username, password in users:
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

# Add programming-related blog posts
posts = [
    ('Understanding Python Decorators',
     '''Decorators are a powerful feature in Python that allow you to modify the behavior of functions. In this post, we will explore how decorators work and provide some practical examples.
\n\n
Decorators are functions that wrap another function, allowing you to add functionality before or after the wrapped function is called. They are often used for logging, access control, and caching.
In Python, decorators are defined using the `@decorator_name` syntax above the function definition. This allows you to apply the decorator to the function without modifying its code directly.
Decorators are a great way to keep your code clean and reusable. They can be used to implement cross-cutting concerns like logging, authentication, and more without cluttering your business logic.
'''),
    ('Getting Started with Flask',
     '''Flask is a lightweight web framework for Python. This post covers the basics of setting up a Flask application and creating your first route.
\n\n
Flask is designed to be simple and easy to use, making it a great choice for beginners. It allows you to quickly create web applications with minimal setup.
To get started with Flask, you need to install it using pip. Once installed, you can create a new Flask application by importing the Flask class and creating an instance of it.
Flask uses decorators to define routes. You can create a route by using the `@app.route()` decorator above a function. This function will be called whenever a request is made to that route.
Flask also supports templates, allowing you to render HTML pages dynamically. You can use Jinja2 templating engine to create reusable HTML components and pass data from your Flask application to the templates.
'''),
    ('Tips for Writing Clean Code',
     '''Writing clean code is essential for maintainability. Here are some tips and best practices to help you write code that is easy to read and understand.
\n\n
Clean code is code that is easy to read, understand, and maintain. It follows best practices and conventions that make it accessible to other developers.
Some tips for writing clean code include using meaningful variable names, keeping functions small and focused, and avoiding unnecessary complexity.
Commenting your code is also important, but it should be used to explain why something is done, not what is done. The code itself should be self-explanatory.
Using consistent formatting and style across your codebase helps improve readability. Tools like linters and formatters can help enforce these standards automatically.
'''),
    ('Introduction to SQL Joins',
     '''SQL joins are used to combine rows from two or more tables. This post explains the different types of joins and provides examples for each.
\n\n
SQL joins allow you to retrieve data from multiple tables based on related columns. They are essential for working with relational databases.
There are several types of joins: INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN. Each type serves a different purpose and returns different results based on the relationship between the tables.
An INNER JOIN returns only the rows that have matching values in both tables. A LEFT JOIN returns all rows from the left table and the matched rows from the right table, filling in NULLs for unmatched rows.
RIGHT JOIN and FULL OUTER JOIN work similarly, but they include all rows from the right table or both tables, respectively. Understanding these joins is crucial for effective database querying.
''')
]
for title, content in posts:
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))

# Add realistic comments from various users
comments = [
    # Post 1: Understanding Python Decorators
    (1, 2, 'Great explanation! Decorators always confused me, but this helped.'),
    (1, 3, 'Can you show an example with arguments?'),
    (1, 4, 'I use decorators for logging in my projects. Very useful!'),
    # Post 2: Getting Started with Flask
    (2, 1, 'Flask is my favorite Python framework. Thanks for the intro!'),
    (2, 3, 'How does Flask compare to Django?'),
    # Post 3: Tips for Writing Clean Code
    (3, 2, 'I agree with using meaningful variable names. It makes a big difference.'),
    (3, 4, 'What tools do you recommend for code formatting?'),
    # Post 4: Introduction to SQL Joins
    (4, 1, 'Joins can be tricky at first. Thanks for breaking it down.'),
    (4, 2, 'Could you add an example with LEFT JOIN?'),
    (4, 3, 'Nice post! I always forget the difference between INNER and OUTER joins.')
]
for post_id, user_id, content in comments:
    cur.execute("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)", (post_id, user_id, content))

connection.commit()
connection.close()
