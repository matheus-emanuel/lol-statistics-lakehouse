import gdown

url = "https://drive.google.com/drive/folders/1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH"
output = "../data/raw"
my_user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0'

gdown.download_folder(url=url, output=output, user_agent=my_user_agent)