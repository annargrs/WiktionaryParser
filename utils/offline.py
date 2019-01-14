file = "/mnt/Data/Datasets/Wiktionary/ukwiktionary-20190101-pages-articles.xml"
bigfile = "/mnt/Data/Datasets/Wiktionary/enwiktionary-latest-pages-articles.xml"
# out_folder = "/mnt/Data/Datasets/Wiktionary/"

language_filtering_templates = {"uk":["[Category:Українськ",
                                      "[Категорія:Українськ"]}

def filter_by_language_templates(language, language_filtering_templates,
                                 location_index, xml_dump):
    templates = language_filtering_templates[language]
    filtered_index = {}
    for item in location_index:
        entry = retrieve_by_index(item, location_index)
        for template in templates:
            if template in entry:
                filtered_index[item] = location_index[item]
                break

    return filtered_index




# the first num is the offset from beginning of the file,
# and the second is the length of the article
locations_index = {"cat":[3000500000, 15]}

def retrieve_by_index(word, locations_index):
    try:
        locations = locations_index[word]
    except KeyError:
        print("The word '"+word+"' was not found in the index.")
        return None
    f = open(file, 'rb')
    f.seek(locations[0], 0)  # move the file pointer forward 6 bytes (i.e. to the 'w')
    article = f.read(locations[1])  # read the rest of the article
    # from the pointer
    f.close()
    return article.decode("utf-8")

locations_index = {'навігатор': [331487, 2639]}

# print(retrieve_by_index('навігатор', locations_index))

def build_index(xml_dump):

    locations_index = []

    fh = open(xml_dump, "r")

    def get_word_position(start_position):
        while True:
            row = fh.readline()
            if "<page>" in row:
                start = fh.tell()
            if "<title>" in row:
                word = row.strip()
                word = word.strip("<title>")
                word = word.strip("</title>")
            if "</page>" in row:
                end = fh.tell()
                length = end-start
                locations_index.append([word, start, length, end])
                return None
            if "</mediawiki>" in row:
                locations_index.append(None)
                return None

    # get the first article starting at position 0
    get_word_position(0)

    #get the rest of the articles
    while True:
        if isinstance(locations_index[-1], list):
            get_word_position(locations_index[-1][-1])
        else:
            break
    locations_index = locations_index[:-1]
    fh.close()

    # save the results
    outpath = file.replace(".xml", ".yaml")
    with open(outpath, "w") as out:
        for l in locations_index:
            # get rid of "category: whatever type pages"
            if not ":" in l[0]:
                out.write(l[0]+": ["+str(l[1])+", "+str(l[2])+"]\n")
    # return locations_index

    #format the output as dictionary

# test = retrieve_by_index("cat", locations_index)
# print(test)
build_index(xml_dump=file)
