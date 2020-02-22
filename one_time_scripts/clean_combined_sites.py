import os
from webscraping.stat_models import *

def clean(directory):
  num_removed = 0
  num_kept = 0
  if "cleaned.html" not in os.listdir(f'../resources/cached_sites/{directory}'):
    page = WebPage(url=directory)
    keys = list(page.css.selectors.keys())
    # print(len(page.css.selectors.items()))
    for selector in keys:
      if not page.html.contains_selector(selector):
        page.css.remove_selector(selector)
        num_removed += 1
      else:
        num_kept += 1      
    # print(len(page.css.selectors.items()))
    print(f"Removed {num_removed} and kept {num_kept} selectors for {directory}")
    page.save(f'../resources/cached_sites/{directory}/cleaned.html')
    return False
  else:
    return True

def main():
  num_cleaned = 0
  for directory in os.listdir('../resources/cached_sites'):
    if clean(directory):
      num_cleaned += 1
      print(f"Already cleaned {directory}, total cleaned: {num_cleaned}")


if __name__ == '__main__':
  main()