from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='weathermashup',
      version=version,
      description="RHoK Weather Data Aggregator",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='RHoK',
      author_email='',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [weather.sources]
      armageddon = weathermashup.data_sources.mayan_calender:armageddon
      google = weathermashup.data_sources.google:source
      metar = weathermashup.data_sources.metar:weather_scraper
      yrno = weathermashup.data_sources.yrno:weather_data
      wetter_com = weathermashup.data_sources.wetter_com:find
      """,
      )
