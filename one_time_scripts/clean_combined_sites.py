import os
from webscraping.stat_models import *

def main():
  for directory in os.listdir('../resources/cached_sites'):
    num_removed = 0
    num_kept = 0
    if directory == 'byu':
      page = WebPage(url=directory)
      keys = list(page.css.selectors.keys())
      print(len(page.css.selectors.items()))
      for selector in keys:
        if not page.html.contains_selector(selector):
          page.css.remove_selector(selector)
          num_removed += 1
        else:
          num_kept += 1      
      print(len(page.css.selectors.items()))
      print(f"Removed {num_removed} and kept {num_kept} selectors for {directory}")
      page.save(f'../resources/cached_sites/{directory}/cleaned.html')
      


if __name__ == '__main__':
  main()