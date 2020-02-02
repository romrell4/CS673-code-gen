import requests

with open("../webscraping/edu_websites.csv") as f:
    websites = f.readline().split(",")

def is_valid(website):
    print("Trying {}".format(website))
    try:
        response = requests.get(website, timeout = 5)
        return response.status_code == 200
    except Exception as e:
        print(e)


valid_websites = list(filter(is_valid, websites))
print(len(valid_websites))

with open("../webscraping/valid_edu_websites.csv", "w") as f:
    f.write(",".join(valid_websites))