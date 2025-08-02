"""
ملف الإعداد لنظام CRM محل الخياطة
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tailor-crm",
    version="1.0.0",
    author="Manus AI",
    author_email="support@example.com",
    description="نظام إدارة شامل لمحل الخياطة الرجالية",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/tailor-crm",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
        "Topic :: Database :: Front-Ends",
        "Natural Language :: Arabic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tailor-crm=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.sql"],
    },
    keywords="crm, tailor, management, arabic, desktop, pyqt",
    project_urls={
        "Bug Reports": "https://github.com/username/tailor-crm/issues",
        "Source": "https://github.com/username/tailor-crm",
        "Documentation": "https://github.com/username/tailor-crm/wiki",
    },
)

