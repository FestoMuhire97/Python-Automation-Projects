import pandas as pd
import json

#defining excel filepaths
excel_filepath = "C:/Users/Festo Muhire/Desktop/Method Manager Python/Method Manager Masterlist.xlsx"

#defining JSON Config files
Groupsjson_filepath = "C:/Users/Festo Muhire/Desktop/Method Manager Python/Method Manager 2/db/groups.json"
Treesjson_filepath = "C:/Users/Festo Muhire/Desktop/Method Manager Python/Method Manager 2/db/tree.json"
Linksjson_filepath = "C:/Users/Festo Muhire/Desktop/Method Manager Python/Method Manager 2/db/links.json"

# Replace 'Sheet2' with the name of your desired worksheet
worksheet_name = 'Sheet1'

# Read the specific worksheet into a pandas DataFrame
df= pd.read_excel(excel_filepath, sheet_name=worksheet_name)

# Reading the :
with open(Groupsjson_filepath,'r') as groups:
    group_data_load = json.load(groups)

with open(Treesjson_filepath,'r') as trees:
    tree_data_load = json.load(trees)

with open(Linksjson_filepath, 'r') as links:
    link_data_load = json.load(links)   


# Replace 'your_column_name' with the actual name of the column you want to analyze
column_groupIDs = list(df['groups'].unique())
column_links = list(df['links'])
column_paths = list(df['paths'])
column_attachments = list(df['attachments'])
#print(column_paths)

for group in column_groupIDs:
    found = False
    tree_found = False
    for item in group_data_load:
        if item["name"] == group:
            found = True
            break  # The GroupID was found; then break

    # If the Group was not found, create a new dictionary entry
    if not found:
        group_data = {}
        group_data['name'] = group
        group_data['icon-class'] = 'fa-dna'
        group_data['default'] = False
        group_data['navbar'] = 'left'
        group_data['favorite'] = True
        group_data['_id'] = group
        group_data_load.append(group_data)
    # Save the updated JSON data back to the file
    with open(Groupsjson_filepath, "w") as g:
        json.dump(group_data_load, g)

    for item in tree_data_load:
        if item["group-id"] == group:
            tree_found = True
            break  # The GroupID was found; then break
    
    if not tree_found:
        tree_data = {}
        tree_data['group-id'] = group
        tree_data['method-ids'] = []
        tree_data['locked'] = False
        tree_data['_id'] = ""
        tree_data_load.append(tree_data)
    # Save the updated JSON data back to the file
    with open(Treesjson_filepath, "w") as t:
        json.dump(tree_data_load, t)
    
#checking if the link is present in the links JSON file:
for link in column_links:
    #corresponding_attachments = (df.loc[df['links'] == link, 'attachments'].values)
    #print(corresponding_attachments)
    found = False
    for item in link_data_load:
        if item["name"] == link:
            found = True
            break  # The GroupID was found; then break

    # If the link was not found, create a new dictionary entry
    if not found:
        link_data = {}
        link_data['name'] = link
        link_data['description'] = ""
        link_data['icon-customImage'] = ""
        link_data['icon-class'] = "fa-dna"
        link_data['icon-color'] = "color-dark"
        link_data['path'] = ""
        link_data['type'] = "method"
        link_data['attachments'] = []
        link_data['default'] = False
        link_data['favorite'] = True
        link_data['last-started'] = ""
        link_data['last-startedUTC'] = ""
        link_data['_id'] = link
        link_data_load.append(link_data)


    # Save the updated JSON data back to the file
    with open(Linksjson_filepath, "w") as l:
        json.dump(link_data_load, l)

# Check if the link is associated to the right group in the tree JSON file:
for link in column_links:
    corresponding_group = (df.loc[df['links'] == link, 'groups'].values)
    found = False

    for item in tree_data_load:
        for entry in item['method-ids']:
            if entry == link:
                if item['group-id'] == corresponding_group:
                    found = True
                    break
                else:
                    item['method-ids'].remove(link)
    
    if not found:
        for item in tree_data_load:
            if item['group-id'] == corresponding_group:
            # locate which group the link belongs to, and append it to the Method-ids key:
                item['method-ids'].append(link)

    # Save the updated JSON data back to the file
    with open(Treesjson_filepath, "w") as l:
        json.dump(tree_data_load, l)


# Check if the path is present in the link JSON file, and if not, add to the JSON file:
for path in column_paths:
    corresponding_link = df.loc[df['paths'] == path, 'links'].values
    #print(corresponding_link)
    found = False

    for item in link_data_load:
        if item ['name'] == corresponding_link:
            if item['path'] == path:
                found = True
                break

    if not found:
        for item in link_data_load:
            if item['name'] == corresponding_link:
            # locate which group the link belongs to, and append it to the Method-ids key:
                item['path'] = path

    # Save the updated JSON data back to the file
    with open(Linksjson_filepath, "w") as j:
        json.dump(link_data_load, j)

# Check if the attachment(s) is present in the link JSON file, and if not, add to the JSON file:
for attachment in column_attachments:
    corresponding_link = df.loc[df['attachments'] == attachment, 'links'].values
    print(corresponding_link)
    found = False

    for item in link_data_load:
        if item ['name'] == corresponding_link:
            if item['attachments'] == [attachment]:
                found = True
                break
            elif item['attachments'] == []:
                found = True
                break

    if not found:
        for item in link_data_load:
            if item['name'] == corresponding_link:
            # locate which group the link belongs to, and append it to the Method-ids key:
                item['attachments'].append(attachment)

    # Save the updated JSON data back to the file
    with open(Linksjson_filepath, "w") as a:
        json.dump(link_data_load, a)

# Check if the link is associated with the right path in the link JSON file:
for link in column_links:
    corresponding_path = (df.loc[df['links'] == link, 'paths'].values)
    found = False

    for item in link_data_load:
        for entry in item['name']:
            if entry == link:
                if item['group-id'] == corresponding_group:
                    found = True
                    break
                else:
                    item['method-ids'].remove(link)
    
    if not found:
        for item in tree_data_load:
            if item['group-id'] == corresponding_group:
            # locate which group the link belongs to, and append it to the Method-ids key:
                item['method-ids'].append(link)

    # Save the updated JSON data back to the file
    with open(Treesjson_filepath, "w") as l:
        json.dump(tree_data_load, l)