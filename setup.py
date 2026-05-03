from setuptools import setup, find_packages

setup(
    name="hermes-biz-tools",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0",
        "jinja2>=3.0",
        "fpdf2>=2.7",
        "markdown>=3.0",
    ],
    entry_points={
        "console_scripts": [
            "biz-tools=biz_tools.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="BasaraNekki500",
    description="AI marketing content generator for Chinese small businesses/B&Bs",
    url="https://github.com/BasaraNekki500/hermes-biz-tools",
)
