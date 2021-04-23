import urllib
import csv

url_surnames = 'https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/surnames/us.txt'
url_names = 'https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/first%20names/us.txt'

def get_list(url):
    return urllib.request.urlopen(url).read().decode()

names = get_list(url_names)
surnames = get_list(url_surnames)

def write_list(listname):
    with open(f'{listname}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([eval(listname)])

write_list('names')
write_list('surnames')